import os
import sys
import re
import glob
import datetime
import subprocess
import argparse
from multiprocessing import Pool, cpu_count
from moviepy.editor import VideoFileClip
from faster_whisper import WhisperModel

# --- Utility Functions ---

def format_time_srt(seconds):
    """Converte segundos para o formato de tempo SRT (HH:MM:SS,ms)."""
    delta = datetime.timedelta(seconds=seconds)
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = delta.microseconds // 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def srt_time_to_ass(srt_time):
    """Converts an SRT timestamp (HH:MM:SS,ms) to an ASS timestamp (H:MM:SS.cs)."""
    parts = srt_time.split(',')
    # ASS format is H:MM:SS.cc (centiseconds)
    return parts[0] + '.' + parts[1][:2]

# --- Core Logic ---

def transcribe_to_srt(video_path, model_size="base", max_words_per_segment=5):
    """
    Extrai o áudio de um vídeo, transcreve e gera um arquivo .srt.
    """
    print(f"[*] Processando vídeo para transcrição: {video_path}")
    
    # 1. Extrair áudio do vídeo
    video_clip = VideoFileClip(video_path)
    audio_path = f"temp_audio_{os.getpid()}.wav"
    video_clip.audio.write_audiofile(audio_path, codec='pcm_s16le', verbose=False, logger=None)

    # 2. Transcrever o áudio com Whisper
    print(f"[*] Carregando modelo Whisper '{model_size}'...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    
    print("[*] Iniciando transcrição...")
    segments, info = model.transcribe(audio_path, beam_size=5, word_timestamps=True)
    
    print(f"[*] Idioma detectado: '{info.language}' ({info.language_probability:.2f})")

    # 3. Gerar o conteúdo do arquivo .srt
    srt_content = ""
    segment_id = 1
    all_words = []
    for segment in segments:
        for word in segment.words:
            all_words.append(word)

    for i in range(0, len(all_words), max_words_per_segment):
        chunk = all_words[i:i + max_words_per_segment]
        if not chunk: continue
            
        start_time = format_time_srt(chunk[0].start)
        end_time = format_time_srt(chunk[-1].end)
        text = " ".join([word.word for word in chunk]).strip()
        
        srt_content += f"{segment_id}\n{start_time} --> {end_time}\n{text}\n\n"
        segment_id += 1

    # 4. Salvar o arquivo .srt
    base_name, _ = os.path.splitext(video_path)
    srt_path = f"{base_name}.srt"
    
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
        
    print(f"[+] Legendas salvas em: {srt_path}")
    
    # Limpar áudio temporário
    if os.path.exists(audio_path):
        os.remove(audio_path)
    
    return srt_path

def convert_srt_to_ass(srt_path, ass_path=None):
    """
    Converte SRT para ASS com um estilo profissional.
    """
    if ass_path is None:
        ass_path = os.path.splitext(srt_path)[0] + '.ass'

    try:
        with open(srt_path, 'r', encoding='utf-8') as f:
            srt_content = f.read()
    except FileNotFoundError:
        print(f"Error: SRT file not found at {srt_path}")
        return None

    ass_header = f"""[Script Info]
Title: Converted from SRT
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: 1920
PlayResY: 1080
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Nunito,55,&H00FFFFFF,&H00FFFFFF,&H00111111,&H80000000,0,0,0,0,100,100,0.00,0.00,1,2,1.5,2,10,10,48,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(ass_path, 'w', encoding='utf-8') as f:
        f.write(ass_header)
        srt_pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n', re.DOTALL)
        matches = srt_pattern.findall(srt_content + '\n\n')

        for match in matches:
            _, start_time_srt, end_time_srt, text = match
            start_time_ass = srt_time_to_ass(start_time_srt)
            end_time_ass = srt_time_to_ass(end_time_srt)
            text = text.strip().replace('\n', '\\N')
            dialogue_line = f"Dialogue: 0,{start_time_ass},{end_time_ass},Default,,0,0,0,,{text}"
            f.write(dialogue_line + '\n')
    
    return ass_path

def embed_subtitles(video_path, srt_path, output_path):
    """
    Queima legendas no vídeo usando ffmpeg.
    """
    ass_path = convert_srt_to_ass(srt_path)
    if not ass_path:
        return None

    subtitle_path_escaped = os.path.abspath(ass_path).replace('\\', '/').replace(':', '\\\\:')

    command = [
        'ffmpeg', '-y',
        '-i', video_path,
        '-vf', f"subtitles={subtitle_path_escaped}",
        '-c:a', 'copy',
        '-crf', '18',
        '-preset', 'veryfast',
        output_path
    ]

    print(f"[*] Executando ffmpeg para {output_path}...")
    process = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace')

    if process.returncode != 0:
        print(f"[-] FALHA no ffmpeg para {video_path}: {process.stderr}")
        return None

    print(f"[+] SUCESSO: {output_path} criado.")
    return output_path

# --- Workflow Wrappers ---

def process_single_video(task_config):
    """
    Função de trabalho para processar um único vídeo.
    """
    video_path = task_config['video_path']
    model_size = task_config.get('model_size', 'base')
    max_words = task_config.get('max_words', 5)
    output_path = task_config.get('output_path')
    only_srt = task_config.get('only_srt', False)
    srt_path = task_config.get('srt_path')

    if not output_path:
        base, ext = os.path.splitext(video_path)
        output_path = f"{base}_legendado{ext}"

    try:
        # 1. Transcrever (apenas se srt_path não for fornecido)
        if not srt_path:
            srt_path = transcribe_to_srt(video_path, model_size, max_words)
        else:
            print(f"[*] Usando legenda fornecida: {srt_path}")
        
        # 2. Embutir (gera vídeo legendado) se não for apenas SRT
        if not only_srt:
            embed_subtitles(video_path, srt_path, output_path)
            return output_path
        return srt_path
    except Exception as e:
        print(f"[!] Erro ao processar {video_path}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Subtitler Pro: Transcrição e Queima de Legendas")
    parser.add_argument("--video", type=str, help="Caminho do vídeo para processar")
    parser.add_argument("--batch", type=str, help="Caminho da pasta para processar em lote (pastas 'aula*')")
    parser.add_argument("--srt", type=str, help="Caminho de um arquivo .srt existente (pula a transcrição)")
    parser.add_argument("--model", type=str, default="base", help="Tamanho do modelo Whisper (base, small, medium, large-v3)")
    parser.add_argument("--max-words", type=int, default=5, help="Máximo de palavras por segmento de legenda")
    parser.add_argument("--only-srt", action="store_true", help="Apenas gera o arquivo .srt, sem queimar no vídeo")
    parser.add_argument("--workers", type=int, default=min(12, cpu_count()), help="Número de processos paralelos")

    args = parser.parse_args()

    if args.video:
        config = {
            'video_path': args.video,
            'srt_path': args.srt,
            'model_size': args.model,
            'max_words': args.max_words,
            'only_srt': args.only_srt
        }
        process_single_video(config)

    elif args.batch:
        from tqdm import tqdm
        tasks = []
        for class_dir in sorted(glob.glob(os.path.join(args.batch, 'aula*'))):
            if not os.path.isdir(class_dir): continue
            
            base_name = os.path.basename(class_dir)
            video_file = os.path.join(class_dir, f"{base_name}.mp4")
            srt_file_candidate = os.path.join(class_dir, f"{base_name}.srt")
            
            if os.path.exists(video_file):
                # Se o arquivo .srt já existe, vamos usá-lo em vez de transcrever novamente
                srt_to_use = srt_file_candidate if os.path.exists(srt_file_candidate) else None
                
                tasks.append({
                    'video_path': video_file,
                    'srt_path': srt_to_use,
                    'model_size': args.model,
                    'max_words': args.max_words,
                    'only_srt': args.only_srt
                })
        
        if not tasks:
            print("[-] Nenhuma pasta 'aula*' com .mp4 encontrada.")
            return

        print(f"[*] Iniciando processamento em lote de {len(tasks)} vídeos com {args.workers} workers...")
        with Pool(processes=args.workers) as pool:
            list(tqdm(pool.imap(process_single_video, tasks), total=len(tasks), desc="Progresso Total"))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

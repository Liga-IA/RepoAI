#!/bin/bash

# ===========================================
# Script para organizar imagens para o jogo
# ===========================================

IMAGES_DIR="frontend/public/images"
OUTPUT_PATTERN="sample_"

echo "📁 Organizando imagens para o jogo..."
echo ""

# Conta imagens existentes
existing_count=$(ls -1 "$IMAGES_DIR"/sample_*.jpg 2>/dev/null | wc -l)
echo "📊 Imagens sample_*.jpg existentes: $existing_count"

# Encontra todas as imagens (incluindo subpastas)
total_images=$(find "$IMAGES_DIR" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) ! -name "sample_*.jpg" | wc -l)
echo "📊 Imagens adicionais encontradas: $total_images"

if [ "$total_images" -eq 0 ]; then
    echo "✅ Nenhuma imagem adicional para organizar"
    exit 0
fi

# Cria diretório temporário
TEMP_DIR=$(mktemp -d)
echo "📦 Processando imagens em: $TEMP_DIR"

# Copia todas as imagens para temp
counter=1
find "$IMAGES_DIR" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) ! -name "sample_*.jpg" | while read img; do
    ext="${img##*.}"
    new_name="${TEMP_DIR}/img_$(printf '%04d' $counter).${ext}"
    cp "$img" "$new_name"
    counter=$((counter + 1))
done

# Renomeia para o padrão sample_XX.jpg
counter=$((existing_count + 1))
for img in "$TEMP_DIR"/*; do
    if [ -f "$img" ]; then
        new_name="${IMAGES_DIR}/${OUTPUT_PATTERN}$(printf '%02d' $counter).jpg"
        
        # Converte para JPG se necessário usando Python
        python3 << EOF
from PIL import Image
import sys

try:
    img = Image.open("$img")
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save("$new_name", "JPEG", quality=85)
    print(f"✅ Convertido: $(basename $img) -> $(basename $new_name)")
except Exception as e:
    print(f"⚠️ Erro ao processar $img: {e}")
EOF
        
        counter=$((counter + 1))
    fi
done

# Limpa temp
rm -rf "$TEMP_DIR"

final_count=$(ls -1 "$IMAGES_DIR"/sample_*.jpg 2>/dev/null | wc -l)
echo ""
echo "✅ Organização concluída!"
echo "📊 Total de imagens disponíveis: $final_count"
echo ""
echo "📝 Imagens disponíveis:"
ls -1 "$IMAGES_DIR"/sample_*.jpg | head -10


// Este código é parte de um algoritmo de busca de ponto de máxima potência (MPPT)
// utilizando o método PSO (Particle Swarm Optimization) para otimizar 
// a eficiência de painéis solares.

// ## Atenção ##
// O algoritmo funciona apenas no software PLECS, acoplado a um bloco de script em C, para simular o
// microcontrolador responsável pelo controle do MPPT.

// Inputs
float tensao = 0; // Tensão obtida do painel solar
float corrente = 0; // Corrente obtida do painel solar
float random = 0;

// Outputs
float pwm = 0; // Output Principal
float D = 0.5; // Resultado do algoritimo

// Definições
#define ExecTime 0.0000001 // Tempo de execução, 1*10^-6 s
#define MAXwave 1 // Valor maximo que a onda triangular vai obter
#define MINwave 0 // Valor minimo que a onda triangular vai obter
#define MAXD 0.975 // Valor maximo que o D poderá obter
#define MIND 0.05 // Valor minimo que o D poderá obter

// Variaveis globais //
float potencia = 0; // Tensão x Corrente

// TriangularWave
float frequencia = 31250; // Frequência desejada para a onda triangular
float periodo = 0; // 1 / Frequência
float valorWave = 0; // Valor atual da onda triangular
float delta = 0; // Valor a se somar ou subtrair a cada periodo de execução 1 / passos por periodo da onda, versão estatica
float somador = 0; // Valor que usa o delta porém é alterado a cada ciclo da onda
float passos = 0; // Valor de passos que irá dar por periodo, Periodo / tempo de execução
int espera = 1; // Variavel que guarda a informação para liberar a inversão do valor delta

///////////////////////

// Função da onda triangular //
///////////////////////////////
void TriangularWave()
{   
   if(valorWave >= MAXwave && espera == 1)
   {
   	espera = 0;
   	valorWave = MAXwave;
   	somador = -delta;
   }
   else if(valorWave <= MINwave && espera == 0)
   {
   	espera = 1;
   	valorWave = MINwave;
   	somador = delta;
   }
   
 	valorWave += somador;
}
///////////////////////////////

// Função do PSO //
///////////////////
#define NUM_PARTICULAS 20 // Define o número de particulas que vão analisar o MPPT
#define CicloAvaliacao 12500 // Ciclos de analise para cada particula
#define CicloReset 250 // Ciclos de analise para o reset, que funciona a parte do algoritmo

// Estrutura que define uma particula, cada particula tem suas caracteristicas
typedef struct {
    float posicao;
    float velocidade;
    float melhorPos;
    float melhorPot;
    float fitness;
} Particle;

// Cria o vetor de particulas com o número de particulas definidas
Particle particulas[NUM_PARTICULAS];

// Peso da inércia
float W = 0.2;
// Peso cognitivo
float C1 = 0.6;
// Peso social
float C2 = 0.6;

int inic = 0; // Variavel responsavel pela inicialização do algoritmo, utilizada apenas na primeira interação
int particulaAtual = 0; // Variavel que define qual particula atual está sendo analisada
int avaliacaoParticula = 0; // Ciclo atual que a particula está em analise
float melhorPos = 0; // Melhor posição global
float melhorPot = 0; // Melhor potencia/fitness global
float melhorPotAnt = 0; // Melhor potencia/fitness global anterior, antes do que está definido no momento
float melhorPosAnt = 0; // Melhor potencia/fitness global anterior, antes do que está definido no momento

// Variaveis referentes ao reset	
float margem = 0.02; // % de intervalo para considerar no reset
int tolerancia_flag = 2000; // Tolerancia para levantar a flag de que achou o mppt
int tolerancia_reset = 0; // Tolerancia para resetar, se sair da curva terá tantos ciclos para voltar
int time_out = 45000; // Time out caso nunca ache o mppt e fique oscilando
int count_ciclo_reset = 0; // Qual ciclo está atualmente no calculo do reset
float media_pot_reset = 0; // Calculo de media de potencia para a analise se precisa resetar

int flag = 0; // Flag de que achou o MPPT
int count_flag = 0; // Quantas vezes ficou estabilizado
int count_reset = 0; // Quantas vezes ja saiu da margem
int count_time_out = 0; // Ciclos que não achou o MPPT

// Inicializa o sistema de particulas, distribuindo em forma de escada, onde cada particula será jogada em uma parcela do eixo de D
void IncializarParticulas()
{
	inic++;
	
	float multi = ((MAXD - MIND) / NUM_PARTICULAS);
	
	for(int i = 0; i < NUM_PARTICULAS; i++)
	{
		particulas[i].posicao = MAXD - (i * multi);	
		particulas[i].velocidade = 0.0;
		particulas[i].melhorPos = MAXD - (i * multi);
		particulas[i].melhorPot = 0.0;
		particulas[i].fitness = 0.0;
	}
}

// Reseta as variaveis	
void Reset()
{
	// Reinicia o sistema por completo
	flag = 0;
	count_flag = 0;
	count_reset = 0;
	inic = 0;
	particulaAtual = 0;
	avaliacaoParticula = 0;
	melhorPos = 0;
	melhorPot = 0;
	melhorPotAnt = 0;
	melhorPosAnt = 0;
	valorWave = 0;
	periodo = 0;
	delta = 0;
	somador = 0;
	passos = 0;
	espera = 1;
	count_ciclo_reset = 0;
	media_pot_reset = 0;
	count_time_out = 0;
	
	periodo = 1.0 / frequencia;
	passos = periodo / ExecTime;
	delta = 1 / passos;
	somador = delta;
	
	IncializarParticulas();
}

// Função responsavel por verificar se precisa fazer o reset
void VerificarReset()
{
	// Verificar se todas as particulas estão na margem de melhor potencia do MPPT
	// Quando estiverem, ativar a flag
	// Com a flag ativa, caso as particulas saiam dessa margem, resetar
	
	if((potencia > melhorPot*(1 + margem) || potencia < melhorPot*(1 - margem)) && flag == 1)
	{
		Reset();
	}
	
	count_ciclo_reset++;
	if(count_ciclo_reset >= CicloReset)
	{
		count_ciclo_reset = 0;
		media_pot_reset = media_pot_reset / CicloReset;
		
		if(media_pot_reset <= melhorPot*(1 + margem) && media_pot_reset >= melhorPot*(1 - margem))
		{
			count_reset = 0;
			count_flag++;
			if(count_flag >= tolerancia_flag)
			{
				flag = 1;
			} 
		}
		else
		{
			count_reset++;
			count_flag = 0;
			if(count_reset >= tolerancia_reset && flag == 1)
			{
				Reset();
			}
		}
		
		if(flag == 0)
		{
			count_time_out++;
			if(count_time_out >= time_out)
			{
				Reset();
			}
		}
		else
		{
			count_time_out = 0;
		}
		
		media_pot_reset = 0;
	}
	else
	{
		media_pot_reset += potencia;
	}
}

// Função principal do PSO, que calcula a velocidade, atualiza posição, MPPT, entre outros
void AtualizarPaticulas()
{
	
	avaliacaoParticula++;
	if(avaliacaoParticula >= CicloAvaliacao)
	{
		particulas[particulaAtual].fitness = particulas[particulaAtual].fitness / CicloAvaliacao;
		
		avaliacaoParticula = 0;
	
		// Atualiza o fitness da partícula atual
		if(particulas[particulaAtual].fitness > melhorPot)
		{
			melhorPotAnt = melhorPot;
			melhorPosAnt = melhorPos;
			melhorPot = particulas[particulaAtual].fitness;
			melhorPos = particulas[particulaAtual].posicao;	
		}		
			
		if(particulas[particulaAtual].fitness > particulas[particulaAtual].melhorPot)
		{
			particulas[particulaAtual].melhorPot = particulas[particulaAtual].fitness;
			particulas[particulaAtual].melhorPos = particulas[particulaAtual].posicao;
		}	
		
		// Equação principal do PSO para a partícula atual
		particulas[particulaAtual].velocidade *= W;
		particulas[particulaAtual].velocidade += C1 * random * ( particulas[particulaAtual].melhorPos - particulas[particulaAtual].posicao );
		particulas[particulaAtual].velocidade += C2 * 1 * ( melhorPos - particulas[particulaAtual].posicao );
		
		// Atualiza a posição considerando a nova velocidade da partícula atual
		particulas[particulaAtual].posicao += particulas[particulaAtual].velocidade;
		
		// Passa para a proxima particula e caso saia do limite volta para a primeira
		particulaAtual++;
		if(particulaAtual >= NUM_PARTICULAS)
		{
			particulaAtual = 0;
		}
	}
	else
	{
		// Atualiza a media de potencia da partícula até atingir o valor maximo de amostras
		particulas[particulaAtual].fitness += potencia;
	}
}

///////////////////
// Função PSO, aplica o algoritmo
void PSO()
{
	// Invoca a inicialização das partículas
	if(inic == 0)
	{
		IncializarParticulas();	
	}
	else
	{	
		VerificarReset();
		if(flag == 0)
		{
			AtualizarPaticulas();
		}
	}
	
	// Atualiza o valor D como a posição da partícula atual
	D = particulas[particulaAtual].posicao;	
	
	if(D > MAXD)
		D = MAXD;
	else if(D < MIND)
		D = MIND;
}

///////////////////

// Função Main //
/////////////////
void IA_MPPT()
{
   // Chama as funções
   TriangularWave();
   PSO();
   
	// comparação para output
	if(D >= valorWave)
	{
		pwm = MAXwave;
	}
	else
	{
		pwm = MINwave;
	}
}
/////////////////

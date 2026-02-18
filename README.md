# 🚀 ProjetoX - Automação de Vídeos YouTube com IA

![ProjetoX Banner](https://via.placeholder.com/1200x300/4A90E2/FFFFFF?text=ProjetoX+-+Automate+YouTube+Videos+with+AI)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ganzer-Publicidade/projetoX/blob/main/notebooks/ProjetoX_Principal.ipynb)

> Sistema completo para gerar vídeos profissionais automaticamente usando Inteligência Artificial. Do roteiro ao vídeo final em 20 minutos! 🎬✨

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Demonstração](#-demonstração)
- [Funcionalidades](#-funcionalidades)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Uso Rápido](#-uso-rápido)
- [Documentação Completa](#-documentação-completa)
- [Custos Detalhados](#-custos-detalhados)
- [Nichos Lucrativos](#-nichos-lucrativos)
- [Roadmap](#%EF%B8%8F-roadmap)
- [Troubleshooting](#-troubleshooting)
- [Contribuição](#-contribuição)
- [Licença](#-licença)
- [Contato](#-contato)

---

## 🎯 Sobre o Projeto

O **ProjetoX** é um sistema completo que automatiza **TODO** o processo de criação de vídeos para YouTube:

### ✨ O que o ProjetoX faz?

- ✅ **Roteiro:** Gerado automaticamente com ChatGPT (GPT-3.5/GPT-4)
- ✅ **Personagens:** Criados em estilo cartoon 3D com IA generativa
- ✅ **Narração:** Voz profissional e natural com ElevenLabs
- ✅ **Animação:** Cenas animadas usando Stable Video Diffusion
- ✅ **Lip-sync:** Sincronização labial perfeita com Wav2Lip
- ✅ **Edição:** Vídeo final montado automaticamente com transições

### 💡 Por que usar o ProjetoX?

| Vantagem | Descrição |
|----------|-----------|
| 🚀 **Rápido** | 15-30 minutos por vídeo de 5 minutos |
| 💰 **Econômico** | R$10-23 por vídeo (com otimizações) |
| 🎨 **Profissional** | Qualidade de estúdio de animação |
| 🌍 **Multi-idioma** | PT-BR, EN, ES com vozes nativas |
| ☁️ **Cloud** | Roda 100% no Google Colab (gratuito!) |
| 🔧 **Customizável** | Configure cada aspecto do vídeo |
| 📦 **Completo** | Sistema end-to-end, sem etapas manuais |

---

## 🎬 Demonstração

### Pipeline Completo

```
┌─────────┐    ┌────────────┐    ┌──────┐    ┌─────────┐    ┌─────────┐    ┌───────┐
│  Ideia  │───▶│   Roteiro  │───▶│ Pers │───▶│  Áudio  │───▶│ Animação│───▶│ Vídeo │
│         │    │ (ChatGPT)  │    │ (IA) │    │(ElevenL)│    │ (Replic)│    │ Final │
└─────────┘    └────────────┘    └──────┘    └─────────┘    └─────────┘    └───────┘
   30s              2min           3min          2min           15min          3min
```

### Exemplos de Vídeos Gerados

**🙏 Conteúdo Religioso:**
- A História de Davi e Golias
- Noé e a Arca
- A Ressurreição de Jesus

**📚 Conteúdo Educativo:**
- Resumos de Livros Clássicos
- Curiosidades Históricas
- Conceitos de Filosofia

**👶 Conteúdo Infantil:**
- Fábulas Animadas
- Histórias Educativas
- Aventuras de Personagens

---

## ⚡ Funcionalidades

### 🤖 Módulo 1: RoteiroGenerator

Gera roteiros profissionais usando ChatGPT com:
- Estruturação em cenas
- Definição de personagens
- Diálogos naturais
- Descrições visuais detalhadas
- Otimização para diferentes durações (3-15 min)

**Exemplo de roteiro gerado:**
```json
{
  "titulo": "A História de Davi e Golias",
  "cenas": [
    {
      "numero": 1,
      "tipo": "narracao",
      "duracao": "10s",
      "texto": "Há muito tempo atrás, na antiga Israel...",
      "personagens": ["Davi"],
      "descricao_visual": "Paisagem de Israel ao pôr do sol"
    }
  ]
}
```

### 👤 Módulo 2: CharacterGenerator

Cria personagens consistentes com:
- Estilo cartoon 3D (Pixar-like)
- Múltiplas variações (ângulos, expressões)
- Cache para reutilização
- Resolução alta (1024x1024)

**Personagens pré-configurados:**
- Personagens bíblicos (Davi, Moisés, Jesus, etc)
- Personagens de fábulas
- Personagens customizados sob demanda

### 🎙️ Módulo 3: AudioGenerator

Narração profissional com ElevenLabs:
- Vozes ultra-realistas
- Suporte a PT-BR, EN, ES
- Ajuste de estabilidade e clareza
- Processamento em lote eficiente

**Qualidade de áudio:**
- Sample rate: 44.1 kHz
- Formato: MP3/WAV
- Canais: Stereo
- Bitrate: 192 kbps

### 🎬 Módulo 4: AnimationGenerator

Anima imagens estáticas usando IA:
- Movimentos naturais e suaves
- Duração configurável (3-10s por cena)
- Múltiplos estilos de movimento
- Qualidade profissional (30 FPS)

### 💋 Módulo 5: LipsyncGenerator

Sincronização labial perfeita:
- Lip-sync automático com Wav2Lip
- Sincronização precisa com áudio
- Mantém qualidade visual
- Processamento rápido

### ✂️ Módulo 6: VideoEditor

Montagem final profissional:
- Transições suaves (fade, crossfade)
- Sincronização áudio/vídeo
- Ajuste de duração automático
- Exportação em múltiplas resoluções

---

## 📦 Pré-requisitos

### APIs Necessárias

Você precisará criar contas e obter API keys nas seguintes plataformas:

| API | Função | Custo | Link de Cadastro |
|-----|--------|-------|------------------|
| **OpenAI** | Geração de roteiros | $5-20/mês | [platform.openai.com](https://platform.openai.com) |
| **ElevenLabs** | Narração profissional | Grátis até 10K chars | [elevenlabs.io](https://elevenlabs.io) |
| **Replicate** | Animação e lip-sync | $10-30/mês | [replicate.com](https://replicate.com) |

**💰 Investimento inicial recomendado:** ~$15 USD (suficiente para 10-15 vídeos)

### Configuração das APIs

#### 1. OpenAI (ChatGPT)

1. Acesse [platform.openai.com](https://platform.openai.com)
2. Crie uma conta
3. Vá em "API Keys"
4. Clique em "Create new secret key"
5. Copie a chave (começa com `sk-...`)
6. Adicione créditos ($5-10 é suficiente para começar)

**Dica:** Use GPT-3.5-turbo em vez de GPT-4 para economizar 20x nos custos!

#### 2. ElevenLabs (Narração)

1. Acesse [elevenlabs.io](https://elevenlabs.io)
2. Crie uma conta gratuita
3. Vá em "Profile" → "API Keys"
4. Copie sua API key
5. Plano gratuito: 10.000 caracteres/mês (≈2-3 vídeos)
6. Plano pago: A partir de $5/mês

**Dica:** O plano gratuito é suficiente para testar!

#### 3. Replicate (Animação)

1. Acesse [replicate.com](https://replicate.com)
2. Crie uma conta
3. Vá em "Account" → "API Tokens"
4. Copie seu token (começa com `r8_...`)
5. Adicione créditos ($10 é suficiente para começar)

---

## 🚀 Instalação

### Opção 1: Google Colab (RECOMENDADO) ⭐

**A forma mais fácil e rápida de usar o ProjetoX!**

1. **Clique no badge abaixo para abrir no Colab:**

   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Ganzer-Publicidade/projetoX/blob/main/notebooks/ProjetoX_Principal.ipynb)

2. **Configure suas API keys nos Secrets:**
   - Clique no ícone 🔑 na barra lateral esquerda
   - Adicione cada chave:
     - Nome: `OPENAI_API_KEY` → Valor: sua chave OpenAI
     - Nome: `ELEVENLABS_API_KEY` → Valor: sua chave ElevenLabs
     - Nome: `REPLICATE_API_TOKEN` → Valor: seu token Replicate
   - Toggle: **Enable notebook access** ✅

3. **Execute as células em ordem:**
   - Pressione `Ctrl+F9` ou vá em "Runtime" → "Run all"
   - Aguarde 15-30 minutos
   - Seu vídeo estará pronto! 🎉

**Vantagens do Colab:**
- ✅ Sem instalação local
- ✅ GPU gratuita
- ✅ Salva vídeos no Google Drive
- ✅ Funciona em qualquer computador

### Opção 2: Instalação Local

**Requisitos:**
- Python 3.8 ou superior
- ffmpeg instalado
- 8GB+ de RAM
- (Opcional) GPU NVIDIA para animação mais rápida

**Passo a passo:**

```bash
# 1. Clone o repositório
git clone https://github.com/Ganzer-Publicidade/projetoX.git
cd projetoX

# 2. Crie ambiente virtual
python -m venv venv

# No Linux/Mac:
source venv/bin/activate

# No Windows:
venv\Scripts\activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Instale ffmpeg (se não tiver)
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# MacOS:
brew install ffmpeg

# Windows:
# Baixe de: https://ffmpeg.org/download.html

# 5. Configure API keys
cp config/api_keys_template.py config/api_keys.py
nano config/api_keys.py  # Edite com suas chaves

# 6. Execute exemplo
python examples/gerar_video.py
```

---

## ⚡ Uso Rápido

### No Google Colab (Modo Simples)

```python
from src.pipeline import VideoAutomationPipeline

config = {
    'nicho': 'conteudo_religioso',
    'tema': 'A História de Davi e Golias',
    'duracao_minutos': 5,
    'idioma': 'pt-br',
    'api_keys': {
        'openai': 'sk-...',
        'elevenlabs': '...',
        'replicate': 'r8_...'
    }
}

pipeline = VideoAutomationPipeline(config)
video_path = pipeline.executar_completo()

print(f"✅ Vídeo pronto: {video_path}")
```

### Com Otimizações de Custo

```python
config = {
    'nicho': 'conteudo_religioso',
    'tema': 'A História de Noé e a Arca',
    'duracao_minutos': 7,
    'idioma': 'pt-br',
    'api_keys': {
        'openai': 'sk-...',
        'elevenlabs': '...',
        'replicate': 'r8_...'
    },
    'optimization': {
        'cena_duration_seconds': 5,      # 50% mais barato
        'use_gpt35': True,                # 20x mais barato que GPT-4
        'enable_cache': True,             # Reutiliza personagens
        'batch_size': 5                   # Processa 5 cenas por vez
    }
}

pipeline = VideoAutomationPipeline(config)
video_path = pipeline.executar_completo()
```

### Notebooks Modulares (Para Testar Separadamente)

Se você quer testar cada módulo individualmente:

1. **[01_Gerador_Roteiro.ipynb](notebooks/01_Gerador_Roteiro.ipynb)** - Testa geração de roteiros
2. **[02_Gerador_Personagens.ipynb](notebooks/02_Gerador_Personagens.ipynb)** - Testa criação de personagens
3. **[03_Gerador_Audio.ipynb](notebooks/03_Gerador_Audio.ipynb)** - Testa narração
4. **[04_Animacao_Video.ipynb](notebooks/04_Animacao_Video.ipynb)** - Testa animação
5. **[05_Editor_Final.ipynb](notebooks/05_Editor_Final.ipynb)** - Testa edição

---

## 📚 Documentação Completa

### Estrutura do Projeto

```
projetoX/
├── src/                          # Módulos principais
│   ├── pipeline.py               # Orquestrador principal
│   ├── roteiro_generator.py      # Geração de roteiros
│   ├── character_generator.py    # Criação de personagens
│   ├── audio_generator.py        # Narração e áudio
│   ├── animation_generator.py    # Animação de cenas
│   ├── lipsync_generator.py      # Sincronização labial
│   ├── video_editor.py           # Edição final
│   └── utils.py                  # Funções auxiliares
├── config/                       # Configurações
│   ├── settings.py               # Configurações globais
│   └── api_keys_template.py      # Template de API keys
├── notebooks/                    # Notebooks Jupyter/Colab
│   ├── ProjetoX_Principal.ipynb  # Notebook principal ⭐
│   ├── 01_Gerador_Roteiro.ipynb
│   ├── 02_Gerador_Personagens.ipynb
│   ├── 03_Gerador_Audio.ipynb
│   ├── 04_Animacao_Video.ipynb
│   └── 05_Editor_Final.ipynb
├── examples/                     # Exemplos e templates
│   ├── exemplo_roteiro.json      # Roteiro de exemplo
│   ├── exemplo_personagens.json  # Catálogo de personagens
│   └── exemplo_completo.json     # Config completa
├── requirements.txt              # Dependências Python
├── LICENSE                       # Licença MIT
└── README.md                     # Este arquivo

```

### Configurações Avançadas

#### Personalizar Estilo Visual

```python
from config.settings import CHARACTER_CONFIG

# Modificar estilo dos personagens
CHARACTER_CONFIG['style'] = 'realistic'  # ou 'cartoon_3d', 'anime', '2d_flat'
CHARACTER_CONFIG['resolution'] = 2048     # Maior resolução
CHARACTER_CONFIG['quality'] = 'ultra'     # Qualidade máxima
```

#### Ajustar Voz da Narração

```python
from config.settings import AI_CONFIG

# Voz mais estável (menos variação)
AI_CONFIG['elevenlabs_stability'] = 0.8

# Voz mais clara (mais semelhante à original)
AI_CONFIG['elevenlabs_similarity_boost'] = 0.9
```

#### Otimizar Custos

```python
from config.settings import OPTIMIZATION_CONFIG

# Reduzir duração de cenas (economiza em animação)
OPTIMIZATION_CONFIG['default_cena_duration_seconds'] = 3  # Mínimo 3s

# Usar GPT-3.5 (muito mais barato)
OPTIMIZATION_CONFIG['use_gpt35_by_default'] = True

# Habilitar cache de personagens
OPTIMIZATION_CONFIG['enable_character_cache'] = True
```

---

## 💰 Custos Detalhados

### Custo por Vídeo (5 minutos)

| Componente | Detalhes | Custo (USD) | Custo (BRL) |
|------------|----------|-------------|-------------|
| **Roteiro** | GPT-3.5 (~2K tokens) | $0.02 | R$ 0.10 |
| **Personagens** | 3-5 personagens (cache) | $0.20 | R$ 1.00 |
| **Narração** | 3000 caracteres | $0.60 | R$ 3.00 |
| **Animação** | 60 cenas de 5s | $1.80 | R$ 9.00 |
| **Lip-sync** | 60 cenas | $0.50 | R$ 2.50 |
| **TOTAL** | | **$3.12** | **R$ 15.60** |

### Com Otimizações de Custo

| Otimização | Economia | Custo Final |
|------------|----------|-------------|
| Cenas de 5s (em vez de 10s) | -50% animação | $2.22 (R$ 11.10) |
| GPT-3.5 (em vez de GPT-4) | -80% roteiro | $2.14 (R$ 10.70) |
| Cache de personagens | -$0.20/vídeo | $1.94 (R$ 9.70) |
| **TOTAL COM TUDO** | | **$1.94** | **R$ 9.70** |

### Custos Mensais (Produção Escalada)

**Cenário 1: Iniciante (10 vídeos/mês)**
- Custo: $19.40 (≈R$ 97)
- Potencial de views: 10K-50K
- Receita estimada (monetizado): R$ 50-250

**Cenário 2: Intermediário (30 vídeos/mês)**
- Custo: $58.20 (≈R$ 291)
- Potencial de views: 100K-300K
- Receita estimada: R$ 500-1500

**Cenário 3: Profissional (100 vídeos/mês)**
- Custo: $194 (≈R$ 970)
- Potencial de views: 500K-1M
- Receita estimada: R$ 2500-10000

---

## 🏆 Nichos Lucrativos

### Top 5 Nichos Recomendados

#### 1. 🙏 Conteúdo Religioso
- **CPM médio:** $3-8
- **Audiência:** Muito engajada e leal
- **Exemplos:** Histórias bíblicas, mensagens de fé, versículos explicados
- **Potencial mensal:** R$ 2.000 - R$ 10.000

**Ideias de vídeos:**
- A História de Moisés
- Noé e a Arca
- José do Egito
- Daniel na Cova dos Leões
- Parábolas de Jesus

#### 2. 📚 Resumos de Livros
- **CPM médio:** $5-12
- **Audiência:** Educada e com poder aquisitivo
- **Exemplos:** Clássicos da literatura, desenvolvimento pessoal, negócios
- **Potencial mensal:** R$ 3.000 - R$ 15.000

**Ideias de vídeos:**
- O Pequeno Príncipe
- 1984 de George Orwell
- Sapiens em 10 minutos
- Hábitos Atômicos resumido

#### 3. 👶 Conteúdo Infantil
- **CPM médio:** $3-8
- **Audiência:** Pais buscando conteúdo seguro
- **Exemplos:** Fábulas, histórias educativas, curiosidades
- **Potencial mensal:** R$ 5.000 - R$ 20.000

**Ideias de vídeos:**
- A Lebre e a Tartaruga
- Os Três Porquinhos
- Chapeuzinho Vermelho
- Como os animais dormem?

#### 4. 😱 Terror/Mistério
- **CPM médio:** $2-6
- **Audiência:** Altamente engajada
- **Exemplos:** Lendas urbanas, histórias de terror, mistérios
- **Potencial mensal:** R$ 1.000 - R$ 8.000

**Ideias de vídeos:**
- A Loira do Banheiro
- Mistérios Não Resolvidos
- Casos Sobrenaturais Reais

#### 5. 🧠 Curiosidades/Educação
- **CPM médio:** $4-10
- **Audiência:** Ampla e diversificada
- **Exemplos:** Fatos históricos, ciência, tecnologia
- **Potencial mensal:** R$ 2.000 - R$ 12.000

**Ideias de vídeos:**
- 10 Curiosidades sobre o Egito
- Como Funciona o Cérebro?
- Invenções que Mudaram o Mundo

---

## 🗺️ Roadmap

### Versão Atual (v1.0) ✅
- [x] Pipeline completo funcionando
- [x] 6 módulos profissionais
- [x] Notebooks Colab interativos
- [x] Exemplos e templates
- [x] Documentação completa
- [x] Otimizações de custo

### Próximas Funcionalidades

#### v1.1 (Em breve)
- [ ] Interface web com Gradio
- [ ] Upload automático no YouTube
- [ ] Geração automática de thumbnails
- [ ] Mais vozes em português

#### v1.2 (Planejado)
- [ ] Suporte a mais idiomas (FR, DE, IT)
- [ ] Análise de tendências do YouTube
- [ ] Sugestões automáticas de temas
- [ ] Agendamento de publicações

#### v2.0 (Futuro)
- [ ] Multi-idioma simultâneo
- [ ] Sistema de templates customizáveis
- [ ] API REST para integração
- [ ] Dashboard de analytics
- [ ] Marketplace de personagens

---

## 🐛 Troubleshooting

### Problemas Comuns e Soluções

#### ❌ Erro: "API key inválida"

**Causa:** API key não configurada ou incorreta

**Solução:**
1. Verifique se configurou nos Secrets do Colab corretamente
2. Confirme que as chaves não expiraram
3. Teste as chaves diretamente nos sites das APIs
4. Verifique se há espaços em branco antes/depois da chave

#### ❌ Erro: "Memória insuficiente"

**Causa:** Colab ficou sem RAM durante processamento

**Solução:**
1. Reduza `cena_duration_seconds` para 3-5 segundos
2. Diminua `batch_size` para 3
3. Reinicie o runtime: Runtime → Restart runtime
4. Use Colab Pro para mais RAM (opcional)

#### ❌ Vídeo não gera / Pipeline trava

**Causa:** Alguma etapa falhou

**Solução:**
1. Verifique se tem créditos suficientes nas APIs
2. Veja os logs para identificar a etapa que falhou
3. Use checkpoints para retomar de onde parou:
   ```python
   pipeline.executar_completo(usar_checkpoint=True)
   ```
4. Execute etapas individualmente para debugar

#### ❌ Áudio e vídeo dessincronizados

**Causa:** Duração de cenas inconsistente

**Solução:**
1. Verifique se todas as cenas têm duração definida
2. Use durações múltiplas de 0.5 segundos
3. Atualize MoviePy para última versão:
   ```bash
   pip install --upgrade moviepy
   ```

#### ❌ Personagens diferentes em cada cena

**Causa:** Cache de personagens não habilitado

**Solução:**
1. Ative o cache:
   ```python
   config['optimization']['enable_character_cache'] = True
   ```
2. Use seed fixo para consistência:
   ```python
   CHARACTER_CONFIG['random_seed'] = 42
   ```

#### ❌ Custo maior que o esperado

**Causa:** Configurações não otimizadas

**Solução:**
1. Use GPT-3.5: `use_gpt35 = True`
2. Reduza duração de cenas: `cena_duration_seconds = 5`
3. Ative cache: `enable_cache = True`
4. Monitore custos nas dashboards das APIs

### Obter Ajuda

Se o problema persistir:

1. **Issues do GitHub:** [github.com/Ganzer-Publicidade/projetoX/issues](https://github.com/Ganzer-Publicidade/projetoX/issues)
2. **Documentação das APIs:**
   - [OpenAI](https://platform.openai.com/docs)
   - [ElevenLabs](https://docs.elevenlabs.io)
   - [Replicate](https://replicate.com/docs)

---

## 🤝 Contribuição

Contribuições são muito bem-vindas! ❤️

### Como Contribuir

1. **Fork o projeto**
   ```bash
   # Clique em "Fork" no GitHub
   ```

2. **Crie sua branch**
   ```bash
   git checkout -b feature/MinhaFeature
   ```

3. **Commit suas mudanças**
   ```bash
   git commit -m 'Add: Minha nova feature incrível'
   ```

4. **Push para a branch**
   ```bash
   git push origin feature/MinhaFeature
   ```

5. **Abra um Pull Request**

### Diretrizes

- ✅ Escreva código limpo e documentado
- ✅ Adicione testes quando aplicável
- ✅ Atualize a documentação
- ✅ Siga o estilo de código existente
- ✅ Teste localmente antes de submeter

### Ideias para Contribuir

- 🎨 Novos estilos de personagens
- 🌍 Suporte a mais idiomas
- 🎵 Biblioteca de músicas de fundo
- 📊 Dashboard de analytics
- 🎬 Novos tipos de transições
- 📱 Interface mobile-friendly

---

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

**Isso significa que você pode:**
- ✅ Usar comercialmente
- ✅ Modificar o código
- ✅ Distribuir
- ✅ Uso privado

**Com a condição de:**
- ⚠️ Incluir a licença original
- ⚠️ Incluir aviso de copyright

---

## 🌟 Agradecimentos

Este projeto não seria possível sem:

- **OpenAI** pelo GPT e tecnologias de IA
- **ElevenLabs** pelas incríveis vozes sintéticas
- **Replicate** pela infraestrutura de modelos de IA
- **Google Colab** pelo ambiente de desenvolvimento gratuito
- **Comunidade Open Source** por todas as bibliotecas utilizadas

---

## 📞 Contato

**Ganzer Publicidade**

- 🐙 GitHub: [@Ganzer-Publicidade](https://github.com/Ganzer-Publicidade)
- 🐛 Issues: [github.com/Ganzer-Publicidade/projetoX/issues](https://github.com/Ganzer-Publicidade/projetoX/issues)
- 📧 Email: [Abrir issue para contato](https://github.com/Ganzer-Publicidade/projetoX/issues/new)

---

## 💡 FAQ (Perguntas Frequentes)

### Quanto custa para começar?

~$15 USD de investimento inicial nas APIs. Suficiente para gerar 5-10 vídeos de teste.

### Preciso saber programar?

Não! Os notebooks do Colab são interativos. Basta clicar em "Execute" em cada célula.

### Funciona em computador fraco?

Sim! No Google Colab roda em qualquer computador, até Chromebooks.

### Posso monetizar os vídeos?

Sim! Os vídeos gerados são 100% seus. Você pode monetizar no YouTube.

### Quanto tempo leva para gerar um vídeo?

15-30 minutos para um vídeo de 5 minutos.

### Posso usar vozes customizadas?

Sim! ElevenLabs permite clonar vozes (plano pago).

### O sistema funciona em português?

Sim! Totalmente em português, incluindo vozes e interface.

### Preciso de GPU?

Não para o Colab (já tem GPU gratuita). Para local, GPU ajuda mas não é obrigatório.

---

<div align="center">

**⭐ Se este projeto te ajudou, deixe uma estrela no GitHub! ⭐**

**Feito com ❤️ e ☕ para dominar o YouTube!**

[![Star on GitHub](https://img.shields.io/github/stars/Ganzer-Publicidade/projetoX?style=social)](https://github.com/Ganzer-Publicidade/projetoX)

**🚀 BORA CRIAR VÍDEOS INCRÍVEIS! 🚀**

</div>

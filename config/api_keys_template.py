"""
🔑 TEMPLATE DE API KEYS - ProjetoX

⚠️ IMPORTANTE: 
- Este é apenas um TEMPLATE - NÃO commite suas chaves reais!
- Use os Secrets do Google Colab para armazenar suas chaves
- Ou use variáveis de ambiente (.env)
- Nunca compartilhe suas API keys publicamente

📚 Como obter cada API Key:
"""

# ============================================================================
# OPENAI (ChatGPT) - Para geração de roteiros
# ============================================================================
# 1. Acesse: https://platform.openai.com/api-keys
# 2. Crie uma conta ou faça login
# 3. Clique em "Create new secret key"
# 4. Copie e guarde em local seguro

OPENAI_API_KEY = "sk-proj-..."  # Substitua com sua chave real


# ============================================================================
# ELEVENLABS - Para narração e áudio
# ============================================================================
# 1. Acesse: https://elevenlabs.io
# 2. Crie uma conta gratuita
# 3. Vá em Settings > API Keys
# 4. Copie sua API key

ELEVENLABS_API_KEY = "..."  # Substitua com sua chave real


# ============================================================================
# REPLICATE - Para animação e efeitos visuais
# ============================================================================
# 1. Acesse: https://replicate.com/account/api-tokens
# 2. Faça login ou crie conta
# 3. Copie seu API token (começa com r8_)

REPLICATE_API_TOKEN = "r8_..."  # Substitua com seu token real


# ============================================================================
# LEONARDO AI (OPCIONAL) - Para geração de personagens
# ============================================================================
# 1. Acesse: https://app.leonardo.ai/settings
# 2. Crie conta gratuita
# 3. Gere sua API key em Settings

LEONARDO_API_KEY = ""  # Opcional - deixe vazio se não for usar


# ============================================================================
# RUNWAY ML (OPCIONAL) - Para animação avançada
# ============================================================================
# 1. Acesse: https://runwayml.com
# 2. Crie conta
# 3. Acesse API settings

RUNWAY_API_KEY = ""  # Opcional - deixe vazio se não for usar


# ============================================================================
# YOUTUBE DATA API (OPCIONAL) - Para análise de tendências
# ============================================================================
# 1. Acesse: https://console.cloud.google.com
# 2. Crie novo projeto
# 3. Ative YouTube Data API v3
# 4. Crie credenciais > API Key

YOUTUBE_API_KEY = ""  # Opcional - para análise de tendências


# ============================================================================
# 💡 DICA: Como usar no Google Colab de forma segura
# ============================================================================
"""
No Google Colab, use Secrets em vez de hardcode:

1. Clique no ícone de chave 🔑 na barra lateral
2. Adicione cada API key como um secret:
   - Nome: OPENAI_API_KEY
   - Valor: sk-proj-...
3. No código, acesse assim:

from google.colab import userdata

OPENAI_API_KEY = userdata.get('OPENAI_API_KEY')
ELEVENLABS_API_KEY = userdata.get('ELEVENLABS_API_KEY')
REPLICATE_API_TOKEN = userdata.get('REPLICATE_API_TOKEN')
"""


# ============================================================================
# 💰 Custos Estimados (Referência)
# ============================================================================
"""
Para um vídeo de 5 minutos:

OpenAI (GPT-4):          ~$0.10 - $0.30
ElevenLabs (11k chars):  ~$0.30 - $1.00
Replicate (Animação):    ~$0.50 - $2.00
Total estimado:          ~$1.00 - $3.50 por vídeo

💡 Use modelos mais baratos para teste:
- GPT-3.5-turbo em vez de GPT-4
- Vozes gratuitas do ElevenLabs (limite mensal)
- Modelos mais simples no Replicate
"""

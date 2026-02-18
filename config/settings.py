"""
⚙️ CONFIGURAÇÕES GLOBAIS - ProjetoX

Este arquivo contém todas as configurações padrão do sistema.
Você pode modificar estes valores conforme necessário.
"""

import os

# ============================================================================
# 🎬 CONFIGURAÇÕES DE VÍDEO
# ============================================================================
VIDEO_CONFIG = {
    # Resolução final do vídeo
    'resolution': (1920, 1080),  # Full HD (16:9)
    
    # Taxa de quadros por segundo
    'fps': 30,
    
    # Bitrate de vídeo (qualidade)
    'bitrate': '5000k',  # 5 Mbps - boa qualidade
    
    # Codec de vídeo
    'codec': 'libx264',  # H.264 - compatível com YouTube
    
    # Codec de áudio
    'audio_codec': 'aac',  # AAC - padrão YouTube
    
    # Formato de saída
    'format': 'mp4',  # MP4 - universal
    
    # Preset de encoding (quanto mais rápido, menor qualidade)
    'preset': 'medium',  # Opções: ultrafast, fast, medium, slow, veryslow
}


# ============================================================================
# 🎵 CONFIGURAÇÕES DE ÁUDIO
# ============================================================================
AUDIO_CONFIG = {
    # Taxa de amostragem
    'sample_rate': 44100,  # 44.1 kHz - qualidade CD
    
    # Canais de áudio
    'channels': 2,  # Estéreo
    
    # Formato de áudio
    'format': 'mp3',  # MP3 para compatibilidade
    
    # Bitrate de áudio
    'bitrate': '192k',  # 192 kbps - boa qualidade
    
    # Volume da música de fundo (dB)
    'background_music_volume': -10,  # -10dB mais baixo que narração
    
    # Volume dos efeitos sonoros (dB)
    'sound_effects_volume': -5,  # -5dB mais baixo que narração
}


# ============================================================================
# 👤 CONFIGURAÇÕES DE PERSONAGENS
# ============================================================================
CHARACTER_CONFIG = {
    # Estilo visual padrão
    'style': 'cartoon_3d',  # Opções: cartoon_3d, realistic, anime, 2d_flat
    
    # Resolução das imagens de personagens
    'resolution': 1024,  # 1024x1024 pixels
    
    # Aspect ratio
    'aspect_ratio': '16:9',  # Para vídeo horizontal
    
    # Número de variações por personagem
    'num_variations': 3,  # Diferentes ângulos/expressões
    
    # Qualidade da imagem
    'quality': 'high',  # Opções: low, medium, high
    
    # Prompt base para personagens
    'base_prompt': 'high quality 3D cartoon character, pixar style, professional render, clean background',
}


# ============================================================================
# 🤖 CONFIGURAÇÕES DE IA
# ============================================================================
AI_CONFIG = {
    # Modelo OpenAI para roteiros
    'openai_model': 'gpt-4-turbo-preview',  # ou 'gpt-3.5-turbo' (mais barato)
    
    # Temperatura para geração de texto (0-2)
    'openai_temperature': 0.7,  # 0 = determinístico, 2 = muito criativo
    
    # Máximo de tokens por resposta
    'openai_max_tokens': 4000,
    
    # Voz padrão ElevenLabs (idioma)
    'elevenlabs_voice_id': 'pt-BR-default',  # Vozes PT-BR disponíveis
    
    # Modelo de voz (qualidade)
    'elevenlabs_model': 'eleven_multilingual_v2',
    
    # Estabilidade da voz (0-1)
    'elevenlabs_stability': 0.5,
    
    # Clareza/similaridade (0-1)
    'elevenlabs_similarity_boost': 0.75,
    
    # Modelo Replicate para animação
    'replicate_animation_model': 'stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438',
    
    # Modelo para lip-sync
    'replicate_lipsync_model': 'devxpy/cog-wav2lip:8d65e3f4f4298520e079198b493c25adfc43c058ffec924f2aefc8010ed25eef',
    
    # Timeout para chamadas API (segundos)
    'timeout': 300,  # 5 minutos
    
    # Número de tentativas em caso de erro
    'max_retries': 3,
    
    # Delay entre tentativas (segundos)
    'retry_delay': 5,
}


# ============================================================================
# 📁 DIRETÓRIOS
# ============================================================================
DIRS = {
    # Diretório de saída (vídeos finais)
    'output': '/content/drive/MyDrive/ProjetoX/videos/',
    
    # Diretório temporário (arquivos intermediários)
    'temp': '/content/temp/',
    
    # Diretório de cache (personagens reutilizáveis)
    'cache': '/content/cache/',
    
    # Diretório de checkpoints (para recuperação)
    'checkpoints': '/content/drive/MyDrive/ProjetoX/checkpoints/',
    
    # Diretório de logs
    'logs': '/content/drive/MyDrive/ProjetoX/logs/',
}


# ============================================================================
# 🎨 ESTILOS DE VÍDEO POR NICHO
# ============================================================================
NICHO_STYLES = {
    'historias_infantis': {
        'character_style': 'cartoon_3d',
        'color_palette': 'bright_colorful',
        'music_mood': 'cheerful',
        'voice_type': 'gentle_narrator',
    },
    'terror': {
        'character_style': 'realistic_dark',
        'color_palette': 'dark_moody',
        'music_mood': 'suspenseful',
        'voice_type': 'deep_dramatic',
    },
    'curiosidades': {
        'character_style': 'modern_flat',
        'color_palette': 'tech_modern',
        'music_mood': 'upbeat',
        'voice_type': 'energetic',
    },
    'motivacional': {
        'character_style': 'realistic',
        'color_palette': 'warm_inspiring',
        'music_mood': 'epic_inspiring',
        'voice_type': 'confident_powerful',
    },
}


# ============================================================================
# 🌍 CONFIGURAÇÕES DE IDIOMA
# ============================================================================
LANGUAGE_CONFIG = {
    'pt-br': {
        'name': 'Português Brasileiro',
        'elevenlabs_voice_ids': {
            'narrator': 'pNInz6obpgDQGcFmaJgB',  # Adam (BR)
            'character_male': 'yoZ06aMxZJJ28mfd3POQ',  # Sam (BR)
            'character_female': 'jsCqWAovK2LkecY7zXl4',  # Freya (BR)
        },
        'openai_instructions': 'Responda sempre em português brasileiro claro e natural.',
    },
    'en': {
        'name': 'English',
        'elevenlabs_voice_ids': {
            'narrator': 'pNInz6obpgDQGcFmaJgB',  # Adam
            'character_male': 'yoZ06aMxZJJ28mfd3POQ',  # Sam
            'character_female': 'jsCqWAovK2LkecY7zXl4',  # Freya
        },
        'openai_instructions': 'Always respond in clear, natural English.',
    },
    'es': {
        'name': 'Español',
        'elevenlabs_voice_ids': {
            'narrator': 'pNInz6obpgDQGcFmaJgB',  # Adam (ES)
            'character_male': 'yoZ06aMxZJJ28mfd3POQ',  # Sam (ES)
            'character_female': 'jsCqWAovK2LkecY7zXl4',  # Freya (ES)
        },
        'openai_instructions': 'Responde siempre en español claro y natural.',
    },
}


# ============================================================================
# ⚡ CONFIGURAÇÕES DE OTIMIZAÇÃO PARA COLAB
# ============================================================================
OPTIMIZATION_CONFIG = {
    # Processar cenas em lotes (para evitar crash de memória)
    'batch_size': 5,
    
    # Limpar memória após cada lote
    'clear_memory_after_batch': True,
    
    # Salvar checkpoint após cada etapa
    'save_checkpoints': True,
    
    # Comprimir imagens temporárias
    'compress_temp_images': True,
    
    # Qualidade de compressão (0-100)
    'compression_quality': 85,
    
    # Deletar arquivos temporários após uso
    'cleanup_temp_files': True,
    
    # ========================================================================
    # 💰 OTIMIZAÇÕES DE CUSTO (Issue #3)
    # ========================================================================
    
    # Duração padrão de cada cena (reduz custo de animação)
    'default_cena_duration_seconds': 5,  # Era 10s, agora 5s = 50% economia!
    
    # Usar GPT-3.5 em vez de GPT-4 por padrão
    'use_gpt35_by_default': True,  # 20x mais barato que GPT-4
    
    # Cache de personagens (reutilizar entre vídeos)
    'enable_character_cache': True,
    
    # Número de cenas a processar em paralelo
    'parallel_batch_size': 3,
}


# ============================================================================
# 📊 CONFIGURAÇÕES DE LOGGING
# ============================================================================
LOGGING_CONFIG = {
    # Nível de log
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    
    # Formato do log
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    
    # Salvar logs em arquivo
    'save_to_file': True,
    
    # Nome do arquivo de log
    'log_file': 'projetoX.log',
    
    # Logs coloridos no console
    'colored_output': True,
}


# ============================================================================
# 🚀 CONFIGURAÇÕES DE PERFORMANCE
# ============================================================================
PERFORMANCE_CONFIG = {
    # Usar cache de personagens
    'use_character_cache': True,
    
    # Usar cache de áudios
    'use_audio_cache': True,
    
    # Processamento paralelo (threads)
    'max_workers': 4,
    
    # Timeout geral (segundos)
    'global_timeout': 3600,  # 1 hora
}


# ============================================================================
# 🎯 CONFIGURAÇÕES PADRÃO DE PROJETO
# ============================================================================
DEFAULT_PROJECT_CONFIG = {
    'nicho': 'historias_infantis',
    'tema': 'História de exemplo',
    'duracao_minutos': 5,
    'idioma': 'pt-br',
    'num_cenas': 25,
    'incluir_musica': True,
    'incluir_efeitos_sonoros': True,
    'aplicar_lipsync': True,
    'gerar_legendas': False,
    'incluir_intro_outro': False,
}


# ============================================================================
# 🔧 FUNÇÕES AUXILIARES
# ============================================================================

def get_config_for_nicho(nicho: str) -> dict:
    """
    Retorna configurações específicas para um nicho.
    
    Args:
        nicho: Nome do nicho (ex: 'historias_infantis')
    
    Returns:
        Dicionário com configurações do nicho
    """
    return NICHO_STYLES.get(nicho, NICHO_STYLES['historias_infantis'])


def get_voice_for_language(language: str, voice_type: str = 'narrator') -> str:
    """
    Retorna o ID da voz adequado para o idioma.
    
    Args:
        language: Código do idioma (ex: 'pt-br')
        voice_type: Tipo de voz (narrator, character_male, character_female)
    
    Returns:
        ID da voz do ElevenLabs
    """
    lang_config = LANGUAGE_CONFIG.get(language, LANGUAGE_CONFIG['pt-br'])
    return lang_config['elevenlabs_voice_ids'].get(voice_type, lang_config['elevenlabs_voice_ids']['narrator'])


def create_directories():
    """
    Cria todos os diretórios necessários se não existirem.
    """
    for dir_path in DIRS.values():
        os.makedirs(dir_path, exist_ok=True)
    print("✅ Diretórios criados com sucesso!")


# ============================================================================
# 📝 VALIDAÇÃO DE CONFIGURAÇÕES
# ============================================================================

def validate_config() -> bool:
    """
    Valida se todas as configurações essenciais estão corretas.
    
    Returns:
        True se válido, False caso contrário
    """
    try:
        # Validar resolução
        assert VIDEO_CONFIG['resolution'][0] > 0 and VIDEO_CONFIG['resolution'][1] > 0
        
        # Validar FPS
        assert VIDEO_CONFIG['fps'] > 0
        
        # Validar sample rate
        assert AUDIO_CONFIG['sample_rate'] > 0
        
        print("✅ Configurações validadas com sucesso!")
        return True
    except AssertionError as e:
        print(f"❌ Erro na validação: {e}")
        return False


if __name__ == '__main__':
    print("🔧 ProjetoX - Configurações")
    print(f"Versão: {__version__}")
    validate_config()
    create_directories()

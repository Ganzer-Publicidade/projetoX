"""
🔧 UTILS - Funções Auxiliares do ProjetoX

Este módulo contém funções utilitárias usadas por todo o sistema.
"""

import os
import sys
import json
import time
import logging
import hashlib
import requests
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import base64
from io import BytesIO

# Imports condicionais (podem não estar disponíveis em todos ambientes)
try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None


# ============================================================================
# 📁 FUNÇÕES DE ARQUIVO E DIRETÓRIO
# ============================================================================

def criar_diretorios(diretorios: List[str]) -> None:
    """
    Cria múltiplos diretórios se não existirem.
    
    Args:
        diretorios: Lista de caminhos de diretórios
    
    Example:
        >>> criar_diretorios(['/tmp/cache', '/tmp/output'])
    """
    for diretorio in diretorios:
        Path(diretorio).mkdir(parents=True, exist_ok=True)
    print(f"✅ {len(diretorios)} diretórios verificados/criados")


def limpar_diretorio(diretorio: str, extensoes: Optional[List[str]] = None) -> int:
    """
    Limpa arquivos de um diretório (opcionalmente apenas certas extensões).
    
    Args:
        diretorio: Caminho do diretório
        extensoes: Lista de extensões para deletar (ex: ['.mp4', '.tmp'])
                  Se None, deleta tudo
    
    Returns:
        Número de arquivos deletados
    
    Example:
        >>> limpar_diretorio('/tmp/temp', ['.tmp', '.cache'])
    """
    if not os.path.exists(diretorio):
        return 0
    
    deletados = 0
    for arquivo in os.listdir(diretorio):
        caminho = os.path.join(diretorio, arquivo)
        
        if os.path.isfile(caminho):
            if extensoes is None or any(arquivo.endswith(ext) for ext in extensoes):
                try:
                    os.remove(caminho)
                    deletados += 1
                except Exception as e:
                    print(f"⚠️ Não foi possível deletar {arquivo}: {e}")
    
    if deletados > 0:
        print(f"🗑️ {deletados} arquivos deletados de {diretorio}")
    
    return deletados


def get_tamanho_arquivo_mb(caminho: str) -> float:
    """
    Retorna o tamanho de um arquivo em MB.
    
    Args:
        caminho: Caminho do arquivo
    
    Returns:
        Tamanho em megabytes
    """
    if not os.path.exists(caminho):
        return 0.0
    
    tamanho_bytes = os.path.getsize(caminho)
    return tamanho_bytes / (1024 * 1024)


def gerar_nome_arquivo_unico(prefixo: str, extensao: str, diretorio: str = '/tmp') -> str:
    """
    Gera um nome de arquivo único com timestamp.
    
    Args:
        prefixo: Prefixo do nome do arquivo
        extensao: Extensão (com ou sem ponto)
        diretorio: Diretório base
    
    Returns:
        Caminho completo do arquivo
    
    Example:
        >>> path = gerar_nome_arquivo_unico('video', '.mp4', '/tmp/videos')
        '/tmp/videos/video_20240218_142530_a3f2.mp4'
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    hash_aleatorio = hashlib.md5(str(time.time()).encode()).hexdigest()[:4]
    
    if not extensao.startswith('.'):
        extensao = f'.{extensao}'
    
    nome_arquivo = f"{prefixo}_{timestamp}_{hash_aleatorio}{extensao}"
    return os.path.join(diretorio, nome_arquivo)


# ============================================================================
# 🌐 FUNÇÕES DE REDE E UPLOAD
# ============================================================================

def download_arquivo(url: str, destino: str, timeout: int = 300) -> bool:
    """
    Baixa um arquivo de uma URL.
    
    Args:
        url: URL do arquivo
        destino: Caminho de destino
        timeout: Timeout em segundos
    
    Returns:
        True se sucesso, False caso contrário
    
    Example:
        >>> download_arquivo('https://example.com/video.mp4', '/tmp/video.mp4')
    """
    try:
        print(f"⬇️ Baixando: {url}")
        
        response = requests.get(url, timeout=timeout, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(destino, 'wb') as f:
            if total_size == 0:
                f.write(response.content)
            else:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Progress simples
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\r⬇️ Progresso: {percent:.1f}%", end='', flush=True)
                
                print()  # Nova linha
        
        print(f"✅ Download completo: {get_tamanho_arquivo_mb(destino):.2f} MB")
        return True
        
    except Exception as e:
        print(f"❌ Erro no download: {e}")
        return False


def upload_para_imgur(caminho_imagem: str, client_id: Optional[str] = None) -> Optional[str]:
    """
    Faz upload de uma imagem para Imgur e retorna a URL pública.
    
    Args:
        caminho_imagem: Caminho da imagem local
        client_id: Client ID do Imgur (opcional)
    
    Returns:
        URL da imagem ou None se falhar
    
    Note:
        Requer uma conta no Imgur e Client ID.
        Alternativa gratuita sem necessidade de conta.
    """
    if not os.path.exists(caminho_imagem):
        print(f"❌ Arquivo não encontrado: {caminho_imagem}")
        return None
    
    try:
        with open(caminho_imagem, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode()
        
        headers = {
            'Authorization': f'Client-ID {client_id}' if client_id else 'Client-ID 546c25a59c58ad7'
        }
        
        data = {'image': image_data}
        
        response = requests.post(
            'https://api.imgur.com/3/image',
            headers=headers,
            data=data,
            timeout=60
        )
        
        if response.status_code == 200:
            url = response.json()['data']['link']
            print(f"✅ Upload Imgur: {url}")
            return url
        else:
            print(f"❌ Erro no upload: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Erro no upload para Imgur: {e}")
        return None


# ============================================================================
# 🖼️ FUNÇÕES DE IMAGEM
# ============================================================================

def redimensionar_imagem(
    caminho_entrada: str,
    caminho_saida: str,
    largura: int,
    altura: int,
    manter_aspecto: bool = True
) -> bool:
    """
    Redimensiona uma imagem.
    
    Args:
        caminho_entrada: Caminho da imagem original
        caminho_saida: Caminho da imagem redimensionada
        largura: Nova largura
        altura: Nova altura
        manter_aspecto: Manter proporção original
    
    Returns:
        True se sucesso
    """
    if not PILLOW_AVAILABLE:
        print("❌ Pillow não disponível")
        return False
    
    try:
        img = Image.open(caminho_entrada)
        
        if manter_aspecto:
            img.thumbnail((largura, altura), Image.Resampling.LANCZOS)
        else:
            img = img.resize((largura, altura), Image.Resampling.LANCZOS)
        
        img.save(caminho_saida, quality=95, optimize=True)
        
        print(f"✅ Imagem redimensionada: {largura}x{altura}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao redimensionar: {e}")
        return False


def converter_formato_imagem(caminho_entrada: str, caminho_saida: str, formato: str = 'PNG') -> bool:
    """
    Converte uma imagem para outro formato.
    
    Args:
        caminho_entrada: Caminho da imagem original
        caminho_saida: Caminho da imagem convertida
        formato: Formato de saída (PNG, JPEG, WEBP, etc)
    
    Returns:
        True se sucesso
    """
    if not PILLOW_AVAILABLE:
        print("❌ Pillow não disponível")
        return False
    
    try:
        img = Image.open(caminho_entrada)
        
        # Converter RGBA para RGB se salvando em JPEG
        if formato.upper() == 'JPEG' and img.mode == 'RGBA':
            img = img.convert('RGB')
        
        img.save(caminho_saida, format=formato, quality=95)
        
        print(f"✅ Imagem convertida para {formato}")
        return True
        
    except Exception as e:
        print(f"❌ Erro na conversão: {e}")
        return False


# ============================================================================
# 🔐 FUNÇÕES DE VALIDAÇÃO
# ============================================================================

def validar_api_key(api_key: str, servico: str) -> bool:
    """
    Valida o formato básico de uma API key.
    
    Args:
        api_key: A chave da API
        servico: Nome do serviço (openai, elevenlabs, replicate)
    
    Returns:
        True se válida
    """
    if not api_key or api_key == "...":
        print(f"❌ API key {servico} não configurada")
        return False
    
    # Validações específicas por serviço
    if servico == 'openai':
        if not (api_key.startswith('sk-') and len(api_key) > 20):
            print(f"❌ API key OpenAI inválida (deve começar com 'sk-')")
            return False
    
    elif servico == 'replicate':
        if not (api_key.startswith('r8_') and len(api_key) > 20):
            print(f"❌ API key Replicate inválida (deve começar com 'r8_')")
            return False
    
    elif servico == 'elevenlabs':
        if len(api_key) < 20:
            print(f"❌ API key ElevenLabs muito curta")
            return False
    
    print(f"✅ API key {servico} válida")
    return True


def validar_arquivo_existe(caminho: str, descricao: str = "Arquivo") -> bool:
    """
    Valida se um arquivo existe.
    
    Args:
        caminho: Caminho do arquivo
        descricao: Descrição para mensagem de erro
    
    Returns:
        True se existe
    """
    if os.path.exists(caminho):
        return True
    else:
        print(f"❌ {descricao} não encontrado: {caminho}")
        return False


# ============================================================================
# 💰 FUNÇÕES DE CÁLCULO DE CUSTOS
# ============================================================================

def calcular_custo_estimado(
    num_cenas: int,
    duracao_minutos: int,
    usar_gpt4: bool = False,
    usar_animacao_premium: bool = False
) -> Dict[str, float]:
    """
    Calcula o custo estimado para gerar um vídeo.
    
    Args:
        num_cenas: Número de cenas
        duracao_minutos: Duração do vídeo em minutos
        usar_gpt4: Usar GPT-4 (mais caro) ou GPT-3.5
        usar_animacao_premium: Usar modelos premium de animação
    
    Returns:
        Dicionário com custos por serviço
    
    Example:
        >>> custos = calcular_custo_estimado(25, 5, usar_gpt4=True)
        >>> print(f"Total: ${custos['total']:.2f}")
    """
    custos = {}
    
    # OpenAI
    if usar_gpt4:
        custos['openai'] = 0.30  # GPT-4
    else:
        custos['openai'] = 0.05  # GPT-3.5-turbo
    
    # ElevenLabs (narração)
    caracteres_estimados = duracao_minutos * 1000  # ~1000 chars por minuto
    custos['elevenlabs'] = (caracteres_estimados / 1000) * 0.30  # $0.30 por 1k chars
    
    # Replicate (animação)
    if usar_animacao_premium:
        custos['replicate'] = num_cenas * 0.10  # $0.10 por cena premium
    else:
        custos['replicate'] = num_cenas * 0.03  # $0.03 por cena básica
    
    # Total
    custos['total'] = sum(custos.values())
    
    return custos


def formatar_custo(custo: float) -> str:
    """
    Formata um valor de custo para exibição.
    
    Args:
        custo: Valor em dólares
    
    Returns:
        String formatada
    
    Example:
        >>> formatar_custo(1.234)
        '$1.23'
    """
    return f"${custo:.2f}"


# ============================================================================
# ⏱️ FUNÇÕES DE TEMPO E DURAÇÃO
# ============================================================================

def formatar_duracao(segundos: float) -> str:
    """
    Formata duração em segundos para formato legível.
    
    Args:
        segundos: Duração em segundos
    
    Returns:
        String formatada (ex: "2m 30s", "1h 15m 30s")
    
    Example:
        >>> formatar_duracao(150)
        '2m 30s'
        >>> formatar_duracao(3665)
        '1h 1m 5s'
    """
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segs = int(segundos % 60)
    
    partes = []
    if horas > 0:
        partes.append(f"{horas}h")
    if minutos > 0:
        partes.append(f"{minutos}m")
    if segs > 0 or not partes:
        partes.append(f"{segs}s")
    
    return " ".join(partes)


def timestamp_para_segundos(timestamp: str) -> float:
    """
    Converte timestamp (MM:SS ou HH:MM:SS) para segundos.
    
    Args:
        timestamp: String no formato "MM:SS" ou "HH:MM:SS"
    
    Returns:
        Segundos
    
    Example:
        >>> timestamp_para_segundos("2:30")
        150.0
        >>> timestamp_para_segundos("1:15:30")
        4530.0
    """
    partes = timestamp.split(':')
    
    if len(partes) == 2:  # MM:SS
        return int(partes[0]) * 60 + int(partes[1])
    elif len(partes) == 3:  # HH:MM:SS
        return int(partes[0]) * 3600 + int(partes[1]) * 60 + int(partes[2])
    else:
        raise ValueError(f"Formato de timestamp inválido: {timestamp}")


# ============================================================================
# 📊 FUNÇÕES DE LOGGING
# ============================================================================

def configurar_logging(nivel: str = 'INFO', arquivo_log: Optional[str] = None) -> logging.Logger:
    """
    Configura o sistema de logging.
    
    Args:
        nivel: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        arquivo_log: Caminho do arquivo de log (opcional)
    
    Returns:
        Logger configurado
    """
    logger = logging.getLogger('ProjetoX')
    logger.setLevel(getattr(logging, nivel.upper()))
    
    # Formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (se especificado)
    if arquivo_log:
        file_handler = logging.FileHandler(arquivo_log, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def print_colorido(texto: str, cor: str = 'green', negrito: bool = False) -> None:
    """
    Imprime texto colorido no console (se Rich disponível).
    
    Args:
        texto: Texto a imprimir
        cor: Cor (green, red, yellow, blue, magenta, cyan)
        negrito: Texto em negrito
    """
    if RICH_AVAILABLE and console:
        estilo = f"bold {cor}" if negrito else cor
        console.print(texto, style=estilo)
    else:
        print(texto)


# ============================================================================
# 💾 FUNÇÕES DE CHECKPOINT
# ============================================================================

def salvar_checkpoint(dados: Dict, nome: str, diretorio: str = '/tmp/checkpoints') -> bool:
    """
    Salva um checkpoint do progresso.
    
    Args:
        dados: Dados a salvar
        nome: Nome do checkpoint
        diretorio: Diretório de checkpoints
    
    Returns:
        True se sucesso
    """
    try:
        criar_diretorios([diretorio])
        caminho = os.path.join(diretorio, f"{nome}.json")
        
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Checkpoint salvo: {nome}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao salvar checkpoint: {e}")
        return False


def carregar_checkpoint(nome: str, diretorio: str = '/tmp/checkpoints') -> Optional[Dict]:
    """
    Carrega um checkpoint salvo.
    
    Args:
        nome: Nome do checkpoint
        diretorio: Diretório de checkpoints
    
    Returns:
        Dados do checkpoint ou None
    """
    try:
        caminho = os.path.join(diretorio, f"{nome}.json")
        
        if not os.path.exists(caminho):
            print(f"⚠️ Checkpoint não encontrado: {nome}")
            return None
        
        with open(caminho, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        print(f"📂 Checkpoint carregado: {nome}")
        return dados
        
    except Exception as e:
        print(f"❌ Erro ao carregar checkpoint: {e}")
        return None


# ============================================================================
# 🧹 FUNÇÕES DE LIMPEZA
# ============================================================================

def limpar_memoria() -> None:
    """
    Força garbage collection para liberar memória.
    Útil no Google Colab após processar arquivos grandes.
    """
    import gc
    gc.collect()
    
    # Se CUDA disponível, limpa cache também
    try:
        import torch
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            print("🧹 Memória GPU limpa")
    except ImportError:
        pass
    
    print("🧹 Memória limpa")


# ============================================================================
# 🎯 FUNÇÕES DE VALIDAÇÃO DE CONFIGURAÇÃO
# ============================================================================

def validar_configuracao_projeto(config: Dict) -> bool:
    """
    Valida se uma configuração de projeto está completa.
    
    Args:
        config: Dicionário de configuração
    
    Returns:
        True se válida
    """
    campos_obrigatorios = ['nicho', 'tema', 'duracao_minutos', 'idioma']
    
    for campo in campos_obrigatorios:
        if campo not in config:
            print(f"❌ Campo obrigatório ausente: {campo}")
            return False
    
    # Validações específicas
    if config['duracao_minutos'] < 1 or config['duracao_minutos'] > 30:
        print("❌ Duração deve estar entre 1 e 30 minutos")
        return False
    
    if config['idioma'] not in ['pt-br', 'en', 'es']:
        print(f"❌ Idioma não suportado: {config['idioma']}")
        return False
    
    print("✅ Configuração válida")
    return True


# ============================================================================
# 📝 FUNÇÕES DE JSON
# ============================================================================

def salvar_json(dados: Dict, caminho: str, identado: bool = True) -> bool:
    """
    Salva dados em arquivo JSON.
    
    Args:
        dados: Dados a salvar
        caminho: Caminho do arquivo
        identado: Formatar com indentação
    
    Returns:
        True se sucesso
    """
    try:
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2 if identado else None)
        
        print(f"💾 JSON salvo: {caminho}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao salvar JSON: {e}")
        return False


def carregar_json(caminho: str) -> Optional[Dict]:
    """
    Carrega dados de arquivo JSON.
    
    Args:
        caminho: Caminho do arquivo
    
    Returns:
        Dados carregados ou None
    """
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        print(f"📂 JSON carregado: {caminho}")
        return dados
        
    except Exception as e:
        print(f"❌ Erro ao carregar JSON: {e}")
        return None


# ============================================================================
# 🎬 FUNÇÕES ESPECÍFICAS DE VÍDEO
# ============================================================================

def calcular_numero_cenas(duracao_minutos: int, duracao_cena_segundos: int = 10) -> int:
    """
    Calcula número de cenas baseado na duração total.
    
    Args:
        duracao_minutos: Duração total do vídeo
        duracao_cena_segundos: Duração média por cena
    
    Returns:
        Número de cenas
    """
    duracao_total_segundos = duracao_minutos * 60
    num_cenas = duracao_total_segundos // duracao_cena_segundos
    
    return max(5, min(50, num_cenas))  # Entre 5 e 50 cenas


if __name__ == '__main__':
    print("🔧 ProjetoX Utils - Teste de Funções")
    print(f"Pillow disponível: {PILLOW_AVAILABLE}")
    print(f"NumPy disponível: {NUMPY_AVAILABLE}")
    print(f"Rich disponível: {RICH_AVAILABLE}")
    
    # Teste de duração
    print(f"\nTeste de duração:")
    print(f"150s = {formatar_duracao(150)}")
    print(f"3665s = {formatar_duracao(3665)}")
    
    # Teste de custos
    print(f"\nTeste de custos:")
    custos = calcular_custo_estimado(25, 5, usar_gpt4=False)
    for servico, custo in custos.items():
        print(f"{servico}: {formatar_custo(custo)}")

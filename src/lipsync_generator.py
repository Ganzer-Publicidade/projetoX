"""
💋 LIPSYNC GENERATOR - ProjetoX

Módulo responsável por aplicar sincronização labial em vídeos.
Usa Replicate (Wav2Lip) ou D-ID API.
"""

import os
import time
import replicate
from typing import Dict, List, Optional

# Imports locais
try:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from config.settings import AI_CONFIG
    from src.utils import (
        validar_api_key, download_arquivo, salvar_json,
        criar_diretorios
    )
except ImportError:
    print("⚠️ Imports locais não disponíveis. Configure o PYTHONPATH.")


class LipsyncGenerator:
    """
    Gerador de lip-sync usando Replicate (Wav2Lip).
    
    Sincroniza movimentos labiais com áudio em vídeos.
    """
    
    def __init__(self, api_token: str):
        """
        Inicializa o gerador de lip-sync.
        
        Args:
            api_token: Token da API Replicate
        """
        if not validar_api_key(api_token, 'replicate'):
            raise ValueError("❌ API token Replicate inválido")
        
        self.api_token = api_token
        os.environ['REPLICATE_API_TOKEN'] = api_token
        
        # Modelo Wav2Lip
        self.modelo = AI_CONFIG.get(
            'replicate_lipsync_model',
            'devxpy/cog-wav2lip:8d65e3f4f4298520e079198b493c25adfc43c058ffec924f2aefc8010ed25eef'
        )
        
        self.output_dir = '/tmp/lipsync_output'
        criar_diretorios([self.output_dir])
        
        print(f"✅ LipsyncGenerator inicializado")
        print(f"   Modelo: Wav2Lip")
    
    def aplicar_lipsync(
        self,
        video_path: str,
        audio_path: str,
        nome_saida: Optional[str] = None
    ) -> Optional[str]:
        """
        Aplica lip-sync a um vídeo usando áudio.
        
        Args:
            video_path: Caminho do vídeo (com rosto)
            audio_path: Caminho do áudio (fala)
            nome_saida: Nome do arquivo de saída (opcional)
        
        Returns:
            Caminho do vídeo com lip-sync ou None
        
        Example:
            >>> gen = LipsyncGenerator(api_token="r8_...")
            >>> video_synced = gen.aplicar_lipsync("video.mp4", "audio.mp3")
        """
        if not os.path.exists(video_path):
            print(f"❌ Vídeo não encontrado: {video_path}")
            return None
        
        if not os.path.exists(audio_path):
            print(f"❌ Áudio não encontrado: {audio_path}")
            return None
        
        print(f"💋 Aplicando lip-sync...")
        print(f"   Vídeo: {os.path.basename(video_path)}")
        print(f"   Áudio: {os.path.basename(audio_path)}")
        
        try:
            # Processar com Wav2Lip
            print("   Processando (pode levar alguns minutos)...")
            
            output = replicate.run(
                self.modelo,
                input={
                    "video": open(video_path, "rb"),
                    "audio": open(audio_path, "rb")
                }
            )
            
            # Output é uma URL de vídeo
            if output:
                video_url = output if isinstance(output, str) else output[0]
                
                # Baixar vídeo
                if nome_saida is None:
                    base_name = os.path.splitext(os.path.basename(video_path))[0]
                    nome_saida = f"{base_name}_lipsync.mp4"
                
                caminho_saida = os.path.join(self.output_dir, nome_saida)
                
                if download_arquivo(video_url, caminho_saida):
                    print(f"✅ Lip-sync aplicado: {caminho_saida}")
                    return caminho_saida
            
            print("❌ Falha ao aplicar lip-sync")
            return None
            
        except Exception as e:
            print(f"❌ Erro ao aplicar lip-sync: {e}")
            print("💡 Wav2Lip requer vídeo com rosto visível")
            return video_path  # Retorna vídeo original como fallback
    
    def aplicar_lipsync_cenas(
        self,
        cenas_videos: Dict[int, str],
        cenas_audios: Dict[int, str],
        apenas_dialogos: bool = True
    ) -> Dict[int, str]:
        """
        Aplica lip-sync em múltiplas cenas.
        
        Args:
            cenas_videos: Dict mapeando número da cena -> caminho do vídeo
            cenas_audios: Dict mapeando número da cena -> caminho do áudio
            apenas_dialogos: Aplicar apenas em cenas com diálogo
        
        Returns:
            Dict mapeando número da cena -> caminho do vídeo com lip-sync
        """
        print(f"💋 Aplicando lip-sync em cenas...")
        
        videos_synced = {}
        
        # Encontrar cenas comuns
        cenas_comuns = set(cenas_videos.keys()) & set(cenas_audios.keys())
        
        if not cenas_comuns:
            print("⚠️ Nenhuma cena com vídeo e áudio correspondentes")
            return cenas_videos
        
        print(f"   Cenas a processar: {len(cenas_comuns)}")
        
        for i, num_cena in enumerate(sorted(cenas_comuns)):
            print(f"\n[{i+1}/{len(cenas_comuns)}] Cena {num_cena}")
            
            video_path = cenas_videos[num_cena]
            audio_path = cenas_audios[num_cena]
            
            nome_saida = f"cena_{num_cena:03d}_lipsync.mp4"
            
            # Aplicar lip-sync
            video_synced = self.aplicar_lipsync(
                video_path=video_path,
                audio_path=audio_path,
                nome_saida=nome_saida
            )
            
            if video_synced:
                videos_synced[num_cena] = video_synced
            else:
                # Usar vídeo original se falhar
                videos_synced[num_cena] = video_path
            
            # Delay entre requisições
            if i < len(cenas_comuns) - 1:
                time.sleep(3)
        
        # Adicionar cenas sem lip-sync
        for num_cena, video_path in cenas_videos.items():
            if num_cena not in videos_synced:
                videos_synced[num_cena] = video_path
        
        print(f"\n✅ Lip-sync aplicado em {len(cenas_comuns)} cenas")
        return videos_synced
    
    def verificar_qualidade(
        self,
        video_path: str
    ) -> Dict[str, any]:
        """
        Verifica a qualidade do lip-sync aplicado.
        
        Args:
            video_path: Caminho do vídeo
        
        Returns:
            Dicionário com métricas de qualidade
        
        Note:
            Implementação básica - retorna informações do arquivo
        """
        print(f"🔍 Verificando qualidade...")
        
        if not os.path.exists(video_path):
            return {'erro': 'Arquivo não encontrado'}
        
        tamanho_mb = os.path.getsize(video_path) / (1024 * 1024)
        
        # Análise básica
        qualidade = {
            'arquivo': os.path.basename(video_path),
            'tamanho_mb': round(tamanho_mb, 2),
            'existe': True,
            'status': 'ok' if tamanho_mb > 0.1 else 'muito_pequeno'
        }
        
        print(f"   Tamanho: {qualidade['tamanho_mb']} MB")
        print(f"   Status: {qualidade['status']}")
        
        return qualidade
    
    def salvar_catalogo_lipsync(
        self,
        videos: Dict,
        caminho: str
    ) -> bool:
        """
        Salva catálogo de vídeos com lip-sync.
        
        Args:
            videos: Dicionário de vídeos
            caminho: Caminho do arquivo JSON
        
        Returns:
            True se sucesso
        """
        print(f"💾 Salvando catálogo de lip-sync...")
        
        catalogo = {
            'gerado_em': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_videos': len(videos),
            'modelo_usado': 'Wav2Lip',
            'videos': videos
        }
        
        return salvar_json(catalogo, caminho, identado=True)


def exemplo_uso():
    """
    Exemplo de uso do LipsyncGenerator.
    """
    print("=" * 60)
    print("💋 EXEMPLO: LipsyncGenerator")
    print("=" * 60)
    
    # Nota: Use seu token real aqui
    api_token = os.getenv('REPLICATE_API_TOKEN', 'r8_...')
    
    if api_token == 'r8_...':
        print("⚠️ Configure REPLICATE_API_TOKEN para testar")
        return
    
    try:
        # Criar gerador
        generator = LipsyncGenerator(api_token=api_token)
        
        print("\n💡 Para testar, você precisa de:")
        print("   - Vídeo com rosto visível")
        print("   - Arquivo de áudio com fala")
        print("\n   Use: generator.aplicar_lipsync('video.mp4', 'audio.mp3')")
        
    except Exception as e:
        print(f"❌ Erro no exemplo: {e}")


if __name__ == '__main__':
    exemplo_uso()

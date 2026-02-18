"""
🎬 ANIMATION GENERATOR - ProjetoX

Módulo responsável por animar imagens estáticas usando IA.
Suporta Replicate (Stable Video Diffusion, Runway Gen-2, etc).
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
        criar_diretorios, gerar_nome_arquivo_unico
    )
except ImportError:
    print("⚠️ Imports locais não disponíveis. Configure o PYTHONPATH.")


class AnimationGenerator:
    """
    Gerador de animações usando Replicate (image-to-video).
    
    Converte imagens estáticas em micro-cenas animadas.
    """
    
    def __init__(self, api_token: str):
        """
        Inicializa o gerador de animações.
        
        Args:
            api_token: Token da API Replicate
        """
        if not validar_api_key(api_token, 'replicate'):
            raise ValueError("❌ API token Replicate inválido")
        
        self.api_token = api_token
        os.environ['REPLICATE_API_TOKEN'] = api_token
        
        # Modelo padrão: Stable Video Diffusion
        self.modelo = AI_CONFIG.get(
            'replicate_animation_model',
            'stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438'
        )
        
        self.video_dir = '/tmp/animations_output'
        criar_diretorios([self.video_dir])
        
        print(f"✅ AnimationGenerator inicializado")
        print(f"   Modelo: {self.modelo.split(':')[0]}")
    
    def animar_imagem(
        self,
        caminho_imagem: str,
        duracao_segundos: int = 5,
        nome_saida: Optional[str] = None,
        motion_bucket_id: int = 127,
        fps: int = 30
    ) -> Optional[str]:
        """
        Anima uma imagem estática.
        
        Args:
            caminho_imagem: Caminho da imagem a animar
            duracao_segundos: Duração do vídeo em segundos
            nome_saida: Nome do arquivo de saída (opcional)
            motion_bucket_id: Intensidade do movimento (0-255)
            fps: Frames por segundo
        
        Returns:
            Caminho do vídeo gerado ou None
        
        Example:
            >>> gen = AnimationGenerator(api_token="r8_...")
            >>> video = gen.animar_imagem("personagem.png", duracao_segundos=10)
        """
        if not os.path.exists(caminho_imagem):
            print(f"❌ Imagem não encontrada: {caminho_imagem}")
            return None
        
        print(f"🎬 Animando imagem: {os.path.basename(caminho_imagem)}")
        print(f"   Duração: {duracao_segundos}s")
        
        try:
            # Upload da imagem (Replicate precisa de URL)
            with open(caminho_imagem, 'rb') as f:
                imagem_data = f.read()
            
            # Gerar animação
            print("   Processando animação (pode levar alguns minutos)...")
            
            output = replicate.run(
                self.modelo,
                input={
                    "image": caminho_imagem,
                    "motion_bucket_id": motion_bucket_id,
                    "fps": fps,
                    "cond_aug": 0.02
                }
            )
            
            # Output é uma URL de vídeo
            if output:
                video_url = output if isinstance(output, str) else output[0]
                
                # Baixar vídeo
                if nome_saida is None:
                    base_name = os.path.splitext(os.path.basename(caminho_imagem))[0]
                    nome_saida = f"{base_name}_animated.mp4"
                
                caminho_saida = os.path.join(self.video_dir, nome_saida)
                
                if download_arquivo(video_url, caminho_saida):
                    print(f"✅ Animação gerada: {caminho_saida}")
                    return caminho_saida
            
            print("❌ Falha ao gerar animação")
            return None
            
        except Exception as e:
            print(f"❌ Erro ao animar imagem: {e}")
            return None
    
    def animar_cenas(
        self,
        cenas_com_imagens: Dict[int, str],
        duracoes: Optional[Dict[int, int]] = None
    ) -> Dict[int, str]:
        """
        Anima múltiplas cenas.
        
        Args:
            cenas_com_imagens: Dict mapeando número da cena -> caminho da imagem
            duracoes: Dict opcional com durações específicas por cena
        
        Returns:
            Dict mapeando número da cena -> caminho do vídeo
        """
        print(f"🎬 Animando {len(cenas_com_imagens)} cenas...")
        
        videos = {}
        
        for i, (num_cena, caminho_imagem) in enumerate(cenas_com_imagens.items()):
            print(f"\n[{i+1}/{len(cenas_com_imagens)}] Cena {num_cena}")
            
            # Duração específica ou padrão
            duracao = duracoes.get(num_cena, 10) if duracoes else 10
            
            # Nome do arquivo
            nome_saida = f"cena_{num_cena:03d}_video.mp4"
            
            # Animar
            video_path = self.animar_imagem(
                caminho_imagem=caminho_imagem,
                duracao_segundos=duracao,
                nome_saida=nome_saida
            )
            
            if video_path:
                videos[num_cena] = video_path
            
            # Delay entre requisições
            if i < len(cenas_com_imagens) - 1:
                time.sleep(3)
        
        print(f"\n✅ {len(videos)} cenas animadas com sucesso!")
        return videos
    
    def gerar_cena_com_texto(
        self,
        prompt: str,
        duracao_segundos: int = 5,
        nome_saida: Optional[str] = None
    ) -> Optional[str]:
        """
        Gera cena animada diretamente de prompt de texto (text-to-video).
        
        Args:
            prompt: Descrição da cena
            duracao_segundos: Duração
            nome_saida: Nome do arquivo
        
        Returns:
            Caminho do vídeo ou None
        
        Note:
            Requer modelo text-to-video (mais caro)
        """
        print(f"🎬 Gerando cena com prompt: {prompt[:50]}...")
        
        try:
            # Usar modelo text-to-video (exemplo: Runway Gen-2)
            # Nota: Modelo pode variar conforme disponibilidade
            output = replicate.run(
                "deforum/deforum_stable_diffusion",
                input={
                    "prompt": prompt,
                    "max_frames": duracao_segundos * 30,  # 30 fps
                }
            )
            
            if output:
                video_url = output if isinstance(output, str) else output[0]
                
                if nome_saida is None:
                    nome_saida = gerar_nome_arquivo_unico('cena', '.mp4', self.video_dir)
                else:
                    nome_saida = os.path.join(self.video_dir, nome_saida)
                
                if download_arquivo(video_url, nome_saida):
                    print(f"✅ Cena gerada: {nome_saida}")
                    return nome_saida
            
            return None
            
        except Exception as e:
            print(f"❌ Erro ao gerar cena: {e}")
            print("💡 Text-to-video pode não estar disponível ou ser muito caro")
            return None
    
    def adicionar_movimento_camera(
        self,
        video_path: str,
        tipo_movimento: str = "zoom_in",
        intensidade: float = 1.0
    ) -> Optional[str]:
        """
        Adiciona movimento de câmera a um vídeo.
        
        Args:
            video_path: Caminho do vídeo
            tipo_movimento: Tipo (zoom_in, zoom_out, pan_left, pan_right)
            intensidade: Intensidade do movimento (0.5-2.0)
        
        Returns:
            Caminho do vídeo com movimento
        
        Note:
            Implementação básica - requer processamento adicional
        """
        print(f"📹 Adicionando movimento de câmera: {tipo_movimento}")
        print("⚠️ Função em desenvolvimento - retornando vídeo original")
        return video_path
    
    def salvar_catalogo_videos(
        self,
        videos: Dict,
        caminho: str
    ) -> bool:
        """
        Salva catálogo de vídeos gerados.
        
        Args:
            videos: Dicionário de vídeos
            caminho: Caminho do arquivo JSON
        
        Returns:
            True se sucesso
        """
        print(f"💾 Salvando catálogo de vídeos...")
        
        catalogo = {
            'gerado_em': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_videos': len(videos),
            'modelo_usado': self.modelo,
            'videos': videos
        }
        
        return salvar_json(catalogo, caminho, identado=True)


def exemplo_uso():
    """
    Exemplo de uso do AnimationGenerator.
    """
    print("=" * 60)
    print("🎬 EXEMPLO: AnimationGenerator")
    print("=" * 60)
    
    # Nota: Use seu token real aqui
    api_token = os.getenv('REPLICATE_API_TOKEN', 'r8_...')
    
    if api_token == 'r8_...':
        print("⚠️ Configure REPLICATE_API_TOKEN para testar")
        return
    
    try:
        # Criar gerador
        generator = AnimationGenerator(api_token=api_token)
        
        print("\n💡 Para testar, você precisa de uma imagem.")
        print("   Use: generator.animar_imagem('caminho/para/imagem.png')")
        
    except Exception as e:
        print(f"❌ Erro no exemplo: {e}")


if __name__ == '__main__':
    exemplo_uso()

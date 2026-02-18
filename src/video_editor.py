"""
🎬 VIDEO EDITOR - ProjetoX

Módulo responsável por editar e montar o vídeo final usando MoviePy.
"""

import os
import time
from typing import Dict, List, Optional, Tuple
from moviepy.editor import (
    VideoFileClip, AudioFileClip, CompositeVideoClip,
    concatenate_videoclips, CompositeAudioClip, TextClip,
    concatenate_audioclips
)

# Imports locais
try:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from config.settings import VIDEO_CONFIG, AUDIO_CONFIG
    from src.utils import (
        criar_diretorios, get_tamanho_arquivo_mb,
        formatar_duracao
    )
except ImportError:
    print("⚠️ Imports locais não disponíveis. Configure o PYTHONPATH.")


class VideoEditor:
    """
    Editor de vídeo usando MoviePy.
    
    Monta o vídeo final combinando cenas, áudio e efeitos.
    """
    
    def __init__(self, output_dir: str = '/tmp/videos_finais'):
        """
        Inicializa o editor de vídeo.
        
        Args:
            output_dir: Diretório para vídeos finais
        """
        self.output_dir = output_dir
        criar_diretorios([self.output_dir])
        
        # Configurações
        self.resolution = VIDEO_CONFIG.get('resolution', (1920, 1080))
        self.fps = VIDEO_CONFIG.get('fps', 30)
        self.codec = VIDEO_CONFIG.get('codec', 'libx264')
        self.bitrate = VIDEO_CONFIG.get('bitrate', '5000k')
        self.audio_codec = VIDEO_CONFIG.get('audio_codec', 'aac')
        
        print(f"✅ VideoEditor inicializado")
        print(f"   Resolução: {self.resolution[0]}x{self.resolution[1]}")
        print(f"   FPS: {self.fps}")
    
    def montar_video_final(
        self,
        cenas_videos: Dict[int, str],
        cenas_audios: Optional[Dict[int, str]] = None,
        musica_fundo: Optional[str] = None,
        nome_saida: str = "video_final.mp4",
        transicao: str = "fade"
    ) -> Optional[str]:
        """
        Monta o vídeo final combinando todas as cenas.
        
        Args:
            cenas_videos: Dict mapeando número da cena -> caminho do vídeo
            cenas_audios: Dict opcional com áudios por cena
            musica_fundo: Caminho da música de fundo (opcional)
            nome_saida: Nome do arquivo de saída
            transicao: Tipo de transição entre cenas
        
        Returns:
            Caminho do vídeo final ou None
        
        Example:
            >>> editor = VideoEditor()
            >>> video_final = editor.montar_video_final(
            ...     cenas_videos={1: "cena1.mp4", 2: "cena2.mp4"},
            ...     nome_saida="meu_video.mp4"
            ... )
        """
        print(f"🎬 Montando vídeo final...")
        print(f"   Cenas: {len(cenas_videos)}")
        
        try:
            # Carregar e ordenar cenas
            clips_video = []
            
            for num_cena in sorted(cenas_videos.keys()):
                video_path = cenas_videos[num_cena]
                
                if not os.path.exists(video_path):
                    print(f"   ⚠️ Cena {num_cena} não encontrada: {video_path}")
                    continue
                
                print(f"   Carregando cena {num_cena}...")
                
                try:
                    clip = VideoFileClip(video_path)
                    
                    # Redimensionar se necessário
                    if clip.size != self.resolution:
                        clip = clip.resize(self.resolution)
                    
                    clips_video.append(clip)
                    
                except Exception as e:
                    print(f"   ⚠️ Erro ao carregar cena {num_cena}: {e}")
            
            if not clips_video:
                print("❌ Nenhuma cena válida encontrada")
                return None
            
            print(f"   ✅ {len(clips_video)} cenas carregadas")
            
            # Concatenar cenas
            print("   Concatenando cenas...")
            
            if transicao == "fade":
                # Adicionar crossfade entre cenas
                video_final = concatenate_videoclips(
                    clips_video,
                    method="compose",
                    padding=-0.5  # 0.5s de crossfade
                )
            else:
                video_final = concatenate_videoclips(clips_video, method="compose")
            
            # Processar áudio
            if cenas_audios:
                print("   Processando áudio...")
                audio_final = self._processar_audio(
                    cenas_audios,
                    video_final.duration,
                    musica_fundo
                )
                
                if audio_final:
                    video_final = video_final.set_audio(audio_final)
            
            # Caminho de saída
            caminho_saida = os.path.join(self.output_dir, nome_saida)
            
            # Exportar vídeo final
            print(f"   Exportando vídeo final...")
            print(f"   Isso pode levar vários minutos...")
            
            video_final.write_videofile(
                caminho_saida,
                fps=self.fps,
                codec=self.codec,
                bitrate=self.bitrate,
                audio_codec=self.audio_codec,
                preset='medium',
                threads=4,
                logger=None  # Desabilitar verbose logging
            )
            
            # Limpar recursos
            video_final.close()
            for clip in clips_video:
                clip.close()
            
            # Informações do vídeo final
            tamanho_mb = get_tamanho_arquivo_mb(caminho_saida)
            
            print(f"\n✅ Vídeo final criado!")
            print(f"   Arquivo: {caminho_saida}")
            print(f"   Tamanho: {tamanho_mb:.2f} MB")
            print(f"   Duração: {formatar_duracao(video_final.duration)}")
            
            return caminho_saida
            
        except Exception as e:
            print(f"❌ Erro ao montar vídeo: {e}")
            return None
    
    def _processar_audio(
        self,
        cenas_audios: Dict[int, str],
        duracao_total: float,
        musica_fundo: Optional[str] = None
    ) -> Optional[AudioFileClip]:
        """
        Processa e combina áudios das cenas.
        
        Args:
            cenas_audios: Dict com áudios por cena
            duracao_total: Duração total do vídeo
            musica_fundo: Caminho da música de fundo
        
        Returns:
            AudioFileClip combinado ou None
        """
        try:
            # Carregar áudios das cenas
            clips_audio = []
            
            for num_cena in sorted(cenas_audios.keys()):
                audio_path = cenas_audios[num_cena]
                
                if os.path.exists(audio_path):
                    audio = AudioFileClip(audio_path)
                    clips_audio.append(audio)
            
            if not clips_audio:
                return None
            
            # Concatenar áudios
            audio_principal = concatenate_audioclips(clips_audio)
            
            # Adicionar música de fundo se fornecida
            if musica_fundo and os.path.exists(musica_fundo):
                print("   Adicionando música de fundo...")
                
                musica = AudioFileClip(musica_fundo)
                
                # Loop da música se necessário
                if musica.duration < audio_principal.duration:
                    num_loops = int(audio_principal.duration / musica.duration) + 1
                    musica = concatenate_audioclips([musica] * num_loops)
                
                # Cortar música para duração do vídeo
                musica = musica.subclip(0, min(musica.duration, audio_principal.duration))
                
                # Reduzir volume da música (background)
                volume_reducao = AUDIO_CONFIG.get('background_music_volume', -10)
                musica = musica.volumex(10 ** (volume_reducao / 20))
                
                # Combinar narração + música
                audio_final = CompositeAudioClip([audio_principal, musica])
            else:
                audio_final = audio_principal
            
            return audio_final
            
        except Exception as e:
            print(f"   ⚠️ Erro ao processar áudio: {e}")
            return None
    
    def adicionar_legendas(
        self,
        video_path: str,
        legendas: List[Dict],
        caminho_saida: Optional[str] = None
    ) -> Optional[str]:
        """
        Adiciona legendas ao vídeo.
        
        Args:
            video_path: Caminho do vídeo
            legendas: Lista de dicts com 'texto', 'inicio', 'fim'
            caminho_saida: Caminho de saída (opcional)
        
        Returns:
            Caminho do vídeo com legendas
        
        Example:
            >>> legendas = [
            ...     {"texto": "Era uma vez...", "inicio": 0, "fim": 3},
            ...     {"texto": "Um rei sábio", "inicio": 3, "fim": 6}
            ... ]
            >>> video_com_legendas = editor.adicionar_legendas("video.mp4", legendas)
        """
        print(f"📝 Adicionando legendas...")
        
        try:
            video = VideoFileClip(video_path)
            
            # Criar clips de texto
            txt_clips = []
            
            for i, leg in enumerate(legendas):
                print(f"   Legenda {i+1}/{len(legendas)}")
                
                txt_clip = TextClip(
                    leg['texto'],
                    fontsize=40,
                    color='white',
                    bg_color='black',
                    size=(video.w * 0.9, None),
                    method='caption'
                ).set_position(('center', 'bottom')).set_start(
                    leg['inicio']
                ).set_duration(
                    leg['fim'] - leg['inicio']
                )
                
                txt_clips.append(txt_clip)
            
            # Compor vídeo com legendas
            video_final = CompositeVideoClip([video] + txt_clips)
            
            # Caminho de saída
            if caminho_saida is None:
                base, ext = os.path.splitext(video_path)
                caminho_saida = f"{base}_legendas{ext}"
            
            # Exportar
            video_final.write_videofile(
                caminho_saida,
                fps=self.fps,
                codec=self.codec,
                bitrate=self.bitrate,
                audio_codec=self.audio_codec,
                logger=None
            )
            
            video.close()
            video_final.close()
            
            print(f"✅ Legendas adicionadas: {caminho_saida}")
            return caminho_saida
            
        except Exception as e:
            print(f"❌ Erro ao adicionar legendas: {e}")
            return video_path
    
    def adicionar_intro_outro(
        self,
        video_path: str,
        intro_path: Optional[str] = None,
        outro_path: Optional[str] = None,
        caminho_saida: Optional[str] = None
    ) -> Optional[str]:
        """
        Adiciona intro e/ou outro ao vídeo.
        
        Args:
            video_path: Caminho do vídeo principal
            intro_path: Caminho da intro (opcional)
            outro_path: Caminho do outro (opcional)
            caminho_saida: Caminho de saída
        
        Returns:
            Caminho do vídeo com intro/outro
        """
        print(f"🎬 Adicionando intro/outro...")
        
        try:
            clips = []
            
            # Adicionar intro
            if intro_path and os.path.exists(intro_path):
                print("   Adicionando intro...")
                intro = VideoFileClip(intro_path).resize(self.resolution)
                clips.append(intro)
            
            # Vídeo principal
            video_principal = VideoFileClip(video_path).resize(self.resolution)
            clips.append(video_principal)
            
            # Adicionar outro
            if outro_path and os.path.exists(outro_path):
                print("   Adicionando outro...")
                outro = VideoFileClip(outro_path).resize(self.resolution)
                clips.append(outro)
            
            # Concatenar
            video_final = concatenate_videoclips(clips, method="compose")
            
            # Caminho de saída
            if caminho_saida is None:
                base, ext = os.path.splitext(video_path)
                caminho_saida = f"{base}_completo{ext}"
            
            # Exportar
            video_final.write_videofile(
                caminho_saida,
                fps=self.fps,
                codec=self.codec,
                bitrate=self.bitrate,
                audio_codec=self.audio_codec,
                logger=None
            )
            
            # Limpar
            for clip in clips:
                clip.close()
            video_final.close()
            
            print(f"✅ Intro/outro adicionados: {caminho_saida}")
            return caminho_saida
            
        except Exception as e:
            print(f"❌ Erro ao adicionar intro/outro: {e}")
            return video_path
    
    def criar_preview(
        self,
        video_path: str,
        duracao_preview: int = 30,
        caminho_saida: Optional[str] = None
    ) -> Optional[str]:
        """
        Cria um preview curto do vídeo.
        
        Args:
            video_path: Caminho do vídeo completo
            duracao_preview: Duração do preview em segundos
            caminho_saida: Caminho de saída
        
        Returns:
            Caminho do preview
        """
        print(f"👀 Criando preview ({duracao_preview}s)...")
        
        try:
            video = VideoFileClip(video_path)
            
            # Pegar início do vídeo
            preview = video.subclip(0, min(duracao_preview, video.duration))
            
            # Caminho de saída
            if caminho_saida is None:
                base, ext = os.path.splitext(video_path)
                caminho_saida = f"{base}_preview{ext}"
            
            # Exportar
            preview.write_videofile(
                caminho_saida,
                fps=self.fps,
                codec=self.codec,
                bitrate='3000k',  # Menor bitrate para preview
                audio_codec=self.audio_codec,
                logger=None
            )
            
            video.close()
            preview.close()
            
            print(f"✅ Preview criado: {caminho_saida}")
            return caminho_saida
            
        except Exception as e:
            print(f"❌ Erro ao criar preview: {e}")
            return None


def exemplo_uso():
    """
    Exemplo de uso do VideoEditor.
    """
    print("=" * 60)
    print("🎬 EXEMPLO: VideoEditor")
    print("=" * 60)
    
    try:
        # Criar editor
        editor = VideoEditor()
        
        print("\n💡 Para testar, você precisa de vídeos das cenas.")
        print("   Use: editor.montar_video_final({1: 'cena1.mp4', 2: 'cena2.mp4'})")
        
    except Exception as e:
        print(f"❌ Erro no exemplo: {e}")


if __name__ == '__main__':
    exemplo_uso()

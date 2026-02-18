"""
🎵 AUDIO GENERATOR - ProjetoX

Módulo responsável por gerar narração e música usando ElevenLabs.
"""

import os
import time
from typing import Dict, List, Optional
from elevenlabs import generate, save, Voice, VoiceSettings

# Imports locais
try:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from config.settings import AUDIO_CONFIG, AI_CONFIG, LANGUAGE_CONFIG
    from src.utils import (
        validar_api_key, salvar_json, criar_diretorios,
        gerar_nome_arquivo_unico
    )
except ImportError:
    print("⚠️ Imports locais não disponíveis. Configure o PYTHONPATH.")


class AudioGenerator:
    """
    Gerador de áudio usando ElevenLabs Text-to-Speech.
    
    Cria narração profissional em múltiplos idiomas.
    """
    
    def __init__(self, api_key: str):
        """
        Inicializa o gerador de áudio.
        
        Args:
            api_key: Chave da API ElevenLabs
        """
        if not validar_api_key(api_key, 'elevenlabs'):
            raise ValueError("❌ API key ElevenLabs inválida")
        
        self.api_key = api_key
        os.environ['ELEVEN_API_KEY'] = api_key
        
        self.model = AI_CONFIG.get('elevenlabs_model', 'eleven_multilingual_v2')
        self.stability = AI_CONFIG.get('elevenlabs_stability', 0.5)
        self.similarity_boost = AI_CONFIG.get('elevenlabs_similarity_boost', 0.75)
        
        self.audio_dir = '/tmp/audio_output'
        criar_diretorios([self.audio_dir])
        
        print(f"✅ AudioGenerator inicializado")
        print(f"   Modelo: {self.model}")
    
    def gerar_narracao(
        self,
        texto: str,
        nome_arquivo: str,
        voice_id: Optional[str] = None,
        idioma: str = "pt-br",
        emocao: str = "neutral"
    ) -> Optional[str]:
        """
        Gera narração a partir de texto.
        
        Args:
            texto: Texto a ser narrado
            nome_arquivo: Nome do arquivo de saída (sem extensão)
            voice_id: ID da voz (opcional, usa padrão do idioma)
            idioma: Código do idioma
            emocao: Emoção da narração
        
        Returns:
            Caminho do arquivo de áudio gerado ou None
        
        Example:
            >>> gen = AudioGenerator(api_key="...")
            >>> audio_path = gen.gerar_narracao(
            ...     "Era uma vez um rei sábio...",
            ...     "cena_01_narracao"
            ... )
        """
        if not texto or not texto.strip():
            print("⚠️ Texto vazio, pulando narração")
            return None
        
        print(f"🎙️ Gerando narração: {nome_arquivo}")
        print(f"   Caracteres: {len(texto)}")
        print(f"   Idioma: {idioma}")
        
        try:
            # Selecionar voz apropriada
            if voice_id is None:
                from config.settings import get_voice_for_language
                voice_id = get_voice_for_language(idioma, 'narrator')
            
            # Gerar áudio
            audio = generate(
                text=texto,
                voice=Voice(
                    voice_id=voice_id,
                    settings=VoiceSettings(
                        stability=self.stability,
                        similarity_boost=self.similarity_boost
                    )
                ),
                model=self.model
            )
            
            # Salvar arquivo
            caminho_saida = os.path.join(
                self.audio_dir,
                f"{nome_arquivo}.mp3"
            )
            
            save(audio, caminho_saida)
            
            # Verificar tamanho do arquivo
            tamanho_mb = os.path.getsize(caminho_saida) / (1024 * 1024)
            
            print(f"✅ Narração gerada: {caminho_saida}")
            print(f"   Tamanho: {tamanho_mb:.2f} MB")
            
            return caminho_saida
            
        except Exception as e:
            print(f"❌ Erro ao gerar narração: {e}")
            return None
    
    def gerar_audio_cenas(
        self,
        roteiro: Dict,
        idioma: str = "pt-br"
    ) -> Dict[int, str]:
        """
        Gera áudio para todas as cenas de um roteiro.
        
        Args:
            roteiro: Roteiro completo com cenas
            idioma: Código do idioma
        
        Returns:
            Dicionário mapeando número da cena -> caminho do áudio
        """
        cenas = roteiro.get('cenas', [])
        
        if not cenas:
            print("❌ Nenhuma cena encontrada no roteiro")
            return {}
        
        print(f"🎬 Gerando áudio para {len(cenas)} cenas...")
        
        audios = {}
        
        for cena in cenas:
            numero = cena.get('numero', 0)
            narrativa = cena.get('narrativa', '')
            tipo_audio = cena.get('tipo_audio', 'narracao')
            emocao = cena.get('emocao', 'neutral')
            
            # Pular se não houver narrativa ou se for música apenas
            if not narrativa or tipo_audio == 'musica_apenas':
                print(f"   Cena {numero}: pulando (sem narração)")
                continue
            
            print(f"   Processando cena {numero}...")
            
            # Gerar narração
            nome_arquivo = f"cena_{numero:03d}_audio"
            
            caminho_audio = self.gerar_narracao(
                texto=narrativa,
                nome_arquivo=nome_arquivo,
                idioma=idioma,
                emocao=emocao
            )
            
            if caminho_audio:
                audios[numero] = caminho_audio
            
            # Delay para evitar rate limiting
            time.sleep(0.5)
        
        print(f"✅ {len(audios)} áudios gerados com sucesso!")
        
        return audios
    
    def gerar_multiplas_vozes(
        self,
        textos_por_personagem: Dict[str, str],
        idioma: str = "pt-br"
    ) -> Dict[str, str]:
        """
        Gera áudio com vozes diferentes para cada personagem.
        
        Args:
            textos_por_personagem: Dict mapeando nome -> texto
            idioma: Código do idioma
        
        Returns:
            Dict mapeando nome -> caminho do áudio
        """
        print(f"👥 Gerando vozes para {len(textos_por_personagem)} personagens...")
        
        audios = {}
        voice_types = ['narrator', 'character_male', 'character_female']
        
        for i, (personagem, texto) in enumerate(textos_por_personagem.items()):
            # Alternar entre tipos de voz
            voice_type = voice_types[i % len(voice_types)]
            
            from config.settings import get_voice_for_language
            voice_id = get_voice_for_language(idioma, voice_type)
            
            nome_arquivo = f"personagem_{personagem.replace(' ', '_').lower()}"
            
            caminho_audio = self.gerar_narracao(
                texto=texto,
                nome_arquivo=nome_arquivo,
                voice_id=voice_id,
                idioma=idioma
            )
            
            if caminho_audio:
                audios[personagem] = caminho_audio
        
        return audios
    
    def ajustar_volume_audio(
        self,
        caminho_audio: str,
        volume_db: float,
        caminho_saida: Optional[str] = None
    ) -> Optional[str]:
        """
        Ajusta o volume de um arquivo de áudio.
        
        Args:
            caminho_audio: Caminho do áudio original
            volume_db: Ajuste em decibéis (negativo para diminuir)
            caminho_saida: Caminho de saída (opcional)
        
        Returns:
            Caminho do áudio ajustado
        """
        try:
            from pydub import AudioSegment
            
            print(f"🔊 Ajustando volume: {volume_db}dB")
            
            # Carregar áudio
            audio = AudioSegment.from_file(caminho_audio)
            
            # Ajustar volume
            audio_ajustado = audio + volume_db
            
            # Determinar caminho de saída
            if caminho_saida is None:
                base, ext = os.path.splitext(caminho_audio)
                caminho_saida = f"{base}_vol{int(volume_db)}{ext}"
            
            # Exportar
            audio_ajustado.export(caminho_saida, format='mp3')
            
            print(f"✅ Volume ajustado: {caminho_saida}")
            return caminho_saida
            
        except Exception as e:
            print(f"❌ Erro ao ajustar volume: {e}")
            return None
    
    def mesclar_audios(
        self,
        audios: List[str],
        caminho_saida: str,
        crossfade_ms: int = 500
    ) -> Optional[str]:
        """
        Mescla múltiplos áudios em sequência.
        
        Args:
            audios: Lista de caminhos de áudio
            caminho_saida: Caminho do áudio mesclado
            crossfade_ms: Duração do crossfade em milissegundos
        
        Returns:
            Caminho do áudio mesclado
        """
        try:
            from pydub import AudioSegment
            
            print(f"🎵 Mesclando {len(audios)} áudios...")
            
            if not audios:
                print("❌ Nenhum áudio para mesclar")
                return None
            
            # Carregar primeiro áudio
            audio_final = AudioSegment.from_file(audios[0])
            
            # Adicionar os demais com crossfade
            for caminho in audios[1:]:
                audio_novo = AudioSegment.from_file(caminho)
                audio_final = audio_final.append(audio_novo, crossfade=crossfade_ms)
            
            # Exportar
            audio_final.export(caminho_saida, format='mp3', bitrate='192k')
            
            duracao_seg = len(audio_final) / 1000.0
            print(f"✅ Áudio mesclado: {duracao_seg:.1f}s - {caminho_saida}")
            
            return caminho_saida
            
        except Exception as e:
            print(f"❌ Erro ao mesclar áudios: {e}")
            return None
    
    def adicionar_musica_fundo(
        self,
        audio_principal: str,
        musica_fundo: str,
        caminho_saida: str,
        volume_musica_db: float = -10
    ) -> Optional[str]:
        """
        Adiciona música de fundo a um áudio principal.
        
        Args:
            audio_principal: Caminho da narração
            musica_fundo: Caminho da música
            caminho_saida: Caminho de saída
            volume_musica_db: Volume da música (negativo para reduzir)
        
        Returns:
            Caminho do áudio com música de fundo
        """
        try:
            from pydub import AudioSegment
            
            print(f"🎶 Adicionando música de fundo...")
            
            # Carregar áudios
            narracao = AudioSegment.from_file(audio_principal)
            musica = AudioSegment.from_file(musica_fundo)
            
            # Ajustar volume da música
            musica = musica + volume_musica_db
            
            # Loop da música se necessário
            if len(musica) < len(narracao):
                repeticoes = (len(narracao) // len(musica)) + 1
                musica = musica * repeticoes
            
            # Cortar música para duração da narração
            musica = musica[:len(narracao)]
            
            # Sobrepor
            audio_final = narracao.overlay(musica)
            
            # Exportar
            audio_final.export(caminho_saida, format='mp3', bitrate='192k')
            
            print(f"✅ Música de fundo adicionada: {caminho_saida}")
            return caminho_saida
            
        except Exception as e:
            print(f"❌ Erro ao adicionar música: {e}")
            return None
    
    def salvar_catalogo_audios(
        self,
        audios: Dict,
        caminho: str
    ) -> bool:
        """
        Salva catálogo de áudios gerados em JSON.
        
        Args:
            audios: Dicionário de áudios
            caminho: Caminho do arquivo
        
        Returns:
            True se sucesso
        """
        print(f"💾 Salvando catálogo de áudios...")
        
        catalogo = {
            'gerado_em': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_audios': len(audios),
            'modelo_usado': self.model,
            'audios': audios
        }
        
        return salvar_json(catalogo, caminho, identado=True)


def exemplo_uso():
    """
    Exemplo de uso do AudioGenerator.
    """
    print("=" * 60)
    print("🎵 EXEMPLO: AudioGenerator")
    print("=" * 60)
    
    # Nota: Use sua API key real aqui
    api_key = os.getenv('ELEVENLABS_API_KEY', '...')
    
    if api_key == '...':
        print("⚠️ Configure ELEVENLABS_API_KEY para testar")
        return
    
    try:
        # Criar gerador
        generator = AudioGenerator(api_key=api_key)
        
        # Gerar narração simples
        audio_path = generator.gerar_narracao(
            texto="Era uma vez um rei muito sábio chamado Salomão. Ele era conhecido em todo o mundo por sua grande sabedoria.",
            nome_arquivo="teste_narracao",
            idioma="pt-br"
        )
        
        if audio_path:
            print(f"\n📋 ÁUDIO GERADO:")
            print(f"   Caminho: {audio_path}")
            print(f"   Tamanho: {os.path.getsize(audio_path) / 1024:.2f} KB")
        
    except Exception as e:
        print(f"❌ Erro no exemplo: {e}")


if __name__ == '__main__':
    exemplo_uso()

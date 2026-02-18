"""
🚀 PIPELINE - ProjetoX

Orquestrador principal do sistema de automação de vídeos.
Gerencia todo o fluxo desde geração do roteiro até o vídeo final.
"""

import os
import time
import json
from typing import Dict, List, Optional
from datetime import datetime

# Imports locais
try:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    
    from src.roteiro_generator import RoteiroGenerator
    from src.character_generator import CharacterGenerator
    from src.audio_generator import AudioGenerator
    from src.animation_generator import AnimationGenerator
    from src.lipsync_generator import LipsyncGenerator
    from src.video_editor import VideoEditor
    from src.utils import (
        criar_diretorios, salvar_checkpoint, carregar_checkpoint,
        limpar_memoria, calcular_custo_estimado, formatar_custo,
        formatar_duracao, validar_configuracao_projeto
    )
    from config.settings import DIRS, OPTIMIZATION_CONFIG
    
except ImportError as e:
    print(f"⚠️ Erro nos imports: {e}")
    print("Configure o PYTHONPATH corretamente")


class VideoAutomationPipeline:
    """
    Pipeline completo de automação de vídeos com IA.
    
    Orquestra todos os módulos para gerar vídeos profissionais automaticamente.
    """
    
    def __init__(self, config: Dict):
        """
        Inicializa o pipeline.
        
        Args:
            config: Configuração do projeto contendo:
                - nicho: Nicho do vídeo
                - tema: Tema do vídeo
                - duracao_minutos: Duração desejada
                - idioma: Código do idioma
                - api_keys: Dict com API keys
                - output_dir: Diretório de saída (opcional)
        
        Example:
            >>> config = {
            ...     'nicho': 'historias_infantis',
            ...     'tema': 'A História do Rei Salomão',
            ...     'duracao_minutos': 5,
            ...     'idioma': 'pt-br',
            ...     'api_keys': {
            ...         'openai': 'sk-...',
            ...         'elevenlabs': '...',
            ...         'replicate': 'r8_...'
            ...     }
            ... }
            >>> pipeline = VideoAutomationPipeline(config)
        """
        print("=" * 70)
        print("🚀 PROJETOX - INICIANDO PIPELINE DE AUTOMAÇÃO")
        print("=" * 70)
        
        # Validar configuração
        if not validar_configuracao_projeto(config):
            raise ValueError("❌ Configuração inválida")
        
        self.config = config
        self.nicho = config['nicho']
        self.tema = config['tema']
        self.duracao_minutos = config['duracao_minutos']
        self.idioma = config['idioma']
        
        # API Keys
        api_keys = config.get('api_keys', {})
        self.openai_key = api_keys.get('openai', os.getenv('OPENAI_API_KEY'))
        self.elevenlabs_key = api_keys.get('elevenlabs', os.getenv('ELEVENLABS_API_KEY'))
        self.replicate_token = api_keys.get('replicate', os.getenv('REPLICATE_API_TOKEN'))
        
        # Verificar API keys
        if not all([self.openai_key, self.elevenlabs_key, self.replicate_token]):
            raise ValueError("❌ API keys não configuradas. Configure: OPENAI_API_KEY, ELEVENLABS_API_KEY, REPLICATE_API_TOKEN")
        
        # Diretórios
        self.output_dir = config.get('output_dir', DIRS['output'])
        self.temp_dir = DIRS['temp']
        self.checkpoint_dir = DIRS['checkpoints']
        
        criar_diretorios([self.output_dir, self.temp_dir, self.checkpoint_dir])
        
        # Estado do pipeline
        self.roteiro = None
        self.personagens = {}
        self.audios = {}
        self.videos_animados = {}
        self.videos_lipsync = {}
        self.video_final = None
        
        # Timestamp
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.projeto_id = f"{self.nicho}_{self.timestamp}"
        
        print(f"\n📋 CONFIGURAÇÃO:")
        print(f"   Projeto ID: {self.projeto_id}")
        print(f"   Nicho: {self.nicho}")
        print(f"   Tema: {self.tema}")
        print(f"   Duração: {self.duracao_minutos} minutos")
        print(f"   Idioma: {self.idioma}")
        print(f"   Output: {self.output_dir}")
        
        # Calcular custos estimados
        self._estimar_custos()
    
    def _estimar_custos(self):
        """
        Calcula e exibe custos estimados do projeto.
        """
        num_cenas = (self.duracao_minutos * 60) // 12
        
        custos = calcular_custo_estimado(
            num_cenas=num_cenas,
            duracao_minutos=self.duracao_minutos,
            usar_gpt4=False,  # Assumindo GPT-3.5
            usar_animacao_premium=False
        )
        
        print(f"\n💰 CUSTOS ESTIMADOS:")
        for servico, custo in custos.items():
            print(f"   {servico}: {formatar_custo(custo)}")
    
    def executar_completo(
        self,
        pular_etapas: Optional[List[str]] = None,
        usar_checkpoint: bool = True
    ) -> Optional[str]:
        """
        Executa o pipeline completo do início ao fim.
        
        Args:
            pular_etapas: Lista de etapas para pular (opcional)
            usar_checkpoint: Retomar de checkpoint se disponível
        
        Returns:
            Caminho do vídeo final ou None
        
        Example:
            >>> pipeline = VideoAutomationPipeline(config)
            >>> video_path = pipeline.executar_completo()
        """
        inicio = time.time()
        
        print("\n" + "=" * 70)
        print("🎬 INICIANDO EXECUÇÃO COMPLETA DO PIPELINE")
        print("=" * 70)
        
        pular = pular_etapas or []
        
        try:
            # Etapa 1: Roteiro
            if 'roteiro' not in pular:
                print("\n" + "-" * 70)
                print("[1/6] 📝 GERAÇÃO DE ROTEIRO")
                print("-" * 70)
                self.roteiro = self.gerar_roteiro()
                self._salvar_checkpoint('roteiro')
            else:
                print("\n⏭️ Pulando etapa: Roteiro")
                self.roteiro = self._carregar_checkpoint_etapa('roteiro')
            
            if not self.roteiro:
                raise Exception("Falha na geração do roteiro")
            
            limpar_memoria()
            
            # Etapa 2: Personagens
            if 'personagens' not in pular:
                print("\n" + "-" * 70)
                print("[2/6] 👤 CRIAÇÃO DE PERSONAGENS")
                print("-" * 70)
                self.personagens = self.gerar_personagens()
                self._salvar_checkpoint('personagens')
            else:
                print("\n⏭️ Pulando etapa: Personagens")
                self.personagens = self._carregar_checkpoint_etapa('personagens')
            
            limpar_memoria()
            
            # Etapa 3: Áudios
            if 'audios' not in pular:
                print("\n" + "-" * 70)
                print("[3/6] 🎵 GERAÇÃO DE ÁUDIOS")
                print("-" * 70)
                self.audios = self.gerar_audios()
                self._salvar_checkpoint('audios')
            else:
                print("\n⏭️ Pulando etapa: Áudios")
                self.audios = self._carregar_checkpoint_etapa('audios')
            
            limpar_memoria()
            
            # Etapa 4: Animações
            if 'animacoes' not in pular:
                print("\n" + "-" * 70)
                print("[4/6] 🎬 ANIMAÇÃO DE CENAS")
                print("-" * 70)
                self.videos_animados = self.animar_cenas()
                self._salvar_checkpoint('videos_animados')
            else:
                print("\n⏭️ Pulando etapa: Animações")
                self.videos_animados = self._carregar_checkpoint_etapa('videos_animados')
            
            limpar_memoria()
            
            # Etapa 5: Lip-sync
            if 'lipsync' not in pular:
                print("\n" + "-" * 70)
                print("[5/6] 💋 APLICAÇÃO DE LIP-SYNC")
                print("-" * 70)
                self.videos_lipsync = self.aplicar_lipsync()
                self._salvar_checkpoint('videos_lipsync')
            else:
                print("\n⏭️ Pulando etapa: Lip-sync")
                self.videos_lipsync = self._carregar_checkpoint_etapa('videos_lipsync')
            
            limpar_memoria()
            
            # Etapa 6: Edição Final
            if 'edicao' not in pular:
                print("\n" + "-" * 70)
                print("[6/6] ✂️ EDIÇÃO FINAL DO VÍDEO")
                print("-" * 70)
                self.video_final = self.editar_video()
                self._salvar_checkpoint('video_final')
            else:
                print("\n⏭️ Pulando etapa: Edição")
                self.video_final = self._carregar_checkpoint_etapa('video_final')
            
            # Finalização
            tempo_total = time.time() - inicio
            
            print("\n" + "=" * 70)
            print("✅ PIPELINE CONCLUÍDO COM SUCESSO!")
            print("=" * 70)
            print(f"\n📊 ESTATÍSTICAS:")
            print(f"   Tempo total: {formatar_duracao(tempo_total)}")
            print(f"   Vídeo final: {self.video_final}")
            
            if self.video_final and os.path.exists(self.video_final):
                from src.utils import get_tamanho_arquivo_mb
                tamanho = get_tamanho_arquivo_mb(self.video_final)
                print(f"   Tamanho: {tamanho:.2f} MB")
            
            print("\n🎉 Seu vídeo está pronto para upload no YouTube!")
            
            return self.video_final
            
        except Exception as e:
            print(f"\n❌ ERRO NO PIPELINE: {e}")
            print("💾 Checkpoint salvo - você pode retomar depois")
            raise
    
    def gerar_roteiro(self) -> Dict:
        """
        Etapa 1: Gera o roteiro do vídeo.
        """
        generator = RoteiroGenerator(api_key=self.openai_key)
        
        roteiro = generator.gerar_roteiro(
            tema=self.tema,
            nicho=self.nicho,
            duracao_minutos=self.duracao_minutos,
            idioma=self.idioma
        )
        
        # Salvar roteiro
        roteiro_path = os.path.join(self.temp_dir, f"{self.projeto_id}_roteiro.json")
        generator.salvar_roteiro(roteiro, roteiro_path)
        
        print(f"✅ Roteiro salvo: {roteiro_path}")
        
        return roteiro
    
    def gerar_personagens(self) -> Dict:
        """
        Etapa 2: Gera os personagens necessários.
        """
        if not self.roteiro:
            raise Exception("Roteiro não disponível")
        
        generator = CharacterGenerator(api_token=self.replicate_token)
        
        personagens = generator.criar_personagem_de_roteiro(self.roteiro)
        
        # Salvar catálogo
        catalogo_path = os.path.join(self.temp_dir, f"{self.projeto_id}_personagens.json")
        generator.salvar_catalogo_personagens(personagens, catalogo_path)
        
        print(f"✅ Personagens salvos: {catalogo_path}")
        
        return personagens
    
    def gerar_audios(self) -> Dict:
        """
        Etapa 3: Gera os áudios (narração).
        """
        if not self.roteiro:
            raise Exception("Roteiro não disponível")
        
        generator = AudioGenerator(api_key=self.elevenlabs_key)
        
        audios = generator.gerar_audio_cenas(
            roteiro=self.roteiro,
            idioma=self.idioma
        )
        
        # Salvar catálogo
        catalogo_path = os.path.join(self.temp_dir, f"{self.projeto_id}_audios.json")
        generator.salvar_catalogo_audios(audios, catalogo_path)
        
        print(f"✅ Áudios salvos: {catalogo_path}")
        
        return audios
    
    def animar_cenas(self) -> Dict:
        """
        Etapa 4: Anima as cenas com personagens.
        """
        if not self.personagens:
            raise Exception("Personagens não disponíveis")
        
        generator = AnimationGenerator(api_token=self.replicate_token)
        
        # Mapear cenas para personagens
        cenas_imagens = self._mapear_cenas_personagens()
        
        # Extrair durações do roteiro
        duracoes = {}
        for cena in self.roteiro.get('cenas', []):
            num = cena['numero']
            dur_str = cena.get('duracao', '10s')
            duracao = int(dur_str.replace('s', ''))
            duracoes[num] = duracao
        
        videos = generator.animar_cenas(cenas_imagens, duracoes)
        
        # Salvar catálogo
        catalogo_path = os.path.join(self.temp_dir, f"{self.projeto_id}_videos.json")
        generator.salvar_catalogo_videos(videos, catalogo_path)
        
        print(f"✅ Vídeos salvos: {catalogo_path}")
        
        return videos
    
    def aplicar_lipsync(self) -> Dict:
        """
        Etapa 5: Aplica lip-sync nos vídeos.
        """
        if not self.videos_animados or not self.audios:
            print("⚠️ Vídeos ou áudios não disponíveis, pulando lip-sync")
            return self.videos_animados
        
        generator = LipsyncGenerator(api_token=self.replicate_token)
        
        videos_synced = generator.aplicar_lipsync_cenas(
            cenas_videos=self.videos_animados,
            cenas_audios=self.audios,
            apenas_dialogos=True
        )
        
        # Salvar catálogo
        catalogo_path = os.path.join(self.temp_dir, f"{self.projeto_id}_lipsync.json")
        generator.salvar_catalogo_lipsync(videos_synced, catalogo_path)
        
        print(f"✅ Lip-sync salvo: {catalogo_path}")
        
        return videos_synced
    
    def editar_video(self) -> Optional[str]:
        """
        Etapa 6: Edita e monta o vídeo final.
        """
        if not self.videos_lipsync:
            raise Exception("Vídeos não disponíveis")
        
        editor = VideoEditor(output_dir=self.output_dir)
        
        nome_saida = f"{self.projeto_id}_final.mp4"
        
        video_final = editor.montar_video_final(
            cenas_videos=self.videos_lipsync,
            cenas_audios=self.audios,
            nome_saida=nome_saida,
            transicao="fade"
        )
        
        return video_final
    
    def _mapear_cenas_personagens(self) -> Dict[int, str]:
        """
        Mapeia cenas para imagens de personagens.
        """
        mapeamento = {}
        
        cenas = self.roteiro.get('cenas', [])
        
        for cena in cenas:
            num_cena = cena['numero']
            personagens_cena = cena.get('personagens', [])
            
            # Pegar primeiro personagem da cena
            if personagens_cena and personagens_cena[0] in self.personagens:
                variacoes = self.personagens[personagens_cena[0]]
                if variacoes:
                    # Usar primeira variação
                    mapeamento[num_cena] = variacoes[0]['caminho_local']
        
        return mapeamento
    
    def _salvar_checkpoint(self, etapa: str):
        """
        Salva checkpoint da etapa atual.
        """
        checkpoint = {
            'projeto_id': self.projeto_id,
            'etapa': etapa,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'config': self.config,
            'roteiro': self.roteiro,
            'personagens': self.personagens,
            'audios': self.audios,
            'videos_animados': self.videos_animados,
            'videos_lipsync': self.videos_lipsync,
            'video_final': self.video_final
        }
        
        salvar_checkpoint(checkpoint, f"pipeline_{self.projeto_id}", self.checkpoint_dir)
    
    def _carregar_checkpoint_etapa(self, etapa: str):
        """
        Carrega dados de uma etapa do checkpoint.
        """
        checkpoint = carregar_checkpoint(f"pipeline_{self.projeto_id}", self.checkpoint_dir)
        
        if checkpoint:
            return checkpoint.get(etapa)
        
        return None


def exemplo_uso():
    """
    Exemplo de uso do Pipeline.
    """
    print("=" * 70)
    print("🚀 EXEMPLO: VideoAutomationPipeline")
    print("=" * 70)
    
    # Configuração de exemplo
    config = {
        'nicho': 'historias_infantis',
        'tema': 'A História do Rei Salomão',
        'duracao_minutos': 5,
        'idioma': 'pt-br',
        'api_keys': {
            'openai': os.getenv('OPENAI_API_KEY', 'sk-...'),
            'elevenlabs': os.getenv('ELEVENLABS_API_KEY', '...'),
            'replicate': os.getenv('REPLICATE_API_TOKEN', 'r8_...')
        }
    }
    
    # Verificar se API keys estão configuradas
    if 'sk-...' in config['api_keys']['openai']:
        print("\n⚠️ Configure as API keys para testar:")
        print("   export OPENAI_API_KEY='sk-...'")
        print("   export ELEVENLABS_API_KEY='...'")
        print("   export REPLICATE_API_TOKEN='r8_...'")
        return
    
    try:
        # Criar e executar pipeline
        pipeline = VideoAutomationPipeline(config)
        video_final = pipeline.executar_completo()
        
        if video_final:
            print(f"\n✅ Sucesso! Vídeo: {video_final}")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")


if __name__ == '__main__':
    exemplo_uso()

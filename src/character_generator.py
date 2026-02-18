"""
👤 CHARACTER GENERATOR - ProjetoX

Módulo responsável por gerar personagens consistentes usando IA.
Suporta Leonardo.AI e Replicate para geração de imagens.
"""

import os
import time
import replicate
from typing import Dict, List, Optional
from pathlib import Path

# Imports locais
try:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from config.settings import CHARACTER_CONFIG, AI_CONFIG
    from src.utils import (
        validar_api_key, download_arquivo, salvar_json,
        gerar_nome_arquivo_unico, criar_diretorios
    )
except ImportError:
    print("⚠️ Imports locais não disponíveis. Configure o PYTHONPATH.")


class CharacterGenerator:
    """
    Gerador de personagens usando Replicate ou Leonardo.AI.
    
    Cria personagens consistentes no estilo especificado para uso em vídeos.
    """
    
    def __init__(self, api_token: str, use_leonardo: bool = False):
        """
        Inicializa o gerador de personagens.
        
        Args:
            api_token: Token da API (Replicate ou Leonardo)
            use_leonardo: Se True, usa Leonardo.AI; se False, usa Replicate
        """
        if not validar_api_key(api_token, 'replicate' if not use_leonardo else 'leonardo'):
            raise ValueError(f"❌ API token inválido")
        
        self.api_token = api_token
        self.use_leonardo = use_leonardo
        
        # Configurar cliente Replicate
        if not use_leonardo:
            os.environ['REPLICATE_API_TOKEN'] = api_token
        
        self.style = CHARACTER_CONFIG.get('style', 'cartoon_3d')
        self.resolution = CHARACTER_CONFIG.get('resolution', 1024)
        self.cache_dir = '/tmp/characters_cache'
        criar_diretorios([self.cache_dir])
        
        print(f"✅ CharacterGenerator inicializado")
        print(f"   Serviço: {'Leonardo.AI' if use_leonardo else 'Replicate'}")
        print(f"   Estilo: {self.style}")
    
    def gerar_personagem(
        self,
        descricao: str,
        nome: str,
        num_variacoes: int = 1,
        estilo_override: Optional[str] = None,
        cache_enabled: bool = True
    ) -> List[Dict]:
        """
        Gera um personagem com base na descrição.
        
        Args:
            descricao: Descrição detalhada do personagem
            nome: Nome do personagem (para identificação)
            num_variacoes: Número de variações a gerar
            estilo_override: Sobrescrever estilo padrão
            cache_enabled: Usar cache se disponível
        
        Returns:
            Lista de dicionários com informações das imagens geradas
        
        Example:
            >>> gen = CharacterGenerator(api_token="r8_...")
            >>> personagens = gen.gerar_personagem(
            ...     "Rei idoso com barba branca, coroa dourada, expressão sábia",
            ...     "Rei Salomão"
            ... )
        """
        print(f"👤 Gerando personagem: {nome}")
        print(f"   Variações: {num_variacoes}")
        
        estilo = estilo_override or self.style
        
        # Construir prompt melhorado
        prompt = self._construir_prompt(descricao, estilo)
        
        resultados = []
        
        for i in range(num_variacoes):
            print(f"   Gerando variação {i+1}/{num_variacoes}...")
            
            try:
                if self.use_leonardo:
                    url_imagem = self._gerar_com_leonardo(prompt)
                else:
                    url_imagem = self._gerar_com_replicate(prompt)
                
                if url_imagem:
                    # Baixar imagem
                    nome_arquivo = f"{nome.replace(' ', '_').lower()}_v{i+1}.png"
                    caminho_local = os.path.join(self.cache_dir, nome_arquivo)
                    
                    if download_arquivo(url_imagem, caminho_local):
                        resultado = {
                            'nome': nome,
                            'variacao': i + 1,
                            'url': url_imagem,
                            'caminho_local': caminho_local,
                            'descricao': descricao,
                            'estilo': estilo,
                            'prompt_usado': prompt,
                            'gerado_em': time.strftime('%Y-%m-%d %H:%M:%S')
                        }
                        resultados.append(resultado)
                        print(f"   ✅ Variação {i+1} gerada e salva")
                    else:
                        print(f"   ⚠️ Erro ao baixar variação {i+1}")
                
                # Delay para evitar rate limiting
                if i < num_variacoes - 1:
                    time.sleep(2)
                    
            except Exception as e:
                print(f"   ❌ Erro na variação {i+1}: {e}")
        
        if resultados:
            print(f"✅ {len(resultados)} personagens gerados com sucesso!")
        else:
            print(f"❌ Nenhum personagem foi gerado")
        
        return resultados
    
    def _construir_prompt(self, descricao: str, estilo: str) -> str:
        """
        Constrói prompt otimizado para geração de personagem.
        
        Args:
            descricao: Descrição do personagem
            estilo: Estilo visual
        
        Returns:
            Prompt completo otimizado
        """
        base_prompt = CHARACTER_CONFIG.get('base_prompt', '')
        
        # Ajustes por estilo
        estilo_prompts = {
            'cartoon_3d': 'high quality 3D cartoon character, pixar style, disney style, professional render, smooth lighting, clean background, vibrant colors',
            'realistic': 'photorealistic character, high detail, professional photography, studio lighting, neutral background',
            'anime': 'anime style character, manga art, clean lines, cel shaded, professional anime art',
            '2d_flat': 'flat design character, vector art, simple shapes, bold colors, minimalist style'
        }
        
        estilo_prompt = estilo_prompts.get(estilo, estilo_prompts['cartoon_3d'])
        
        # Combinar tudo
        prompt_completo = f"{descricao}, {estilo_prompt}"
        
        # Adicionar qualificadores técnicos
        prompt_completo += f", {self.resolution}px, high quality, masterpiece, best quality"
        
        # Negative prompt (o que evitar)
        negative_elements = "low quality, blurry, distorted, deformed, ugly, bad anatomy, watermark, text"
        
        return prompt_completo
    
    def _gerar_com_replicate(self, prompt: str) -> Optional[str]:
        """
        Gera imagem usando Replicate.
        
        Args:
            prompt: Prompt para geração
        
        Returns:
            URL da imagem gerada ou None
        """
        try:
            # Usar SDXL (Stable Diffusion XL) para qualidade
            output = replicate.run(
                "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                input={
                    "prompt": prompt,
                    "width": self.resolution,
                    "height": self.resolution,
                    "num_outputs": 1,
                    "guidance_scale": 7.5,
                    "num_inference_steps": 30,
                }
            )
            
            # Output é uma lista de URLs
            if output and len(output) > 0:
                return output[0]
            
            return None
            
        except Exception as e:
            error_msg = str(e).lower()
            
            # Mensagens específicas por tipo de erro
            if "insufficient" in error_msg and "credit" in error_msg:
                print("\n" + "=" * 60)
                print("❌ REPLICATE SEM CRÉDITOS!")
                print("   Sua conta Replicate não tem créditos suficientes.")
                print("   Soluções:")
                print("   1. Acesse: https://replicate.com/account/billing")
                print("   2. Adicione créditos ao seu plano")
                print("   3. Tente novamente após adicionar créditos")
                print("=" * 60 + "\n")
            elif "throttled" in error_msg or "rate" in error_msg or "limit" in error_msg:
                print("\n" + "=" * 60)
                print("⚠️  RATE LIMIT ATINGIDO!")
                print("   Você excedeu o limite de requisições do Replicate.")
                print("   Soluções:")
                print("   1. Aguarde alguns minutos antes de tentar novamente")
                print("   2. Considere fazer upgrade do plano para maior limite")
                print("   3. Reduza a frequência de chamadas à API")
                print("=" * 60 + "\n")
            elif "unauthorized" in error_msg or "authentication" in error_msg:
                print("\n" + "=" * 60)
                print("❌ ERRO DE AUTENTICAÇÃO!")
                print("   Token de API inválido ou expirado.")
                print("   Soluções:")
                print("   1. Verifique se o REPLICATE_API_TOKEN está correto")
                print("   2. Gere um novo token em: https://replicate.com/account/api-tokens")
                print("=" * 60 + "\n")
            else:
                print(f"❌ Erro no Replicate: {e}")
            
            return None
    
    def _gerar_com_leonardo(self, prompt: str) -> Optional[str]:
        """
        Gera imagem usando Leonardo.AI.
        
        Args:
            prompt: Prompt para geração
        
        Returns:
            URL da imagem gerada ou None
        
        Note:
            Implementação placeholder - requer SDK do Leonardo.AI
        """
        print("⚠️ Leonardo.AI não implementado ainda - usando Replicate como fallback")
        return self._gerar_com_replicate(prompt)
    
    def gerar_conjunto_personagens(
        self,
        lista_personagens: List[Dict],
        cache_enabled: bool = True
    ) -> Dict[str, List[Dict]]:
        """
        Gera múltiplos personagens de uma vez.
        
        Args:
            lista_personagens: Lista de dicts com 'nome' e 'descricao'
            cache_enabled: Usar cache
        
        Returns:
            Dicionário mapeando nome -> lista de variações
        
        Example:
            >>> personagens = [
            ...     {"nome": "Rei Salomão", "descricao": "Rei idoso..."},
            ...     {"nome": "Rainha de Sabá", "descricao": "Rainha elegante..."}
            ... ]
            >>> resultado = gen.gerar_conjunto_personagens(personagens)
        """
        print(f"👥 Gerando conjunto de {len(lista_personagens)} personagens...")
        
        resultados = {}
        
        for i, personagem in enumerate(lista_personagens):
            nome = personagem.get('nome', f'Personagem_{i+1}')
            descricao = personagem.get('descricao', '')
            num_variacoes = personagem.get('num_variacoes', 1)
            
            print(f"\n[{i+1}/{len(lista_personagens)}] Processando: {nome}")
            
            variacoes = self.gerar_personagem(
                descricao=descricao,
                nome=nome,
                num_variacoes=num_variacoes,
                cache_enabled=cache_enabled
            )
            
            if variacoes:
                resultados[nome] = variacoes
        
        print(f"\n✅ Conjunto completo: {len(resultados)} personagens gerados")
        return resultados
    
    def gerar_expressoes(
        self,
        personagem_base: str,
        expressoes: List[str]
    ) -> List[Dict]:
        """
        Gera diferentes expressões faciais do mesmo personagem.
        
        Args:
            personagem_base: Descrição base do personagem
            expressoes: Lista de expressões (feliz, triste, pensativo, etc)
        
        Returns:
            Lista de variações com diferentes expressões
        
        Example:
            >>> expressoes = gen.gerar_expressoes(
            ...     "Rei idoso com barba branca",
            ...     ["feliz", "sério", "pensativo"]
            ... )
        """
        print(f"😊 Gerando {len(expressoes)} expressões...")
        
        resultados = []
        
        for expressao in expressoes:
            descricao_completa = f"{personagem_base}, expressão {expressao}"
            
            variacoes = self.gerar_personagem(
                descricao=descricao_completa,
                nome=f"personagem_{expressao}",
                num_variacoes=1,
                cache_enabled=False
            )
            
            if variacoes:
                resultados.extend(variacoes)
        
        return resultados
    
    def criar_personagem_de_roteiro(
        self,
        roteiro: Dict
    ) -> Dict[str, List[Dict]]:
        """
        Cria todos os personagens necessários de um roteiro.
        
        Args:
            roteiro: Roteiro completo com seção 'personagens_necessarios'
        
        Returns:
            Dicionário com todos os personagens gerados
        """
        personagens_info = roteiro.get('personagens_necessarios', [])
        
        if not personagens_info:
            print("⚠️ Nenhum personagem especificado no roteiro")
            return {}
        
        print(f"📋 Criando personagens do roteiro...")
        
        # Converter para formato adequado
        lista_personagens = []
        for p in personagens_info:
            lista_personagens.append({
                'nome': p.get('nome', 'Personagem'),
                'descricao': p.get('descricao', ''),
                'num_variacoes': 2  # Gerar 2 variações por personagem
            })
        
        return self.gerar_conjunto_personagens(lista_personagens)
    
    def salvar_catalogo_personagens(
        self,
        personagens: Dict[str, List[Dict]],
        caminho: str
    ) -> bool:
        """
        Salva catálogo de personagens em JSON.
        
        Args:
            personagens: Dicionário de personagens
            caminho: Caminho do arquivo
        
        Returns:
            True se sucesso
        """
        print(f"💾 Salvando catálogo de personagens...")
        
        # Preparar dados para serialização
        catalogo = {
            'gerado_em': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_personagens': len(personagens),
            'estilo': self.style,
            'personagens': personagens
        }
        
        return salvar_json(catalogo, caminho, identado=True)
    
    def limpar_cache(self) -> int:
        """
        Limpa cache de personagens.
        
        Returns:
            Número de arquivos deletados
        """
        from src.utils import limpar_diretorio
        
        print(f"🗑️ Limpando cache de personagens...")
        return limpar_diretorio(self.cache_dir, ['.png', '.jpg', '.jpeg'])


def exemplo_uso():
    """
    Exemplo de uso do CharacterGenerator.
    """
    print("=" * 60)
    print("👤 EXEMPLO: CharacterGenerator")
    print("=" * 60)
    
    # Nota: Use seu token real aqui
    api_token = os.getenv('REPLICATE_API_TOKEN', 'r8_...')
    
    if api_token == 'r8_...':
        print("⚠️ Configure REPLICATE_API_TOKEN para testar")
        return
    
    try:
        # Criar gerador
        generator = CharacterGenerator(api_token=api_token)
        
        # Gerar um personagem
        personagens = generator.gerar_personagem(
            descricao="Rei idoso com longa barba branca, coroa dourada ornamentada, túnica roxa real, expressão sábia e bondosa, olhos gentis",
            nome="Rei Salomão",
            num_variacoes=2
        )
        
        # Exibir resultados
        print(f"\n📋 PERSONAGENS GERADOS:")
        for p in personagens:
            print(f"   {p['nome']} (v{p['variacao']}): {p['caminho_local']}")
        
        # Salvar catálogo
        if personagens:
            catalogo = {"Rei Salomão": personagens}
            generator.salvar_catalogo_personagens(
                catalogo,
                '/tmp/personagens_exemplo.json'
            )
        
    except Exception as e:
        print(f"❌ Erro no exemplo: {e}")


if __name__ == '__main__':
    exemplo_uso()

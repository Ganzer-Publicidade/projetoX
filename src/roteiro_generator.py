"""
📝 ROTEIRO GENERATOR - ProjetoX

Módulo responsável por gerar roteiros completos para vídeos usando ChatGPT.
"""

import os
import json
import time
from typing import Dict, List, Optional
from openai import OpenAI

# Imports locais
try:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from config.settings import AI_CONFIG, LANGUAGE_CONFIG
    from src.utils import validar_api_key, salvar_json, configurar_logging
except ImportError:
    print("⚠️ Imports locais não disponíveis. Configure o PYTHONPATH.")


class RoteiroGenerator:
    """
    Gerador de roteiros usando OpenAI GPT.
    
    Este gerador cria roteiros estruturados e profissionais para vídeos,
    incluindo cenas, diálogos, descrições visuais e metadados.
    """
    
    def __init__(self, api_key: str, modelo: str = None):
        """
        Inicializa o gerador de roteiros.
        
        Args:
            api_key: Chave da API OpenAI
            modelo: Modelo a usar (padrão: gpt-4-turbo-preview)
        """
        if not validar_api_key(api_key, 'openai'):
            raise ValueError("❌ API key OpenAI inválida")
        
        self.client = OpenAI(api_key=api_key)
        self.modelo = modelo or AI_CONFIG.get('openai_model', 'gpt-4-turbo-preview')
        self.temperature = AI_CONFIG.get('openai_temperature', 0.7)
        self.max_tokens = AI_CONFIG.get('openai_max_tokens', 4000)
        
        print(f"✅ RoteiroGenerator inicializado com modelo {self.modelo}")
    
    def gerar_roteiro(
        self,
        tema: str,
        nicho: str = "historias_infantis",
        duracao_minutos: int = 5,
        idioma: str = "pt-br",
        num_cenas: Optional[int] = None
    ) -> Dict:
        """
        Gera um roteiro completo para vídeo.
        
        Args:
            tema: Tema do vídeo (ex: "A História do Rei Salomão")
            nicho: Nicho/categoria do vídeo
            duracao_minutos: Duração estimada do vídeo
            idioma: Código do idioma (pt-br, en, es)
            num_cenas: Número de cenas (calculado automaticamente se None)
        
        Returns:
            Dicionário com roteiro completo estruturado
        
        Example:
            >>> generator = RoteiroGenerator(api_key="sk-...")
            >>> roteiro = generator.gerar_roteiro("Rei Salomão", duracao_minutos=5)
        """
        if not tema:
            raise ValueError("❌ Tema não pode estar vazio")
        
        # Calcular número de cenas se não fornecido
        if num_cenas is None:
            num_cenas = (duracao_minutos * 60) // 12  # ~12 segundos por cena
            num_cenas = max(10, min(40, num_cenas))  # Entre 10 e 40 cenas
        
        print(f"📝 Gerando roteiro: {tema}")
        print(f"   Nicho: {nicho} | Duração: {duracao_minutos}min | Cenas: {num_cenas}")
        
        # Construir prompt
        prompt = self._construir_prompt(tema, nicho, duracao_minutos, num_cenas, idioma)
        
        try:
            # Chamar API OpenAI
            print("🤖 Consultando ChatGPT...")
            
            response = self.client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(idioma, nicho)
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            
            # Extrair resposta
            conteudo = response.choices[0].message.content
            roteiro = json.loads(conteudo)
            
            # Adicionar metadados
            roteiro['metadata'] = {
                'gerado_em': time.strftime('%Y-%m-%d %H:%M:%S'),
                'modelo_usado': self.modelo,
                'tokens_usados': response.usage.total_tokens,
                'idioma': idioma,
                'nicho': nicho
            }
            
            print(f"✅ Roteiro gerado com sucesso!")
            print(f"   Título: {roteiro.get('titulo', 'N/A')}")
            print(f"   Cenas: {len(roteiro.get('cenas', []))}")
            print(f"   Tokens: {response.usage.total_tokens}")
            
            return roteiro
            
        except Exception as e:
            print(f"❌ Erro ao gerar roteiro: {e}")
            raise
    
    def _get_system_prompt(self, idioma: str, nicho: str) -> str:
        """
        Retorna o prompt de sistema adequado.
        
        Args:
            idioma: Código do idioma
            nicho: Nicho do vídeo
        
        Returns:
            Prompt de sistema
        """
        lang_instruction = LANGUAGE_CONFIG.get(idioma, LANGUAGE_CONFIG['pt-br'])['openai_instructions']
        
        nicho_instructions = {
            'historias_infantis': 'Crie histórias educativas e divertidas para crianças, com linguagem simples e personagens carismáticos.',
            'terror': 'Crie histórias de terror envolventes com suspense, atmosfera sombria e reviravoltas.',
            'curiosidades': 'Apresente fatos interessantes de forma educativa e envolvente, com informações precisas.',
            'motivacional': 'Crie conteúdo inspirador e motivacional com mensagens poderosas e exemplos práticos.'
        }
        
        nicho_instruction = nicho_instructions.get(nicho, nicho_instructions['historias_infantis'])
        
        return f"""Você é um roteirista profissional especializado em criar roteiros para vídeos do YouTube.

{lang_instruction}

Especialidade: {nicho_instruction}

IMPORTANTE: Sua resposta DEVE ser um JSON válido com a estrutura exata especificada no prompt do usuário.
Use formatação JSON correta e certifique-se de que todos os campos estão presentes."""
    
    def _construir_prompt(
        self,
        tema: str,
        nicho: str,
        duracao_minutos: int,
        num_cenas: int,
        idioma: str
    ) -> str:
        """
        Constrói o prompt para geração do roteiro.
        
        Args:
            tema: Tema do vídeo
            nicho: Nicho do vídeo
            duracao_minutos: Duração em minutos
            num_cenas: Número de cenas
            idioma: Código do idioma
        
        Returns:
            Prompt completo
        """
        duracao_por_cena = (duracao_minutos * 60) // num_cenas
        
        prompt = f"""Crie um roteiro COMPLETO para um vídeo de YouTube sobre: "{tema}"

ESPECIFICAÇÕES:
- Nicho: {nicho}
- Duração total: {duracao_minutos} minutos
- Número de cenas: {num_cenas}
- Duração por cena: aproximadamente {duracao_por_cena} segundos
- Idioma: {idioma}
- Estilo visual: Cartoon 3D (estilo Pixar)

O roteiro deve ser ESTRUTURADO e PROFISSIONAL, pronto para produção.

Retorne um JSON com esta estrutura EXATA:

{{
  "titulo": "Título otimizado para YouTube (50-60 caracteres)",
  "descricao": "Descrição atrativa do vídeo (2-3 frases)",
  "duracao_estimada": "{duracao_minutos}min",
  "idioma": "{idioma}",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "thumbnail_sugestao": "Descrição da thumbnail ideal",
  "cenas": [
    {{
      "numero": 1,
      "titulo": "Título da cena",
      "duracao": "{duracao_por_cena}s",
      "tipo_cena": "abertura",
      "narrativa": "Texto completo que será narrado nesta cena",
      "descricao_visual": "Descrição detalhada do que aparece visualmente",
      "personagens": ["personagem1", "personagem2"],
      "tipo_audio": "dialogo",
      "emocao": "confiante",
      "transicao": "fade",
      "notas_producao": "Notas importantes para produção"
    }},
    ...
  ],
  "personagens_necessarios": [
    {{
      "nome": "Nome do Personagem",
      "descricao": "Descrição física detalhada para geração de imagem",
      "tipo": "protagonista",
      "caracteristicas": ["característica1", "característica2"]
    }}
  ],
  "musica_sugerida": {{
    "mood": "inspirador",
    "estilo": "orquestral",
    "intensidade": "média"
  }},
  "seo": {{
    "titulo_alternativo": "Título SEO otimizado",
    "palavras_chave": ["keyword1", "keyword2", "keyword3"],
    "categoria": "Education"
  }}
}}

DIRETRIZES IMPORTANTES:
1. Cada cena deve ter narrativa completa e natural
2. Descrições visuais devem ser MUITO detalhadas para geração de imagens IA
3. Inclua variedade de emoções e tipos de cena
4. Mantenha o ritmo adequado (início cativante, meio envolvente, final impactante)
5. Para personagens cartoon 3D: descreva estilo visual, cores, expressões
6. Narrativa deve ser adequada para o nicho especificado
7. Crie continuidade entre as cenas

Tipos de cena possíveis: abertura, apresentacao, desenvolvimento, conflito, climax, resolucao, encerramento
Tipos de áudio: dialogo, narracao, musica_apenas, silencio
Emoções: confiante, feliz, triste, pensativo, animado, sério, misterioso, tenso
Transições: fade, corte, dissolve, slide

Gere o roteiro completo agora em JSON:"""
        
        return prompt
    
    def refinar_roteiro(
        self,
        roteiro_original: Dict,
        instrucoes_refinamento: str
    ) -> Dict:
        """
        Refina um roteiro existente com base em instruções.
        
        Args:
            roteiro_original: Roteiro a ser refinado
            instrucoes_refinamento: Instruções de refinamento
        
        Returns:
            Roteiro refinado
        """
        print(f"🔧 Refinando roteiro...")
        
        prompt = f"""Refine o seguinte roteiro de vídeo com base nestas instruções:

INSTRUÇÕES: {instrucoes_refinamento}

ROTEIRO ORIGINAL:
{json.dumps(roteiro_original, ensure_ascii=False, indent=2)}

Retorne o roteiro refinado mantendo a MESMA ESTRUTURA JSON, mas aplicando as melhorias solicitadas."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um roteirista profissional refinando roteiros de vídeo."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            
            roteiro_refinado = json.loads(response.choices[0].message.content)
            
            # Atualizar metadados
            roteiro_refinado['metadata'] = roteiro_original.get('metadata', {})
            roteiro_refinado['metadata']['refinado_em'] = time.strftime('%Y-%m-%d %H:%M:%S')
            roteiro_refinado['metadata']['instrucoes_refinamento'] = instrucoes_refinamento
            
            print(f"✅ Roteiro refinado com sucesso!")
            return roteiro_refinado
            
        except Exception as e:
            print(f"❌ Erro ao refinar roteiro: {e}")
            return roteiro_original
    
    def gerar_titulo_alternativo(self, tema: str, idioma: str = "pt-br") -> List[str]:
        """
        Gera títulos alternativos para o vídeo.
        
        Args:
            tema: Tema do vídeo
            idioma: Código do idioma
        
        Returns:
            Lista de títulos alternativos
        """
        print(f"💡 Gerando títulos alternativos...")
        
        prompt = f"""Gere 5 títulos alternativos otimizados para YouTube sobre: "{tema}"

Requisitos:
- Entre 50-60 caracteres
- Cativantes e otimizados para SEO
- Idioma: {idioma}
- Incluir emojis apropriados

Retorne apenas um JSON com array de títulos:
{{"titulos": ["titulo1", "titulo2", "titulo3", "titulo4", "titulo5"]}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.modelo,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.9,
                max_tokens=300,
                response_format={"type": "json_object"}
            )
            
            resultado = json.loads(response.choices[0].message.content)
            titulos = resultado.get('titulos', [])
            
            print(f"✅ {len(titulos)} títulos gerados")
            return titulos
            
        except Exception as e:
            print(f"❌ Erro ao gerar títulos: {e}")
            return []
    
    def salvar_roteiro(self, roteiro: Dict, caminho: str) -> bool:
        """
        Salva o roteiro em arquivo JSON.
        
        Args:
            roteiro: Roteiro a salvar
            caminho: Caminho do arquivo
        
        Returns:
            True se sucesso
        """
        return salvar_json(roteiro, caminho, identado=True)
    
    def analisar_tendencias(self, nicho: str, idioma: str = "pt-br") -> Dict:
        """
        Analisa tendências do nicho para sugerir temas.
        
        Args:
            nicho: Nicho a analisar
            idioma: Código do idioma
        
        Returns:
            Análise de tendências com sugestões
        """
        print(f"📊 Analisando tendências do nicho: {nicho}")
        
        prompt = f"""Como especialista em tendências de YouTube, analise o nicho "{nicho}" e sugira:

1. 5 temas em alta no momento
2. Formatos de vídeo que funcionam bem
3. Duração ideal dos vídeos
4. Palavras-chave importantes
5. Estilo de narrativa recomendado

Idioma: {idioma}

Retorne JSON estruturado:
{{
  "nicho": "{nicho}",
  "temas_em_alta": ["tema1", "tema2", ...],
  "formatos_recomendados": ["formato1", "formato2", ...],
  "duracao_ideal": "5-7 minutos",
  "palavras_chave": ["palavra1", "palavra2", ...],
  "estilo_narrativa": "descrição do estilo",
  "dicas": ["dica1", "dica2", ...]
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.modelo,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=1000,
                response_format={"type": "json_object"}
            )
            
            analise = json.loads(response.choices[0].message.content)
            
            print(f"✅ Análise de tendências concluída")
            return analise
            
        except Exception as e:
            print(f"❌ Erro na análise de tendências: {e}")
            return {}


def exemplo_uso():
    """
    Exemplo de uso do RoteiroGenerator.
    """
    print("=" * 60)
    print("📝 EXEMPLO: RoteiroGenerator")
    print("=" * 60)
    
    # Nota: Use sua API key real aqui
    api_key = os.getenv('OPENAI_API_KEY', 'sk-...')
    
    if api_key == 'sk-...':
        print("⚠️ Configure OPENAI_API_KEY para testar")
        return
    
    try:
        # Criar gerador
        generator = RoteiroGenerator(api_key=api_key)
        
        # Gerar roteiro
        roteiro = generator.gerar_roteiro(
            tema="A Sabedoria do Rei Salomão",
            nicho="historias_infantis",
            duracao_minutos=5,
            idioma="pt-br"
        )
        
        # Exibir resumo
        print(f"\n📋 ROTEIRO GERADO:")
        print(f"Título: {roteiro['titulo']}")
        print(f"Cenas: {len(roteiro['cenas'])}")
        print(f"Personagens: {len(roteiro.get('personagens_necessarios', []))}")
        
        # Salvar
        generator.salvar_roteiro(roteiro, '/tmp/roteiro_exemplo.json')
        
    except Exception as e:
        print(f"❌ Erro no exemplo: {e}")


if __name__ == '__main__':
    exemplo_uso()

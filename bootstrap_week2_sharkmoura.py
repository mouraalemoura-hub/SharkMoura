import pathlib
import os

# Função utilitária para gravar arquivos com codificação UTF-8 e mostrar tamanho
def gravar_arquivo(caminho, conteudo):
    """
    Grava o conteúdo em um arquivo, criando diretórios se necessário.
    Mostra o tamanho do arquivo em bytes.
    """
    caminho = pathlib.Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    tamanho = caminho.stat().st_size
    print(f'Arquivo {caminho} gerado com sucesso. Tamanho: {tamanho} bytes.')

# Função principal para gerar todos os arquivos da Semana 2
def main():
    # Criar diretório docs se não existir
    docs_dir = pathlib.Path('docs')
    docs_dir.mkdir(exist_ok=True)

    # Conteúdo do documento 08 - Famílias de Sinais
    conteudo_08 = """# 08 - Famílias de Sinais

## Objetivo
Este documento define as famílias de sinais utilizados no motor de análise do SharkMoura 2.0, visando uma classificação estruturada para otimizar a tomada de decisão.

## Posição Técnica de Abertura
A posição técnica de abertura é determinada pela combinação de sinais de múltiplas famílias, priorizando a consistência e a redundância.

## Princípio de Classificação
Os sinais são classificados em famílias baseadas em sua natureza: momentum, estrutura, volume, etc.

## Observação sobre Camada 0
O sinal `preco_ref_meta` é classificado como Camada 0 — Referência Operacional, servindo como base para todas as análises.

## Famílias 1 a 6
- **Família 1: Momentum** - Inclui sinais como RSI e MACD.
- **Família 2: Estrutura de Mercado** - Engloba SMC_Structure e BOS.
- **Família 3: Volume e Liquidez** - Compreende PD_Area e níveis de liquidez.
- **Família 4: Volatilidade** - Inclui ATR e Bollinger Bands.
- **Família 5: Projeção e Alvos** - Engloba projeção e Alvo_Semana.
- **Família 6: Outros** - Sinais complementares como FFFD e OB.

## Resumo Executivo
As famílias garantem uma cobertura abrangente dos aspectos técnicos do mercado.

## Decisões Oficiais
Aprovar a estrutura de famílias para implementação imediata.

## Veredicto Técnico Final
Estrutura validada e pronta para integração no motor.
"""

    gravar_arquivo('docs/08_familias_de_sinais.md', conteudo_08)

    # Conteúdo do documento 09 - Matriz de Redundância
    conteudo_09 = """# 09 - Matriz de Redundância de Sinais

## Critério Tipo A/B/C/D
- Tipo A: Alta redundância, alta confiança.
- Tipo B: Média redundância.
- Tipo C: Baixa redundância.
- Tipo D: Sem redundância.

## Regra de Decisão
Decidir com base na maioria dos sinais redundantes.

## Análise dos Blocos Principais
- **infer_direction**: Tipo A.
- **SMC_Structure**: Tipo B.
- **BOS**: Tipo A.
- **CHOCH**: Tipo B.
- **PD_Area/PD_Value**: Tipo C.
- **FVG**: Tipo B.
- **OB**: Tipo C.
- **Níveis de Liquidez**: Tipo A.
- **ATR**: Tipo B.
- **move_cap**: Tipo C.
- **Bollinger**: Tipo B.
- **FFFD**: Tipo D.
- **Projeção**: Tipo B.
- **Alvo_Semana**: Tipo A.

## Consolidação por Blocos
Blocos com Tipo A são prioritários.

## Decisões Oficiais
Implementar regras de redundância.

## Veredicto Final
Matriz aprovada para uso.
"""

    gravar_arquivo('docs/09_matriz_redundancia_sinais.md', conteudo_09)

    # Conteúdo do documento 10 - Classificador de Regime v1
    conteudo_10 = """# 10 - Classificador de Regime v1

## Objetivo
Classificar o regime de mercado atual para ajustar estratégias.

## Função Oficial
Retornar o regime principal e flags associadas.

## Estrutura
Regime principal com flags de suporte.

## Regimes Principais
- TENDENCIA_ALTA
- TENDENCIA_BAIXA
- LATERAL_ESTRUTURADA
- TRANSICAO
- EXPANSAO_DIRECIONAL
- EXAUSTAO_OU_ESTICAMENTO

## Hierarquia de Leitura
Priorizar regimes de tendência sobre laterais.

## Regras de Precedência
Tendência > Lateral > Transição.

## Saída Esperada
Dicionário com regime e flags.

## Impacto no Motor
Ajusta pesos e decisões.
"""

    gravar_arquivo('docs/10_classificador_regime_v1.md', conteudo_10)

    # Conteúdo do documento 11 - Score do Ativo v2
    conteudo_11 = """# 11 - Score do Ativo v2

## Objetivo
Avaliar a atratividade do ativo para investimento.

## Princípio Central
Combinação ponderada de fatores técnicos.

## O que Mede e Não Mede
Mede força técnica; não mede fundamentos.

## 5 Blocos Oficiais
1. Momentum (15%)
2. Estrutura (35%)
3. Volume (20%)
4. Volatilidade (20%)
5. Projeção (10%)

## Blocos Fora do Score
Fundamentais e notícias.

## Regra de Ouro
Manter equilíbrio entre blocos.

## Escala 0 a 100
Pontuação normalizada.

## Pesos Conceituais
15/35/20/20/10.

## Penalidades
Redução por conflitos.

## Regras de Teto
Máximo 100.

## Relação com Regime
Ajusta baseado no regime.

## Saída Esperada
Valor numérico de 0 a 100.
"""

    gravar_arquivo('docs/11_score_ativo_v2.md', conteudo_11)

    # Conteúdo do documento 12 - Adequação ao Horizonte Semanal
    conteudo_12 = """# 12 - Adequação ao Horizonte Semanal

## Objetivo
Verificar se o ativo é adequado para horizonte semanal.

## Função Oficial
Avaliar compatibilidade com semana.

## O que Mede e Não Mede
Mede tempo e espaço; não mede risco absoluto.

## Relação entre Score, Regime e Adequação
Integra score e regime.

## 4 Blocos
1. Tempo restante
2. Espaço útil
3. Plausibilidade do deslocamento
4. Maturidade da tese

## Classificações
- ADEQUADA
- ADEQUADA_COM_RESSALVAS
- FRACA_PARA_SEMANA
- INADEQUADA

## Penalidades e Bônus
Penalidades por tempo curto.

## Relação com Alvo_Semana
Integra alvo projetado.

## Saída Esperada
Classificação textual.
"""

    gravar_arquivo('docs/12_adequacao_horizonte_semanal.md', conteudo_12)

    # Conteúdo do documento 13 - Fechamento Oficial da Semana 2
    conteudo_13 = """# 13 - Fechamento Oficial da Semana 2

## Objetivo
Consolidar os avanços da Semana 2.

## Veredito Executivo
Semana 2 concluída com sucesso.

## Missão da Semana 2 e Status
Missão: Refinar sinais e regimes. Status: Concluída.

## O que Foi Consolidado
Famílias, matriz, classificador, score, adequação.

## Arquitetura Final Consolidada
Motor com sinais organizados.

## Critérios de Aceite
Todos os documentos aprovados.

## Entregáveis Produzidos
Documentos e script de bootstrap.

## Pendências
Nenhuma.

## Riscos Residuais
Mínimos.

## Prontidão para Semana 3
Total.

## Decisões Finais
Avançar para Semana 3.

## Encerramento Oficial
Semana 2 finalizada.
"""

    gravar_arquivo('docs/13_fechamento_oficial_semana_2.md', conteudo_13)

    # Conteúdo do README_WEEK2.md
    conteudo_readme = """# README - Semana 2 do SharkMoura 2.0

## Propósito da Semana 2
Refinar e organizar os sinais e regimes para o motor de análise.

## Arquivos Gerados
- docs/08_familias_de_sinais.md
- docs/09_matriz_redundancia_sinais.md
- docs/10_classificador_regime_v1.md
- docs/11_score_ativo_v2.md
- docs/12_adequacao_horizonte_semanal.md
- docs/13_fechamento_oficial_semana_2.md
- docs/00_indice_arquitetura_sharkmoura_v2.md

## Como a Semana 2 Reorganiza o Motor
Introduz famílias, redundância e regimes.

## Conexão com Semana 3
Prepara base para implementação avançada.
"""

    gravar_arquivo('README_WEEK2.md', conteudo_readme)

    # Conteúdo do índice opcional
    conteudo_indice = """# 00 - Índice da Arquitetura SharkMoura v2

## Visão Geral do Projeto
Sistema de análise técnica automatizada.

## Documentos da Semana 1
- 01 a 07: Definições iniciais.

## Documentos da Semana 2
- 08 a 13: Refinamentos.

## Ordem de Leitura Recomendada
1. Índice
2. Semana 1
3. Semana 2

## Relação entre Documentos
Sequencial e dependente.
"""

    gravar_arquivo('docs/00_indice_arquitetura_sharkmoura_v2.md', conteudo_indice)

    # Resumo final
    print('\nResumo dos arquivos gerados:')
    arquivos = [
        'docs/08_familias_de_sinais.md',
        'docs/09_matriz_redundancia_sinais.md',
        'docs/10_classificador_regime_v1.md',
        'docs/11_score_ativo_v2.md',
        'docs/12_adequacao_horizonte_semanal.md',
        'docs/13_fechamento_oficial_semana_2.md',
        'README_WEEK2.md',
        'docs/00_indice_arquitetura_sharkmoura_v2.md'
    ]
    for arq in arquivos:
        if pathlib.Path(arq).exists():
            print(f'- {arq}')
    print('\nSemana 2 materializada com sucesso!')

if __name__ == "__main__":
    main()
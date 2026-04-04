# Inventário Funcional do Legado

## Visão Geral

Este documento apresenta o inventário completo dos componentes funcionais herdados das versões v1.8.13 e v1.8.18 do sistema SharkMoura. O inventário abrange estruturas de dados, algoritmos e lógicas de decisão utilizados no legado.

## Componentes Principais

### Referência Operacional
- Preço de referência com regras de cálculo (CLOSE, OPEN, VWAP, etc.).
- Data de referência para contextualização temporal.

### Hipótese Direcional
- Inferência de direção baseada em EMAs e tendências semanais/horárias.

### Núcleo Estrutural
- Estruturas SMC (Smart Money Concepts) incluindo BOS, CHOCH, PD e FVG.
- Mapeamento de liquidez com zonas de alta/baixa e alvos.

### Volatilidade e Timing
- Indicadores como ATR, RSI, MACD e Bollinger Bands.
- Flags de Fair Value Gaps e contextos semanais.

### Projeções de Entrada
- Sugestões de entradas primárias/secundárias com probabilidades.
- Alvos (T1, T2, T3) e stops com métricas de risco-retorno.

### Score e Veredicto
- Scores de confluência e probabilidade.
- Veredictos categorizados (DIAMANTE, OURO, etc.).

## Considerações

O inventário confirma a robustez do legado, servindo como base para expansões futuras sem reinventar componentes funcionais.

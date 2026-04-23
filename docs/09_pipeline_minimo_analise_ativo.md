# 09 — Pipeline Mínimo de Análise do Ativo

## Objetivo do documento

Este documento define o pipeline mínimo de análise do ativo para a Semana 2 do SharkMoura 2.0. O foco não é descrever o motor final do projeto, mas estabelecer a primeira cadeia funcional confiável entre entrada, processamento, consolidação e saída.

A lógica central desta etapa é simples: antes de sofisticar inteligência, o sistema precisa conseguir rodar um fluxo mínimo de forma previsível, validável e explicável.

---

## Papel deste pipeline na arquitetura do projeto

O pipeline mínimo ocupa a fronteira entre:

- a **base documental e contratual** fechada na Semana 1; e
- a **execução funcional real** que começa a ganhar forma na Semana 2.

Ele existe para responder a uma pergunta objetiva:

**dado um conjunto mínimo de dados de entrada, o sistema consegue produzir um `AssetAnalysisPayload` válido, coerente e rastreável?**

Se a resposta for sim, a Semana 2 está no caminho certo.  
Se a resposta for não, qualquer sofisticação posterior será construída sobre base instável.

---

## Princípios do pipeline mínimo

O pipeline da Semana 2 deve obedecer aos seguintes princípios:

### 1. Conservadorismo
A primeira versão funcional deve preferir clareza a ambição.

### 2. Separação de responsabilidades
Cada camada deve fazer uma coisa bem definida.

### 3. Validação explícita
Entradas e saídas devem ser validadas de forma objetiva.

### 4. Rastreabilidade
Todo veredito precisa poder ser explicado a partir das camadas processadas.

### 5. Evolução incremental
O pipeline mínimo não precisa ser completo; precisa ser confiável o suficiente para evoluir.

---

## Escopo funcional do pipeline mínimo

O pipeline mínimo deve cobrir estas etapas:

1. receber input padronizado;
2. validar o input mínimo;
3. processar tendência-base;
4. processar estrutura;
5. processar liquidez;
6. processar volatilidade e timing;
7. processar projeção;
8. consolidar score legado e campos auxiliares quando aplicável;
9. gerar veredito inicial;
10. montar `AssetAnalysisPayload`;
11. validar a saída pelo schema oficial.

---

## Contrato de entrada mínima

A Semana 2 precisa trabalhar com um input mínimo de ativo. Esse input ainda não é a estrutura definitiva do projeto, mas já deve ser suficiente para alimentar o pipeline sem improvisação.

## Campos mínimos recomendados

### Identificação
- `ticker`
- `analysis_date`

### Referência operacional
- `price_ref`
- `ref_date`
- `ref_rule`

### Tendência-base
- `infer_direction`
- `direcao_inst`
- `w1_trend`
- `h1_trend`
- `slope_ema200`

### Estrutura
- `smc_structure`
- `smc_last_bos`
- `smc_last_choch`
- `smc_pd_area`
- `smc_pd_value`
- `smc_ob_type`
- `smc_fvg_side`
- `smc_fvg_size_atr`

### Liquidez
- `liq_side`
- `eq_high`
- `eq_low`
- `pdh`
- `pdl`
- `pwh`
- `pwl`

### Volatilidade e timing
- `atr14`
- `rsi14`
- `macd`
- `macd_hist`
- `bb_percent_b`
- `bb_bandwidth`
- `fffd`
- `fffd_side`

### Projeção
- `preco_ref`
- `entrada_sugerida`
- `entrada_primaria`
- `entrada_secundaria`
- `stop_inst`
- `stop_loss`
- `t1`
- `t2`
- `t3`
- `risk_reward_ratio`

### Fechamento auxiliar
- `legacy_score` ou componentes mínimos equivalentes
- `notas` opcionais

---

## Estrutura proposta do pipeline

## Etapa 1 — Ingestão do input

### Objetivo
Receber o input bruto e verificar se ele possui o conjunto mínimo necessário para análise.

### Regras
- recusar input sem `ticker`;
- recusar input sem `analysis_date`;
- recusar input sem referência operacional mínima;
- aceitar ausência de várias camadas avançadas, desde que a análise mínima ainda seja possível;
- padronizar formatos básicos antes do processamento.

### Saída esperada
Um objeto intermediário normalizado, pronto para ser consumido pelos serviços.

---

## Etapa 2 — Serviço de tendência

### Objetivo
Transformar sinais direcionais mínimos em uma leitura inicial de tendência-base.

### Responsabilidades
- consolidar `infer_direction`;
- consolidar `direcao_inst`;
- ler coerência entre `w1_trend` e `h1_trend`;
- usar `slope_ema200` como reforço contextual, não como regra única.

### Saída esperada
`TrendBasePayload`

### Regra operacional da Semana 2
Nesta fase, o serviço deve ser simples. Ele não precisa inferir inteligência sofisticada. Ele só precisa produzir uma leitura consistente e explicável.

---

## Etapa 3 — Serviço de estrutura

### Objetivo
Consolidar a leitura estrutural institucional mínima.

### Responsabilidades
- mapear estrutura predominante;
- registrar último BOS;
- registrar último CHOCH;
- registrar área de PD;
- registrar informações relevantes de OB e FVG.

### Saída esperada
`StructurePayload`

### Regra operacional da Semana 2
A leitura estrutural da Semana 2 deve priorizar estabilidade do contrato, não exaustividade semântica.

---

## Etapa 4 — Serviço de liquidez

### Objetivo
Consolidar o mapa mínimo de liquidez relevante para a análise.

### Responsabilidades
- organizar lado predominante de liquidez;
- manter níveis equivalentes;
- manter máximas e mínimas relevantes;
- preparar alvos de liquidez quando existirem.

### Saída esperada
`LiquidityMapPayload`

### Regra operacional da Semana 2
Não tentar transformar a liquidez em motor autônomo de decisão ainda. A função dela nesta etapa é contextualizar a projeção e o veredito.

---

## Etapa 5 — Serviço de volatilidade e timing

### Objetivo
Traduzir indicadores de volatilidade e timing para uma camada consolidada.

### Responsabilidades
- validar ATR;
- validar RSI;
- validar MACD e histograma;
- validar banda e dispersão;
- registrar `fffd` e `fffd_side`;
- registrar contexto tático adicional.

### Saída esperada
`VolatilityTimingPayload`

### Regra operacional da Semana 2
Esse serviço não deve “mandar” sozinho no veredito. Ele deve atuar como reforço ou moderação das leituras estruturais e direcionais.

---

## Etapa 6 — Serviço de projeção

### Objetivo
Montar a primeira projeção executável do ativo.

### Responsabilidades
- consolidar preço-base;
- definir entrada sugerida;
- registrar entradas alternativas;
- limpar tags;
- registrar stops;
- registrar alvos;
- validar risco-retorno;
- impedir inconsistências triviais.

### Saída esperada
`EntryProjectionPayload`

### Regra operacional da Semana 2
A projeção deve ser tratada como camada operacional mínima, não como promessa de precisão final.

---

## Etapa 7 — Serviço de veredito inicial

### Objetivo
Produzir um veredito técnico inicial a partir da combinação das camadas já processadas.

### Responsabilidades
- ler coerência entre tendência, estrutura, liquidez, timing e projeção;
- evitar veredito forte quando houver conflito estrutural evidente;
- favorecer veredito neutro ou conservador quando a leitura estiver insuficiente;
- registrar racional sintético.

### Saída esperada
- `veredito`
- `notas`
- eventual preenchimento auxiliar de `legacy_score`

### Regra operacional da Semana 2
O veredito inicial não é o veredito final do projeto. Ele é a primeira forma disciplinada de saída integrada.

---

## Etapa 8 — Orquestração final

### Objetivo
Montar o `AssetAnalysisPayload` consolidado.

### Responsabilidades
- receber o input mínimo;
- chamar serviços em ordem correta;
- consolidar os payloads;
- preencher campos finais;
- validar a saída pelo schema oficial.

### Saída esperada
`AssetAnalysisPayload`

---

## Ordem de execução recomendada

A ordem recomendada do orquestrador deve ser:

1. validar input;
2. montar `ReferenceMeta`;
3. processar `TrendBasePayload`;
4. processar `StructurePayload`;
5. processar `LiquidityMapPayload`;
6. processar `VolatilityTimingPayload`;
7. processar `EntryProjectionPayload`;
8. calcular ou consolidar `LegacyScorePayload` quando houver dados suficientes;
9. gerar veredito inicial;
10. montar `AssetAnalysisPayload`;
11. validar saída.

Essa ordem é importante porque evita circularidade entre serviços.

---

## Estrutura técnica sugerida

Uma divisão simples e saudável para a Semana 2 seria:

### Serviços
- `trend_service.py`
- `structure_service.py`
- `liquidity_service.py`
- `volatility_service.py`
- `projection_service.py`
- `verdict_service.py`

### Orquestração
- `analysis_orchestrator.py`

### Testes
- `test_trend_service.py`
- `test_projection_service.py`
- `test_verdict_service.py`
- `test_analysis_orchestrator.py`

---

## Interface funcional sugerida

Uma assinatura mínima aceitável seria algo como:

`analyze_asset(input_data: dict) -> AssetAnalysisPayload`

Ou, se quiser maior disciplina desde já:

`analyze_asset(input_data: AssetInputPayload) -> AssetAnalysisPayload`

## Posição recomendada
Na Semana 2, eu recomendo começar com `dict` validado internamente ou com um input payload mínimo simples, desde que isso não reabra complexidade excessiva.

---

## Falhas esperadas e comportamento desejado

O pipeline não deve apenas funcionar em caso bom. Ele precisa falhar bem.

## Falhas que devem ser tratadas

### 1. Dados obrigatórios ausentes
Exemplo:
- sem ticker;
- sem analysis_date;
- sem referência mínima.

### 2. Inconsistência de datas
Exemplo:
- data de referência posterior à data de análise.

### 3. Valores inválidos
Exemplo:
- preço negativo;
- RSI maior que 100;
- stop igual ao preço-base.

### 4. Conflito analítico forte
Exemplo:
- tendência fortemente bullish e estrutura fortemente bearish sem explicação contextual.

## Comportamento desejado
- falha explícita quando o contrato mínimo for violado;
- saída conservadora quando houver insuficiência analítica;
- nunca inventar campos para completar payload.

---

## Cenários mínimos de teste

A Semana 2 deve terminar com pelo menos estes cenários cobertos.

### Cenário 1 — Bullish simples
- tendência alinhada;
- estrutura favorável;
- liquidez coerente;
- timing aceitável;
- projeção válida.

### Cenário 2 — Bearish simples
- direção oposta ao cenário bullish;
- veredito coerente com leitura estrutural e direcional.

### Cenário 3 — Neutro ou inconclusivo
- sinais mistos;
- veredito conservador.

### Cenário 4 — Input inconsistente
- falha validada.

### Cenário 5 — Input insuficiente
- falha clara ou saída neutra documentada, dependendo da política adotada.

---

## Critérios de aceite do pipeline mínimo

O pipeline mínimo da Semana 2 deve ser aceito apenas se:

1. receber input mínimo e produzir saída válida;
2. gerar `AssetAnalysisPayload` compatível com o schema oficial;
3. falhar claramente em casos inválidos;
4. produzir veredito inicial explicável;
5. passar por testes controlados;
6. manter separação clara entre serviços.

---

## O que a Semana 2 ainda não deve fazer

Mesmo com o pipeline funcionando, esta semana ainda não deve ser confundida com maturidade total.

Ainda não é objetivo desta etapa:
- resolver score v2 maduro;
- fechar regime v1 maduro;
- consolidar adequação semanal madura;
- sofisticar demais a camada de opções;
- produzir decisão final complexa em múltiplas camadas redundantes.

A Semana 2 deve preferir um sistema simples que funciona a um sistema ambicioso que não se sustenta.

---

## Veredito técnico do documento

O pipeline mínimo de análise do ativo é a peça certa para inaugurar a fase funcional do SharkMoura 2.0. Ele cria a ponte entre o que foi documentado na Semana 1 e o que passará a ser executado a partir da Semana 2.

A regra de qualidade aqui é objetiva:

**primeiro consolidar um fluxo mínimo confiável; depois aumentar inteligência e sofisticação.**
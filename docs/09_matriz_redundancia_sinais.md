# Documento 09 — Matriz de Redundância dos Sinais
## Projeto SharkMoura 2.0

### 1. Objetivo do documento

Este documento formaliza a **matriz de redundância dos sinais** do SharkMoura 2.0.

Seu objetivo não é remover sinais por estética nem simplificar o motor por empobrecimento. O objetivo é decidir, com critério técnico, quais sinais:

- devem permanecer como pilares;
- devem permanecer com peso reduzido;
- devem mudar de papel;
- devem ser agrupados;
- não podem mais ser tratados como evidências independentes.

Em outras palavras, este documento existe para impedir que o motor continue transformando **confluência aparente** em **inflação artificial de convicção**.

---

### 2. Posição técnica de abertura

A principal conclusão da Semana 2 é esta:

> O problema do SharkMoura não era excesso de sinais. Era excesso de sinais sem governança de dependência.

Ter muitos sinais não é, por si só, um problema.  
O problema aparece quando:

- vários sinais contam a mesma história;
- sinais irmãos da mesma família pontuam como se fossem independentes;
- níveis operacionais são confundidos com sinais de convicção;
- saídas da projeção passam a ser tratadas como insumos do score;
- timing tático disputa protagonismo com estrutura institucional.

A função desta matriz é criar disciplina nesse ponto.

---

### 3. Critério oficial de redundância

A partir deste documento, cada sinal ou bloco passa a ser classificado dentro de uma das quatro relações abaixo.

#### Tipo A — Independência útil

O sinal mede algo realmente distinto e entrega informação nova ao motor.

Ele pode coexistir com outros sem inflar artificialmente a tese, porque sua contribuição é materialmente diferente.

#### Tipo B — Sobreposição parcial aceitável

O sinal conversa com outro bloco e compartilha parte da narrativa, mas ainda entrega ganho marginal relevante.

Neste caso, a convivência é aceitável, desde que o peso seja controlado.

#### Tipo C — Redundância funcional

O sinal, na prática, reforça uma tese já capturada por outro bloco com ganho marginal baixo.

Ele pode até continuar existindo, mas não deve pontuar como evidência independente.

#### Tipo D — Reclassificação obrigatória

O sinal pode ser útil, mas está ocupando o lugar errado dentro do motor.

Neste caso, o problema não é a existência do sinal.  
O problema é o papel que ele está desempenhando.

---

### 4. Regra oficial de decisão

Para cada item avaliado, a decisão deve cair em uma destas categorias:

- **manter como pilar**
- **manter com peso reduzido**
- **reclassificar como auxiliar**
- **agrupar em bloco único**
- **usar só como racional / explicação**
- **não permitir como score independente**

Essa regra evita decisões vagas como “deixa como está, mas com cuidado”.

A partir daqui, o motor precisa de decisões explícitas.

---

### 5. Análise item a item

### 5.1 `infer_direction(...)` / `ema_stack_up` / `ema_stack_down`

#### O que mede
Mede o viés direcional inicial do ativo a partir da organização das médias móveis.

#### Relação com outros sinais
Possui forte sobreposição com:

- `SMC_Structure`
- `SMC_Last_BOS`

porque todos esses elementos acabam contando, em algum nível, a história de direção / continuidade.

#### Diagnóstico
É útil como ponto de partida, mas perigoso como definidor soberano.

Quando o motor ancora cedo demais em `infer_direction(...)`, ele passa a premiar o resto do fluxo apenas por concordar com essa hipótese inicial.

#### Tipo de relação
**Tipo C — Redundância funcional**

#### Decisão oficial
**Manter com peso reduzido**

#### Novo papel
Passa a ser:

> hipótese direcional inicial

e não mais árbitro final do lado da tese.

---

### 5.2 `SMC_Structure`

#### O que mede
Mede o estado estrutural dominante do ativo.

#### Relação com outros sinais
Conversa com:

- `infer_direction(...)`
- `SMC_Last_BOS`

mas não é equivalente a eles.

#### Diagnóstico
É um dos sinais mais importantes do motor porque não mede apenas inclinação; mede **organização estrutural do preço**.

#### Tipo de relação
**Tipo B — Sobreposição parcial aceitável**

#### Decisão oficial
**Manter como pilar**

#### Novo papel
Passa a ser um dos eixos centrais da:

> Família 2 — Estrutura institucional

---

### 5.3 `SMC_Last_BOS`

#### O que mede
Mede o evento de rompimento estrutural mais recente.

#### Relação com outros sinais
Se relaciona com:

- `SMC_Structure`
- `infer_direction(...)`

mas entrega informação diferente, porque é **evento**, não estado.

#### Diagnóstico
É essencial para diferenciar:
- estrutura consolidada
de
- deslocamento recente.

#### Tipo de relação
**Tipo B — Sobreposição parcial aceitável**

#### Decisão oficial
**Manter como pilar**

#### Novo papel
Passa a ser tratado como:

> bônus estrutural de evento

e não como mera repetição do estado estrutural.

---

### 5.4 `SMC_Last_CHOCH`

#### O que mede
Mede possível mudança de caráter estrutural.

#### Relação com outros sinais
Conversa com:
- `SMC_Structure`
- `SMC_Last_BOS`

mas sua natureza é diferente.

#### Diagnóstico
Não é redundante.  
O problema é que ele estava mal encaixado.

`CHOCH` não deve entrar como “mais um ponto estrutural” de forma neutra. Ele deve alterar a confiança da tese.

#### Tipo de relação
**Tipo D — Reclassificação obrigatória**

#### Decisão oficial
**Manter, mas reclassificar**

#### Novo papel
Passa a operar como:

- penalidade para continuação;
- ou bônus condicional para reversão estruturada.

---

### 5.5 `SMC_PD_Area` e `SMC_PD_Value`

#### O que mede
Ambos medem a posição relativa do preço dentro de um range de referência.

- `PD_Value` entrega leitura contínua
- `PD_Area` entrega leitura discretizada

#### Relação com outros sinais
Conversa com:
- estrutura
- localização
- desequilíbrio
- timing de entrada

#### Diagnóstico
Os dois não podem pontuar como se fossem sinais independentes.

`PD_Area` é, na prática, uma tradução simplificada de `PD_Value`.

#### Tipo de relação
**Tipo C — Redundância funcional**

#### Decisão oficial
- **Manter ambos no payload**
- **Usar `PD_Value` como variável principal**
- **Usar `PD_Area` apenas como rótulo explicativo**

#### Novo papel
- `PD_Value` = variável de score / localização
- `PD_Area` = interpretação legível para racional

---

### 5.6 `SMC_FVG_Side`, `SMC_FVG_Mid`, `SMC_FVG_Size_ATR`

#### O que mede
Mede desequilíbrio estrutural.

- `FVG_Side` = direção do gap
- `FVG_Mid` = ponto médio
- `FVG_Size_ATR` = tamanho relativo normalizado por ATR

#### Relação com outros sinais
Se relaciona com:
- estrutura
- PD
- OB

mas não é equivalente a nenhum deles.

#### Diagnóstico
O FVG é valioso e precisa ser preservado.  
O problema não é redundância literal, mas risco de empilhamento estrutural.

#### Tipo de relação
**Tipo B — Sobreposição parcial aceitável**

#### Decisão oficial
- **Manter como pilar estrutural**
- `FVG_Side` e `FVG_Size_ATR` podem entrar no score
- `FVG_Mid` não deve pontuar sozinho

#### Novo papel
- `FVG_Side` = leitura de alinhamento estrutural
- `FVG_Size_ATR` = qualificação do desequilíbrio
- `FVG_Mid` = nível operacional

---

### 5.7 `SMC_OB_Type` e `SMC_OB_Refine`

#### O que mede
Mede a presença de um proxy de Order Block e o nível refinado associado.

#### Relação com outros sinais
Conversa com:
- FVG
- PD
- BOS
- estrutura geral

#### Diagnóstico
É útil, mas ainda está em estágio de proxy.  
Não deve carregar peso exagerado enquanto não tiver maturidade maior.

#### Tipo de relação
**Tipo B — Sobreposição parcial aceitável**

#### Decisão oficial
- **Manter com peso reduzido**
- `OB_Type` pode contribuir para score estrutural
- `OB_Refine` não deve pontuar sozinho

#### Novo papel
- `OB_Type` = reforço estrutural auxiliar
- `OB_Refine` = nível operacional / racional

---

### 5.8 `eq_high` / `eq_low`

#### O que mede
Mede potenciais equal highs e equal lows, representando liquidez horizontal.

#### Relação com outros sinais
Tem sobreposição funcional com:
- `pdh / pdl`
- `pwh / pwl`

#### Diagnóstico
São úteis, mas não são sinais independentes de convicção.

#### Tipo de relação
**Tipo D — Reclassificação obrigatória**

#### Decisão oficial
**Agrupar em bloco único**

#### Novo papel
Passam a integrar:

> `liquidity_map`

---

### 5.9 `pdh` / `pdl`

#### O que mede
Mede máxima e mínima anteriores.

#### Relação com outros sinais
Sobreposição funcional com:
- `eq_high / eq_low`
- `pwh / pwl`

#### Diagnóstico
São relevantes como níveis, mas não como score independente.

#### Tipo de relação
**Tipo D — Reclassificação obrigatória**

#### Decisão oficial
**Agrupar em bloco único**

#### Novo papel
Passam a integrar:

> `liquidity_map`

---

### 5.10 `pwh` / `pwl`

#### O que mede
Mede máxima e mínima da semana anterior.

#### Relação com outros sinais
Sobreposição funcional com os demais níveis horizontais.

#### Diagnóstico
São muito relevantes para contexto, mas não devem ser tratados como convicção isolada.

#### Tipo de relação
**Tipo D — Reclassificação obrigatória**

#### Decisão oficial
**Agrupar em bloco único e reutilizar na adequação semanal**

#### Novo papel
Passam a integrar:
- `liquidity_map`
- camada de contexto semanal

---

### 5.11 `Liq_Target_1` / `Liq_Target_2` / `Liq_Side`

#### O que mede
Mede hierarquia operacional de alvos de liquidez.

#### Relação com outros sinais
São derivados do próprio mapa de liquidez.

#### Diagnóstico
Não são sinais novos.  
São saídas operacionais do bloco de liquidez.

#### Tipo de relação
**Tipo C — Redundância funcional**

#### Decisão oficial
**Não permitir como score independente**

#### Novo papel
Passam a ser tratados como:

> saídas do `liquidity_map`

---

### 5.12 `atr14`

#### O que mede
Mede amplitude média.

#### Relação com outros sinais
Conversa com:
- `move_cap`
- `BB_bandwidth`
- sizing do FVG

#### Diagnóstico
É um dos pilares reais do motor, porque fornece normalização e noção de deslocamento.

#### Tipo de relação
**Tipo A — Independência útil**

#### Decisão oficial
**Manter como pilar**

#### Novo papel
Núcleo da família de volatilidade e expansão.

---

### 5.13 `move_cap`

#### O que mede
Mede o deslocamento plausível dado o horizonte.

#### Relação com outros sinais
É uma transformação operacional de:
- ATR
- horizonte temporal

#### Diagnóstico
Não é convicção.  
É plausibilidade.

#### Tipo de relação
**Tipo D — Reclassificação obrigatória**

#### Decisão oficial
**Reclassificar para a camada semanal**

#### Novo papel
Passa a ser componente de:

> `weekly_adequacy_layer`

---

### 5.14 `BB_bandwidth`

#### O que mede
Mede compressão e expansão da volatilidade.

#### Relação com outros sinais
Conversa com:
- ATR
- FVG
- timing de expansão

#### Diagnóstico
É útil e suficientemente independente.

#### Tipo de relação
**Tipo A — Independência útil**

#### Decisão oficial
**Manter**

#### Novo papel
Pilar da família de volatilidade e expansão.

---

### 5.15 `BB_percent_b`

#### O que mede
Mede posição relativa do preço dentro das bandas.

#### Relação com outros sinais
Conversa com:
- timing
- esticamento
- `FFFD`

#### Diagnóstico
É útil, mas não deve carregar peso alto.

#### Tipo de relação
**Tipo B — Sobreposição parcial aceitável**

#### Decisão oficial
**Reclassificar como auxiliar**

#### Novo papel
Contexto de timing e exaustão.

---

### 5.16 `FFFD` e confirmação por RSI

#### O que mede
Mede exaustão curta / reentrada tática com filtro de momentum.

#### Relação com outros sinais
Conversa com:
- Bollinger
- RSI
- timing de curtíssimo prazo

#### Diagnóstico
É valioso, mas estava filosoficamente no lugar errado quando tratado como parte do núcleo da tese.

#### Tipo de relação
**Tipo D — Reclassificação obrigatória**

#### Decisão oficial
**Manter e reclassificar**

#### Novo papel
Passa a ser tratado como:

> timing tático

---

### 5.17 `T1` / `T2` / `T3` / `Stop_Inst`

#### O que mede
Mede projeção operacional da tese.

#### Relação com outros sinais
São derivados da leitura do motor, não construtores da leitura.

#### Diagnóstico
Não são sinais de convicção.

#### Tipo de relação
**Tipo D — Reclassificação obrigatória**

#### Decisão oficial
**Retirar do score e da matriz de convicção**

#### Novo papel
Passam a integrar:

> `projection_layer`

---

### 5.18 `Alvo_Semana` / `Faixa_Semana_Alta` / `Faixa_Semana_Baixa`

#### O que mede
Mede tradução semanal da tese.

#### Relação com outros sinais
Conversa com:
- `move_cap`
- liquidez
- contexto semanal
- projeção

#### Diagnóstico
Antes estavam perto demais de `T2` e da camada de projeção.

#### Tipo de relação
**Tipo C — Redundância funcional**, se continuarem colados à projeção

#### Decisão oficial
**Manter, mas emancipar como camada semanal**

#### Novo papel
Passam a integrar:

> `weekly_adequacy_layer`

---

### 6. Consolidação por blocos

### 6.1 Pilares reais

Os sinais que permanecem como pilares reais do motor são:

- `SMC_Structure`
- `SMC_Last_BOS`
- `SMC_Last_CHOCH`
- `SMC_PD_Value`
- `SMC_FVG_Side`
- `SMC_FVG_Size_ATR`
- `atr14`
- `BB_bandwidth`

---

### 6.2 Sinais com papel reduzido

Os sinais que continuam relevantes, mas com peso reduzido ou governado, são:

- `infer_direction(...)`
- `SMC_OB_Type`
- `BB_percent_b`

---

### 6.3 Sinais auxiliares / explicativos

Os sinais que devem existir mais como racional, refinamento ou apoio analítico são:

- `SMC_PD_Area`
- `SMC_FVG_Mid`
- `SMC_OB_Refine`
- `FFFD_note`

---

### 6.4 Blocos agrupados

#### `liquidity_map`

Agrupa:

- `eq_high`
- `eq_low`
- `pdh`
- `pdl`
- `pwh`
- `pwl`
- `Liq_Target_1`
- `Liq_Target_2`
- `Liq_Side`

#### `projection_layer`

Agrupa:

- `price_ref`
- `T1`
- `T2`
- `T3`
- `Stop_Inst`

#### `weekly_adequacy_layer`

Agrupa:

- `move_cap`
- `Alvo_Semana`
- `Faixa_Semana_Alta`
- `Faixa_Semana_Baixa`
- `horizon_bdays`

---

### 7. Decisões oficiais derivadas da matriz

1. Liquidez horizontal deixa de ser coleção de sinais independentes.
2. `PD_Value` passa a ser a variável principal de localização.
3. `infer_direction(...)` perde soberania.
4. `FFFD` vira timing tático.
5. `move_cap` sai do score e passa a ser plausibilidade semanal.
6. `Alvo_Semana` precisa deixar de funcionar como quase-alias de `T2`.
7. Projeção deixa de ser tratada como convicção.

---

### 8. Veredito técnico final

A matriz mostra que o SharkMoura já tem os componentes necessários para um motor forte.

O que faltava não era mais sinal.  
O que faltava era disciplina para:

- separar sinal de contexto;
- separar convicção de plausibilidade;
- separar alvo de evidência;
- impedir que o motor contasse várias vezes a mesma história.

Essa matriz é uma das peças centrais da limpeza arquitetural da Semana 2.

---

### 9. Próximo passo lógico

O próximo passo lógico é o:

**Documento 10 — Classificador de Regime v1**

Porque, depois de saber:

- quais sinais existem;
- quais são pilares;
- quais são auxiliares;
- quais são redundantes;
- quais blocos precisam ser agrupados;

é preciso saber:

> em que ambiente de mercado esses sinais estão operando.
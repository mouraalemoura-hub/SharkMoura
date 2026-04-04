# Documento 08 — Famílias de Sinais
## Projeto SharkMoura 2.0

### 1. Objetivo do documento

Este documento formaliza a organização dos sinais do motor atual do SharkMoura em **famílias funcionais**, com base no material real analisado ao longo da Semana 2.

O objetivo deste documento **não** é definir pesos finais, thresholds definitivos ou o cálculo exato do score. O objetivo é organizar o motor por **papel analítico**, reduzindo ambiguidade e preparando a arquitetura para a fase de especificação executável e implementação.

Ao final deste documento, deve ficar claro:

- quais sinais existem de fato;
- que tipo de informação cada sinal entrega;
- a qual família cada sinal pertence;
- quais famílias são centrais;
- quais famílias são auxiliares;
- quais papéis precisam ser reforçados, rebaixados ou separados.

---

### 2. Posição técnica de abertura

A posição técnica consolidada da Semana 2 é a seguinte:

> O SharkMoura já possui sinais suficientes para sustentar um motor forte, mas ainda estava organizado como um conjunto útil de leituras sem governança arquitetural suficiente.

O problema central do desenho anterior não era falta de inteligência analítica. O problema era a mistura entre:

- tendência;
- estrutura;
- liquidez;
- timing;
- projeção;
- adequação semanal.

Essa mistura fazia com que sinais diferentes fossem tratados como se tivessem o mesmo papel, gerando:

- sobreposição funcional;
- inflação artificial de convicção;
- dificuldade de auditoria;
- dificuldade de explicar por que uma tese parecia forte;
- risco de decisões excessivamente ancoradas em uma primeira hipótese direcional.

A Semana 2 existe justamente para corrigir isso.

---

### 3. Princípio de classificação por papel analítico

A regra de classificação adotada neste documento é simples:

> Cada sinal deve ser agrupado pelo tipo de informação que entrega ao motor, e não pela função do código onde ele aparece.

Esse princípio é importante porque um mesmo helper pode misturar:

- contexto;
- gatilho;
- nível operacional;
- leitura estrutural;
- plausibilidade temporal;
- filtro tático.

A família correta de um sinal depende do seu **papel analítico real**, e não da sua origem no código.

Isso evita um erro muito comum em motores que crescem organicamente: classificar como “indicador principal” algo que, na prática, é apenas um detalhe operacional ou um refinador de entrada.

---

### 4. Observação arquitetural crítica: Camada 0 — Referência Operacional

Fica formalmente registrado que `preco_ref_meta(...)` **não pertence a nenhuma família de sinais**.

Esse bloco pertence à:

## Camada 0 — Referência Operacional

Sua função é definir:

- `price_ref`
- `ref_date`
- `ref_rule`

Ou seja, antes de qualquer leitura estrutural, score, regime ou adequação semanal, o motor precisa saber:

- qual é o preço de referência válido;
- de qual data ele vem;
- sob qual regra esse preço foi aceito.

A função dessa camada é preparar o terreno analítico, e não pontuar ou qualificar a tese.

Essa distinção é importante porque evita misturar:
- qualidade da análise
com
- qualidade do insumo de entrada.

---

### 5. Mapa oficial das famílias de sinais

A arquitetura oficial da Semana 2 reconhece as seguintes famílias:

1. **Família 1 — Tendência-base**
2. **Família 2 — Estrutura institucional**
3. **Família 3 — Liquidez e localização no range**
4. **Família 4 — Volatilidade e expansão**
5. **Família 5 — Timing tático / momentum curto**
6. **Família 6 — Contexto semanal e adequação temporal**

---

### 6. Família 1 — Tendência-base

#### 6.1 Função da família

Responder:

> Qual é o viés direcional inicial do ativo antes da leitura estrutural mais profunda?

#### 6.2 Sinais que pertencem a esta família

- `ema_stack_up`
- `ema_stack_down`
- `infer_direction(...)`

Em sentido complementar, essa família também conversa com:
- `SMC_Structure`, quando a estrutura reforça a inclinação predominante

#### 6.3 Papel correto no novo motor

A tendência-base deve:

- oferecer uma hipótese direcional inicial;
- indicar inclinação predominante;
- servir como ponto de partida do raciocínio;
- ajudar a organizar o lado preliminar da análise.

Ela **não** deve:

- decidir sozinha `COMPRA` ou `VENDA`;
- mandar no score final;
- ter autoridade soberana sobre o bloco estrutural;
- transformar uma leitura inicial em viés obrigatório para o resto do motor.

#### 6.4 Diagnóstico do estado atual

No desenho anterior, `infer_direction(...)` estava simples demais e poderoso demais.  
Ao depender de forma excessiva do empilhamento de EMA, o motor corria o risco de:

- ancorar cedo demais;
- escolher um lado antes da leitura estrutural;
- premiar depois tudo o que apenas confirmasse esse lado.

Isso não significa que a tendência-base seja inútil.  
Significa apenas que ela estava **ocupando mais espaço do que deveria**.

#### 6.5 Decisão oficial da Semana 2

- **Manter** a família.
- **Rebaixar** `infer_direction(...)` de definidor final para **hipótese direcional inicial**.
- Não permitir mais que a tendência-base defina sozinha o lado operacional da tese.

---

### 7. Família 2 — Estrutura institucional

#### 7.1 Função da família

Responder:

> Há estrutura institucional coerente com continuidade, transição, rompimento, desequilíbrio e leitura de valor?

#### 7.2 Sinais que pertencem a esta família

- `SMC_Structure`
- `SMC_Last_BOS`
- `SMC_Last_CHOCH`
- `SMC_PD_Area`
- `SMC_PD_Value`
- `SMC_FVG_Side`
- `SMC_FVG_Mid`
- `SMC_FVG_Size_ATR`
- `SMC_OB_Type`
- `SMC_OB_Refine`

#### 7.3 Papel correto no novo motor

Essa família deve ser o **núcleo analítico central** do SharkMoura 2.0.

Ela deve responder por:

- estado estrutural dominante;
- eventos de rompimento;
- sinais de transição;
- desequilíbrios relevantes;
- localização institucional do preço;
- regiões de interesse estrutural.

#### 7.4 Diagnóstico do estado atual

Este é o bloco mais rico do motor e, ao mesmo tempo, o mais exposto ao risco de:

- empilhamento confirmatório;
- soma ingênua de sinais irmãos;
- excesso de confluência artificial.

Mesmo assim, ele é o principal diferencial do SharkMoura.

A leitura consolidada da Semana 2 é esta:

> o bloco estrutural institucional é o verdadeiro coração do motor.

#### 7.5 Decisão oficial da Semana 2

- **Manter integralmente** a família.
- Tratar `Structure` como **estado**.
- Tratar `BOS` como **evento**.
- Tratar `CHOCH` como **sinal de transição**, e não como ponto neutro.
- Tratar `PD_Value` como variável principal de localização.
- Tratar `FVG` e `OB` com governança interna, evitando soma ingênua.

---

### 8. Família 3 — Liquidez e localização no range

#### 8.1 Função da família

Responder:

> Onde estão os pools de liquidez e como o preço está posicionado em relação a eles?

#### 8.2 Sinais que pertencem a esta família

- `eq_high`
- `eq_low`
- `pdh`
- `pdl`
- `pwh`
- `pwl`
- `Liq_Target_1`
- `Liq_Target_2`
- `Liq_Side`

Em leitura contínua, esta família também conversa com:
- `PD_Value`, quando usado como noção de posição relativa dentro do range

#### 8.3 Papel correto no novo motor

Essa família deve servir para:

- mapear liquidez horizontal;
- organizar alvos naturais;
- medir espaço útil;
- enriquecer o racional institucional;
- apoiar a adequação semanal.

Ela **não** deve:

- definir direção sozinha;
- funcionar como coleção de mini-sinais independentes;
- inflar score apenas porque existem muitos níveis no entorno do preço.

#### 8.4 Diagnóstico do estado atual

O principal problema aqui era conceitual:

`PDH`, `PDL`, `PWH`, `PWL`, `EQH`, `EQL` não são seis sinais de convicção.  
Eles são partes de um mesmo mapa de liquidez.

Tratá-los como sinais independentes gera:

- duplicidade narrativa;
- inflação de score;
- falsa sensação de confluência.

#### 8.5 Decisão oficial da Semana 2

- **Manter** todos os níveis.
- **Agrupar** tudo em um único bloco lógico:

## `liquidity_map`

- Não permitir score independente para cada nível isolado.

---

### 9. Família 4 — Volatilidade e expansão

#### 9.1 Função da família

Responder:

> Há amplitude suficiente para que a tese respire e se desenvolva?

#### 9.2 Sinais que pertencem a esta família

- `atr14`
- `BB_bandwidth`
- `BB_percent_b`
- `SMC_FVG_Size_ATR`

Em conexão com a camada semanal:
- `move_cap`

#### 9.3 Papel correto no novo motor

Essa família deve:

- medir amplitude;
- qualificar expansão;
- evitar setups mortos;
- penalizar teses sem deslocamento plausível;
- ajudar a separar contexto de compressão, expansão e esticamento.

#### 9.4 Diagnóstico do estado atual

A volatilidade já existia no motor, mas estava espalhada entre vários pontos do fluxo analítico, sem identidade formal.

Isso fazia com que:

- parte da amplitude ficasse no ATR;
- parte do contexto ficasse no Bollinger;
- parte da leitura de deslocamento ficasse no FVG;
- parte da plausibilidade temporal ficasse escondida no `move_cap`.

#### 9.5 Decisão oficial da Semana 2

- **Formalizar** a família como bloco próprio.
- Usar ATR e bandwidth como pilares centrais.
- Tratar `move_cap` mais como plausibilidade temporal do que como convicção.

---

### 10. Família 5 — Timing tático / momentum curto

#### 10.1 Função da família

Responder:

> O momento imediato favorece entrar agora ou recomenda cautela?

#### 10.2 Sinais que pertencem a esta família

- `FFFD`
- `FFFD_side`
- `FFFD_note`
- confirmação por RSI
- contexto de Bollinger de curtíssimo prazo

#### 10.3 Papel correto no novo motor

Essa família deve:

- melhorar timing de entrada;
- penalizar entradas tardias;
- identificar exaustão curta;
- refinar execução.

Ela **não** deve:

- construir a tese-base;
- inverter sozinha a leitura estrutural forte;
- disputar protagonismo com o bloco institucional.

#### 10.4 Diagnóstico do estado atual

O `FFFD` é útil, mas estava em posição conceitualmente errada quando interpretado como componente estrutural forte.

Ele não é um problema.  
O problema era o lugar que ele ocupava na hierarquia analítica.

#### 10.5 Decisão oficial da Semana 2

- **Manter** `FFFD`.
- Reclassificá-lo formalmente como **timing tático**.
- Usá-lo como bônus moderado ou penalidade de entrada.
- Não permitir que ele defina a tese-base.

---

### 11. Família 6 — Contexto semanal e adequação temporal

#### 11.1 Função da família

Responder:

> A tese cabe dentro da janela operacional do produto semanal?

#### 11.2 Sinais e blocos que pertencem a esta família

- `weekly_context_from_daily(...)`
- `PWH`
- `PWL`
- `PWC`
- `Faixa_Semana_Alta`
- `Faixa_Semana_Baixa`
- `Alvo_Semana`
- `horizon_bdays`
- `move_cap`

#### 11.3 Papel correto no novo motor

Essa família deve:

- medir compatibilidade com a semana;
- avaliar espaço útil;
- avaliar tempo útil;
- separar tese boa de tese boa para o produto semanal;
- evitar que uma tese forte, porém tardia, seja tratada como excelente.

#### 11.4 Diagnóstico do estado atual

O contexto semanal já existia de forma implícita, mas ainda estava misturado com:

- projeção operacional;
- alvo técnico;
- cálculo de convicção;
- leitura de deslocamento.

Ou seja, o motor ainda não separava com clareza:
- qualidade da tese
de
- compatibilidade com a janela semanal.

#### 11.5 Decisão oficial da Semana 2

- **Emancipar** essa camada como família própria.
- Garantir que `Alvo_Semana` deixe de ser um quase-alias de `T2`.
- Tornar a adequação semanal uma camada formal posterior ao score e ao regime.

---

### 12. Resumo executivo por família

- **Família 1 — Tendência-base:** necessária, mas simples demais; será mantida com papel rebaixado.
- **Família 2 — Estrutura institucional:** núcleo diferencial do motor; será preservada como centro da arquitetura.
- **Família 3 — Liquidez e localização:** rica e útil; será agrupada em `liquidity_map`.
- **Família 4 — Volatilidade e expansão:** importante e antes dispersa; será formalizada.
- **Família 5 — Timing tático:** útil, mas não soberana; ficará como ajuste de execução.
- **Família 6 — Contexto semanal:** central para o produto; passará a ser camada autônoma.

---

### 13. Decisões oficiais derivadas do documento

1. `infer_direction(...)` deixa de ser decisor soberano.
2. O bloco estrutural institucional passa a ser o núcleo analítico do motor.
3. A liquidez horizontal passa a ser tratada como `liquidity_map`.
4. `FFFD` passa a ser timing tático.
5. O contexto semanal passa a ser camada de adequação, e não simples extensão da projeção.
6. A volatilidade passa a ser reconhecida como família formal.

---

### 14. Veredito técnico final

O motor do SharkMoura **não precisava de mais sinais antes de precisar de mais ordem**.

A Semana 2 deixa claro que o verdadeiro avanço do projeto não é empilhar indicadores, mas sim:

- separar papéis;
- disciplinar dependências;
- impedir inflação de confluência;
- preparar uma arquitetura executável.

---

### 15. Próximo passo lógico

O próximo passo lógico é o:

**Documento 09 — Matriz de Redundância dos Sinais**

Porque, uma vez organizadas as famílias, o motor precisa deixar explícito:

- o que é pilar;
- o que é auxiliar;
- o que é redundante;
- o que precisa mudar de papel.
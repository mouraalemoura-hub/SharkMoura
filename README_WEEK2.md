# README — Semana 2 do Projeto SharkMoura 2.0

## 1. Propósito da Semana 2

A Semana 2 teve como objetivo **reorganizar o núcleo analítico do SharkMoura 2.0**.

Se a Semana 1 foi a etapa de leitura, inventário e compreensão do legado, a Semana 2 foi a etapa de **reestruturação arquitetural**. O foco deixou de ser apenas entender o que o motor já fazia e passou a ser definir, com clareza técnica, **como ele deve funcionar daqui para frente**.

Em termos práticos, a Semana 2 foi a fase em que o projeto passou a:

- separar sinais por função analítica;
- reduzir redundância entre componentes;
- definir o papel correto de cada bloco do motor;
- formalizar uma camada de regime;
- formalizar um score do ativo em blocos;
- formalizar uma camada posterior de adequação semanal;
- preparar a transição da arquitetura conceitual para a futura implementação operacional.

O ganho central desta semana não foi adicionar mais indicadores.

O ganho central foi:

> transformar um conjunto útil de leituras e heurísticas em uma arquitetura analítica coerente, explicável e preparada para evolução.

---

## 2. O que a Semana 2 mudou no projeto

A Semana 2 introduziu mudanças estruturais profundas no modo como o motor SharkMoura 2.0 deve ser entendido.

### 2.1 Sinais deixam de ser uma lista solta

Antes, o motor podia ser interpretado como um conjunto de sinais e confirmações que, somados, formavam uma tese.

Após a Semana 2, isso deixa de ser aceitável como leitura arquitetural.

Os sinais passam a ser organizados em **famílias analíticas**, cada uma com função própria:

1. Tendência-base  
2. Estrutura institucional  
3. Liquidez e localização no range  
4. Volatilidade e expansão  
5. Timing tático / momentum curto  
6. Contexto semanal e adequação temporal  

Essa reorganização corrige um problema importante: sinais de natureza diferente não podem mais ser tratados como se todos fossem equivalentes.

### 2.2 O bloco estrutural passa a ser o coração do motor

Uma das decisões mais importantes da Semana 2 foi reconhecer que o verdadeiro diferencial do SharkMoura está no bloco de leitura institucional.

Isso inclui elementos como:

- `SMC_Structure`
- `BOS`
- `CHOCH`
- `PD_Value`
- `FVG`
- `OB`

A partir daqui, o motor passa a ser organizado com base na ideia de que:

> a estrutura institucional é o núcleo da tese, e não apenas um complemento da direção inicial.

### 2.3 `infer_direction(...)` perde soberania

A função `infer_direction(...)`, antes muito próxima do papel de decisora primária do lado do setup, foi rebaixada para o papel correto:

> hipótese direcional inicial

Isso significa que o motor não deve mais escolher cedo demais um lado e depois premiar tudo que apenas confirma essa primeira inclinação.

Essa decisão reduz:

- viés de confirmação;
- dependência excessiva de EMA stack;
- sobrepeso indevido da leitura de tendência-base.

### 2.4 Liquidez horizontal vira bloco único

Outro ganho importante da Semana 2 foi a consolidação da liquidez horizontal em um agrupamento formal:

## `liquidity_map`

Esse bloco reúne elementos como:

- `eq_high`
- `eq_low`
- `pdh`
- `pdl`
- `pwh`
- `pwl`
- `Liq_Target_1`
- `Liq_Target_2`
- `Liq_Side`

O objetivo dessa mudança é impedir que vários níveis horizontais sejam tratados como se fossem vários sinais independentes de convicção.

Eles não são.

Eles são partes de um único mapa de liquidez e, por isso, devem ser governados como bloco único.

### 2.5 `FFFD` vira timing tático

A Semana 2 também corrigiu o papel do `FFFD`.

Ele deixa de ser tratado como evidência estrutural central e passa a ser entendido como:

> mecanismo de timing tático / exaustão curta

Na prática, isso significa que o `FFFD` pode:

- melhorar o timing de entrada;
- penalizar entradas ruins;
- sinalizar exaustão local;

mas não pode:

- construir a tese-base sozinho;
- inverter a leitura estrutural forte;
- competir com o bloco institucional.

### 2.6 O motor passa a ter regime formal

A Semana 2 cria uma camada explícita de **classificação de regime**.

Isso é importante porque o motor deixa de olhar apenas para “se está bom” e passa também a perguntar:

> em que tipo de ambiente esta tese está operando?

Os regimes definidos foram:

- `TENDENCIA_ALTA`
- `TENDENCIA_BAIXA`
- `LATERAL_ESTRUTURADA`
- `TRANSICAO`
- `EXPANSAO_DIRECIONAL`
- `EXAUSTAO_OU_ESTICAMENTO`

Essa camada ajuda a impedir que o sistema trate da mesma forma:

- um ativo forte em ambiente limpo;
- um ativo forte em ambiente esticado;
- um ativo aparentemente forte em ambiente de transição.

### 2.7 O Score do Ativo v2 deixa de ser soma ingênua

A Semana 2 também formaliza um novo modelo de score para o ativo.

O **Score do Ativo v2** passa a ser estruturado em cinco blocos:

1. Tendência-base  
2. Estrutura institucional  
3. Volatilidade e expansão  
4. Localização e espaço  
5. Timing tático  

Com isso, o score deixa de ser apenas uma agregação linear de confirmações e passa a se comportar como um sistema com:

- blocos;
- pesos conceituais;
- penalidades;
- teto por contexto;
- interpretação mais explicável.

### 2.8 A camada semanal deixa de contaminar a tese-base

Uma das mudanças mais importantes da Semana 2 foi a criação da camada de:

## Adequação ao Horizonte Semanal

Essa camada existe para responder:

> a tese é boa para o ativo, mas ela é boa para o produto semanal?

Esse ponto é central porque o SharkMoura não é apenas um motor de leitura de ativo. Ele é um sistema que precisa avaliar se a tese cabe dentro de uma janela semanal específica.

A partir desta semana, isso fica formalmente separado.

---

## 3. Arquivos gerados na Semana 2

A Semana 2 é composta pelos seguintes arquivos principais:

- `docs/00_indice_arquitetura_sharkmoura_v2.md`
- `docs/08_familias_de_sinais.md`
- `docs/09_matriz_redundancia_sinais.md`
- `docs/10_classificador_regime_v1.md`
- `docs/11_score_ativo_v2.md`
- `docs/12_adequacao_horizonte_semanal.md`
- `docs/13_fechamento_oficial_semana_2.md`
- `README_WEEK2.md`

Esses documentos formam o pacote arquitetural oficial da Semana 2.

---

## 4. Como a Semana 2 reorganiza o motor

Ao final desta etapa, o SharkMoura 2.0 passa a ser entendido em camadas.

### Camada 0 — Referência Operacional

Essa camada define qual é o preço válido para iniciar a análise.

Seu elemento central é:

- `preco_ref_meta(...)`

Ela decide:

- `price_ref`
- `ref_date`
- `ref_rule`

Essa decisão é anterior ao score, ao regime e à adequação semanal.

### Camada 1 — Tese-base do ativo

Essa camada responde:

- existe uma tese boa?
- quão forte ela é?
- em que regime ela opera?

Elementos centrais:
- famílias de sinais
- classificador de regime
- score do ativo v2

### Camada 2 — Adequação ao Horizonte Semanal

Essa camada responde:

- há tempo útil?
- há espaço útil?
- o deslocamento é plausível?
- o setup está cedo, maduro ou tarde demais?

### Camada 3 — Operacionalização em derivativos

Essa camada fica responsável por traduzir a tese adequada em decisão operacional de mercado de opções:

- strike
- vencimento
- estrutura
- payoff
- montagem

### Camada 4 — Linguagem comercial

Essa é a camada que eventualmente transforma a leitura técnica em saída comunicável, como:

- `DIAMANTE`
- `OURO`
- `PRATA`

Essa separação em camadas foi um dos maiores ganhos da Semana 2.

---

## 5. O que a Semana 2 não tentou resolver

A Semana 2 não tinha como objetivo resolver tudo.  
E isso foi metodologicamente correto.

Ela não tentou fechar:

- calibração estatística final da probabilidade;
- engine final de strike e vencimento;
- qualidade de liquidez da cadeia de opções;
- lógica econômica final de payoff;
- implementação produtiva completa;
- validação quantitativa extensiva.

Esses pontos pertencem à sequência natural do projeto.

A função da Semana 2 foi outra:

> limpar, reorganizar e formalizar a arquitetura do motor.

---

## 6. Como a Semana 2 se conecta à Semana 3

A Semana 3 deve herdar da Semana 2 uma arquitetura mais limpa e começar a transformá-la em especificação operacional.

Em termos práticos, a Semana 2 entrega para a Semana 3:

- famílias formalizadas;
- redundâncias mapeadas;
- regime definido;
- score v2 definido;
- adequação semanal definida;
- fechamento oficial da etapa analítica.

Ou seja:

> a Semana 2 fecha o desenho conceitual e abre o caminho para a materialização operacional.

---

## 7. Markdown como fonte viva e PDF como congelamento posterior

A política documental recomendada para o SharkMoura 2.0 é a seguinte:

### Markdown como fonte viva
Os arquivos `.md` devem ser tratados como:
- base principal de trabalho;
- material editável;
- documento versionável;
- referência para implementação.

### PDF como congelamento posterior
Os arquivos `.pdf` devem ser tratados como:
- fechamento oficial de semana;
- consolidação executiva;
- documento formal de apresentação;
- versão congelada de marcos.

Isso permite ao projeto preservar duas qualidades ao mesmo tempo:

- flexibilidade de evolução;
- governança documental.

---

## 8. Leitura recomendada

Para entender a Semana 2 na ordem lógica correta, a leitura recomendada é:

1. `docs/00_indice_arquitetura_sharkmoura_v2.md`
2. `README_WEEK2.md`
3. `docs/08_familias_de_sinais.md`
4. `docs/09_matriz_redundancia_sinais.md`
5. `docs/10_classificador_regime_v1.md`
6. `docs/11_score_ativo_v2.md`
7. `docs/12_adequacao_horizonte_semanal.md`
8. `docs/13_fechamento_oficial_semana_2.md`

---

## 9. Veredito executivo da Semana 2

A Semana 2 foi a etapa em que o SharkMoura deixou de ser apenas um conjunto promissor de leituras e passou a ter uma arquitetura analítica séria.

Ela não encerra o projeto.  
Ela não encerra a modelagem.  
Ela não implementa tudo.

Mas ela faz o que era mais importante neste momento:

> colocar ordem conceitual no coração do sistema.

Esse é o valor real desta semana.

---

## 10. Encerramento

A Semana 2 está formalmente posicionada como a etapa de:

- reorganização analítica;
- consolidação arquitetural;
- separação de camadas;
- preparação para implementação.

O próximo passo natural do projeto é a abertura da **Semana 3**, voltada à materialização operacional da arquitetura definida aqui.
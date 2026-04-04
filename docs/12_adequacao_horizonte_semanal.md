# Documento 12 — Adequação ao Horizonte Semanal
## Projeto SharkMoura 2.0

### 1. Objetivo do documento

Este documento formaliza a camada de **Adequação ao Horizonte Semanal** do SharkMoura 2.0.

O objetivo dessa camada é responder, com clareza técnica:

> uma tese que parece boa para o ativo também é boa para o produto semanal?

Essa pergunta é central para o projeto porque o SharkMoura não existe apenas para reconhecer ativos com boa estrutura. Ele existe para reconhecer ativos cuja tese seja **utilizável dentro de uma janela semanal específica**, com tempo, espaço e plausibilidade suficientes.

A camada semanal não substitui o score, não substitui o regime e não substitui a futura camada de opções.  
Ela existe para responder uma pergunta posterior:

> depois de saber que a tese é boa, ela ainda cabe dentro da semana?

---

### 2. Posição técnica de abertura

A principal correção conceitual deste documento é a seguinte:

> o horizonte semanal não pode contaminar a tese-base do ativo.

Esse foi um dos maiores riscos do desenho anterior.

Quando o motor mistura:
- qualidade da tese,
- timing tático,
- alvo projetado,
- urgência da semana,
- e expectativa de sexta-feira,

ele perde clareza.

A arquitetura correta é separar:

1. **qualidade da tese-base**
2. **regime do ambiente**
3. **adequação ao horizonte semanal**

Essa separação evita um erro caro:

- estar certo sobre o ativo
- e errado sobre o produto

Ou seja:
- a tese pode ser boa,
- mas o setup pode ser ruim para a semana.

---

### 3. Função oficial da camada de adequação semanal

A camada de adequação semanal deve responder perguntas como:

- ainda há tempo útil?
- ainda há espaço útil?
- o alvo semanal é plausível?
- a tese está cedo, madura ou tardia dentro da semana?
- o contexto semanal favorece ou atrapalha a operação?

Ela **não** deve responder:

- se a estrutura institucional é boa;
- se a tese é forte no médio prazo;
- qual strike deve ser usado;
- qual opção está mais barata;
- se o payoff final é bom;
- se o ativo merece selo comercial premium.

Essas perguntas pertencem a outras camadas do projeto.

---

### 4. O que a adequação semanal mede

A camada mede:

- tempo restante útil;
- espaço útil até liquidez ou alvo;
- plausibilidade do deslocamento;
- maturidade da tese dentro da semana;
- compatibilidade entre a urgência do produto e o estado do ativo.

Em termos conceituais, ela mede:

> a capacidade de a tese-base gerar oportunidade utilizável dentro do ciclo semanal.

---

### 5. O que a adequação semanal não mede

Ela **não** mede diretamente:

- qualidade estrutural do ativo;
- probabilidade calibrada final;
- liquidez da cadeia de opções;
- strike ideal;
- prêmio;
- payoff;
- seleção final de estrutura;
- linguagem comercial em definitivo.

Se esses elementos forem misturados nesta camada, a arquitetura deixa de ser auditável.

---

### 6. Princípio central da adequação semanal

O princípio central desta camada é:

> o produto semanal não deve premiar apenas a direção correta; deve premiar a direção correta com tempo útil e espaço útil.

Essa frase resume por que esta camada existe.

Um ativo pode estar:

- alinhado estruturalmente;
- com score alto;
- em regime favorável;

e ainda assim ser inadequado para a semana porque:

- já andou demais;
- tem pouco espaço até liquidez;
- exige deslocamento improvável;
- entrou tarde demais no ciclo semanal;
- já está esticado demais para a entrada.

É exatamente esse tipo de erro que esta camada precisa impedir.

---

### 7. Relação oficial entre Score, Regime e Adequação

A sequência lógica correta do motor é:

1. **Camada 0 — Referência Operacional**
2. **Score do Ativo v2**
3. **Classificador de Regime v1**
4. **Adequação ao Horizonte Semanal**
5. **Camada posterior de opções**
6. **Linguagem comercial**

Isso significa que a camada semanal:

- não constrói a tese-base;
- não disputa espaço com o score;
- não reclassifica sozinha o regime;
- opera **depois** do score e do regime.

Em termos simples:

> primeiro o sistema pergunta se a tese é boa;  
> depois pergunta em que ambiente ela existe;  
> depois pergunta se ela cabe na semana.

---

### 8. Fontes de informação da adequação semanal

A camada deve consumir informações vindas de múltiplos blocos.

#### 8.1 Contexto temporal
- `horizon_bdays`
- data de referência
- estágio da semana
- proximidade da sexta-feira

#### 8.2 Contexto semanal
- `PWH`
- `PWL`
- `PWC`
- `Faixa_Semana_Alta`
- `Faixa_Semana_Baixa`
- `Alvo_Semana`

#### 8.3 Projeção operacional
- `price_ref`
- `T1`
- `T2`
- `T3`
- `Stop_Inst`

#### 8.4 Volatilidade e plausibilidade
- `atr14`
- `move_cap`
- `BB_bandwidth`

#### 8.5 Liquidez e espaço
- `liquidity_map`
- `Liq_Target_1`
- `Liq_Target_2`
- `PD_Value`

#### 8.6 Base da tese
- `score_final_ativo`
- `regime_principal`
- `regime_flags`

---

### 9. Perguntas que a camada deve responder

A camada de adequação semanal precisa responder, no mínimo, as seguintes perguntas:

1. A tese ainda tem tempo?
2. A tese ainda tem espaço?
3. O alvo semanal é plausível?
4. O setup está cedo, maduro ou tarde?
5. O contexto semanal ajuda ou atrapalha?
6. O produto está exigindo urgência demais para um ativo que ainda não confirmou?
7. O ativo já entregou boa parte da perna e agora restou pouco valor operacional?

Essas perguntas dão forma operacional à adequação.

---

### 10. Estrutura oficial da camada

A camada de adequação semanal será composta por **quatro blocos oficiais**.

1. **Tempo restante**
2. **Espaço útil**
3. **Plausibilidade do deslocamento**
4. **Maturidade da tese na semana**

---

### 11. Bloco A — Tempo restante

#### Função
Responder:

> ainda existe tempo útil suficiente até sexta-feira?

#### Entradas principais
- `horizon_bdays`
- data de referência
- estágio da semana

#### Interpretação
Tempo não é apenas número de dias.  
É a relação entre:

- dias disponíveis;
- urgência do produto;
- deslocamento ainda necessário;
- estado atual da tese.

#### Leitura conceitual
Exemplos:

- segunda-feira com tese limpa → tempo favorável;
- quinta-feira com alvo distante → tempo hostil;
- sexta cedo com setup curto e espaço razoável → caso específico, não padrão geral.

#### Status sugeridos
- `TEMPO_FAVORAVEL`
- `TEMPO_NEUTRO`
- `TEMPO_APERTADO`
- `TEMPO_INSUFICIENTE`

---

### 12. Bloco B — Espaço útil

#### Função
Responder:

> ainda existe espaço operacional até a próxima liquidez ou alvo relevante?

#### Entradas principais
- `price_ref`
- `Liq_Target_1`
- `Liq_Target_2`
- `PWH`
- `PWL`
- `PDH`
- `PDL`
- `EQH`
- `EQL`
- `PD_Value`

#### Interpretação
Uma tese boa sem espaço útil é uma tese pior do que parece.

Mesmo que a direção esteja certa, se o preço já estiver colado na liquidez relevante, o valor operacional diminui.

#### Status sugeridos
- `ESPACO_ABUNDANTE`
- `ESPACO_SAUDAVEL`
- `ESPACO_CURTO`
- `ESPACO_CRITICO`

---

### 13. Bloco C — Plausibilidade do deslocamento

#### Função
Responder:

> o deslocamento que a tese ainda precisa fazer cabe dentro da amplitude plausível da semana?

#### Entradas principais
- `move_cap`
- `atr14`
- `Alvo_Semana`
- distância até o alvo
- `BB_bandwidth`
- regime

#### Interpretação
Aqui o motor precisa fazer uma pergunta objetiva:

> não importa apenas se o ativo pode andar; importa se ele pode andar o suficiente dentro do tempo que resta.

Essa camada é especialmente importante para evitar setups que parecem ótimos no papel, mas exigem deslocamento improvável para o produto semanal.

#### Status sugeridos
- `DESLOCAMENTO_PLAUSIVEL`
- `DESLOCAMENTO_EXIGENTE`
- `DESLOCAMENTO_IMPROVAVEL`

---

### 14. Bloco D — Maturidade da tese na semana

#### Função
Responder:

> o setup está no ponto certo da semana ou já está adiantado, tardio ou exaurido?

#### Entradas principais
- `PD_Value`
- proximidade de liquidez
- `FFFD`
- `BB_percent_b`
- estágio da semana
- relação entre projeção e posição atual

#### Interpretação
Uma tese pode estar:

- cedo demais;
- bem posicionada;
- tarde demais;
- exaurida.

Esse bloco existe para impedir que o motor trate como excelente uma tese que já andou demais e deixou pouco valor operacional.

#### Status sugeridos
- `MATURIDADE_IDEAL`
- `MATURIDADE_NEUTRA`
- `MATURIDADE_TARDIA`
- `MATURIDADE_EXAURIDA`

---

### 15. Classificação oficial da adequação semanal

A camada semanal deve devolver um status principal entre estes quatro:

#### `ADEQUADA`
A tese tem tempo, espaço e plausibilidade suficientes para o produto semanal.

#### `ADEQUADA_COM_RESSALVAS`
A tese é utilizável, mas com limitações importantes.

#### `FRACA_PARA_SEMANA`
A tese pode até ser boa no ativo, mas está ruim para o horizonte semanal.

#### `INADEQUADA`
A tese não deve ser promovida como oportunidade semanal.

---

### 16. Diferença entre tese boa e tese adequada

Essa distinção precisa ficar cristalina.

#### Tese boa
É uma tese com:
- score bom;
- regime coerente;
- estrutura favorável.

#### Tese adequada
É uma tese boa que também:
- cabe na semana;
- tem tempo;
- tem espaço;
- tem plausibilidade;
- não está tarde demais.

Em forma de regra:

> toda tese adequada precisa ser boa;  
> nem toda tese boa é adequada.

Essa é uma das teses centrais de toda a arquitetura da Semana 2.

---

### 17. Penalidades oficiais

A camada semanal deve aplicar penalidades claras.

As principais são:

- tempo curto;
- alvo distante demais;
- espaço já consumido;
- tese tardia;
- exaustão local;
- faixa semanal apertada;
- regime incompatível com a urgência do produto;
- proximidade excessiva de liquidez;
- dependência de deslocamento fora do plausível.

Sem essas penalidades, a camada semanal perde utilidade.

---

### 18. Bônus possíveis

A camada também pode reconhecer cenários favoráveis.

Exemplos de bônus:

- espaço limpo até a próxima liquidez;
- deslocamento plausível e compatível com a amplitude;
- início de semana com tese limpa;
- regime de expansão direcional;
- maturidade ideal;
- ausência de esticamento relevante.

Esses bônus não substituem a tese-base, mas aumentam a utilidade operacional.

---

### 19. Interação com o regime

O regime deve influenciar a adequação semanal, mas não pode ser confundido com ela.

Exemplos:

- regime bom + semana ruim → tese boa, adequação reduzida;
- regime ruim + semana curta → inadequação severa;
- regime de expansão + início de semana + espaço amplo → adequação forte.

Ou seja:

> o regime modula a camada semanal, mas não substitui os testes de tempo, espaço e plausibilidade.

---

### 20. Interação com o score

O score do ativo funciona como pré-requisito.

Se o score é fraco, não faz sentido tentar salvar a tese via adequação semanal.

Se o score é bom, a camada semanal decide se essa boa tese pode ser promovida como oportunidade compatível com o produto.

Se o score é excelente, ainda assim a tese pode ser inadequada para a semana.

Essa é justamente a utilidade desta camada.

---

### 21. Relação com `Alvo_Semana`

`Alvo_Semana` deixa de ser tratado como quase-alias de `T2`.

Ele passa a ser entendido como:

> alvo plausível e útil para o produto semanal

Isso significa que `Alvo_Semana` deve nascer da combinação entre:

- tese-base;
- contexto semanal;
- espaço disponível;
- `move_cap`;
- regime;
- estágio da semana.

Essa decisão é importante porque devolve autonomia real à camada semanal.

---

### 22. Saída oficial esperada

A camada de adequação semanal deve devolver, no mínimo:

- `adequacao_semanal_status`
- `adequacao_semanal_score`
- `tempo_status`
- `espaco_status`
- `deslocamento_status`
- `maturidade_status`
- `motivos_positivos`
- `motivos_negativos`
- `alvo_semanal_plausivel`
- `racional_adequacao`

Isso torna a camada utilizável, explicável e auditável.

---

### 23. Relação com a linguagem comercial

`DIAMANTE`, `OURO` e `PRATA` não podem ignorar a adequação semanal.

Uma tese com:

- score alto;
- regime bom;

ainda pode ser:

- tardia;
- esticada;
- sem espaço;
- pouco plausível para a semana.

Se isso acontecer, a linguagem comercial precisa refletir essa limitação.

Caso contrário, o sistema estará promovendo como premium algo que já chegou tarde.

---

### 24. O que não fazer

Este documento também define o que o motor **não deve fazer**.

- não transformar a adequação semanal em duplicata do score;
- não usar apenas “dias restantes” como critério;
- não usar apenas `move_cap` como sentença final;
- não deixar `Alvo_Semana` continuar colado à projeção simples;
- não usar a camada semanal para salvar tese ruim;
- não permitir que timing tático de curtíssimo prazo redefina sozinho a adequação geral.

---

### 25. Decisões oficiais derivadas do documento

1. Fica formalmente criada a camada de Adequação ao Horizonte Semanal.
2. Essa camada será posterior ao score e ao regime.
3. A camada será composta por quatro blocos oficiais.
4. `Alvo_Semana` deixa de ser quase equivalente a `T2`.
5. Tese boa poderá ser rebaixada se for ruim para a semana.
6. A linguagem comercial futura deverá respeitar adequação semanal.

---

### 26. Veredito técnico final

Este documento é a peça que separa definitivamente:

- tese boa para o ativo
de
- tese boa para o produto semanal.

Essa separação é uma das correções mais importantes do SharkMoura 2.0.

Ela impede um dos erros mais caros desse tipo de sistema:

> estar certo sobre o ativo e errado sobre o produto.

---

### 27. Próximo passo lógico

O próximo passo lógico é o:

**Documento 13 — Fechamento Oficial da Semana 2**

Porque, com:

- famílias formalizadas;
- redundâncias tratadas;
- regime definido;
- score formalizado;
- adequação semanal formalizada;

o projeto já tem base para consolidar a semana e abrir a transição para a materialização operacional da Semana 3.
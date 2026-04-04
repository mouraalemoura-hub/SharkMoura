# Documento 11 — Score do Ativo v2
## Projeto SharkMoura 2.0

### 1. Objetivo do documento

Este documento formaliza o **Score do Ativo v2** do SharkMoura 2.0.

O objetivo do score não é decidir sozinho:

- qual estrutura de opção montar;
- qual strike escolher;
- qual payoff aceitar;
- qual rótulo comercial exibir;
- se a tese cabe ou não até sexta-feira.

O objetivo do score é responder, de forma técnica e explicável:

> quão forte, limpa e operacionalmente coerente é a tese-base do ativo, antes da camada semanal e antes da camada específica de derivativos?

Essa distinção é central para a nova arquitetura.

O SharkMoura precisa separar com disciplina:

- **qualidade da tese-base do ativo**
- **regime do ambiente**
- **adequação ao horizonte semanal**
- **operacionalização em opções**
- **linguagem comercial final**

O Score do Ativo v2 existe para cuidar apenas da primeira dessas tarefas.

---

### 2. Posição técnica de abertura

A principal correção introduzida neste documento é a seguinte:

> o score do motor não pode continuar se comportando como uma soma ingênua de confluências.

No desenho anterior, havia um risco recorrente de o sistema parecer mais inteligente do que realmente era porque somava:

- sinais estruturalmente parecidos;
- leituras derivadas umas das outras;
- proxies de mesmo significado;
- confirmações de timing como se fossem tese;
- níveis operacionais como se fossem convicção.

O Score v2 precisa corrigir isso.

Ele deve deixar de ser um “acumulador de pontos” e passar a funcionar como:

- arquitetura em blocos;
- sistema com hierarquia;
- sistema com penalidades;
- sistema com teto contextual;
- sistema com explicabilidade.

---

### 3. Princípio central do Score v2

O Score do Ativo v2 segue o seguinte princípio:

> o score final deve refletir a qualidade da tese-base do ativo, e não a simples soma de tudo que parece favorável.

Na prática, isso significa que:

- sinais da mesma família não podem inflar o score como se fossem independentes;
- o bloco estrutural pode ser o mais importante, mas não pode virar um saco de pontos;
- timing ruim deve reduzir nota;
- regime hostil deve limitar o teto;
- liquidez não deve pontuar como convicção, mas como espaço e contexto;
- adequação semanal não pode entrar escondida dentro do score-base.

Esse princípio é a espinha dorsal do documento.

---

### 4. O que o score mede

O Score do Ativo v2 mede a **qualidade da tese-base** do ativo.

Em termos concretos, ele mede:

- força da leitura direcional;
- coerência estrutural;
- qualidade do ambiente para a tese;
- qualidade da localização no range;
- qualidade da amplitude / expansão;
- qualidade do timing imediato, apenas como ajuste.

Ou seja, o score mede:

> quão boa é a tese do ativo em si, antes de perguntar se ela é adequada ao produto semanal.

---

### 5. O que o score não mede

O Score do Ativo v2 **não** deve medir diretamente:

- liquidez da cadeia de opções;
- strike ideal;
- prêmio relativo da opção;
- payoff final da estrutura;
- break-even;
- qualidade comercial final;
- adequação temporal definitiva até sexta;
- custo operacional real da montagem;
- seleção final de derivativo.

Esses itens pertencem a outras camadas do projeto.

Misturá-los no score-base destrói a clareza arquitetural conquistada na Semana 2.

---

### 6. Estrutura oficial do Score v2

O Score do Ativo v2 será composto por **cinco blocos oficiais**.

1. **Bloco A — Tendência-base**
2. **Bloco B — Estrutura institucional**
3. **Bloco C — Volatilidade e expansão**
4. **Bloco D — Localização e espaço**
5. **Bloco E — Timing tático**

Cada bloco existe para responder um tipo diferente de pergunta.

---

### 7. Blocos fora do score

Dois blocos importantes ficam **fora** do Score do Ativo v2, ainda que interajam com ele.

#### 7.1 Camada 0 — Referência Operacional

A Camada 0 é composta por:

- `preco_ref_meta(...)`
- `price_ref`
- `ref_date`
- `ref_rule`

Ela prepara a análise, mas não pontua a tese.

#### 7.2 Camada posterior — Adequação Semanal

A camada semanal é composta por elementos como:

- `move_cap`
- `Alvo_Semana`
- `Faixa_Semana_Alta`
- `Faixa_Semana_Baixa`
- `horizon_bdays`
- critérios de tempo, espaço e maturidade

Ela opera **depois** do score e do regime.

---

### 8. Regra de ouro do Score v2

A regra de ouro do Score v2 é esta:

> famílias diferentes podem compor o score; sinais irmãos da mesma família não podem inflá-lo sem controle.

Essa regra existe para impedir que o motor conte duas ou três vezes a mesma narrativa.

Exemplos de risco de inflação:

- `SMC_Structure` + `BOS` + `PD_Value` + `FVG` + `OB`
- todos somando como se fossem cinco histórias completamente novas

Isso é conceitualmente errado.

O correto é reconhecer que:
- todos pertencem ao bloco estrutural,
- ainda que tenham papéis distintos dentro dele.

---

### 9. Escala oficial do score

O Score do Ativo v2 será expresso em escala:

## 0 a 100

Essa escala terá três níveis internos.

#### 9.1 `score_bruto`
Soma ponderada dos blocos antes de penalidades e antes da modulação de regime.

#### 9.2 `score_ajustado`
Score após penalidades por conflito, timing ruim, esticamento, pouco espaço e outras degradações.

#### 9.3 `score_final_ativo`
Score ajustado após modulação de teto e interpretação pelo regime.

Essa decomposição é importante porque torna o motor auditável.

---

### 10. Composição oficial por blocos

### 10.1 Bloco A — Tendência-base

#### Função
Responder:

- existe uma inclinação direcional inicial?
- essa inclinação é legível?
- ela está minimamente coerente com o resto da tese?

#### Entradas principais
- `infer_direction(...)`
- `ema_stack_up`
- `ema_stack_down`

#### Papel
Oferecer a direção inicial do raciocínio.

#### Peso conceitual
**baixo a médio**

#### Observação importante
Esse bloco existe para iniciar a leitura, não para dominá-la.

---

### 10.2 Bloco B — Estrutura institucional

#### Função
Responder:

- há estrutura coerente?
- houve rompimento relevante?
- existe desequilíbrio útil?
- existe leitura institucional favorável?
- há transição contra a tese?

#### Entradas principais
- `SMC_Structure`
- `SMC_Last_BOS`
- `SMC_Last_CHOCH`
- `SMC_PD_Value`
- `SMC_FVG_Side`
- `SMC_FVG_Size_ATR`
- `SMC_OB_Type`

#### Papel
Esse é o **bloco central do Score v2**.

#### Peso conceitual
**alto**

#### Observação importante
Este bloco é o coração do motor, mas precisa de governança interna para não inflar artificialmente a convicção.

---

### 10.3 Bloco C — Volatilidade e expansão

#### Função
Responder:

- há amplitude suficiente?
- o ativo está comprimido, saudável ou esticado?
- há deslocamento razoável para a tese respirar?

#### Entradas principais
- `atr14`
- `BB_bandwidth`
- `SMC_FVG_Size_ATR`

#### Papel
Qualificar a viabilidade operacional da tese.

#### Peso conceitual
**médio**

#### Observação importante
Sem amplitude, uma tese estrutural boa pode continuar sendo ruim operacionalmente.

---

### 10.4 Bloco D — Localização e espaço

#### Função
Responder:

- o preço está bem posicionado para a tese?
- há espaço útil até a próxima liquidez?
- o ativo está em desconto, prêmio ou região neutra?
- a tese está do lado certo, mas no ponto errado?

#### Entradas principais
- `SMC_PD_Value`
- `PD_Area` como apoio descritivo
- `liquidity_map`

#### Papel
Medir qualidade de posição relativa e espaço disponível.

#### Peso conceitual
**médio**

#### Observação importante
Estar do lado certo sem espaço é uma tese pior do que parece.

---

### 10.5 Bloco E — Timing tático

#### Função
Responder:

- entrar agora faz sentido?
- o timing está bom ou ruim?
- há exaustão local?
- há risco de entrada tardia?

#### Entradas principais
- `FFFD`
- `FFFD_side`
- `BB_percent_b`
- RSI curto, quando disponível

#### Papel
Refinar a entrada, não construir a tese.

#### Peso conceitual
**baixo a médio**

#### Observação importante
Timing ruim deve penalizar mais do que timing bom bonifica.

---

### 11. Distribuição conceitual de pesos

A distribuição conceitual proposta para o Score v2 é:

- **Tendência-base:** 15%
- **Estrutura institucional:** 35%
- **Volatilidade e expansão:** 20%
- **Localização e espaço:** 20%
- **Timing tático:** 10%

---

### 12. Justificativa dos pesos

#### 12.1 Tendência-base — 15%
É importante para organizar a hipótese inicial, mas não pode voltar a ser soberana.

#### 12.2 Estrutura institucional — 35%
É o principal diferencial do SharkMoura e o bloco de maior densidade analítica.

#### 12.3 Volatilidade e expansão — 20%
Sem amplitude, a tese perde poder operacional.

#### 12.4 Localização e espaço — 20%
Porque estar do lado certo no lugar errado continua sendo um problema.

#### 12.5 Timing tático — 10%
Timing importa, mas não pode sequestrar a tese.

---

### 13. Subgovernança do bloco estrutural

O bloco estrutural precisa de regras internas próprias.

#### 13.1 `SMC_Structure`
Representa o **estado estrutural dominante**.

#### 13.2 `SMC_Last_BOS`
Representa o **evento de rompimento**.

#### 13.3 `SMC_Last_CHOCH`
Representa **transição / contestação da estrutura**.

#### 13.4 `SMC_PD_Value`
Representa **localização contínua no range institucional**.

#### 13.5 `SMC_FVG_Side` e `SMC_FVG_Size_ATR`
Representam **desequilíbrio e qualidade de deslocamento**.

#### 13.6 `SMC_OB_Type`
Representa **reforço estrutural auxiliar**.

Essa decomposição interna impede que tudo vire apenas “mais estrutura”.

---

### 14. Penalidades oficiais do Score v2

O score deixa de apenas premiar e passa a punir de forma explícita.

As penalidades formais incluem:

- conflito entre tendência-base e estrutura;
- `CHOCH` contra tese de continuação;
- timing contrário;
- esticamento no range;
- pouco espaço até liquidez relevante;
- amplitude inadequada;
- excesso de proximidade com alvo sem folga operacional.

Sem penalidade, o motor fica viciado em confirmação positiva.

---

### 15. Regras de teto do score

Nem sempre o score pode usar a escala cheia.

O motor passa a reconhecer tetos contextuais.

Exemplos de lógica:

- regime limpo e alinhado → teto cheio;
- transição → teto reduzido;
- exaustão → teto reduzido;
- conflito estrutural forte → teto severamente reduzido.

Essa abordagem é melhor do que apenas subtrair pontos, porque evita que uma tese ruim em ambiente hostil ainda pareça “quase excelente”.

---

### 16. Relação entre Score v2 e Regime

O regime deve atuar como **modulador** do score.

Fluxo correto:

1. calcular os blocos;
2. somar o score bruto;
3. aplicar penalidades;
4. consultar o regime;
5. ajustar teto e interpretação;
6. devolver o score final do ativo.

Isso significa que o score não existe isoladamente.

O regime não substitui o score, mas impede que o score seja lido fora de contexto.

---

### 17. Relação entre Score v2 e linguagem comercial

`DIAMANTE`, `OURO` e `PRATA` **não são o score**.

A linguagem comercial é uma camada posterior que deve considerar, no mínimo:

- score final do ativo;
- regime;
- adequação semanal;
- qualidade operacional do contexto.

Isso evita que o sistema trate como premium uma tese que é forte numericamente, mas ruim em ambiente, timing ou semana.

---

### 18. Relação entre Score v2 e `Probabilidade_Perc`

`Probabilidade_Perc` não deve ser confundida com o score.

O score mede:
- qualidade relativa da tese

A probabilidade tenta medir:
- chance estimada de sucesso, ainda que em nível provisório e não calibrado definitivamente

Logo:

> score e probabilidade são relacionados, mas não equivalentes.

O Score v2 pode alimentar a construção de probabilidade bruta, mas não pode ser tratado como sinônimo dela.

---

### 19. Saída oficial esperada

O Score do Ativo v2 deve devolver, no mínimo:

- `score_bruto`
- `score_ajustado`
- `score_final_ativo`
- `score_tendencia`
- `score_estrutura`
- `score_volatilidade`
- `score_localizacao`
- `score_timing`
- `penalidades_aplicadas`
- `teto_aplicado`
- `racional_score`

Essa estrutura é importante porque aumenta explicabilidade e auditabilidade.

---

### 20. Faixas de interpretação do score

Sugestão conceitual de leitura:

- **0 a 39:** tese fraca ou hostil
- **40 a 59:** tese moderada, incompleta ou conflitada
- **60 a 74:** tese boa, mas ainda dependente de contexto
- **75 a 89:** tese forte e bem organizada
- **90 a 100:** tese excepcionalmente limpa

O objetivo não é banalizar score alto.

Um bom score precisa ser relativamente raro.

---

### 21. O que deve sair do score

Os seguintes itens deixam de pontuar isoladamente como convicção:

- `PD_Area`
- `FVG_Mid`
- `OB_Refine`
- `eq_high`
- `eq_low`
- `pdh`
- `pdl`
- `pwh`
- `pwl`
- `Liq_Target_1`
- `Liq_Target_2`
- `Liq_Side`
- `T1`
- `T2`
- `T3`
- `Stop_Inst`

Esses elementos continuam úteis, mas como:

- contexto;
- espaço;
- racional;
- explicabilidade;
- projeção;
- adequação.

---

### 22. Decisões oficiais derivadas do documento

1. O Score do Ativo passa a ser dividido em cinco blocos.
2. O bloco estrutural passa a ser o mais importante.
3. A tendência-base perde autoridade soberana.
4. O timing passa a ser bloco de ajuste.
5. A liquidez horizontal deixa de pontuar como coleção independente.
6. Penalidades tornam-se obrigatórias.
7. O regime passa a modular teto e interpretação.
8. Score, probabilidade e linguagem comercial ficam formalmente separados.

---

### 23. Veredito técnico final

O Score do Ativo v2 transforma o SharkMoura de um somador de confluências em um sistema com:

- blocos;
- hierarquia;
- penalidade;
- teto;
- explicabilidade.

Essa é uma das viradas mais importantes de toda a Semana 2.

---

### 24. Próximo passo lógico

O próximo passo lógico é o:

**Documento 12 — Adequação ao Horizonte Semanal**

Porque, uma vez definido:
- o que é uma boa tese-base;
- em que regime ela opera;
- como ela é pontuada;

o sistema precisa responder à pergunta seguinte:

> essa tese boa também é boa para o produto semanal?
# Documento 10 — Classificador de Regime v1
## Projeto SharkMoura 2.0

### 1. Objetivo do documento

Este documento formaliza o **Classificador de Regime v1** do SharkMoura 2.0.

O objetivo do classificador não é decidir sozinho:

- qual operação executar;
- qual strike selecionar;
- qual estrutura de opção montar;
- qual selo comercial atribuir.

O objetivo dele é responder, antes disso:

> em que tipo de ambiente de mercado o ativo está operando agora?

Essa resposta é decisiva porque o mesmo sinal muda completamente de significado dependendo do contexto em que aparece.

Uma estrutura bullish em ambiente de:

- continuação limpa;
- transição;
- expansão;
- lateralidade estruturada;
- exaustão;

não deve ser interpretada da mesma forma.

O Classificador de Regime v1 existe para impedir justamente esse erro.

---

### 2. Posição técnica de abertura

A principal correção conceitual que este documento introduz é a seguinte:

> o SharkMoura não pode continuar operando apenas com direção implícita e confluência estrutural sem uma camada formal de regime.

Sem regime formal, o motor tende a cometer três erros graves:

1. tratar setups semelhantes como se estivessem no mesmo ambiente;
2. permitir score alto em contexto ruim;
3. confundir:
   - bias,
   - estrutura,
   - timing,
   - e adequação temporal
   como se fossem a mesma coisa.

Eles não são.

A partir da Semana 2, isso fica formalmente separado.

---

### 3. Função oficial do classificador de regime

O classificador de regime deve servir para:

- contextualizar a tese-base;
- modular a leitura do score do ativo;
- reduzir falsos positivos;
- distinguir continuidade de transição;
- distinguir força real de esticamento;
- melhorar a leitura do contexto antes da camada semanal;
- impedir que o motor premie a mesma tese do mesmo jeito em ambientes diferentes.

Ele **não** deve:

- substituir o Score do Ativo v2;
- substituir a camada de adequação semanal;
- substituir a camada de opções;
- funcionar como decisão isolada de compra ou venda.

Em termos arquiteturais:

> o regime não substitui a tese; ele qualifica o ambiente onde a tese existe.

---

### 4. Princípio central do Regime v1

O Regime v1 segue o seguinte princípio:

> regime não é um indicador isolado; regime é uma leitura composta e hierárquica do ambiente.

Isso significa que o classificador não pode depender de um único sinal, como:

- EMA stack;
- RSI;
- Bollinger;
- BOS isolado;
- `FFFD`.

Ele precisa sintetizar, em ordem lógica, sinais vindos de famílias diferentes, respeitando precedência e papel analítico.

---

### 5. Estrutura oficial do Classificador de Regime v1

O classificador será composto por **dois níveis**.

#### 5.1 Nível 1 — Regime Principal

É o rótulo principal do ambiente dominante.

Ele responde:

> qual é a natureza predominante do mercado neste momento?

#### 5.2 Nível 2 — Flags de Regime

São qualificadores complementares do ambiente.

Eles existem porque o mercado raramente cabe de forma perfeita em um único rótulo estático.

Exemplo conceitual:

- `regime_principal = TENDENCIA_ALTA`
- `flags = [BOS_RECENTE, FVG_RELEVANTE, TIMING_CONTRA]`

Nesse caso, o ambiente continua sendo de alta, mas com nuances importantes.

Essa separação é melhor do que tentar criar dezenas de regimes hiper-específicos.

---

### 6. Regimes principais oficiais

O Classificador de Regime v1 adota os seguintes regimes principais:

1. `TENDENCIA_ALTA`
2. `TENDENCIA_BAIXA`
3. `LATERAL_ESTRUTURADA`
4. `TRANSICAO`
5. `EXPANSAO_DIRECIONAL`
6. `EXAUSTAO_OU_ESTICAMENTO`

---

### 7. Por que esses regimes foram escolhidos

A escolha desses regimes segue um critério de equilíbrio entre:

- clareza;
- utilidade;
- auditabilidade;
- capacidade de evolução.

Se o classificador nascesse complexo demais, ele correria o risco de virar um exercício narrativo e pouco implementável.

Se nascesse simples demais, ele viraria uma camada decorativa sem capacidade real de modular o motor.

Esses seis estados foram escolhidos porque conseguem cobrir, com boa densidade prática, os principais ambientes que importam para o SharkMoura:

- continuidade;
- continuidade de baixa;
- lateralidade legível;
- transição estrutural;
- expansão com urgência;
- esticamento / exaustão.

---

### 8. Fontes de informação do classificador

O Classificador de Regime v1 deve consumir sinais vindos de múltiplas famílias.

#### 8.1 Tendência-base
- `ema_stack_up`
- `ema_stack_down`
- `infer_direction(...)`

#### 8.2 Estrutura institucional
- `SMC_Structure`
- `SMC_Last_BOS`
- `SMC_Last_CHOCH`
- `SMC_PD_Value`
- `SMC_FVG_Side`
- `SMC_FVG_Size_ATR`
- `SMC_OB_Type`

#### 8.3 Volatilidade e expansão
- `atr14`
- `BB_bandwidth`
- `move_cap` (como pista de deslocamento plausível, não como núcleo do regime)

#### 8.4 Timing tático
- `FFFD`
- `FFFD_side`
- `BB_percent_b`
- RSI curto, quando disponível

#### 8.5 Contexto semanal
- `PWH`
- `PWL`
- `Alvo_Semana`
- `Faixa_Semana_Alta`
- `Faixa_Semana_Baixa`
- `horizon_bdays`

Observação importante:

O contexto semanal pode modular o **uso operacional** do regime, mas não deve redefinir sozinho sua natureza estrutural.

---

### 9. Hierarquia oficial de leitura do regime

A leitura do regime deve respeitar a seguinte ordem de precedência:

1. **Estrutura institucional**
2. **Tendência-base**
3. **Volatilidade e expansão**
4. **Timing tático**
5. **Contexto semanal**

Essa hierarquia existe por um motivo simples:

> o regime deve ser guiado primeiro pelo que o mercado está estruturalmente fazendo, e só depois pelo que o resto dos filtros sugere.

Se essa ordem for invertida, o motor corre o risco de transformar:
- timing curto
ou
- inclinação de EMA

em leitura soberana de ambiente, o que seria um erro.

---

### 10. Regras conceituais por regime principal

### 10.1 `TENDENCIA_ALTA`

#### Condições centrais
- `infer_direction(...)` favorece compra;
- `SMC_Structure = BULL`;
- `SMC_Last_BOS` alinhado para cima ou ausência de evento contrário forte;
- `CHOCH` ausente ou irrelevante no lado contrário;
- `PD_Value` não excessivamente esticado para compra imediata;
- timing não claramente contra.

#### Interpretação
O ativo está em ambiente de continuidade de alta.

#### O que esse regime permite
- priorizar continuidade;
- aceitar compra em desconto estrutural;
- usar estrutura bullish como núcleo da tese.

#### O que esse regime não autoriza automaticamente
- comprar qualquer esticamento;
- ignorar timing ruim;
- assumir adequação semanal;
- tratar alta estrutural como entrada obrigatória.

---

### 10.2 `TENDENCIA_BAIXA`

#### Condições centrais
- `infer_direction(...)` favorece venda;
- `SMC_Structure = BEAR`;
- `SMC_Last_BOS` alinhado para baixo;
- `CHOCH` ausente ou sem força no lado contrário;
- `PD_Value` não excessivamente descontado para novas vendas;
- timing não claramente contra.

#### Interpretação
O ativo está em ambiente de continuidade de baixa.

#### O que esse regime permite
- priorizar teses de venda;
- aceitar venda em prêmio;
- reforçar continuidade bearish.

#### O que esse regime não autoriza automaticamente
- vender já exaurido;
- ignorar proximidade de liquidez;
- assumir que a tese cabe até sexta;
- transformar qualquer fraqueza local em venda imediata.

---

### 10.3 `LATERAL_ESTRUTURADA`

#### Condições centrais
- estrutura sem direção dominante clara;
- ausência de BOS relevante de continuidade;
- conflito fraco ou neutralidade na direção-base;
- range legível;
- níveis horizontais úteis e respeitados.

#### Interpretação
O mercado não está limpo em tendência, mas ainda é inteligível.

Não é “ruído puro”.  
É um ambiente onde a leitura de range e liquidez pode fazer mais sentido do que a leitura de continuação.

#### O que esse regime permite
- priorizar leitura de borda de range;
- reforçar valor do `liquidity_map`;
- exigir maior disciplina na entrada.

#### O que esse regime não autoriza automaticamente
- score direcional exagerado;
- dependência excessiva de EMA stack;
- leitura de continuação forte sem evento estrutural novo.

---

### 10.4 `TRANSICAO`

#### Condições centrais
- conflito entre tendência-base e estrutura;
- `CHOCH` ativo;
- BOS recente em lado diferente do estado anterior;
- sinais mistos entre direção, estrutura e timing;
- perda de limpeza do ambiente.

#### Interpretação
O mercado está mudando de estado ou, no mínimo, contestando o estado anterior.

Esse é o regime em que o motor precisa reduzir a convicção e exigir mais confirmação.

#### O que esse regime permite
- leitura de cautela;
- redução do teto do score;
- exigência de confirmação adicional;
- valorização maior de evidência estrutural nova.

#### O que esse regime não autoriza automaticamente
- continuar operando como se estivesse em tendência limpa;
- premiar score alto apenas por inércia;
- ignorar conflito interno entre os blocos.

---

### 10.5 `EXPANSAO_DIRECIONAL`

#### Condições centrais
- estrutura alinhada;
- BOS recente alinhado;
- FVG relevante;
- `BB_bandwidth` saudável ou em expansão;
- deslocamento claro e coerente.

#### Interpretação
O ativo não está apenas direcional. Ele está em deslocamento com urgência.

É um ambiente importante porque pode sustentar movimentos com mais velocidade e mais convicção do que uma tendência simplesmente “limpa”.

#### O que esse regime permite
- maior confiança em continuidade;
- mais tolerância para ambição de alvo, com disciplina;
- melhor leitura de urgência institucional.

#### O que esse regime não autoriza automaticamente
- comprar ou vender sem checar esticamento;
- ignorar timing;
- ignorar que a expansão pode estar perto de exaustão.

---

### 10.6 `EXAUSTAO_OU_ESTICAMENTO`

#### Condições centrais
- a tese-base ainda pode existir;
- mas o timing está degradado;
- `FFFD` contrário à direção da tese;
- `BB_percent_b` em extremo;
- `PD_Value` muito alto para compra ou muito baixo para venda;
- proximidade de alvo ou liquidez reduz espaço útil.

#### Interpretação
O problema aqui não é necessariamente a direção da tese.  
O problema é o **momento da entrada**.

Esse regime é central para impedir que o motor trate como excelente uma tese que está certa no sentido, mas errada no timing.

#### O que esse regime permite
- reduzir agressividade;
- penalizar entrada imediata;
- priorizar espera ou reaproximação.

#### O que esse regime não autoriza automaticamente
- inverter sozinho a tese estrutural;
- transformar exaustão local em reversão confirmada;
- anular estrutura forte sem validação adicional.

---

### 11. Flags oficiais de regime

As flags do Regime v1 funcionam como qualificadores complementares.

As flags oficiais são:

- `ALINHADO_TENDENCIA_E_ESTRUTURA`
- `CONFLITO_TENDENCIA_E_ESTRUTURA`
- `BOS_RECENTE`
- `CHOCH_ATIVO`
- `EM_DESCONTO`
- `EM_PREMIO`
- `FVG_RELEVANTE`
- `OB_PRESENTE`
- `PROXIMO_DE_LIQUIDEZ`
- `AMPLITUDE_BAIXA`
- `AMPLITUDE_SAUDAVEL`
- `TIMING_CONTRA`
- `TIMING_A_FAVOR`
- `SEMANA_APERTADA`
- `ALVO_SEMANAL_PLAUSIVEL`

Essas flags não substituem o regime principal.  
Elas ajudam a refiná-lo.

---

### 12. Regras de precedência

O Classificador de Regime v1 deve respeitar as seguintes regras de precedência.

#### 12.1 Estrutura vence tendência-base
Se houver conflito claro entre:

- `infer_direction(...)`
e
- `SMC_Structure` / `BOS`

a estrutura deve ter prioridade.

#### 12.2 `CHOCH` reduz convicção
Se `CHOCH` estiver ativo, o regime não deve continuar sendo tratado como “limpo” sem confirmação adicional.

#### 12.3 Timing não redefine regime sozinho
`FFFD`, RSI curto e Bollinger podem degradar o timing, mas não devem redefinir sozinhos o ambiente principal.

#### 12.4 Contexto semanal modula utilidade, não natureza
A semana pode estar apertada e ainda assim o ativo continuar em `TENDENCIA_ALTA`.

O que muda é a utilidade operacional, não a natureza estrutural do regime.

#### 12.5 Liquidez próxima muda leitura de espaço
Proximidade de liquidez relevante pode degradar continuidade, mas não redefine sozinha o ambiente principal.

---

### 13. Saída oficial esperada

O classificador deve devolver, no mínimo:

- `regime_principal`
- `regime_bias`
- `regime_strength`
- `regime_flags`
- `regime_conflicts`
- `regime_rationale`

Isso garante que a camada não seja apenas um rótulo, mas uma estrutura utilizável pelo resto do motor.

---

### 14. Como o regime deve mudar o motor

O regime precisa afetar o motor de forma concreta.

Ele deve:

- modular a interpretação do score;
- reduzir tetos em ambientes ruins;
- impedir leituras excessivamente otimistas em transição;
- influenciar a adequação semanal;
- ajudar a governar a linguagem comercial futura.

Em outras palavras:

> o regime precisa ter efeito operacional real, e não apenas valor descritivo.

---

### 15. O que não fazer

Este documento também define o que o motor **não deve fazer**.

- não usar EMA stack sozinha como regime;
- não usar RSI sozinho como regime;
- não transformar timing em ambiente;
- não misturar adequação semanal com natureza estrutural;
- não criar dezenas de regimes excessivamente específicos nesta fase.

O Regime v1 precisa nascer útil, legível e implementável.

---

### 16. Decisões oficiais derivadas do documento

1. O SharkMoura passa a ter camada formal de regime.
2. O regime será composto por regime principal + flags.
3. A estrutura terá precedência sobre a tendência-base em caso de conflito.
4. Timing poderá degradar leitura, mas não redefinir sozinho a natureza do ambiente.
5. O contexto semanal poderá modular utilidade, mas não substituir a classificação estrutural.
6. O regime deverá afetar score, adequação semanal e interpretação operacional.

---

### 17. Veredito técnico final

O Classificador de Regime v1 é a peça que impede o SharkMoura de tratar sinais bons em mercado ruim como se fossem equivalentes a sinais bons em mercado bom.

Ele não substitui o score.  
Ele não substitui a adequação semanal.  
Ele não substitui a camada de opções.

Mas ele impede um erro central:

> decidir o quanto confiar sem antes entender em que ambiente a tese está operando.

---

### 18. Próximo passo lógico

O próximo passo lógico é o:

**Documento 11 — Score do Ativo v2**

Porque, uma vez definidos:

- famílias de sinais;
- matriz de redundância;
- classificador de regime;

o sistema já tem base suficiente para transformar a tese-base em um score estruturado, com:

- blocos;
- pesos;
- penalidades;
- teto contextual.
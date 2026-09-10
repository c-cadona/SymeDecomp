# Trilha de Aprendizado e Realização
## Analisador de Componentes Simétricas em Tempo Real para Redes Trifásicas

**Dupla:** Arthur (A) & Guilherme (G) — INEP, Disciplina de Projetos Nível I e II
**Prazo:** 45 dias · **Stack:** Python + Streamlit (fase software) → ESP32 (fase hardware)
**Modo de trabalho:** os dois em paralelo em cada fase (software juntos, depois hardware juntos), integrando via GitHub

---

## Convenções de trabalho no GitHub

Como vocês têm experiência intermediária com branches/PR, a estrutura fica simples e não precisa de gitflow complexo:

- **`main`** sempre estável — só recebe merge via Pull Request, nunca commit direto.
- **1 branch por etapa**, nomeada `feature/<iniciais>-<nome-curto>` (ex: `feature/A-gerador-sinais`, `feature/G-decompositor`).
- **PR obrigatório com revisão cruzada**: quem não escreveu o código revisa antes do merge. Em dupla isso parece burocracia, mas é o que garante que os dois entendam o projeto inteiro na hora de apresentar/defender.
- **Commits pequenos e frequentes**, mensagem descrevendo o "porquê", não só o "o quê".
- Um **GitHub Project** (kanban) com colunas *A Fazer / Em Progresso / Em Revisão / Feito*, uma issue por etapa desta trilha — dá pra literalmente colar essas etapas como issues.
- Cada "Gatilho de integração" abaixo é o momento de abrir o PR ou de sincronizar com o parceiro — não esperem até o fim da fase pra conversar.

---

## FASE 0 — Fundamentação teórica (dias 1–4, ambos juntos)

### Etapa 0.1 — Base matemática e normativa

**1. Objetivo do passo**
Ter, antes de escrever qualquer código, uma base sólida do que é o fenômeno físico e como ele é medido oficialmente — isso evita retrabalho quando alguém perguntar "por que vocês calcularam assim?" na banca.

**2. Conceitos teóricos**
- Sistema trifásico equilibrado vs. desequilibrado (amplitude e/ou defasagem fora de 120°)
- Componentes simétricas: sequência positiva, negativa e zero
- Transformada de Fortescue e o operador `a = 1∠120°`
- Definição do fator de desequilíbrio (existe a definição IEEE/NEMA e a usada pelo PRODIST Módulo 8 — confiram qual é qual, elas não são idênticas)
- Limiar de 2% do PRODIST

**3. Conceitos de programação**
Ainda não há código, mas comecem a pensar em como representar fasores: em Python, número complexo é tipo nativo (`3+4j`) e a biblioteca `cmath`/`numpy` já faz as contas de módulo, ângulo e rotação — vale já esboçar mentalmente "um sistema trifásico é uma lista de 3 números complexos".

**4. Gatilhos de integração**
- Criar o repositório GitHub compartilhado, com `README.md`, estrutura de pastas (`/src`, `/tests`, `/docs`, `/firmware`) e o board de issues.
- Os dois revisam juntos as fórmulas antes de qualquer um começar a codar — evita que gerador e decompositor "aprendam" definições diferentes.

**5. Entrega da etapa (palpável)**
`docs/teoria.md` no repositório, com as fórmulas, a definição de fator de desequilíbrio escolhida (com justificativa) e as referências (PRODIST + livro-texto/artigo). Repositório criado e estruturado.

---

## FASE 1 — Núcleo Python (dias 5–18, em paralelo)

### Etapa 1.A (Arthur) — Gerador de sinais sintéticos

**1. Objetivo**
Criar a "fonte de dados" do projeto: um gerador de tensões trifásicas configurável, capaz de impor desequilíbrio de propósito.

**2. Conceitos teóricos**
Três senoides defasadas 120°; tipos de desequilíbrio (amplitude, fase, ambos); frequência de amostragem vs. frequência do sinal (Nyquist); ruído de medição.

**3. Conceitos de programação**
Pense na função como **pura**: recebe parâmetros (amplitude por fase, defasagem, frequência, `fs`, duração, ruído) e devolve arrays — sem estado interno, sem efeito colateral. Isso a torna trivial de testar e de reaproveitar depois no firmware. Use `numpy` vetorizado (gerar o vetor de tempo inteiro e aplicar `sin` de uma vez) em vez de loop `for` amostra a amostra.

**4. Gatilhos de integração**
Antes de escrever a primeira linha, combinem com o G o **contrato de dados**: formato exato do retorno (ex: `dict` com `t`, `va`, `vb`, `vc` como arrays numpy). Documentem isso em `docs/contrato_dados.md`. Esse contrato é o que permite os dois codarem em paralelo sem esperar um pelo outro.

**5. Entrega**
`src/gerador.py` + `tests/test_gerador.py` (pytest) validando: sistema equilibrado → RMS igual nas 3 fases; parâmetro de desequilíbrio → desvio no RMS proporcional ao esperado. PR aberto, revisado por G, mergeado.

---

### Etapa 1.G (Guilherme) — Decompositor de Fortescue + fator de desequilíbrio + alarme

**1. Objetivo**
Implementar o núcleo matemático do projeto: decompor as 3 tensões em componentes de sequência e decidir quando disparar o alarme.

**2. Conceitos teóricos**
Matriz de transformação de Fortescue; cálculo do fator de desequilíbrio (definição travada na Etapa 0.1); limiar de 2%.

**3. Conceitos de programação**
Pense a transformação como **multiplicação de matriz** (3x3, complexa) usando `numpy` — não escreva as 3 equações "na mão", deixe a álgebra linear fazer o trabalho, é menos propenso a erro de digitação de sinal. Separe em duas funções: uma que **calcula** (Fortescue → V+, V-, V0 → fator), outra que **decide** (fator → alarme sim/não). Isso deixa cada parte testável isoladamente e facilita trocar a lógica do alarme depois sem mexer na matemática.

**4. Gatilhos de integração**
Como o gerador do A ainda não existe no dia 5, trabalhe com **casos fixos escritos à mão**: um sistema perfeitamente equilibrado (resultado esperado: V- ≈ 0) e um caso didático com desequilíbrio conhecido, calculado manualmente à parte, pra comparar. O gatilho real de integração é quando as duas branches (`feature/A-gerador-sinais` e `feature/G-decompositor`) se encontram — nesse ponto, testem o decompositor com a *saída real* do gerador pela primeira vez.

**5. Entrega**
`src/decompositor.py` + `tests/test_decompositor.py`, validado contra os 2 casos conhecidos. PR aberto, revisado por A, mergeado.

---

### Etapa 1.INT (ambos, ~dia 16–18) — Primeira integração

**1. Objetivo**
Validar o pipeline ponta a ponta: gerador → decompositor → resultado.

**2. Conceitos teóricos**
Nenhum novo — é validação do que já foi estudado.

**3. Conceitos de programação**
Escrevam um `src/pipeline.py` que só **orquestra** (chama gerador, passa pro decompositor, imprime resultado) — sem lógica própria de cálculo. Separar "orquestração" de "cálculo" é o princípio que vai facilitar demais quando isso virar um app Streamlit na Fase 2.

**4. Gatilhos de integração**
Merge cruzado das duas branches na `main` via PR — primeiro *gate* de qualidade real do projeto: se os contratos de dados da Etapa 0.1 estiverem certos, isso deve funcionar quase sem ajuste.

**5. Entrega**
`pipeline.py` rodando via terminal, imprimindo V+, V-, V0 e status do alarme para um caso de teste. Este é o esqueleto funcional completo do algoritmo.

---

## FASE 2 — Interface Streamlit (dias 19–28, em paralelo)

### Etapa 2.A (Arthur) — Painel de controle

**1. Objetivo**
Construir a interface onde o usuário ajusta os parâmetros do sistema trifásico ao vivo (amplitude por fase, defasagem, ruído).

**2. Conceitos teóricos**
Nenhum novo — é aplicação prática dos parâmetros da Fase 1.

**3. Conceitos de programação**
Entenda o modelo de execução do Streamlit: o script inteiro **reroda do zero a cada interação** do usuário. Isso muda como se pensa em estado — use `st.session_state` para guardar valores entre essas re-execuções. Pense nos widgets (sliders, inputs) como um "formulário" que no final produz um dicionário de parâmetros — o mesmo formato do contrato de dados da Fase 1.

**4. Gatilhos de integração**
O dicionário que sai do painel de controle precisa bater exatamente com o que `gerador.py` espera. Combine nomes de chave com G antes de codar.

**5. Entrega**
`app/controls.py` com os widgets funcionando isoladamente, testado com dados mockados (sem depender ainda do painel de gráficos).

---

### Etapa 2.G (Guilherme) — Painel de visualização

**1. Objetivo**
Construir a visualização: as 3 tensões de fase, as componentes simétricas e o indicador de alarme.

**2. Conceitos teóricos**
Nenhum novo.

**3. Conceitos de programação**
Isole **dado** de **desenho**: escreva uma função que recebe arrays numéricos e devolve uma figura (Plotly, por ex.), sem saber de onde os dados vieram. Isso permite testar o painel com dados falsos enquanto o resto do sistema não está pronto — e é o mesmo princípio de "função pura" da Etapa 1.A.

**4. Gatilhos de integração**
Combine com A o formato de saída do `decompositor.py` que esse painel vai consumir.

**5. Entrega**
`app/plots.py` renderizando gráficos com dados mockados (sem depender ainda do painel de controle).

---

### Etapa 2.INT (ambos) — App completo (MVP)

**1. Objetivo**
Unir `controls.py` + `plots.py` + `pipeline.py` num `app.py` Streamlit funcional e ao vivo.

**2. Conceitos teóricos**
Nenhum.

**3. Conceitos de programação**
`app.py` deve **só orquestrar** — importar e chamar, sem lógica própria (mesma separação de responsabilidades da Etapa 1.INT). Para simular "tempo real", pensem em um loop de atualização (`st.rerun`, ou um botão/timer que reprocessa o pipeline periodicamente).

**4. Gatilhos de integração**
Merge cruzado de `feature/A-painel-controle` e `feature/G-painel-visualizacao` na `main`.

**5. Entrega**
`streamlit run app.py` funcionando localmente, demonstrável: usuário ajusta o desequilíbrio e vê o alarme reagir ao vivo.

> **Este é o MVP do projeto.** A partir daqui, tudo é "etapa adicional" — o que importa é que, se o cronograma apertar, o projeto já é completo e defensável só com isso.

---

## FASE 3 — Sensores e firmware ESP32 (dias 29–36, em paralelo)

### Etapa 3.A (Arthur) — Sensor e condicionamento de sinal

**1. Objetivo**
Montar o circuito de aquisição: sensor de tensão isolado (ZMPT101B) + condicionamento de sinal para caber em 0–3,3V do ADC.

**2. Conceitos teóricos**
Isolamento galvânico (por que não se liga a rede direto no microcontrolador); transformador de tensão de instrumentação; offset DC necessário porque o ADC do ESP32 só lê tensão positiva; ganho/atenuação do estágio de condicionamento.

**3. Conceitos de programação**
Pouco código aqui, mas já pensem à frente: o firmware vai precisar de uma **constante de calibração** (volts por código de ADC) — meçam essa constante experimentalmente e documentem, ela vira uma linha de código depois.

**4. Gatilhos de integração**
Entregar a constante de calibração e o range esperado de código ADC para G, antes dele fechar o firmware de leitura.

**5. Entrega**
Circuito montado em protoboard para 1 fase (modelo replicável para as outras 2), validado com multímetro. Foto/esquema documentado em `docs/hardware.md`.

---

### Etapa 3.G (Guilherme) — Firmware de aquisição

**1. Objetivo**
Firmware ESP32 que amostra o ADC em taxa fixa e entrega um buffer de amostras.

**2. Conceitos teóricos**
Nyquist aplicado a 60Hz (tipicamente 12+ amostras por ciclo são necessárias para o Fortescue funcionar bem); limitações de linearidade do ADC interno do ESP32 fora da faixa recomendada — vale revisar a referência do Embarcados antes de projetar o range de tensão de entrada.

**3. Conceitos de programação**
Amostragem em intervalo fixo não pode depender de `delay()` (impreciso e bloqueante) — pensem em timer/interrupção. Estruturem um **buffer circular** para acumular amostras sem travar o loop principal.

**4. Gatilhos de integração**
Testar o firmware junto com o circuito de A assim que ambos estiverem prontos — validar que os códigos ADC lidos batem com a calibração esperada.

**5. Entrega**
Firmware imprimindo via serial as amostras de 1 canal, rodando estável por pelo menos alguns minutos.

---

### Etapa 3.INT (ambos) — Aquisição trifásica completa

**1. Objetivo**
Replicar o circuito para as 3 fases e validar leitura simultânea.

**2. Conceitos teóricos**
Nenhum novo — é escala do que já foi validado.

**3. Conceitos de programação**
Pensar em ler múltiplos canais ADC sem perder o sincronismo temporal entre eles — isso é crítico, porque o Fortescue depende da relação de **fase** entre as 3 senoides, não só da amplitude.

**4. Gatilhos de integração**
Merge do firmware validado com o circuito de 3 fases no repositório `/firmware`.

**5. Entrega**
ESP32 lendo e imprimindo 3 canais simultâneos, com timestamp coerente entre eles.

---

## FASE 4 — Algoritmo embarcado e alarme físico (dias 37–42, em paralelo)

### Etapa 4.A (Arthur) — Port do algoritmo de Fortescue para C/C++

**1. Objetivo**
Traduzir o decompositor Python para o firmware embarcado.

**2. Conceitos teóricos**
Revisão da mesma matemática da Etapa 1.G, agora sob restrições de sistema embarcado.

**3. Conceitos de programação**
Sem `numpy` no ESP32: representem número complexo como `struct` com parte real e imaginária, e implementem a multiplicação de matriz "na mão" com essas structs. Se performance virar problema, considerem ponto fixo em vez de `float` — mas comecem com `float`, é mais simples e provavelmente suficiente aqui.

**4. Gatilhos de integração**
Validem a porta comparando a saída do C com a saída do `decompositor.py` da Fase 1, usando os **mesmos casos de teste** como gabarito.

**5. Entrega**
Função `calcula_fortescue()` em C, rodando no ESP32, validada contra os casos de teste em Python.

---

### Etapa 4.G (Guilherme) — Alarme físico e testes de bancada

**1. Objetivo**
Acionamento físico do alarme (LED/buzzer) e validação com sinal real.

**2. Conceitos teóricos**
Aplicação do limiar PRODIST no contexto físico; histerese (evitar que o alarme "pisque" quando o fator ficar oscilando perto do limiar).

**3. Conceitos de programação**
Máquina de estados simples para o alarme (normal / alerta), com histerese para evitar oscilação — pensem em dois limiares (liga em 2%, desliga em 1,5%, por exemplo) em vez de um só.

**4. Gatilhos de integração**
Validação real só é possível quando 4.A tiver o cálculo funcionando no firmware — combinem esse ponto de encontro com antecedência.

**5. Entrega**
Sistema completo disparando o alarme físico com um desequilíbrio real aplicado em bancada (com segurança — nada de mexer direto na rede sem orientação do professor).

---

## FASE 5 — Relatório e buffer (dias 43–45, ambos)

**1. Objetivo**
Consolidar documentação, validar o sistema de ponta a ponta e deixar folga para imprevistos de última hora.

**2. Conceitos teóricos**
Revisão geral — é o momento de garantir que o relatório reflete corretamente as decisões teóricas tomadas na Etapa 0.1.

**3. Conceitos de programação**
Nenhum novo — foco em gerar os gráficos/capturas finais que vão para o relatório.

**4. Gatilhos de integração**
Merge final de qualquer branch pendente; tag de release no GitHub (ex: `v1.0-entrega`).

**5. Entrega**
Relatório final + repositório organizado e documentado + demonstração gravada (vídeo curto do sistema funcionando, útil como backup caso algo falhe na apresentação ao vivo).

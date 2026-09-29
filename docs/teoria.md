# Fundamentação Teórica — Etapa 0.1

**Projeto:** SymeDecomp
**Disciplina:** Projeto Nível I em Eletrônica Pot. e Acion. III
**Alunos:** Arthur Augusto Dahlke e Guilherme Cadona da Silva

---

## 1. Sistema trifásico equilibrado vs. desequilibrado

Um sistema trifásico é dito **equilibrado** quando as três tensões de fase
têm:

- a mesma **amplitude** (módulo);
- a mesma **frequência**;
- defasagem de exatamente **120°** entre si, na sequência de fases padrão
  (sequência positiva: A → B → C).

Matematicamente, um sistema equilibrado em sequência positiva é escrito como:

```
va(t) = Vm · sin(ωt)
vb(t) = Vm · sin(ωt − 120°)
vc(t) = Vm · sin(ωt + 120°)
```

onde `Vm` é a amplitude de pico e `ω = 2πf`.

Um sistema é **desequilibrado** quando pelo menos uma dessas condições é
violada. No escopo deste projeto, dois tipos de desequilíbrio são
considerados (e são exatamente os dois modos que `src/gerador.py` permite
impor):

- **Desequilíbrio de amplitude**: uma ou mais fases têm módulo de tensão
  diferente das demais (ex.: `amp_b ≠ amp_a`).
- **Desequilíbrio de fase (ângulo)**: a defasagem entre as fases se afasta
  de 120° (ex.: `fase_c_deg ≠ 120°`).
- **Desequilíbrio misto**: combinação dos dois casos acima — é o cenário
  mais realista, já que na prática cargas desbalanceadas costumam afetar
  simultaneamente módulo e ângulo das tensões.

Essas causas costumam vir de cargas monofásicas mal distribuídas entre as
fases, impedâncias de linha desiguais, faltas assimétricas ou grandes
cargas monofásicas concentradas (ex.: fornos a arco, tração elétrica).

---

## 2. Componentes simétricas

A técnica de **componentes simétricas**, proposta por Charles Fortescue em
1918, permite decompor um sistema trifásico desequilibrado (e, portanto,
difícil de analisar diretamente) em três sistemas equilibrados
sobrepostos, cada um muito mais simples de tratar:

| Componente | Símbolo | Característica |
|---|---|---|
| Sequência positiva | `V₁` (ou `V+`) | Três fasores de mesmo módulo, defasados 120°, na mesma ordem de rotação do sistema original (A→B→C). Representa a parcela "saudável" do sistema. |
| Sequência negativa | `V₂` (ou `V−`) | Três fasores de mesmo módulo, defasados 120°, mas com ordem de rotação invertida (A→C→B). É a componente responsável, por exemplo, por aquecimento e torque reverso em motores de indução. |
| Sequência zero | `V₀` | Três fasores de mesmo módulo e **em fase** entre si (sem defasagem). Só existe em sistemas com neutro/retorno de terra e está associada a correntes de neutro/desequilíbrios que envolvem a terra. |

A ideia central: qualquer conjunto desequilibrado de fasores `Va, Vb, Vc`
pode ser reescrito como a soma:

```
Va = V0 + V1 + V2
Vb = V0 + a²V1 + aV2
Vc = V0 + aV1 + a²V2
```

---

## 3. O operador `a` e a Transformada de Fortescue

O operador de Fortescue é definido como o fasor unitário que gira 120°:

```
a = 1∠120° = e^(j2π/3) = −0,5 + j0,866
a² = 1∠240° = e^(j4π/3) = −0,5 − j0,866
a³ = 1∠0° = 1
```

Em Python, isso é naturalmente representado com números complexos
(`complex`), que já são um tipo nativo da linguagem:

```python
import cmath
a = cmath.exp(1j * 2 * cmath.pi / 3)   # a = 1∠120°
```

A **matriz de Fortescue** relaciona os fasores de fase `[Va, Vb, Vc]` às
componentes de sequência `[V0, V1, V2]`:

**Transformação direta (fase → sequência):**

```
⎡V0⎤       ⎡1   1    1  ⎤ ⎡Va⎤
⎢V1⎥ = 1/3 ⎢1   a    a² ⎥ ⎢Vb⎥
⎣V2⎦       ⎣1   a²   a  ⎦ ⎣Vc⎦
```

**Transformação inversa (sequência → fase):**

```
⎡Va⎤     ⎡1   1    1  ⎤ ⎡V0⎤
⎢Vb⎥  =  ⎢1   a²   a  ⎥ ⎢V1⎥
⎣Vc⎦     ⎣1   a    a² ⎦ ⎣V2⎦
```

Importante: essas equações trabalham com **fasores** (amplitude + ângulo
de um regime senoidal permanente), não diretamente com as amostras
instantâneas no tempo que `gerador.py` produz. Na prática, o decompositor
precisa primeiro extrair o fasor de cada fase (por exemplo, via DFT/FFT de
um ciclo completo, ou via ajuste de mínimos quadrados a uma senoide) antes
de aplicar a matriz de Fortescue acima. Essa conversão amostras → fasor é
parte do que a Etapa 1.G (decompositor) precisa implementar.

Do ponto de vista de programação, a transformação acima deve ser tratada
como uma simples **multiplicação de matriz complexa 3×3** via `numpy`, em
vez de escrever as três equações manualmente — isso reduz o risco de erro
de sinal/digitação.

---

## 4. Fator de desequilíbrio de tensão

Existem duas definições de uso comum para quantificar o desequilíbrio de
tensão, e **elas não são idênticas** — por isso a escolha precisa ser
explícita e documentada:

### 4.1 Definição PRODIST / IEC / ANSI (adotada neste projeto)

O Módulo 8 do PRODIST (ANEEL) define o **Fator de Desequilíbrio de Tensão
(FD)** como a razão entre o módulo da tensão de sequência negativa e o
módulo da tensão de sequência positiva, expressa em porcentagem:

```
FD (%) = (|V2| / |V1|) × 100
```

Essa é a mesma definição usada pelas normas **IEC** e **ANSI**, e também
coincide com a métrica adotada pelo conjunto de normas **IEEE**. É a
definição matematicamente mais simples e a que este projeto usa como
referência, por ser diretamente a que o PRODIST fiscaliza.

**Limites regulatórios (PRODIST, Módulo 8, Seção 8.1):**

| Tensão nominal do ponto de conexão | Limite de FD |
|---|---|
| `Vn ≤ 1,0 kV` (baixa tensão) | **3,0 %** |
| `1,0 kV < Vn < 230 kV` (média/alta tensão) | **2,0 %** |

> **Nota:** o objetivo do projeto (documento de descrição) cita o limiar de
> **2%** como referência de disparo do alarme — esse valor corresponde à
> faixa de média/alta tensão do PRODIST. Para o protótipo de bancada
> (tipicamente em baixa tensão), o limite tecnicamente aplicável seria
> 3,0%. **Decisão de projeto:** manter o limiar configurável no código
> (não *hardcoded*), com **2%** como valor padrão — exatamente como
> proposto na descrição do projeto — permitindo ajustar para 3% ao
> justificar a análise para a banca.

### 4.2 Definição alternativa: NEMA / método CIGRÉ (não adotada como principal)

A norma NEMA MG-1 (voltada a motores) define o desequilíbrio de forma
diferente, usando apenas os módulos das tensões de linha (sem envolver
componentes simétricas):

```
FD_NEMA (%) = (Máximo desvio da tensão média em relação à média) / (Tensão média) × 100
```

Essa definição é mais simples de calcular (não exige a transformada de
Fortescue), mas é uma **aproximação** menos precisa que a definição
PRODIST/IEEE, principalmente porque ignora a informação de fase.

**Decisão de projeto:** este trabalho adota a definição PRODIST/IEC/ANSI
(item 4.1), pois (a) é a exigida pela norma regulatória citada no objetivo
do projeto, e (b) já demanda o cálculo de `V1` e `V2`, que o projeto
precisa calcular de qualquer forma para a análise de componentes
simétricas — reaproveitando o mesmo resultado do decompositor de
Fortescue.

---

## 5. Frequência de amostragem e Nyquist

Para que o algoritmo de Fortescue funcione corretamente sobre um sinal
amostrado (e não sobre um fasor ideal), a taxa de amostragem `fs` precisa
capturar fielmente a forma de onda de 60 Hz. Pelo critério de Nyquist,
`fs > 2 × 60 Hz = 120 Hz` é o mínimo teórico absoluto, mas isso é
insuficiente na prática: com poucas amostras por ciclo, o cálculo de RMS e
de fasor fica impreciso e sensível a ruído.

**Decisão de projeto:** usar, no mínimo, **12 amostras por ciclo**
(referência do firmware ESP32, ~720 Hz para 60 Hz) na fase embarcada, e
**32 amostras por ciclo** (`fs = 1920 Hz`) como padrão na simulação em
Python, valor já implementado como default em `src/gerador.py`. Isso dá
margem confortável acima do mínimo de Nyquist e é consistente com a prática
usual de relés de proteção digitais.

---

## 6. Ruído de medição

Sinais reais medidos por um ADC nunca são senoides perfeitas: há ruído
térmico do circuito de condicionamento, quantização do ADC, interferência
eletromagnética, entre outros. Por isso, `src/gerador.py` permite somar
ruído gaussiano (branco) de desvio padrão configurável (`ruido_std`) aos
sinais sintéticos — isso é essencial para validar que o algoritmo de
Fortescue e o alarme não disparam falsos positivos apenas por causa de
ruído de medição normal, e sim por desequilíbrio real acima do limiar.

---

## 7. Referências

1. ANEEL. **PRODIST — Módulo 8: Qualidade da Energia Elétrica**, Seção 8.1
   (Qualidade do Produto), revisão vigente.
2. FORTESCUE, C. L. "Method of Symmetrical Co-Ordinates Applied to the
   Solution of Polyphase Networks", *Transactions of the American
   Institute of Electrical Engineers*, vol. XXXVII, 1918.
3. Livro-texto de referência da disciplina (a completar com a bibliografia
   indicada pelo professor — ex.: Fuchs & Almeida, *Componentes Simétricas
   Aplicadas a Sistemas Elétricos*, ou Stevenson, *Elementos de Análise de
   Sistemas de Potência*).
4. NEMA MG-1 — definição alternativa de desequilíbrio de tensão (citada
   para contraste, não adotada como definição principal do projeto).

---

## 8. Decisões fechadas nesta etapa (resumo para a banca)

- [x] Definição de FD adotada: **PRODIST/IEC/ANSI** — `FD(%) = 100·|V2|/|V1|`.
- [x] Limiar de alarme padrão: **2%** (configurável; 3% é o limite formal
  para baixa tensão segundo o PRODIST).
- [x] Amostragem: mínimo 12 amostras/ciclo no firmware; 32 amostras/ciclo
  (`fs = 1920 Hz`) na simulação Python.
- [x] Representação de fasores: números complexos nativos do Python
  (`complex`/`numpy`), com a matriz de Fortescue aplicada via multiplicação
  matricial `numpy`, não por equações escritas "na mão".

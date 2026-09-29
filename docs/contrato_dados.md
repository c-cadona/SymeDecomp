# Contrato de Dados — Gerador ↔ Decompositor

Este documento fixa o formato exato de dados trocado entre o Gerador de Sinais
e o Decompositor, definido **antes** de qualquer
linha de código, conforme o gatilho de integração da Etapa 1.A/1.G. O
objetivo é permitir que os dois codem em paralelo sem esperar um pelo outro.

## Formato de saída do gerador

`gerar_sinais_trifasicos(...)` retorna um `dict` Python com as chaves:

| Chave    | Tipo         | Unidade | Descrição                                   |
|----------|--------------|---------|----------------------------------------------|
| `t`      | `np.ndarray` | s       | Vetor de tempo, tamanho `N`                   |
| `va`     | `np.ndarray` | V       | Tensão instantânea da fase A, tamanho `N`     |
| `vb`     | `np.ndarray` | V       | Tensão instantânea da fase B, tamanho `N`     |
| `vc`     | `np.ndarray` | V       | Tensão instantânea da fase C, tamanho `N`     |
| `params` | `dict`       | —       | Eco dos parâmetros usados (auditoria/teste)   |

Onde `N = round(fs * duracao)`, todos os arrays têm o mesmo comprimento `N`
e são alinhados amostra a amostra (`t[i]`, `va[i]`, `vb[i]`, `vc[i]`
correspondem ao mesmo instante).

`params` contém: `amp_a`, `amp_b`, `amp_c`, `fase_a_deg`, `fase_b_deg`,
`fase_c_deg`, `freq`, `fs`, `duracao`, `ruido_std`, `seed`.

## Parâmetros de entrada do gerador

| Parâmetro     | Tipo    | Padrão   | Observação                                        |
|---------------|---------|----------|----------------------------------------------------|
| `amp_a/b/c`   | float   | `1.0`    | Amplitude (pico) de cada fase                       |
| `fase_a_deg`  | float   | `0.0`    | Ângulo da fase A, em graus                          |
| `fase_b_deg`  | float   | `-120.0` | Ângulo da fase B, em graus (sequência positiva)     |
| `fase_c_deg`  | float   | `120.0`  | Ângulo da fase C, em graus (sequência positiva)     |
| `freq`        | float   | `60.0`   | Frequência do sinal, Hz                             |
| `fs`          | float   | `1920.0` | Frequência de amostragem, Hz (deve ser `> 2*freq`)  |
| `duracao`     | float   | `1.0`    | Duração do sinal, s                                 |
| `ruido_std`   | float   | `0.0`    | Desvio padrão do ruído gaussiano de medição, V      |
| `seed`        | int\|None | `None` | Semente do RNG, para reprodutibilidade em testes    |

## Convenção de desequilíbrio

- **Equilíbrio perfeito**: usar os valores padrão (mesma amplitude nas 3
  fases, defasagem exata de 120° entre elas — sequência positiva ABC).
- **Desequilíbrio de amplitude**: variar `amp_a`, `amp_b` e/ou `amp_c`
  independentemente.
- **Desequilíbrio de fase**: variar `fase_b_deg` e/ou `fase_c_deg` para
  valores diferentes de `-120°`/`+120°`.
- **Desequilíbrio misto**: combinar os dois casos acima.

## O que o decompositor pode assumir

1. `va`, `vb`, `vc` e `t` sempre têm o mesmo comprimento.
2. As amostras estão em ordem temporal crescente e igualmente espaçadas
   (`t[i+1] - t[i] == 1/fs`).
3. Os valores são `float64` (padrão do numpy), nunca `None`/`NaN` em
   operação normal.
4. `fs` sempre respeita Nyquist em relação a `freq` (o gerador levanta
   `ValueError` caso contrário — o decompositor não precisa validar isso de
   novo, mas pode assumir que, se recebeu dados, eles são válidos).
5. `params` é somente para depuração/testes; o decompositor **não** deve
   depender de nenhuma chave de `params` para calcular Fortescue — apenas
   de `va`, `vb`, `vc` (e opcionalmente `t`, se precisar de referência de
   tempo real, por exemplo na integração com o firmware).

## Exemplo de uso

```python
from gerador import gerar_sinais_trifasicos

dados = gerar_sinais_trifasicos(amp_b=0.9, freq=60.0, fs=1920.0, duracao=1.0)
# dados["va"], dados["vb"], dados["vc"] -> prontos para o decompositor
resultado = decompor_fortescue(dados["va"], dados["vb"], dados["vc"])
```

## Histórico

- v1 (Etapa 1.A/1.G): contrato inicial, fechado antes do início da
  implementação em paralelo.

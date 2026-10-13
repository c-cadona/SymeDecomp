import math
import sys
from pathlib import Path

import numpy as np
import pytest

# Permite rodar `pytest` a partir da raiz do repo sem instalar o pacote.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from gerador import calcular_rms, gerar_sinais_trifasicos  # noqa: E402


# -----------------
# CONTRATO DE DADOS
# -----------------

def test_formato_retorno():
    """O retorno deve seguir exatamente o contrato de docs/contrato_dados.md."""
    dados = gerar_sinais_trifasicos(duracao=0.1, fs=1920.0)

    assert set(["t", "va", "vb", "vc", "params"]).issubset(dados.keys())
    for chave in ("t", "va", "vb", "vc"):
        assert isinstance(dados[chave], np.ndarray)

    n = len(dados["t"])
    assert len(dados["va"]) == n
    assert len(dados["vb"]) == n
    assert len(dados["vc"]) == n
    # duração=0.1s, fs=1920Hz -> 192 amostras
    assert n == 192


def test_validacao_nyquist():
    """fs abaixo do critério de Nyquist deve levantar erro, não gerar lixo."""
    with pytest.raises(ValueError):
        gerar_sinais_trifasicos(freq=60.0, fs=100.0, duracao=1.0)


def test_validacao_duracao_positiva():
    with pytest.raises(ValueError):
        gerar_sinais_trifasicos(duracao=0.0)


# -------------------
# SISTEMA EQUILIBRADO
# -------------------

def test_sistema_equilibrado_rms_igual():
    """Com amplitudes e defasagens padrão (120°), o RMS deve ser igual
    (dentro de tolerância numérica) nas 3 fases, e bater com Vpico/sqrt(2)."""
    amp = 10.0
    dados = gerar_sinais_trifasicos(
        amp_a=amp, amp_b=amp, amp_c=amp,
        freq=60.0, fs=1920.0, duracao=1.0,  # 1s = 60 ciclos completos
    )

    rms_a = calcular_rms(dados["va"])
    rms_b = calcular_rms(dados["vb"])
    rms_c = calcular_rms(dados["vc"])
    rms_teorico = amp / math.sqrt(2)

    assert rms_a == pytest.approx(rms_teorico, rel=1e-3)
    assert rms_b == pytest.approx(rms_teorico, rel=1e-3)
    assert rms_c == pytest.approx(rms_teorico, rel=1e-3)
    assert rms_a == pytest.approx(rms_b, rel=1e-9)
    assert rms_b == pytest.approx(rms_c, rel=1e-9)


def test_sistema_equilibrado_defasagem_120_graus():
    """As 3 fases devem estar defasadas de 120° entre si (sequência positiva)."""
    dados = gerar_sinais_trifasicos(freq=60.0, fs=19200.0, duracao=1 / 60)

    # Correlação cruzada simplificada: va(t) deve coincidir com
    # vb(t) deslocada de +120° em fase (equivalente a T/3 no tempo).
    t = dados["t"]
    fs = 19200.0
    deslocamento_amostras = int(round(fs * (1 / 60) / 3))  # 1/3 do período

    va_deslocado = np.roll(dados["va"], -deslocamento_amostras)
    # ignora bordas afetadas pelo roll circular
    borda = deslocamento_amostras
    erro = np.abs(va_deslocado[:-borda] - dados["vb"][:-borda])
    assert np.max(erro) < 1e-2


# -------------------
# DESVIO DE AMPLITUDE
# -------------------

@pytest.mark.parametrize("fator", [0.9, 0.8, 1.1])
def test_desequilibrio_amplitude_proporcional(fator):
    """Reduzir/aumentar a amplitude de uma fase por um fator deve refletir
    no RMS dessa fase pelo mesmo fator (dentro de tolerância)."""
    amp_base = 10.0
    dados = gerar_sinais_trifasicos(
        amp_a=amp_base,
        amp_b=amp_base * fator,
        amp_c=amp_base,
        freq=60.0, fs=1920.0, duracao=1.0,
    )

    rms_a = calcular_rms(dados["va"])
    rms_b = calcular_rms(dados["vb"])

    assert rms_b == pytest.approx(rms_a * fator, rel=1e-3)


def test_desequilibrio_amplitude_altera_apenas_fase_afetada():
    """Fases não alteradas continuam com o mesmo RMS entre si."""
    dados = gerar_sinais_trifasicos(
        amp_a=10.0, amp_b=7.0, amp_c=10.0,
        freq=60.0, fs=1920.0, duracao=1.0,
    )
    rms_a = calcular_rms(dados["va"])
    rms_c = calcular_rms(dados["vc"])
    assert rms_a == pytest.approx(rms_c, rel=1e-9)


# ----------------
# RUÍDO DE MEDIÇÃO
# ----------------

def test_ruido_e_reprodutivel_com_seed():
    """Mesma seed -> mesmo ruído -> sinais idênticos (importante p/ testes)."""
    d1 = gerar_sinais_trifasicos(duracao=0.1, ruido_std=0.05, seed=42)
    d2 = gerar_sinais_trifasicos(duracao=0.1, ruido_std=0.05, seed=42)
    np.testing.assert_array_equal(d1["va"], d2["va"])


def test_ruido_aumenta_dispersao():
    """Com ruído, o sinal real deve se afastar do sinal ideal (sem ruído)."""
    limpo = gerar_sinais_trifasicos(duracao=0.5, ruido_std=0.0)
    ruidoso = gerar_sinais_trifasicos(duracao=0.5, ruido_std=0.2, seed=1)

    diferenca = np.std(ruidoso["va"] - limpo["va"])
    assert diferenca > 0.1  # ruído_std=0.2 deve gerar dispersão perceptível


# ----------------
# PUREZA DA FUNÇÃO
# ----------------

def test_funcao_e_pura():
    """Chamar duas vezes com os mesmos parâmetros (sem seed) deve gerar
    sinais deterministicamente iguais quando ruido_std=0."""
    d1 = gerar_sinais_trifasicos(amp_a=5.0, duracao=0.2)
    d2 = gerar_sinais_trifasicos(amp_a=5.0, duracao=0.2)
    np.testing.assert_array_equal(d1["va"], d2["va"])
    np.testing.assert_array_equal(d1["t"], d2["t"])

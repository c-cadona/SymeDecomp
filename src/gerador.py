from __future__ import annotations

import numpy as np


def gerar_sinais_trifasicos(
    amp_a: float = 1.0,
    amp_b: float = 1.0,
    amp_c: float = 1.0,
    fase_a_deg: float = 0.0,
    fase_b_deg: float = -120.0,
    fase_c_deg: float = 120.0,
    freq: float = 60.0,
    fs: float = 1920.0,
    duracao: float = 1.0,
    ruido_std: float = 0.0,
    seed: int | None = None,
) -> dict:
    if fs <= 2 * freq:
        raise ValueError(
            f"fs={fs} Hz não respeita Nyquist para freq={freq} Hz "
            f"(fs deve ser > 2*freq)."
        )
    if duracao <= 0:
        raise ValueError("duracao deve ser positiva.")
    if fs <= 0:
        raise ValueError("fs deve ser positiva.")

    n_amostras = int(round(fs * duracao))
    t = np.arange(n_amostras) / fs

    w = 2.0 * np.pi * freq
    fase_a = np.deg2rad(fase_a_deg)
    fase_b = np.deg2rad(fase_b_deg)
    fase_c = np.deg2rad(fase_c_deg)

    va = amp_a * np.sin(w * t + fase_a)
    vb = amp_b * np.sin(w * t + fase_b)
    vc = amp_c * np.sin(w * t + fase_c)

    if ruido_std > 0.0:
        rng = np.random.default_rng(seed)
        va = va + rng.normal(0.0, ruido_std, n_amostras)
        vb = vb + rng.normal(0.0, ruido_std, n_amostras)
        vc = vc + rng.normal(0.0, ruido_std, n_amostras)

    return {
        "t": t,
        "va": va,
        "vb": vb,
        "vc": vc,
        "params": {
            "amp_a": amp_a,
            "amp_b": amp_b,
            "amp_c": amp_c,
            "fase_a_deg": fase_a_deg,
            "fase_b_deg": fase_b_deg,
            "fase_c_deg": fase_c_deg,
            "freq": freq,
            "fs": fs,
            "duracao": duracao,
            "ruido_std": ruido_std,
            "seed": seed,
        },
    }


def calcular_rms(sinal: np.ndarray) -> float:
    """RMS (valor eficaz) de um array de amostras."""
    return float(np.sqrt(np.mean(np.asarray(sinal, dtype=float) ** 2)))


if __name__ == "__main__":
    # Exemplo rápido de uso manual (não substitui os testes em pytest).
    dados = gerar_sinais_trifasicos(amp_b=0.9, duracao=0.05)
    print("RMS va:", calcular_rms(dados["va"]))
    print("RMS vb:", calcular_rms(dados["vb"]))
    print("RMS vc:", calcular_rms(dados["vc"]))

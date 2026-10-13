# Analisador de Componentes Simétricas em Tempo Real para Redes Trifásicas

Projeto da disciplina **Projeto Nível I em Eletrônica Pot. e Acion. III**

**Alunos:** Arthur Augusto Dahlke e Guilherme Cadona da Silva
**Matrícula:** 24105025 / 23100665

## Descrição

Sistema capaz de decompor tensões trifásicas em suas componentes de
sequência (positiva, negativa e zero) utilizando a transformada de
Fortescue, com o objetivo de detectar desequilíbrio de tensão em tempo real
e disparar um alarme quando o fator de desequilíbrio ultrapassar o limiar
de 2% definido pelo PRODIST (Módulo 8).

O desenvolvimento é feito em duas grandes fases:
1. **Simulação computacional** (Python) — validação do algoritmo e da
   lógica de alarme com sinais sintéticos.
2. **Implementação física** (ESP32 + ADC) — leitura de sinais reais, caso
   haja tempo hábil no cronograma.

## Estrutura do repositório

```
.
├── src/            # Código-fonte principal (gerador, decompositor, pipeline)
├── tests/          # Testes automatizados (pytest)
├── docs/           # Documentação teórica e contratos de dados
├── app/            # Interface Streamlit (Fase 2)
├── firmware/       # Firmware ESP32 (Fase 3-4)
├── requirements.txt
└── README.md
```

## Como rodar

### 1. Ambiente

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Gerador de sinais (exemplo rápido)

```bash
python src/gerador.py
```

### 3. Testes

```bash
pytest tests/ -v
```

## Status do projeto

- [x] Etapa 0.1 — Base matemática e normativa
- [x] Etapa 1.A — Gerador de sinais sintéticos
- [ ] Etapa 1.G — Decompositor de Fortescue + fator de desequilíbrio + alarme
- [ ] Etapa 1.INT — Primeira integração (pipeline completo)
- [ ] Fase 2 — Interface Streamlit
- [ ] Fase 3 — Sensores e firmware ESP32
- [ ] Fase 4 — Algoritmo embarcado e alarme físico
- [ ] Fase 5 — Relatório final

## Documentação

- [`docs/teoria.md`](docs/teoria.md) — fundamentação teórica e definição do
  fator de desequilíbrio adotada.
- [`docs/contrato_dados.md`](docs/contrato_dados.md) — contrato de dados
  entre gerador e decompositor.

## Convenções de trabalho (Git)

- `main` sempre estável — só recebe merge via Pull Request.
- 1 branch por etapa: `feature/<iniciais>-<nome-curto>` (ex.:
  `feature/A-gerador-sinais`, `feature/G-decompositor`).
- PR obrigatório com revisão cruzada (quem não escreveu revisa).
- Commits pequenos e frequentes, explicando o "porquê".

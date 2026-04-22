### ARQUIVO: .github/workflows/project-gate.yml
name: project-gate

on:
  push:
  pull_request:

jobs:
  gate:
    runs-on: windows-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v5

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Show Python version
        run: python --version

      - name: Upgrade pip
        run: python -m pip install --upgrade pip

      - name: Install pytest
        run: pip install pytest

      - name: Install project dependencies
        shell: pwsh
        run: |
          if (Test-Path requirements.txt) {
            pip install -r requirements.txt
          }
          if (Test-Path requirements-dev.txt) {
            pip install -r requirements-dev.txt
          }
          if (Test-Path pyproject.toml) {
            try {
              pip install .
            } catch {
              Write-Host "Failed to install from pyproject.toml, continuing..."
            }
          }
          if (Test-Path setup.py) {
            try {
              pip install .
            } catch {
              Write-Host "Failed to install from setup.py, continuing..."
            }
          }

      - name: Show installed packages
        run: pip list

      - name: Run regression tests
        run: python -m pytest tests/test_analysis_orchestrator_regression.py -q

      - name: Run integration tests
        run: python -m pytest tests/test_analysis_orchestrator_integration.py -q

### ARQUIVO: README_GATE.md
# Gate do Projeto SharkNovo

O gate do projeto valida a integridade e funcionalidade do sistema de análise, garantindo que mudanças em orchestrator, inputs, schemas e regras não quebrem o comportamento esperado.

## Execução Local

Para executar o gate localmente, use um dos comandos abaixo:

- `python scripts/run_project_gate.py`
- `powershell -ExecutionPolicy Bypass -File scripts/run_project_gate.ps1`

## Interpretação de Falhas

- **Falha na regressão**: Indica que testes de regressão falharam, significando que funcionalidades existentes foram quebradas por mudanças recentes.
- **Falha na integração**: Indica que testes de integração falharam, significando problemas na interação entre componentes do sistema.

## Quando Executar

Execute o gate antes de qualquer mudança em orchestrator, inputs, schemas ou regras para evitar regressões.

## CI

O workflow de CI roda automaticamente em eventos de `push` e `pull_request`, executando os mesmos testes no ambiente Windows com Python 3.10.
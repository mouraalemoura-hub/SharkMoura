# Bloco para evitar erro de encoding no CI Windows (GitHub Actions)
# Usa apenas ASCII e marcadores [OK], [WARN], [ERRO]

import sys
from pathlib import Path


def print_status(status: str, message: str) -> None:
    """Imprime mensagem padronizada com flush para CI."""
    print(f'[{status}] {message}', flush=True)


root = Path.cwd()
print_status('INFO', f'Raiz detectada: {root}')

# Validacoes obrigatorias
if not (root / 'scripts').exists():
    print_status('ERRO', "Pasta 'scripts/' obrigatoria nao encontrada.")
    sys.exit(1)

if not (root / '.github').exists():
    print_status('ERRO', ".Pasta '.github/' obrigatoria nao encontrada.")
    sys.exit(1)

# Validacoes opcionais
if not (root / 'app').exists():
    print_status('WARN', "Pasta 'app/' nao encontrada (opcional).")

if not (root / 'tests').exists():
    print_status('WARN', "Pasta 'tests/' nao encontrada (opcional).")

print_status('OK', 'Estrutura do projeto validada com sucesso.')

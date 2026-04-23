from pathlib import Path
import sys

# Substitui a validação antiga da raiz do projeto.
# Marcadores mínimos: 'scripts/' e '.github/'. 'app/' e 'tests/' são opcionais.

script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent

print(f"Raiz do projeto detectada: {project_root}")

# Validar marcadores mínimos
markers = ["scripts", ".github"]
for marker in markers:
    marker_path = project_root / marker
    if not marker_path.is_dir():
        print(f"Erro: Marcador '{marker}' não encontrado. Verifique a raiz do projeto.")
        sys.exit(1)

# Validar opcionais
app_path = project_root / "app"
if app_path.is_dir():
    print("\u2713 Pasta 'app/' encontrada.")
else:
    print("\u26a0 Pasta 'app/' não encontrada (opcional).")

tests_path = project_root / "tests"
if tests_path.is_dir():
    print("\u2713 Pasta 'tests/' encontrada.")
else:
    print("\u26a0 Pasta 'tests/' não encontrada (opcional).")

print("Validação da raiz concluída.")

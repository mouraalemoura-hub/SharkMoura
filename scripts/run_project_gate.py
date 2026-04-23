#!/usr/bin/env python3
"""
Script para executar os testes de gate do projeto SharkNovo.
Detecta a raiz do projeto de forma robusta e executa testes específicos.
"""

import sys
from pathlib import Path
import subprocess


def is_project_root(path: Path) -> bool:
    """Verifica se o caminho é a raiz do projeto checando por 'app' e 'tests'."""
    return path.is_dir() and (path / 'app').is_dir() and (path / 'tests').is_dir()


def find_project_root() -> Path:
    """Encontra a raiz do projeto subindo diretórios até encontrar 'app' e 'tests'."""
    # Primeiro, tenta o diretório pai de scripts/
    candidate = Path(__file__).resolve().parents[1]
    if is_project_root(candidate):
        return candidate
    
    # Se não, sobe diretórios
    current = Path(__file__).resolve().parent
    while current.parent != current:
        if is_project_root(current):
            return current
        current = current.parent
    
    raise FileNotFoundError("Raiz do projeto não encontrada. Verifique se 'app' e 'tests' existem.")


def run_step(title: str, command: list, cwd: Path):
    """Executa um passo, imprime o título e falha se o comando falhar."""
    print(f"Executando: {title}")
    result = subprocess.run(command, cwd=cwd)
    if result.returncode != 0:
        print(f"Falha em: {title}")
        sys.exit(result.returncode)


def main():
    """Função principal para detectar raiz e executar testes."""
    try:
        project_root = find_project_root()
        print(f"Raiz do projeto detectada: {project_root}")
        
        # Comando base para pytest
        python_exe = sys.executable
        
        # Executar testes de regressão
        run_step(
            "Testes de regressão",
            [python_exe, "-m", "pytest", "tests/test_analysis_orchestrator_regression.py", "-q"],
            project_root
        )
        
        # Executar testes de integração
        run_step(
            "Testes de integração",
            [python_exe, "-m", "pytest", "tests/test_analysis_orchestrator_integration.py", "-q"],
            project_root
        )
        
        print("Todos os testes passaram com sucesso!")
    
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

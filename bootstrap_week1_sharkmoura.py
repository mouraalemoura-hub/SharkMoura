# bootstrap_week1_sharkmoura.py
"""
Bootstrap documental fiel da Semana 1 do projeto SharkMoura 2.0.

Este script preserva exatamente o estado já validado do repositório,
normalizando arquivos oficiais para line endings '\n' e garantindo
quebra de linha final. Opera de forma idempotente, validando a
presença de todos os arquivos oficiais antes de qualquer escrita.

Arquivos oficiais processados:
- README_WEEK1.md
- docs/01_inventario_funcional_legado.md
- docs/02_matriz_comparativa_v1813_v1818.md
- docs/03_contrato_dados_ativo.md
- docs/04_contrato_dados_opcoes.md
- docs/05_payloads_oficiais_sistema.md
- docs/06_decisoes_fechadas_semana_1.md
- docs/07_fechamento_oficial_semana_1.md
- schemas/pydantic_models.py
- scripts/validate_pydantic_models.py

Uso: execute na raiz do projeto para materializar a Semana 1.
"""

from pathlib import Path
from textwrap import dedent
import os

OFFICIAL_FILES = [
    "README_WEEK1.md",
    "docs/01_inventario_funcional_legado.md",
    "docs/02_matriz_comparativa_v1813_v1818.md",
    "docs/03_contrato_dados_ativo.md",
    "docs/04_contrato_dados_opcoes.md",
    "docs/05_payloads_oficiais_sistema.md",
    "docs/06_decisoes_fechadas_semana_1.md",
    "docs/07_fechamento_oficial_semana_1.md",
    "schemas/pydantic_models.py",
    "scripts/validate_pydantic_models.py",
]


def _normalize_text(text: str) -> str:
    """Normaliza o texto para \\n e garante quebra final."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.endswith("\n"):
        normalized += "\n"
    return normalized


def _read_text_file(path_str: str) -> str:
    """Lê um arquivo texto em UTF-8."""
    path = Path(path_str)
    return path.read_text(encoding="utf-8")


def _write_text_file(path_str: str, content: str) -> dict[str, object]:
    """Escreve um arquivo texto criando diretórios quando necessário."""
    path = Path(path_str)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return {
        "path": str(path),
        "characters": len(content),
        "bytes": len(content.encode("utf-8")),
    }


def build_documents() -> dict[str, str]:
    """Lê e normaliza os arquivos oficiais existentes."""
    docs: dict[str, str] = {}
    for file_path in OFFICIAL_FILES:
        docs[file_path] = _normalize_text(_read_text_file(file_path))
    return docs


def write_documents(docs: dict[str, str]) -> list[dict[str, object]]:
    """Regrava os documentos de forma idempotente."""
    written: list[dict[str, object]] = []
    for path_str, content in docs.items():
        written.append(_write_text_file(path_str, content))
    return written


def print_summary(written: list[dict[str, object]]) -> None:
    """Imprime resumo dos arquivos materializados."""
    for item in written:
        print(
            f"{item['path']} | caracteres={item['characters']} | bytes={item['bytes']}"
        )
    print("Semana 1 materializada com sucesso.")


def main() -> None:
    """Executa a materialização fiel da Semana 1."""
    project_root = Path(__file__).resolve().parent
    os.chdir(project_root)

    missing = [file_path for file_path in OFFICIAL_FILES if not Path(file_path).exists()]
    if missing:
        missing_list = "\n".join(f"- {item}" for item in missing)
        raise FileNotFoundError(
            dedent(
                f"""
                Não é possível materializar a Semana 1 porque faltam arquivos oficiais.

                Arquivos ausentes:
                {missing_list}
                """
            ).strip()
        )

    docs = build_documents()
    written = write_documents(docs)
    print_summary(written)


if __name__ == "__main__":
    main()
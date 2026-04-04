# Contrato de Dados para Ativo

## Estrutura Geral

O contrato define os campos obrigatórios e opcionais para análise de ativos, incluindo ticker, período e payloads aninhados.

## Campos Obrigatórios
- Ticker: Identificador único do ativo.
- Analysis Date: Data da análise.
- Reference Meta: Metadados de referência.

## Payloads Opcionais
- Trend, Structure, Liquidity, etc., conforme definido nos modelos Pydantic.

## Validações

Inclui validações de tipos, ranges e consistências, como preços positivos e datas lógicas.

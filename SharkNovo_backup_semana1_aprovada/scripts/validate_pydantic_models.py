from __future__ import annotations

import sys
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable

# Garante import a partir da raiz do projeto
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from schemas.pydantic_models import (
    AssetAnalysisPayload,
    EntryProjectionPayload,
    FinalSystemPayload,
    LegacyScorePayload,
    LiquidityMapPayload,
    OptionsSelectionPayload,
    ReferenceMeta,
    RegimeV1Payload,
    ScoreAtivoV2Payload,
    StructurePayload,
    SuggestedOptionPayload,
    TrendBasePayload,
    VolatilityTimingPayload,
    WeeklyAdequacyPayload,
)


FIXED_DATE = date(2026, 4, 3)
FIXED_EXPIRATION = date(2026, 5, 16)
FIXED_DATETIME = datetime(2026, 4, 3, 10, 0, 0)


def run_test(name: str, fn) -> dict[str, object]:
    """Executa um teste e captura o resultado."""
    try:
        fn()
        return {"name": name, "success": True, "error": None}
    except Exception as exc:
        return {"name": name, "success": False, "error": str(exc)}


def expect_success(name: str, fn) -> dict[str, object]:
    """Espera que o teste passe."""
    result = run_test(name, fn)
    if result["success"]:
        print(f"[OK] {name}")
    else:
        print(f"[FAIL] {name}: {result['error']}")
    return result


def expect_failure(name: str, fn, expected_exception=Exception) -> dict[str, object]:
    """Espera que o teste falhe."""
    try:
        fn()
    except expected_exception:
        print(f"[OK] {name}")
        return {"name": name, "success": True, "error": None}
    except Exception as exc:
        print(f"[FAIL] {name}: exceção inesperada: {exc}")
        return {"name": name, "success": False, "error": str(exc)}

    print(f"[FAIL] {name}: esperava falha, mas passou")
    return {"name": name, "success": False, "error": "esperava falha, mas passou"}


def build_reference_meta() -> ReferenceMeta:
    return ReferenceMeta.model_validate(
        {
            "Preco_ref": "100.1234567",
            "Data_Referencia": FIXED_DATE,
            "Regra_Referencia": "CLOSE",
        }
    )


def build_trend() -> TrendBasePayload:
    return TrendBasePayload.model_validate(
        {
            "Infer_Direction": "COMPRA",
            "Direcao_Inst": "COMPRA",
            "W1_Trend": "UP",
            "H1_Trend": "DOWN",
            "Slope_EMA200": 1.25,
        }
    )


def build_structure() -> StructurePayload:
    return StructurePayload.model_validate(
        {
            "SMC_Structure": "BULL",
            "SMC_Last_BOS": "UP",
            "SMC_Last_CHOCH": True,
            "SMC_PD_Area": "DISCOUNT",
            "SMC_PD50": "99.50",
            "SMC_PD_Value": 0.55,
            "SMC_OB_Type": "breaker",
            "SMC_OB_Refine": "98.75",
            "SMC_FVG_Side": "UP",
            "SMC_FVG_Mid": "100.25",
            "SMC_FVG_Size_ATR": 0.42,
        }
    )


def build_liquidity() -> LiquidityMapPayload:
    return LiquidityMapPayload.model_validate(
        {
            "EQ_High": "105.00",
            "EQ_Low": "95.00",
            "PDH": "104.00",
            "PDL": "96.00",
            "PWH": "106.00",
            "PWL": "94.00",
            "Liq_Side": "ABOVE",
            "Liq_Target_1": "104.50",
            "Liq_Target_2": "105.50",
        }
    )


def build_volatility() -> VolatilityTimingPayload:
    return VolatilityTimingPayload.model_validate(
        {
            "ATR14": 1.2,
            "RSI14": 63.4,
            "MACD": 0.8,
            "MACD_hist": 0.2,
            "BB_percent_b": 0.88,
            "BB_bandwidth": 0.14,
            "FFFD": True,
            "FFFD_side": "LONG",
            "FFFD_note": "timing tático favorável",
            "W1_context": "continuidade semanal",
            "H1_entry_hint": "pullback leve",
            "TickVolume_ZScore": 1.6,
            "HV_21": 22.7,
        }
    )


def build_projection() -> EntryProjectionPayload:
    return EntryProjectionPayload.model_validate(
        {
            "Preco_ref": "100.00",
            "Entrada_Sugerida": "100.50",
            "Entrada_Primaria": "100.25",
            "Entrada_Secundaria": "99.90",
            "Prob_Fill_Prim": "alta",
            "Prob_Fill_Sec": "média",
            "Tags_Entrada_Prim": ["pullback", "", "fvg"],
            "Tags_Entrada_Sec": ["discount", " "],
            "T1": "102.00",
            "T2": "104.00",
            "T3": "106.00",
            "Stop_Inst": "98.90",
            "Stop_Loss": "98.50",
            "Risk_Reward_Ratio": 2.4,
            "RR_T2_Prim": 1.8,
            "RR_T2_Sec": 2.1,
            "Alvo_Sexta_T1": "101.80",
            "Alvo_Semana": "105.00",
            "Faixa_Semana_Alta": "106.50",
            "Faixa_Semana_Baixa": "97.80",
        }
    )


def build_legacy_score() -> LegacyScorePayload:
    return LegacyScorePayload.model_validate(
        {
            "Confluencia_Score_SMC": 78.0,
            "Confluencia_Score": 74.0,
            "Probabilidade_Perc": 81.0,
            "Setup_Tag": "pullback_smc",
            "Veredito": "OURO",
            "Racional": "Confluência estrutural com timing favorável.",
        }
    )


def build_score_v2() -> ScoreAtivoV2Payload:
    return ScoreAtivoV2Payload.model_validate(
        {
            "score_bruto": 84.0,
            "score_ajustado": 79.0,
            "score_final_ativo": 76.0,
            "score_tendencia": 82.0,
            "score_estrutura": 80.0,
            "score_volatilidade": 74.0,
            "score_localizacao": 78.0,
            "score_timing": 77.0,
            "penalidades_aplicadas": ["spread amplo", "", "liquidez parcial"],
            "teto_aplicado": 90.0,
            "racional_score": "Ajuste conservador por contexto intrassemanal.",
        }
    )


def build_regime() -> RegimeV1Payload:
    return RegimeV1Payload.model_validate(
        {
            "regime_principal": "TENDENCIA_ALTA",
            "regime_bias": "COMPRA",
            "regime_strength": 73.0,
            "regime_flags": ["tendência limpa", "", "w1 alinhado"],
            "regime_conflicts": ["h1 esticado", ""],
            "regime_rationale": "Regime favorável, porém sem maturidade total.",
        }
    )


def build_weekly_adequacy() -> WeeklyAdequacyPayload:
    return WeeklyAdequacyPayload.model_validate(
        {
            "Horizon_bdays": 5,
            "adequacao_semanal_status": "ADEQUADA_COM_RESSALVAS",
            "adequacao_semanal_score": 72.0,
            "tempo_status": "tempo suficiente",
            "espaco_status": "espaço moderado",
            "deslocamento_status": "deslocamento plausível",
            "maturidade_status": "maturidade média",
            "motivos_positivos": ["w1 alinhado", "", "alvo plausível"],
            "motivos_negativos": ["sexta já próxima", ""],
            "alvo_semanal_plausivel": True,
            "racional_adequacao": "Cenário aceitável, mas não ideal.",
        }
    )


def build_option() -> SuggestedOptionPayload:
    return SuggestedOptionPayload.model_validate(
        {
            "Codigo_Opcao": "valeA123",
            "Tipo_Opcao": "CALL",
            "Sugestao_Strike": "102.00",
            "Vencimento": FIXED_EXPIRATION,
            "Premio": 2.35,
            "delta": 0.48,
            "Open_Interest": 2500,
            "spread": 0.12,
            "Stop_Loss": "1.20",
            "Alvo_Sexta_T1": "3.10",
            "Risk_Reward_Ratio": 2.1,
            "Racional_Opcao": "Melhor equilíbrio entre prêmio e sensibilidade.",
        }
    )


def build_asset() -> AssetAnalysisPayload:
    return AssetAnalysisPayload.model_validate(
        {
            "Ticker": "vale3",
            "Periodo": "D1",
            "Data_Analise": FIXED_DATETIME,
            "reference_meta": build_reference_meta(),
            "trend": build_trend(),
            "structure": build_structure(),
            "liquidity_map": build_liquidity(),
            "volatility_timing": build_volatility(),
            "projection": build_projection(),
            "legacy_score": build_legacy_score(),
            "score_v2": build_score_v2(),
            "regime_v1": build_regime(),
            "weekly_adequacy": build_weekly_adequacy(),
            "Veredito": "OURO",
            "Notas": "Payload mínimo realista da Semana 1.",
        }
    )


def build_options_selection() -> OptionsSelectionPayload:
    return OptionsSelectionPayload.model_validate(
        {
            "Ticker": "vale3",
            "Lado_Base": "COMPRA",
            "Opcoes_Sugeridas": [build_option()],
            "Notas_Selecao": "Seleção inicial coerente com a tese base.",
        }
    )


# 1. ReferenceMeta sucesso
def test_01_reference_meta_success() -> None:
    ref = build_reference_meta()
    if ref.price_ref != Decimal("100.123457"):
        raise ValueError(f"quantização inesperada: {ref.price_ref}")
    if ref.ref_date != FIXED_DATE:
        raise ValueError("ref_date incorreta")
    if ref.ref_rule != "CLOSE":
        raise ValueError("ref_rule incorreta")


# 2. ReferenceMeta Decimal quantizado
def test_02_reference_meta_quantization() -> None:
    ref = build_reference_meta()
    if ref.price_ref != Decimal("100.123457"):
        raise ValueError("Decimal não quantizado corretamente")


# 3. ReferenceMeta falha preço zero
def test_03_reference_meta_zero_price() -> None:
    ReferenceMeta.model_validate(
        {
            "Preco_ref": "0",
            "Data_Referencia": FIXED_DATE,
            "Regra_Referencia": "CLOSE",
        }
    )


# 4. TrendBasePayload aliases reais
def test_04_trend_success() -> None:
    trend = build_trend()
    if trend.infer_direction != "COMPRA":
        raise ValueError("infer_direction incorreto")
    if trend.direcao_inst != "COMPRA":
        raise ValueError("direcao_inst incorreto")
    if trend.w1_trend != "UP":
        raise ValueError("w1_trend incorreto")
    if trend.h1_trend != "DOWN":
        raise ValueError("h1_trend incorreto")


# 5. StructurePayload sucesso
def test_05_structure_success() -> None:
    structure = build_structure()
    if structure.smc_structure != "BULL":
        raise ValueError("smc_structure incorreto")
    if structure.smc_pd_value != 0.55:
        raise ValueError("smc_pd_value incorreto")


# 6. StructurePayload falha com pd_value > 1
def test_06_structure_invalid_pd_value() -> None:
    StructurePayload.model_validate(
        {
            "SMC_PD_Value": 1.2,
        }
    )


# 7. StructurePayload uppercase em ob_type
def test_07_structure_ob_type_uppercase() -> None:
    structure = build_structure()
    if structure.smc_ob_type != "BREAKER":
        raise ValueError("smc_ob_type não foi normalizado para uppercase")


# 8. LiquidityMapPayload sucesso
def test_08_liquidity_success() -> None:
    liq = build_liquidity()
    if liq.liq_side != "ABOVE":
        raise ValueError("liq_side incorreto")
    if liq.eq_high != Decimal("105.00"):
        raise ValueError("eq_high incorreto")


# 9. VolatilityTimingPayload sucesso
def test_09_volatility_success() -> None:
    vol = build_volatility()
    if vol.rsi14 != 63.4:
        raise ValueError("rsi14 incorreto")
    if vol.fffd_side != "LONG":
        raise ValueError("fffd_side incorreto")


# 10. VolatilityTimingPayload falha RSI > 100
def test_10_volatility_invalid_rsi() -> None:
    VolatilityTimingPayload.model_validate(
        {
            "RSI14": 101,
        }
    )


# 11. VolatilityTimingPayload falha BB_percent_b > 1.5
def test_11_volatility_invalid_bb() -> None:
    VolatilityTimingPayload.model_validate(
        {
            "BB_percent_b": 1.6,
        }
    )


# 12. VolatilityTimingPayload falha ATR negativo
def test_12_volatility_invalid_atr() -> None:
    VolatilityTimingPayload.model_validate(
        {
            "ATR14": -1,
        }
    )


# 13. EntryProjectionPayload sucesso
def test_13_projection_success() -> None:
    proj = build_projection()
    if proj.risk_reward_ratio != 2.4:
        raise ValueError("risk_reward_ratio incorreto")


# 14. EntryProjectionPayload limpa tags
def test_14_projection_clean_tags() -> None:
    proj = build_projection()
    if proj.tags_entrada_prim != ["pullback", "fvg"]:
        raise ValueError(f"tags_entrada_prim incorretas: {proj.tags_entrada_prim}")
    if proj.tags_entrada_sec != ["discount"]:
        raise ValueError(f"tags_entrada_sec incorretas: {proj.tags_entrada_sec}")


# 15. EntryProjectionPayload falha Stop_Inst == Entrada_Sugerida
def test_15_projection_stop_inst_equals_entry() -> None:
    EntryProjectionPayload.model_validate(
        {
            "Entrada_Sugerida": "100.50",
            "Stop_Inst": "100.50",
        }
    )


# 16. EntryProjectionPayload falha Stop_Loss == Preco_ref
def test_16_projection_stop_loss_equals_preco_ref() -> None:
    EntryProjectionPayload.model_validate(
        {
            "Preco_ref": "100.00",
            "Stop_Loss": "100.00",
        }
    )


# 17. EntryProjectionPayload falha RR negativo
def test_17_projection_negative_rr() -> None:
    EntryProjectionPayload.model_validate(
        {
            "Risk_Reward_Ratio": -1,
        }
    )


# 18. LegacyScorePayload sucesso
def test_18_legacy_score_success() -> None:
    score = build_legacy_score()
    if score.probabilidade_perc != 81.0:
        raise ValueError("probabilidade_perc incorreta")


# 19. LegacyScorePayload uppercase em Setup_Tag
def test_19_legacy_score_setup_tag_upper() -> None:
    score = build_legacy_score()
    if score.setup_tag != "PULLBACK_SMC":
        raise ValueError("setup_tag não foi normalizado")


# 20. LegacyScorePayload falha probabilidade > 100
def test_20_legacy_score_invalid_prob() -> None:
    LegacyScorePayload.model_validate(
        {
            "Probabilidade_Perc": 120,
        }
    )


# 21. ScoreAtivoV2Payload sucesso
def test_21_score_v2_success() -> None:
    score = build_score_v2()
    if score.score_bruto != 84.0:
        raise ValueError("score_bruto incorreto")


# 22. ScoreAtivoV2Payload limpa penalidades
def test_22_score_v2_clean_penalties() -> None:
    score = build_score_v2()
    if score.penalidades_aplicadas != ["spread amplo", "liquidez parcial"]:
        raise ValueError("penalidades_aplicadas não foram limpas")


# 23. ScoreAtivoV2Payload falha score_ajustado > score_bruto
def test_23_score_v2_invalid_adjusted() -> None:
    ScoreAtivoV2Payload.model_validate(
        {
            "score_bruto": 60,
            "score_ajustado": 70,
        }
    )


# 24. ScoreAtivoV2Payload falha score_final_ativo > teto_aplicado
def test_24_score_v2_invalid_final() -> None:
    ScoreAtivoV2Payload.model_validate(
        {
            "score_final_ativo": 95,
            "teto_aplicado": 90,
        }
    )


# 25. RegimeV1Payload sucesso
def test_25_regime_success() -> None:
    reg = build_regime()
    if reg.regime_flags != ["tendência limpa", "w1 alinhado"]:
        raise ValueError("regime_flags não foram limpas")


# 26. RegimeV1Payload falha regime_strength > 100
def test_26_regime_invalid_strength() -> None:
    RegimeV1Payload.model_validate(
        {
            "regime_strength": 101,
        }
    )


# 27. WeeklyAdequacyPayload sucesso
def test_27_weekly_success() -> None:
    week = build_weekly_adequacy()
    if week.horizon_bdays != 5:
        raise ValueError("horizon_bdays incorreto")


# 28. WeeklyAdequacyPayload limpa listas
def test_28_weekly_clean_lists() -> None:
    week = build_weekly_adequacy()
    if week.motivos_positivos != ["w1 alinhado", "alvo plausível"]:
        raise ValueError("motivos_positivos não foram limpos")
    if week.motivos_negativos != ["sexta já próxima"]:
        raise ValueError("motivos_negativos não foram limpos")


# 29. WeeklyAdequacyPayload falha score > 100
def test_29_weekly_invalid_score() -> None:
    WeeklyAdequacyPayload.model_validate(
        {
            "adequacao_semanal_score": 101,
        }
    )


# 30. SuggestedOptionPayload sucesso
def test_30_option_success() -> None:
    opt = build_option()
    if opt.delta != 0.48:
        raise ValueError("delta incorreto")


# 31. SuggestedOptionPayload uppercase em Codigo_Opcao
def test_31_option_code_uppercase() -> None:
    opt = build_option()
    if opt.codigo_opcao != "VALEA123":
        raise ValueError("codigo_opcao não foi normalizado")


# 32. SuggestedOptionPayload falha delta > 1
def test_32_option_invalid_delta() -> None:
    SuggestedOptionPayload.model_validate(
        {
            "Codigo_Opcao": "abc1",
            "delta": 1.2,
        }
    )


# 33. SuggestedOptionPayload falha strike <= 0
def test_33_option_invalid_strike() -> None:
    SuggestedOptionPayload.model_validate(
        {
            "Codigo_Opcao": "abc1",
            "Sugestao_Strike": 0,
        }
    )


# 34. AssetAnalysisPayload sucesso mínimo realista
def test_34_asset_success() -> None:
    asset = build_asset()
    if asset.ticker != "VALE3":
        raise ValueError("ticker não foi normalizado")


# 35. AssetAnalysisPayload ticker uppercase
def test_35_asset_ticker_uppercase() -> None:
    asset = build_asset()
    if asset.ticker != "VALE3":
        raise ValueError("ticker deveria estar em uppercase")


# 36. AssetAnalysisPayload falha ref_date > analysis_date.date()
def test_36_asset_invalid_ref_date() -> None:
    AssetAnalysisPayload.model_validate(
        {
            "Ticker": "vale3",
            "Periodo": "D1",
            "Data_Analise": FIXED_DATETIME,
            "reference_meta": {
                "Preco_ref": "100.00",
                "Data_Referencia": FIXED_EXPIRATION,
                "Regra_Referencia": "CLOSE",
            },
            "trend": {},
            "structure": {},
            "liquidity_map": {},
            "volatility_timing": {},
            "projection": {},
            "legacy_score": {},
        }
    )


# 37. OptionsSelectionPayload sucesso mínimo
def test_37_options_selection_success() -> None:
    sel = build_options_selection()
    if len(sel.opcoes_sugeridas) != 1:
        raise ValueError("opcoes_sugeridas incorreto")


# 38. OptionsSelectionPayload ticker uppercase
def test_38_options_selection_ticker_uppercase() -> None:
    sel = build_options_selection()
    if sel.ticker != "VALE3":
        raise ValueError("ticker da seleção não foi normalizado")


# 39. FinalSystemPayload sucesso sem opções
def test_39_final_without_options() -> None:
    final_payload = FinalSystemPayload.model_validate(
        {
            "Versao_Sistema": "2.0",
            "Gerado_Em": FIXED_DATETIME,
            "Ativo": build_asset(),
            "Opcoes": None,
            "Observacoes_Exportacao": "sem opções nesta execução",
        }
    )
    if final_payload.options is not None:
        raise ValueError("options deveria ser None")


# 40. FinalSystemPayload sucesso com opções
def test_40_final_with_options() -> None:
    final_payload = FinalSystemPayload.model_validate(
        {
            "Versao_Sistema": "2.0",
            "Gerado_Em": FIXED_DATETIME,
            "Ativo": build_asset(),
            "Opcoes": build_options_selection(),
            "Observacoes_Exportacao": "com opções nesta execução",
        }
    )
    if final_payload.options is None:
        raise ValueError("options não deveria ser None")


# 41. Dump com alias Preco_ref
def test_41_dump_reference_alias() -> None:
    dumped = build_reference_meta().model_dump(by_alias=True)
    if "Preco_ref" not in dumped:
        raise ValueError("alias Preco_ref ausente no dump")


# 42. Dump com alias Ticker
def test_42_dump_asset_alias() -> None:
    dumped = build_asset().model_dump(by_alias=True)
    if "Ticker" not in dumped:
        raise ValueError("alias Ticker ausente no dump")


# 43. Dump com alias Ativo
def test_43_dump_final_alias() -> None:
    dumped = FinalSystemPayload.model_validate(
        {
            "Versao_Sistema": "2.0",
            "Gerado_Em": FIXED_DATETIME,
            "Ativo": build_asset(),
            "Opcoes": None,
            "Observacoes_Exportacao": "teste de dump",
        }
    ).model_dump(by_alias=True)
    if "Ativo" not in dumped:
        raise ValueError("alias Ativo ausente no dump")


def main() -> None:
    tests: list[tuple[str, Callable[[], Any], bool]] = [
        ("ReferenceMeta sucesso", test_01_reference_meta_success, True),
        ("ReferenceMeta Decimal quantizado", test_02_reference_meta_quantization, True),
        ("ReferenceMeta falha com Preco_ref=0", test_03_reference_meta_zero_price, False),
        ("TrendBasePayload sucesso com aliases", test_04_trend_success, True),
        ("StructurePayload sucesso", test_05_structure_success, True),
        ("StructurePayload falha com SMC_PD_Value=1.2", test_06_structure_invalid_pd_value, False),
        ("StructurePayload uppercase em SMC_OB_Type", test_07_structure_ob_type_uppercase, True),
        ("LiquidityMapPayload sucesso", test_08_liquidity_success, True),
        ("VolatilityTimingPayload sucesso", test_09_volatility_success, True),
        ("VolatilityTimingPayload falha com RSI14=101", test_10_volatility_invalid_rsi, False),
        ("VolatilityTimingPayload falha com BB_percent_b=1.6", test_11_volatility_invalid_bb, False),
        ("VolatilityTimingPayload falha com ATR14=-1", test_12_volatility_invalid_atr, False),
        ("EntryProjectionPayload sucesso", test_13_projection_success, True),
        ("EntryProjectionPayload limpa tags vazias", test_14_projection_clean_tags, True),
        ("EntryProjectionPayload falha com Stop_Inst == Entrada_Sugerida", test_15_projection_stop_inst_equals_entry, False),
        ("EntryProjectionPayload falha com Stop_Loss == Preco_ref", test_16_projection_stop_loss_equals_preco_ref, False),
        ("EntryProjectionPayload falha com Risk_Reward_Ratio=-1", test_17_projection_negative_rr, False),
        ("LegacyScorePayload sucesso", test_18_legacy_score_success, True),
        ("LegacyScorePayload uppercase em Setup_Tag", test_19_legacy_score_setup_tag_upper, True),
        ("LegacyScorePayload falha com Probabilidade_Perc=120", test_20_legacy_score_invalid_prob, False),
        ("ScoreAtivoV2Payload sucesso", test_21_score_v2_success, True),
        ("ScoreAtivoV2Payload limpa penalidades", test_22_score_v2_clean_penalties, True),
        ("ScoreAtivoV2Payload falha com score_ajustado > score_bruto", test_23_score_v2_invalid_adjusted, False),
        ("ScoreAtivoV2Payload falha com score_final_ativo > teto_aplicado", test_24_score_v2_invalid_final, False),
        ("RegimeV1Payload sucesso", test_25_regime_success, True),
        ("RegimeV1Payload falha com regime_strength=101", test_26_regime_invalid_strength, False),
        ("WeeklyAdequacyPayload sucesso", test_27_weekly_success, True),
        ("WeeklyAdequacyPayload limpa listas", test_28_weekly_clean_lists, True),
        ("WeeklyAdequacyPayload falha com adequacao_semanal_score=101", test_29_weekly_invalid_score, False),
        ("SuggestedOptionPayload sucesso", test_30_option_success, True),
        ("SuggestedOptionPayload uppercase em Codigo_Opcao", test_31_option_code_uppercase, True),
        ("SuggestedOptionPayload falha com delta=1.2", test_32_option_invalid_delta, False),
        ("SuggestedOptionPayload falha com Sugestao_Strike=0", test_33_option_invalid_strike, False),
        ("AssetAnalysisPayload sucesso mínimo realista", test_34_asset_success, True),
        ("AssetAnalysisPayload ticker uppercase", test_35_asset_ticker_uppercase, True),
        ("AssetAnalysisPayload falha com ref_date > analysis_date.date()", test_36_asset_invalid_ref_date, False),
        ("OptionsSelectionPayload sucesso mínimo", test_37_options_selection_success, True),
        ("OptionsSelectionPayload ticker uppercase", test_38_options_selection_ticker_uppercase, True),
        ("FinalSystemPayload sucesso com ativo sem opções", test_39_final_without_options, True),
        ("FinalSystemPayload sucesso com ativo e com opções", test_40_final_with_options, True),
        ("model_dump(by_alias=True) com Preco_ref", test_41_dump_reference_alias, True),
        ("model_dump(by_alias=True) com Ticker", test_42_dump_asset_alias, True),
        ("model_dump(by_alias=True) com Ativo", test_43_dump_final_alias, True),
    ]

    results: list[dict[str, object]] = []

    for name, fn, should_pass in tests:
        if should_pass:
            results.append(expect_success(name, fn))
        else:
            results.append(expect_failure(name, fn))

    total = len(results)
    passed = sum(1 for item in results if item["success"])
    failed = total - passed

    print(f"Testes executados: {total}")
    print(f"Aprovados: {passed}")
    print(f"Falhos: {failed}")

    if failed > 0:
        print("Testes falhos:")
        for item in results:
            if not item["success"]:
                print(f"- {item['name']}")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()

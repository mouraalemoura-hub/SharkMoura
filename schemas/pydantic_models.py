from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator, model_validator


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        str_strip_whitespace=True,
        extra="forbid",
        use_enum_values=True,
    )


def _clean_string_list(values: List[str]) -> List[str]:
    cleaned: List[str] = []
    for item in values:
        item = str(item).strip()
        if item:
            cleaned.append(item)
    return cleaned


class RefRuleEnum(str, Enum):
    CLOSE = "CLOSE"
    OPEN = "OPEN"
    VWAP = "VWAP"
    MID = "MID"
    MANUAL = "MANUAL"
    UNKNOWN = "UNKNOWN"


class DirecaoInstEnum(str, Enum):
    COMPRA = "COMPRA"
    VENDA = "VENDA"
    NEUTRO = "NEUTRO"


class TrendSideEnum(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    NEUTRO = "NEUTRO"


class FFFDEnum(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    NEUTRO = "NEUTRO"


class SMCStructureEnum(str, Enum):
    BULL = "BULL"
    BEAR = "BEAR"
    NEUTRO = "NEUTRO"


class BosSideEnum(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    NONE = "NONE"


class PDAreaEnum(str, Enum):
    DISCOUNT = "DISCOUNT"
    PREMIUM = "PREMIUM"
    EQUILIBRIO = "EQUILIBRIO"
    NEUTRO = "NEUTRO"


class LiqSideEnum(str, Enum):
    ABOVE = "ABOVE"
    BELOW = "BELOW"
    BOTH = "BOTH"
    NONE = "NONE"


class ProbFillEnum(str, Enum):
    ALTA = "alta"
    MEDIA = "média"
    BAIXA = "baixa"
    DESCONHECIDA = "desconhecida"


class VerdictEnum(str, Enum):
    DIAMANTE = "DIAMANTE"
    OURO = "OURO"
    PRATA = "PRATA"
    OBSERVACAO = "OBSERVACAO"


class RegimePrincipalEnum(str, Enum):
    TENDENCIA_ALTA = "TENDENCIA_ALTA"
    TENDENCIA_BAIXA = "TENDENCIA_BAIXA"
    LATERAL_ESTRUTURADA = "LATERAL_ESTRUTURADA"
    TRANSICAO = "TRANSICAO"
    EXPANSAO_DIRECIONAL = "EXPANSAO_DIRECIONAL"
    EXAUSTAO_OU_ESTICAMENTO = "EXAUSTAO_OU_ESTICAMENTO"


class AdequacaoSemanalStatusEnum(str, Enum):
    ADEQUADA = "ADEQUADA"
    ADEQUADA_COM_RESSALVAS = "ADEQUADA_COM_RESSALVAS"
    FRACA_PARA_SEMANA = "FRACA_PARA_SEMANA"
    INADEQUADA = "INADEQUADA"


class OptionTypeEnum(str, Enum):
    CALL = "CALL"
    PUT = "PUT"


class ReferenceMeta(BaseSchema):
    """Camada 0 de referência operacional."""

    price_ref: Decimal = Field(
        ...,
        validation_alias=AliasChoices("Preco_ref", "price_ref"),
        serialization_alias="Preco_ref",
    )
    ref_date: Optional[date] = Field(
        default=None,
        validation_alias=AliasChoices("Data_Referencia", "ref_date"),
        serialization_alias="Data_Referencia",
    )
    ref_rule: RefRuleEnum = Field(
        default=RefRuleEnum.UNKNOWN,
        validation_alias=AliasChoices("Regra_Referencia", "ref_rule"),
        serialization_alias="Regra_Referencia",
    )

    @field_validator("price_ref", mode="before")
    @classmethod
    def validate_price_ref(cls, value):
        if isinstance(value, str):
            value = Decimal(value)
        elif not isinstance(value, Decimal):
            value = Decimal(str(value))
        value = value.quantize(Decimal("0.000001"))
        if value <= 0:
            raise ValueError("price_ref deve ser maior que zero.")
        return value


class TrendBasePayload(BaseSchema):
    """Hipótese direcional inicial do legado."""

    infer_direction: Optional[DirecaoInstEnum] = Field(
        default=None,
        validation_alias=AliasChoices("Infer_Direction", "infer_direction"),
        serialization_alias="Infer_Direction",
    )
    direcao_inst: Optional[DirecaoInstEnum] = Field(
        default=None,
        validation_alias=AliasChoices("Direcao_Inst", "direcao_inst"),
        serialization_alias="Direcao_Inst",
    )
    ema_stack_up: Optional[bool] = Field(default=None)
    ema_stack_down: Optional[bool] = Field(default=None)
    w1_trend: Optional[TrendSideEnum] = Field(
        default=None,
        validation_alias=AliasChoices("W1_Trend", "w1_trend"),
        serialization_alias="W1_Trend",
    )
    h1_trend: Optional[TrendSideEnum] = Field(
        default=None,
        validation_alias=AliasChoices("H1_Trend", "h1_trend"),
        serialization_alias="H1_Trend",
    )
    slope_ema200: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("Slope_EMA200", "slope_ema200"),
        serialization_alias="Slope_EMA200",
    )


class StructurePayload(BaseSchema):
    """Núcleo estrutural institucional observado no legado."""

    smc_structure: Optional[SMCStructureEnum] = Field(
        default=None,
        validation_alias=AliasChoices("SMC_Structure", "smc_structure"),
        serialization_alias="SMC_Structure",
    )
    smc_last_bos: Optional[BosSideEnum] = Field(
        default=None,
        validation_alias=AliasChoices("SMC_Last_BOS", "smc_last_bos"),
        serialization_alias="SMC_Last_BOS",
    )
    smc_last_choch: Optional[bool] = Field(
        default=None,
        validation_alias=AliasChoices("SMC_Last_CHOCH", "smc_last_choch"),
        serialization_alias="SMC_Last_CHOCH",
    )
    smc_pd_area: Optional[PDAreaEnum] = Field(
        default=None,
        validation_alias=AliasChoices("SMC_PD_Area", "smc_pd_area"),
        serialization_alias="SMC_PD_Area",
    )
    smc_pd50: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("SMC_PD50", "smc_pd50"),
        serialization_alias="SMC_PD50",
    )
    smc_pd_value: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("SMC_PD_Value", "smc_pd_value"),
        serialization_alias="SMC_PD_Value",
    )
    smc_ob_type: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("SMC_OB_Type", "smc_ob_type"),
        serialization_alias="SMC_OB_Type",
    )
    smc_ob_refine: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("SMC_OB_Refine", "smc_ob_refine"),
        serialization_alias="SMC_OB_Refine",
    )
    smc_fvg_side: Optional[BosSideEnum] = Field(
        default=None,
        validation_alias=AliasChoices("SMC_FVG_Side", "smc_fvg_side"),
        serialization_alias="SMC_FVG_Side",
    )
    smc_fvg_mid: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("SMC_FVG_Mid", "smc_fvg_mid"),
        serialization_alias="SMC_FVG_Mid",
    )
    smc_fvg_size_atr: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("SMC_FVG_Size_ATR", "smc_fvg_size_atr"),
        serialization_alias="SMC_FVG_Size_ATR",
    )

    @field_validator("smc_pd_value", mode="after")
    @classmethod
    def validate_smc_pd_value(cls, value: Optional[float]) -> Optional[float]:
        if value is not None and not (0 <= value <= 1):
            raise ValueError("smc_pd_value deve estar entre 0 e 1.")
        return value

    @field_validator("smc_fvg_size_atr", mode="after")
    @classmethod
    def validate_smc_fvg_size_atr(cls, value: Optional[float]) -> Optional[float]:
        if value is not None and value < 0:
            raise ValueError("smc_fvg_size_atr não pode ser negativo.")
        return value

    @field_validator("smc_ob_type", mode="after")
    @classmethod
    def normalize_smc_ob_type(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = value.strip()
        return value.upper() if value else None


class LiquidityMapPayload(BaseSchema):
    """Mapa agrupado de liquidez horizontal."""

    eq_high: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("EQ_High", "eq_high"),
        serialization_alias="EQ_High",
    )
    eq_low: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("EQ_Low", "eq_low"),
        serialization_alias="EQ_Low",
    )
    pdh: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("PDH", "pdh"),
        serialization_alias="PDH",
    )
    pdl: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("PDL", "pdl"),
        serialization_alias="PDL",
    )
    pwh: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("PWH", "pwh"),
        serialization_alias="PWH",
    )
    pwl: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("PWL", "pwl"),
        serialization_alias="PWL",
    )
    liq_side: Optional[LiqSideEnum] = Field(
        default=None,
        validation_alias=AliasChoices("Liq_Side", "liq_side"),
        serialization_alias="Liq_Side",
    )
    liq_target_1: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("Liq_Target_1", "liq_target_1"),
        serialization_alias="Liq_Target_1",
    )
    liq_target_2: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("Liq_Target_2", "liq_target_2"),
        serialization_alias="Liq_Target_2",
    )


class VolatilityTimingPayload(BaseSchema):
    """Volatilidade e timing tático do legado."""

    atr14: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("ATR14", "atr14"),
        serialization_alias="ATR14",
    )
    rsi14: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("RSI14", "rsi14"),
        serialization_alias="RSI14",
    )
    macd: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("MACD", "macd"),
        serialization_alias="MACD",
    )
    macd_hist: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("MACD_hist", "macd_hist"),
        serialization_alias="MACD_hist",
    )
    bb_percent_b: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("BB_percent_b", "bb_percent_b"),
        serialization_alias="BB_percent_b",
    )
    bb_bandwidth: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("BB_bandwidth", "bb_bandwidth"),
        serialization_alias="BB_bandwidth",
    )
    fffd: Optional[bool] = Field(
        default=None,
        validation_alias=AliasChoices("FFFD", "fffd"),
        serialization_alias="FFFD",
    )
    fffd_side: Optional[FFFDEnum] = Field(
        default=None,
        validation_alias=AliasChoices("FFFD_side", "fffd_side"),
        serialization_alias="FFFD_side",
    )
    fffd_note: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("FFFD_note", "fffd_note"),
        serialization_alias="FFFD_note",
    )
    w1_context: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("W1_context", "w1_context"),
        serialization_alias="W1_context",
    )
    h1_entry_hint: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("H1_entry_hint", "h1_entry_hint"),
        serialization_alias="H1_entry_hint",
    )
    tickvolume_zscore: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("TickVolume_ZScore", "tickvolume_zscore"),
        serialization_alias="TickVolume_ZScore",
    )
    historical_volatility_21: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("HV_21", "historical_volatility_21"),
        serialization_alias="HV_21",
    )

    @field_validator("rsi14", mode="after")
    @classmethod
    def validate_rsi14(cls, value: Optional[float]) -> Optional[float]:
        if value is not None and not (0 <= value <= 100):
            raise ValueError("rsi14 deve estar entre 0 e 100.")
        return value

    @field_validator("bb_percent_b", mode="after")
    @classmethod
    def validate_bb_percent_b(cls, value: Optional[float]) -> Optional[float]:
        if value is not None and not (0 <= value <= 1.5):
            raise ValueError("bb_percent_b deve estar entre 0 e 1.5.")
        return value

    @field_validator("atr14", "bb_bandwidth", "historical_volatility_21", mode="after")
    @classmethod
    def validate_non_negative_metrics(cls, value: Optional[float]) -> Optional[float]:
        if value is not None and value < 0:
            raise ValueError("O valor não pode ser negativo.")
        return value


class EntryProjectionPayload(BaseSchema):
    """Estrutura de entradas, alvos, stops e métricas operacionais."""

    preco_ref: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("Preco_ref", "preco_ref"),
        serialization_alias="Preco_ref",
    )
    entrada_sugerida: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("Entrada_Sugerida", "entrada_sugerida"),
        serialization_alias="Entrada_Sugerida",
    )
    entrada_primaria: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("Entrada_Primaria", "entrada_primaria"),
        serialization_alias="Entrada_Primaria",
    )
    entrada_secundaria: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("Entrada_Secundaria", "entrada_secundaria"),
        serialization_alias="Entrada_Secundaria",
    )
    prob_fill_prim: Optional[ProbFillEnum] = Field(
        default=None,
        validation_alias=AliasChoices("Prob_Fill_Prim", "prob_fill_prim"),
        serialization_alias="Prob_Fill_Prim",
    )
    prob_fill_sec: Optional[ProbFillEnum] = Field(
        default=None,
        validation_alias=AliasChoices("Prob_Fill_Sec", "prob_fill_sec"),
        serialization_alias="Prob_Fill_Sec",
    )
    tags_entrada_prim: List[str] = Field(
        default_factory=list,
        validation_alias=AliasChoices("Tags_Entrada_Prim", "tags_entrada_prim"),
        serialization_alias="Tags_Entrada_Prim",
    )
    tags_entrada_sec: List[str] = Field(
        default_factory=list,
        validation_alias=AliasChoices("Tags_Entrada_Sec", "tags_entrada_sec"),
        serialization_alias="Tags_Entrada_Sec",
    )
    t1: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("T1", "t1"),
        serialization_alias="T1",
    )
    t2: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("T2", "t2"),
        serialization_alias="T2",
    )
    t3: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("T3", "t3"),
        serialization_alias="T3",
    )
    stop_inst: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("Stop_Inst", "stop_inst"),
        serialization_alias="Stop_Inst",
    )
    stop_loss: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("Stop_Loss", "stop_loss"),
        serialization_alias="Stop_Loss",
    )
    risk_reward_ratio: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("Risk_Reward_Ratio", "risk_reward_ratio"),
        serialization_alias="Risk_Reward_Ratio",
    )
    rr_t2_prim: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("RR_T2_Prim", "rr_t2_prim"),
        serialization_alias="RR_T2_Prim",
    )
    rr_t2_sec: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("RR_T2_Sec", "rr_t2_sec"),
        serialization_alias="RR_T2_Sec",
    )
    alvo_sexta_t1: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("Alvo_Sexta_T1", "alvo_sexta_t1"),
        serialization_alias="Alvo_Sexta_T1",
    )
    alvo_semana: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("Alvo_Semana", "alvo_semana"),
        serialization_alias="Alvo_Semana",
    )
    faixa_semana_alta: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("Faixa_Semana_Alta", "faixa_semana_alta"),
        serialization_alias="Faixa_Semana_Alta",
    )
    faixa_semana_baixa: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("Faixa_Semana_Baixa", "faixa_semana_baixa"),
        serialization_alias="Faixa_Semana_Baixa",
    )

    @field_validator(
        "preco_ref",
        "entrada_sugerida",
        "entrada_primaria",
        "entrada_secundaria",
        "t1",
        "t2",
        "t3",
        "stop_inst",
        "stop_loss",
        "alvo_sexta_t1",
        "alvo_semana",
        "faixa_semana_alta",
        "faixa_semana_baixa",
        mode="before",
    )
    @classmethod
    def normalize_decimals(cls, value):
        if value is None:
            return value
        if isinstance(value, str):
            return Decimal(value)
        if not isinstance(value, Decimal):
            return Decimal(str(value))
        return value

    @field_validator("tags_entrada_prim", "tags_entrada_sec", mode="before")
    @classmethod
    def clean_tags(cls, values):
        if values is None:
            return []
        return _clean_string_list(values)

    @field_validator("risk_reward_ratio", "rr_t2_prim", "rr_t2_sec", mode="after")
    @classmethod
    def validate_non_negative_rr(cls, value: Optional[float]) -> Optional[float]:
        if value is not None and value < 0:
            raise ValueError("Métricas de risco-retorno não podem ser negativas.")
        return value

    @model_validator(mode="after")
    def validate_stops_against_base_price(self) -> "EntryProjectionPayload":
        base_price = self.entrada_sugerida or self.entrada_primaria or self.preco_ref

        if base_price is not None and self.stop_inst is not None and self.stop_inst == base_price:
            raise ValueError("stop_inst não pode ser igual ao preço base comparável.")

        if base_price is not None and self.stop_loss is not None and self.stop_loss == base_price:
            raise ValueError("stop_loss não pode ser igual ao preço base comparável.")

        return self


class LegacyScorePayload(BaseSchema):
    """Score, setup, probabilidade e veredito do legado."""

    confluencia_score_smc: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("Confluencia_Score_SMC", "confluencia_score_smc"),
        serialization_alias="Confluencia_Score_SMC",
        ge=0,
        le=100,
    )
    confluencia_score: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("Confluencia_Score", "confluencia_score"),
        serialization_alias="Confluencia_Score",
        ge=0,
        le=100,
    )
    probabilidade_perc: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("Probabilidade_Perc", "probabilidade_perc"),
        serialization_alias="Probabilidade_Perc",
        ge=0,
        le=100,
    )
    setup_tag: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("Setup_Tag", "setup_tag"),
        serialization_alias="Setup_Tag",
    )
    veredito: Optional[VerdictEnum] = Field(
        default=None,
        validation_alias=AliasChoices("Veredito", "veredito"),
        serialization_alias="Veredito",
    )
    racional: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("Racional", "racional"),
        serialization_alias="Racional",
    )

    @field_validator("setup_tag", mode="after")
    @classmethod
    def normalize_setup_tag(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = value.strip()
        return value.upper() if value else None


class ScoreAtivoV2Payload(BaseSchema):
    """Estrutura forward-compatible para o Score do Ativo v2."""

    score_bruto: Optional[float] = Field(default=None, ge=0, le=100)
    score_ajustado: Optional[float] = Field(default=None, ge=0, le=100)
    score_final_ativo: Optional[float] = Field(default=None, ge=0, le=100)
    score_tendencia: Optional[float] = Field(default=None, ge=0, le=100)
    score_estrutura: Optional[float] = Field(default=None, ge=0, le=100)
    score_volatilidade: Optional[float] = Field(default=None, ge=0, le=100)
    score_localizacao: Optional[float] = Field(default=None, ge=0, le=100)
    score_timing: Optional[float] = Field(default=None, ge=0, le=100)
    penalidades_aplicadas: List[str] = Field(default_factory=list)
    teto_aplicado: Optional[float] = Field(default=None, ge=0, le=100)
    racional_score: Optional[str] = None

    @field_validator("penalidades_aplicadas", mode="before")
    @classmethod
    def clean_penalties(cls, values):
        if values is None:
            return []
        return _clean_string_list(values)

    @model_validator(mode="after")
    def validate_score_logic(self) -> "ScoreAtivoV2Payload":
        if self.score_bruto is not None and self.score_ajustado is not None:
            if self.score_ajustado > self.score_bruto:
                raise ValueError("score_ajustado não pode ser maior que score_bruto.")

        if self.score_final_ativo is not None and self.teto_aplicado is not None:
            if self.score_final_ativo > self.teto_aplicado:
                raise ValueError("score_final_ativo não pode ser maior que teto_aplicado.")

        return self


class RegimeV1Payload(BaseSchema):
    """Estrutura forward-compatible para Regime v1."""

    regime_principal: Optional[RegimePrincipalEnum] = Field(default=None)
    regime_bias: Optional[DirecaoInstEnum] = Field(default=None)
    regime_strength: Optional[float] = Field(default=None, ge=0, le=100)
    regime_flags: List[str] = Field(default_factory=list)
    regime_conflicts: List[str] = Field(default_factory=list)
    regime_rationale: Optional[str] = Field(default=None)

    @field_validator("regime_flags", "regime_conflicts", mode="before")
    @classmethod
    def clean_regime_lists(cls, values):
        if values is None:
            return []
        return _clean_string_list(values)


class WeeklyAdequacyPayload(BaseSchema):
    """Estrutura forward-compatible para adequação semanal."""

    adequacao_semanal_status: Optional[AdequacaoSemanalStatusEnum] = Field(default=None)
    adequacao_semanal_score: Optional[float] = Field(default=None, ge=0, le=100)
    tempo_status: Optional[str] = Field(default=None)
    espaco_status: Optional[str] = Field(default=None)
    deslocamento_status: Optional[str] = Field(default=None)
    maturidade_status: Optional[str] = Field(default=None)
    horizon_bdays: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("Horizon_bdays", "horizon_bdays"),
        serialization_alias="Horizon_bdays",
        ge=0,
    )
    motivos_positivos: List[str] = Field(default_factory=list)
    motivos_negativos: List[str] = Field(default_factory=list)
    alvo_semanal_plausivel: Optional[bool] = Field(default=None)
    racional_adequacao: Optional[str] = Field(default=None)

    @field_validator("motivos_positivos", "motivos_negativos", mode="before")
    @classmethod
    def clean_reason_lists(cls, values):
        if values is None:
            return []
        return _clean_string_list(values)


class SuggestedOptionPayload(BaseSchema):
    """Estrutura da camada de opções."""

    codigo_opcao: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("Codigo_Opcao", "codigo_opcao"),
        serialization_alias="Codigo_Opcao",
    )
    tipo_opcao: Optional[OptionTypeEnum] = Field(
        default=None,
        validation_alias=AliasChoices("Tipo_Opcao", "tipo_opcao"),
        serialization_alias="Tipo_Opcao",
    )
    sugestao_strike: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("Sugestao_Strike", "sugestao_strike"),
        serialization_alias="Sugestao_Strike",
    )
    vencimento: Optional[date] = Field(
        default=None,
        validation_alias=AliasChoices("Vencimento", "vencimento"),
        serialization_alias="Vencimento",
    )
    premio: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("Premio", "premio"),
        serialization_alias="Premio",
        ge=0,
    )
    delta: Optional[float] = Field(default=None, ge=-1, le=1)
    open_interest: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("Open_Interest", "open_interest"),
        serialization_alias="Open_Interest",
        ge=0,
    )
    spread: Optional[float] = Field(default=None, ge=0)
    stop_loss: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("Stop_Loss", "stop_loss"),
        serialization_alias="Stop_Loss",
    )
    alvo_sexta_t1: Optional[Decimal] = Field(
        default=None,
        validation_alias=AliasChoices("Alvo_Sexta_T1", "alvo_sexta_t1"),
        serialization_alias="Alvo_Sexta_T1",
    )
    risk_reward_ratio: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("Risk_Reward_Ratio", "risk_reward_ratio"),
        serialization_alias="Risk_Reward_Ratio",
        ge=0,
    )
    racional_opcao: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("Racional_Opcao", "racional_opcao"),
        serialization_alias="Racional_Opcao",
    )

    @field_validator("codigo_opcao", mode="after")
    @classmethod
    def normalize_option_code(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = value.strip()
        return value.upper() if value else None

    @field_validator("sugestao_strike", "stop_loss", "alvo_sexta_t1", mode="before")
    @classmethod
    def normalize_option_decimals(cls, value):
        if value is None:
            return value
        if isinstance(value, str):
            value = Decimal(value)
        elif not isinstance(value, Decimal):
            value = Decimal(str(value))
        if value <= 0:
            raise ValueError("Preços e strikes devem ser maiores que zero.")
        return value.quantize(Decimal("0.000001"))


class AssetAnalysisPayload(BaseSchema):
    """Payload consolidado da análise-base do ativo."""

    ticker: str = Field(
        ...,
        validation_alias=AliasChoices("Ticker", "Símbolo", "ticker"),
        serialization_alias="Ticker",
    )
    periodo: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("Período", "Periodo", "periodo"),
        serialization_alias="Periodo",
    )
    analysis_date: datetime = Field(
        default_factory=datetime.utcnow,
        validation_alias=AliasChoices("Data_Analise", "analysis_date"),
        serialization_alias="Data_Analise",
    )

    reference_meta: ReferenceMeta
    trend: TrendBasePayload = Field(default_factory=TrendBasePayload)
    structure: StructurePayload = Field(default_factory=StructurePayload)
    liquidity_map: LiquidityMapPayload = Field(default_factory=LiquidityMapPayload)
    volatility_timing: VolatilityTimingPayload = Field(default_factory=VolatilityTimingPayload)
    projection: EntryProjectionPayload = Field(default_factory=EntryProjectionPayload)
    legacy_score: LegacyScorePayload = Field(default_factory=LegacyScorePayload)

    score_v2: Optional[ScoreAtivoV2Payload] = Field(default=None)
    regime_v1: Optional[RegimeV1Payload] = Field(default=None)
    weekly_adequacy: Optional[WeeklyAdequacyPayload] = Field(default=None)

    veredito: Optional[VerdictEnum] = Field(
        default=None,
        validation_alias=AliasChoices("Veredito", "veredito"),
        serialization_alias="Veredito",
    )
    notas: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("Notas", "notas"),
        serialization_alias="Notas",
    )

    @field_validator("ticker", mode="after")
    @classmethod
    def validate_ticker(cls, value: str) -> str:
        value = value.strip().upper()
        if not value:
            raise ValueError("ticker não pode ser vazio.")
        return value

    @model_validator(mode="after")
    def validate_reference_date(self) -> "AssetAnalysisPayload":
        if self.reference_meta.ref_date is not None:
            if self.reference_meta.ref_date > self.analysis_date.date():
                raise ValueError("ref_date não pode ser posterior à analysis_date.")
        return self


class OptionsSelectionPayload(BaseSchema):
    """Payload consolidado da camada de opções."""

    ticker: str = Field(
        ...,
        validation_alias=AliasChoices("Ticker", "ticker"),
        serialization_alias="Ticker",
    )
    lado_base: Optional[DirecaoInstEnum] = Field(
        default=None,
        validation_alias=AliasChoices("Lado_Base", "lado_base"),
        serialization_alias="Lado_Base",
    )
    opcoes_sugeridas: List[SuggestedOptionPayload] = Field(
        default_factory=list,
        validation_alias=AliasChoices("Opcoes_Sugeridas", "opcoes_sugeridas"),
        serialization_alias="Opcoes_Sugeridas",
    )
    notas_selecao: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("Notas_Selecao", "notas_selecao"),
        serialization_alias="Notas_Selecao",
    )

    @field_validator("ticker", mode="after")
    @classmethod
    def validate_ticker(cls, value: str) -> str:
        value = value.strip().upper()
        if not value:
            raise ValueError("ticker não pode ser vazio.")
        return value


class FinalSystemPayload(BaseSchema):
    """Payload final consolidado do sistema."""

    system_version: str = Field(
        default="2.0",
        validation_alias=AliasChoices("Versao_Sistema", "system_version"),
        serialization_alias="Versao_Sistema",
    )
    generated_at: datetime = Field(
        default_factory=datetime.utcnow,
        validation_alias=AliasChoices("Gerado_Em", "generated_at"),
        serialization_alias="Gerado_Em",
    )
    asset: AssetAnalysisPayload = Field(
        ...,
        validation_alias=AliasChoices("Ativo", "asset"),
        serialization_alias="Ativo",
    )
    options: Optional[OptionsSelectionPayload] = Field(
        default=None,
        validation_alias=AliasChoices("Opcoes", "options"),
        serialization_alias="Opcoes",
    )
    export_notes: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("Observacoes_Exportacao", "export_notes"),
        serialization_alias="Observacoes_Exportacao",
    )


__all__ = [
    "BaseSchema",
    "RefRuleEnum",
    "DirecaoInstEnum",
    "TrendSideEnum",
    "FFFDEnum",
    "SMCStructureEnum",
    "BosSideEnum",
    "PDAreaEnum",
    "LiqSideEnum",
    "ProbFillEnum",
    "VerdictEnum",
    "RegimePrincipalEnum",
    "AdequacaoSemanalStatusEnum",
    "OptionTypeEnum",
    "ReferenceMeta",
    "TrendBasePayload",
    "StructurePayload",
    "LiquidityMapPayload",
    "VolatilityTimingPayload",
    "EntryProjectionPayload",
    "LegacyScorePayload",
    "ScoreAtivoV2Payload",
    "RegimeV1Payload",
    "WeeklyAdequacyPayload",
    "SuggestedOptionPayload",
    "AssetAnalysisPayload",
    "OptionsSelectionPayload",
    "FinalSystemPayload",
]

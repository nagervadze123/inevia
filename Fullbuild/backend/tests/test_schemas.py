import pytest
from pydantic import ValidationError
from app.schemas.agent_schemas import OpportunityCard


def test_schema_strict_rejects_extra_keys():
    with pytest.raises(ValidationError):
        OpportunityCard.model_validate({
            'title': 'x', 'demand_signals': [], 'competition_level': 'low', 'differentiation_angles': [],
            'suggested_formats': [], 'suggested_price_range': '$1', 'confidence_score': 1,
            'demand_score': 1, 'competition_score': 1, 'profit_score': 1, 'extra': 'bad'
        })

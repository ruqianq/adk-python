from .trajectory_evaluator import TrajectoryEvaluator
from pydantic import BaseModel
from typing import Dict, Type

BUILDIN_METRICS = {
    "tool_accuracy": {'evaluator': TrajectoryEvaluator}
}

class EvaluationConfig(BaseModel):
    metric: str
    threshold: float | None = None

    @model_valuator('metric')
    def validate_metric(cls, v: str) -> str:
        if v not in BUILDIN_METRICS:
            raise ValueError(f"Metric {v} is not supported. Supported metrics are: {list(BUILDIN_METRICS.keys())}")
        return v
    

def validate_evaluation_input(evaluation_input: Dict[str, Dict[str, str] | None]) -> None:
    for key, value in evaluation_input.items():
        if not isinstance(key, str):
            raise ValueError(f"Key {key} is not a string.")
        if value is not None and not isinstance(value, dict):
            raise ValueError(f"Value {value} for key {key} is not a dict or None.")
        if value is not None:
            for sub_key, sub_value in value.items():
                if not isinstance(sub_key, str):
                    raise ValueError(f"Sub-key {sub_key} in value {value} for key {key} is not a string.")
                if not isinstance(sub_value, str):
                    raise ValueError(f"Sub-value {sub_value} in value {value} for key {key} is not a string.")
        EvaluationConfig(evaluation_input=evaluation_input)  # This will trigger pydantic validation
        
        
def build_evaluator(config: EvaluationConfig) -> Evaluator:
    evaluator_class: Type[Evaluator] = BUILDIN_METRICS[config.metric]['evaluator']
    return evaluator_class(threshold=config.threshold)


                


    
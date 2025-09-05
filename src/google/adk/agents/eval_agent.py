from base_agent import BaseAgent
from sequential_agent import SeqAgent
from collections.abc import AsyncGenerator
from .invocation_context import InvocationContext
from evaluation.evaluation_config import build_evaluator

class EvalAgent(BaseAgent):
    evaluation_input: dict[str, dict[str, str]| None] 
    model: str | None

    async def run(self, ctx: InvocationContext) -> AsyncGenerator[dict[str, str], None]:
        evaluator = build_evaluator(self.evaluation_input['metric'])
        result = evaluator.evaluate_invocations(
            actual_invocations=ctx.actual_invocations,
            expected_invocations=ctx.expected_invocations
        )
        yield {"evaluation_result": result.json()}

class EvaluatedAgent(SeqAgent):
    evaluation_input: dict[str, dict[str, str]| None] 
    model: str | None
    
    def model_post_init(self, context: dict) -> None:
       eval_agent = EvalAgent(
           evaluation_input=self.evaluation_input,
           model=self.model
       )
       
       self.sub_agents.append(eval_agent)
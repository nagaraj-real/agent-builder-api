from __future__ import annotations
from pyparsing import Optional
from typing import Any, Optional
from nemoguardrails.integrations.langchain.runnable_rails import RunnableRails
from langchain_core.messages import AIMessage
from langchain_core.prompt_values import ChatPromptValue, StringPromptValue
from langchain_core.runnables.config import RunnableConfig
from langchain_core.runnables.utils import Input, Output

from nemoguardrails.rails.llm.options import GenerationOptions


# Overriding the Class to bypass 'output_vars' error in colang version 2.x
class RunnableAgentRails(RunnableRails):
    def invoke(
        self,
        input: Input,
        config: Optional[RunnableConfig] = None, # type: ignore
        **kwargs: Optional[Any], # type: ignore
    ) -> Output:
        """Invoke this runnable synchronously."""
        input_messages = self._transform_input_to_rails_format(input)
        res = self.rails.generate(
            messages=input_messages, options=GenerationOptions(output_vars=False)
        )
        context = res.output_data
        result = res.response

        # If more than one message is returned, we only take the first one.
        # This can happen for advanced use cases, e.g., when the LLM could predict
        # multiple function calls at the same time. We'll deal with these later.
        if isinstance(result, list):
            result = result[0]

        if self.passthrough and self.passthrough_runnable:
            passthrough_output = context.get("passthrough_output")

            # If a rail was triggered (input or dialog), the passthrough_output
            # will not be set. In this case, we only set the output key to the
            # message that was received from the guardrail configuration.
            if passthrough_output is None:
                passthrough_output = {
                    self.passthrough_bot_output_key: result["content"]
                }

            bot_message = context.get("bot_message")

            # We make sure that, if the output rails altered the bot message, we
            # replace it in the passthrough_output
            if isinstance(passthrough_output, str):
                passthrough_output = bot_message
            elif isinstance(passthrough_output, dict):
                passthrough_output[self.passthrough_bot_output_key] = bot_message

            return passthrough_output
        else:
            if isinstance(input, ChatPromptValue):
                return AIMessage(content=result["content"])
            elif isinstance(input, StringPromptValue):
                if isinstance(result, dict):
                    return result["content"]
                else:
                    return result
            elif isinstance(input, dict):
                user_input = input["input"]
                if isinstance(user_input, str):
                    return {"output": result["content"]}
                elif isinstance(user_input, list):
                    return {"output": result}
            else:
                raise ValueError(f"Unexpected input type: {type(input)}")

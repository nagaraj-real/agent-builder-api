from nemoguardrails.actions import action

@action(name="SumAction", execute_async=True)
async def sum_action(a:float,b:float):
    return a + b


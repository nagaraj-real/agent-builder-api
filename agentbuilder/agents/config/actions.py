from nemoguardrails.actions import action

@action(name="int_parse_action")
async def int_parse_action(value: str):
    return int(value)
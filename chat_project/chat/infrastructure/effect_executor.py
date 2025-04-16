from typing import Dict, Any, List, Tuple

async def execute_effects(effects: List[Tuple], channel_layer) -> None:
    """효과 실행"""
    for effect_type, *args in effects:
        if effect_type == "group_send":
            group_name, message = args
            await channel_layer.group_send(group_name, message)
        elif effect_type == "send":
            channel_name, message = args
            await channel_layer.send(channel_name, message) 
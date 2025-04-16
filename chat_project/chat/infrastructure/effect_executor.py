from typing import Dict, Any, List, Tuple, Optional
from channels.layers import get_channel_layer

async def execute_effects(effects: List[Tuple], channel_layer=None) -> Optional[Dict[str, Any]]:
    """효과 실행"""
    if channel_layer is None:
        channel_layer = get_channel_layer()
    
    for effect_type, *args in effects:
        if effect_type == "group_add":
            group_name, channel_name = args
            await channel_layer.group_add(group_name, channel_name)
        elif effect_type == "group_send":
            group_name, message = args
            await channel_layer.group_send(group_name, message)
        elif effect_type == "group_discard":
            group_name, channel_name = args
            await channel_layer.group_discard(group_name, channel_name)
        elif effect_type == "send":
            channel_name, message = args
            await channel_layer.send(channel_name, message)
        elif effect_type == "error":
            error_message = args[0]
            return error_message
    return None 
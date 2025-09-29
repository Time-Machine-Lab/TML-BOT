from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

@register("TML-Bot", "TML", "Just For TML", "1.0.0")
class TMLBotPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
    
    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("[mm]AI视频", alias={"AI视频"})
    async def helloworld(self, event: AstrMessageEvent):
        """生产AI视频"""
        raw = event.message_str.removeprefix("[mm]AI视频").removeprefix("AI视频").strip()
        user_name = event.get_sender_name()
        if raw is empty:
            yield event.plain_result("请输入AI视频的描述")
            return
       
        logger.info(f"{user_name} 准备生成AI视频：{raw}")

        yield event.plain_result(f"ModelMaster已生成视频, 提示词{raw}.") # 发送一条纯文本消息

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""

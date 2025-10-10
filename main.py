from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.core import AstrBotConfig
from .core.handler.modelmaster_handle import ModelMasterHandler
from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import (
    AiocqhttpMessageEvent,
)

@register("TML-Bot", "TML", "Just For TML", "...", "...")
class TMLBotPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        logger.info(f"初始化TML-Bot插件，配置：{config}")
        self.context = context 
        self.config = config
        
    async def initialize(self):
        self.modelMaster = ModelMasterHandler(self.context, self.config)
        logger.info("√ ModelMasterHandler 初始化完成")

    # ModelMaster
    @filter.command("生成AI视频", desc="生成AI视频 xxxx")
    async def genAIVideo(self, event: AiocqhttpMessageEvent):
        await self.modelMaster.genAIVideo(event)

    @filter.command("测试", desc="测试一下")
    async def genAIPic(self, event: AiocqhttpMessageEvent):
        yield event.plain_result(f"Hello~ 这里是TML AI助手.") # 发送一条纯文本消息

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""

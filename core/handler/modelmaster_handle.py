from astrbot import logger
from astrbot.api.event import filter
from astrbot.api.star import Context, Star, StarTools, register
from astrbot.core import AstrBotConfig
from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import (
    AiocqhttpMessageEvent,
)

class ModelMasterHandler:
    def __init__(self, context: Context ,config: AstrBotConfig):
        self.context = context
        self.conf = config
        self.api_url = self.conf["mm_api_url"]
        self.api_key = self.conf["mm_api_key"]
        self.headers = {
            "secret": f"{self.api_key}",
            "Content-Type": "application/json",
        }

    async def genAIVideo(self, event: AiocqhttpMessageEvent):
        """生成AI视频"""
        raw = event.message_str.removeprefix("生成AI视频").strip()
        user_name = event.get_sender_name()
        if not raw:
            yield event.plain_result("未检测到AI视频生成提示词，请补充")
            return
       
        logger.info(f"{user_name} 准备生成AI视频：{raw}")

        yield event.plain_result(f"ModelMaster已生成视频, 提示词{raw}.") # 发送一条纯文本消息
        
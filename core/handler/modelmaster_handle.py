from astrbot import logger
from astrbot.api.event import filter
from astrbot.api.star import Context, Star, StarTools, register
from astrbot.core import AstrBotConfig
from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import (
    AiocqhttpMessageEvent,
)
from ..client.modelmaster_client import ModelMasterClient, GenerateVideoReq



class ModelMasterHandler:
    def __init__(self, context: Context, config: AstrBotConfig):
        self.context = context
        self.config = config
        self.api_url = self.config["model_master_config"]["mm_api_url"]
        self.api_key = self.config["model_master_config"]["mm_api_key"]
        self.client = ModelMasterClient(timeout=30, api_url=self.api_url, api_key=self.api_key)
       

    async def gen_ai_video(self, event: AiocqhttpMessageEvent, prompt: str | None = None):
        """生成AI视频"""
        if not prompt:
            await event.send(event.plain_result("未检测到AI视频生成提示词，请补充"))
            return
       
        raw = str(prompt).strip()
        
        user_name = event.get_sender_name()
        
        try:
            logger.info(f"{user_name} 准备生成AI视频：{raw}")
            resp = await self.client.post_generate_ai_video(GenerateVideoReq(nickName=user_name, prompt=raw))
            
            # 处理API响应
            if resp and resp.get('success', False):
                await event.send(event.plain_result(f"ModelMaster已成功生成视频，提示词: {raw}"))
            else:
                error_msg = resp.get('message', '未知错误') if resp else '请求失败'
                await event.send(event.plain_result(f"视频生成失败: {error_msg}"))
                
        except Exception as e:
            logger.error(f"生成AI视频时发生错误: {e}")
            await event.send(event.plain_result(f"视频生成失败，请稍后重试。错误: {str(e)}"))
        
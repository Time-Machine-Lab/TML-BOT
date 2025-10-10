from dataclasses import dataclass
from typing import Dict, Any, Optional
import aiohttp
import json
from astrbot.api import logger


@dataclass
class GenerateVideoReq:
    """生成AI视频请求参数"""
    nickName: str  # 用户昵称
    prompt: str    # 提示词

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "nickName": self.nickName,
            "prompt": self.prompt
        }


class ModelMasterClient:
    """ModelMaster API客户端"""
    
    def __init__(self, timeout: int = 30, api_url: str = None, api_key: str = None):
        """初始化客户端"""
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.api_url = api_url
        self.api_key = api_key

        self.headers = {
            "secret": f"{self.api_key}",
            "Content-Type": "application/json",
        }
    
    async def post_generate_ai_video(
        self, 
        body: GenerateVideoReq
    ) -> Dict[str, Any]:
        """发送生成AI视频请求
        
        Args:
            host: 服务器地址
            headers: 请求头
            body: 请求体参数
            
        Returns:
            API响应结果
            
        Raises:
            aiohttp.ClientError: 网络请求异常
            json.JSONDecodeError: 响应解析异常
        """
        # 构建完整的请求URL
        url = f"{self.api_url.rstrip('/')}/api/tml/bot/video/generate"
        
        # 准备请求数据
        request_data = body.to_dict()
        
        logger.info(f"发送AI视频生成请求到: {url}")
        logger.debug(f"请求参数: {request_data}")
        
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(
                    url=url,
                    headers=self.headers,
                    json=request_data
                ) as response:
                    # 检查HTTP状态码
                    response.raise_for_status()
                    
                    # 解析响应
                    result = await response.json()
                    
                    logger.info(f"AI视频生成请求成功，状态码: {response.status}")
                    logger.debug(f"响应结果: {result}")
                    
                    return result
                    
        except aiohttp.ClientError as e:
            logger.error(f"AI视频生成请求失败: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"响应解析失败: {e}")
            raise
        except Exception as e:
            logger.error(f"未知错误: {e}")
            raise
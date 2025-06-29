import requests
import json
import time
import logging
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL

# 配置日志
logger = logging.getLogger()

class DeepseekAPI:
    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.api_url = DEEPSEEK_API_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def chat_completion(self, messages, model="deepseek-chat", temperature=0.7, max_tokens=4000, max_retries=3, retry_delay=2):
        """
        调用Deepseek API进行对话补全
        
        Args:
            messages: 对话消息列表
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大生成token数
            max_retries: 最大重试次数
            retry_delay: 重试延迟（秒）
            
        Returns:
            API响应内容或None（如果失败）
        """
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        for attempt in range(max_retries):
            try:
                logger.info(f"调用Deepseek API (尝试 {attempt + 1}/{max_retries})")
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    data=json.dumps(payload),
                    timeout=60  # 设置超时时间为60秒
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.warning(f"API调用失败: HTTP {response.status_code}, 响应: {response.text}")
                    
                    # 处理特定错误码
                    if response.status_code == 429:  # 速率限制
                        logger.info(f"触发速率限制，等待更长时间...")
                        time.sleep(retry_delay * 3)  # 速率限制时等待更长时间
                    elif response.status_code >= 500:  # 服务器错误
                        logger.info(f"服务器错误，等待后重试...")
                        time.sleep(retry_delay)
                    else:
                        # 其他错误可能是请求问题，等待后重试
                        time.sleep(retry_delay)
                        
            except requests.exceptions.Timeout:
                logger.warning(f"API请求超时 (尝试 {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
            except requests.exceptions.ConnectionError:
                logger.warning(f"API连接错误 (尝试 {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
            except Exception as e:
                logger.error(f"API调用异常: {str(e)} (尝试 {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
                
            # 最后一次尝试失败
            if attempt == max_retries - 1:
                logger.error(f"API调用失败，已达到最大重试次数 ({max_retries})")
                return None
                
        return None
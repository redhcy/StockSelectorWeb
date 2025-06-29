import requests
import logging
import time
from config import WECHAT_PUSH_KEY, WECHAT_PUSH_URL

# 配置日志
logger = logging.getLogger()

class WechatPush:
    def __init__(self):
        self.push_key = WECHAT_PUSH_KEY
        self.push_url = WECHAT_PUSH_URL.format(self.push_key)

    def send(self, content, title="股票分析报告", max_retries=3, retry_delay=2):
        """
        发送消息到微信
        
        Args:
            content: 消息内容
            title: 消息标题
            max_retries: 最大重试次数
            retry_delay: 重试延迟（秒）
            
        Returns:
            bool: 是否发送成功
        """
        if not self.push_key:
            logger.error("未配置WECHAT_PUSH_KEY")
            return False

        payload = {
            "title": title,
            "desp": content
        }

        for attempt in range(max_retries):
            try:
                logger.info(f"发送微信推送 (尝试 {attempt + 1}/{max_retries})")
                response = requests.post(
                    self.push_url,
                    data=payload,
                    timeout=30  # 设置30秒超时
                )

                if response.status_code == 200:
                    result = response.json()
                    if result.get('code') == 0:
                        logger.info("微信推送成功")
                        return True
                    else:
                        error_msg = result.get('message', '未知错误')
                        logger.warning(f"推送返回错误: {error_msg}")
                else:
                    logger.warning(f"推送请求失败: HTTP {response.status_code}, 响应: {response.text}")

            except requests.exceptions.Timeout:
                logger.warning(f"推送请求超时 (尝试 {attempt + 1}/{max_retries})")
            except requests.exceptions.ConnectionError:
                logger.warning(f"推送连接错误 (尝试 {attempt + 1}/{max_retries})")
            except Exception as e:
                logger.error(f"推送异常: {str(e)} (尝试 {attempt + 1}/{max_retries})")

            # 如果不是最后一次尝试，等待后重试
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                logger.error(f"推送失败，已达到最大重试次数 ({max_retries})")
                return False

        return False

    def format_markdown(self, title, content):
        """
        格式化Markdown内容
        
        Args:
            title: 标题
            content: 内容
            
        Returns:
            str: 格式化后的Markdown文本
        """
        return f"""# {title}

{content}

> 由StockSelector自动生成 - {time.strftime('%Y-%m-%d %H:%M:%S')}"""
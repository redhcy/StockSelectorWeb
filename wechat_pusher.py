import requests
import logging
from config import SERVERCHAN_KEY, SERVERCHAN_URL

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("stock_selector.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("wechat_pusher")

class WechatPusher:
    def __init__(self):
        self.push_url = SERVERCHAN_URL
        if not SERVERCHAN_KEY:
            logger.warning("未配置Server酱密钥，微信推送功能将无法使用")
    
    def push(self, title, content):
        """
        使用Server酱推送消息到微信
        
        Args:
            title (str): 消息标题
            content (str): 消息内容（支持Markdown格式）
            
        Returns:
            bool: 推送是否成功
        """
        if not SERVERCHAN_KEY:
            logger.error("未配置Server酱密钥，无法推送消息")
            return False
            
        try:
            # Server酱API参数
            data = {
                "title": title,
                "desp": content  # Server酱支持Markdown格式
            }
            
            logger.info("正在推送消息到微信...")
            response = requests.post(self.push_url, data=data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    logger.info("消息推送成功")
                    return True
                else:
                    logger.error(f"消息推送失败: {result.get('message', '未知错误')}")
                    return False
            else:
                logger.error(f"请求失败: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"推送消息时发生错误: {e}")
            return False
    
    def push_stock_analysis(self, analysis_content):
        """
        推送股票分析结果
        
        Args:
            analysis_content (str): 分析结果内容（Markdown格式）
            
        Returns:
            bool: 推送是否成功
        """
        title = "今日A股热点概念及推荐个股"
        return self.push(title, analysis_content)

# 测试代码
if __name__ == "__main__":
    pusher = WechatPusher()
    test_content = """
# 测试推送

这是一条测试消息，用于验证微信推送功能是否正常工作。

## 功能特点
1. 支持Markdown格式
2. 实时推送
3. 可靠性高

*这是一条测试消息*
    """
    pusher.push("测试消息", test_content)
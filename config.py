import os
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# API配置
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')
DEEPSEEK_API_URL = os.environ.get('DEEPSEEK_API_URL', 'https://api.deepseek.com/v1/chat/completions')

# 微信推送配置 (Server酱)
SERVERCHAN_KEY = os.environ.get('SERVERCHAN_KEY', '')
SERVERCHAN_URL = "https://sctapi.ftqq.com/{}.send".format(SERVERCHAN_KEY)

# 首次运行设置
FIRST_RUN = os.environ.get('FIRST_RUN', 'true').lower() == 'true'

# 新闻来源配置
NEWS_SOURCES = [
    "证券时报",
    "上海证券报",
    "中国证券报",
    "证券日报",
    "东方财富网",
    "21世纪经济报道"
]

# 验证配置
def validate_config():
    """验证配置是否完整"""
    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "your_api_key_here":
        raise ValueError("""
请配置有效的DEEPSEEK_API_KEY：
1. 打开.env文件
2. 将your_api_key_here替换为您的实际API密钥
3. 保存文件后重新运行应用
""")
    if not SERVERCHAN_KEY:
        raise ValueError("未配置SERVERCHAN_KEY")

# Web服务器配置
WEB_HOST = os.getenv("WEB_HOST", "0.0.0.0")
WEB_PORT = int(os.getenv("WEB_PORT", "5000"))
WEB_DEBUG = os.getenv("WEB_DEBUG", "true").lower() == "true"

# 分析任务配置
ANALYSIS_TIME = "09:30"  # 每天上午9:30分析一次
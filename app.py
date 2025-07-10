from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
load_dotenv()  # 确保加载.env文件
from stock_analyzer import StockAnalyzer
from deepseek_api import DeepseekAPI
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("web")

app = Flask(__name__)

# 创建分析器实例
analyzer = StockAnalyzer()

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/analyze_hotspots', methods=['POST'])
def analyze_hotspots():
    """分析热点股票"""
    try:
        logger.info("收到热点分析请求")
        
        # 获取请求数据
        data = request.get_json()
        sources = data.get('sources', ['东方财富'])
        
        # 获取热点新闻
        news = analyzer.get_hotspot_news(sources)
        # 构建提示词
        prompt = "请综合东方财富网等的最新热点头条与社区话题，分析热点概念板块，推荐明天最有可能涨停的个股，优先推荐中小盘股票或央企国企股票。\n" + analyzer.build_hotspot_prompt(news)
        # 调用Deepseek API
        api = DeepseekAPI()
        response = api.chat_completion([
            {"role": "system", "content": "你是一位专业的股票分析师，擅长分析A股市场热点概念。"},
            {"role": "user", "content": prompt}
        ])
        if not response:
            logger.error("API调用失败")
            return jsonify({
                "status": "error",
                "message": "API调用失败"
            }), 500
        # 解析结果
        content = response['choices'][0]['message']['content']
        result = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "analysis": content
        }
        logger.info("热点分析完成")
        return jsonify({
            "status": "success",
            "result": result
        })
    except Exception as e:
        logger.error(f"处理热点分析请求时出错: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

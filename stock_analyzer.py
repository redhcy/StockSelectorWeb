import json
import logging
import time
from datetime import datetime
import requests
from deepseek_api import DeepseekAPI
from config import NEWS_SOURCES, validate_config

# 配置日志
logger = logging.getLogger()

class StockAnalyzer:
    def __init__(self):
        # 验证配置
        validate_config()
        self.api = DeepseekAPI()
        
    def get_news(self, sources=None):
        """
        获取今日财经新闻
        
        Args:
            sources: 新闻来源列表，默认使用配置中的NEWS_SOURCES
            
        Returns:
            str: 新闻文本
        """
        if sources is None:
            sources = NEWS_SOURCES
            
        try:
            logger.info("获取今日财经新闻...")
            # 这里可以添加实际的新闻API调用
            # 目前使用模拟数据
            
            # 获取当前日期
            today = datetime.now().strftime("%Y年%m月%d日")
            
            # 模拟新闻数据
            news = f"{today}财经要闻：\n"
            news += "1. 央行发布2023年第四季度货币政策执行报告\n"
            news += "2. 证监会：进一步深化资本市场改革\n"
            news += "3. 国家统计局：4月份CPI同比上涨0.3%\n"
            news += "4. 多部门联合发文促进民营经济发展\n"
            news += "5. 沪指震荡收涨0.5%，创业板指跌0.2%\n"
            
            logger.info("新闻获取成功")
            return news
        except Exception as e:
            logger.error(f"获取新闻失败: {str(e)}")
            return f"获取新闻失败: {str(e)}"
    
    def analyze(self, test_mode=False):
        """
        分析股市并生成报告
        
        Args:
            test_mode: 是否为测试模式
            
        Returns:
            dict: 分析结果
        """
        try:
            # 获取新闻
            news = self.get_news()
            
            if test_mode:
                logger.info("测试模式：跳过API调用，返回测试数据")
                return {
                    "market_analysis": "这是测试市场分析",
                    "stock_picks": ["测试股票1", "测试股票2", "测试股票3"],
                    "reasoning": "这是测试推理过程"
                }
            
            # 构建提示词
            prompt = self._build_prompt(news)
            
            # 调用API
            logger.info("调用Deepseek API进行分析...")
            response = self.api.chat_completion([
                {"role": "system", "content": "你是一位专业的股票分析师，擅长分析A股市场。"},
                {"role": "user", "content": prompt}
            ])
            
            if not response:
                logger.error("API调用失败，无响应")
                return None
                
            # 解析结果
            try:
                content = response['choices'][0]['message']['content']
                logger.info("成功获取API响应")
                
                # 尝试解析JSON
                try:
                    # 提取JSON部分
                    json_str = content
                    if "```json" in content:
                        json_str = content.split("```json")[1].split("```")[0].strip()
                    elif "```" in content:
                        json_str = content.split("```")[1].split("```")[0].strip()
                        
                    result = json.loads(json_str)
                    logger.info("成功解析JSON结果")
                    return result
                except json.JSONDecodeError:
                    logger.warning("JSON解析失败，尝试使用原始文本")
                    # 如果JSON解析失败，返回原始文本
                    return {
                        "market_analysis": content,
                        "stock_picks": [],
                        "reasoning": "JSON解析失败，使用原始文本"
                    }
            except (KeyError, IndexError) as e:
                logger.error(f"解析API响应失败: {str(e)}")
                return None
                
        except Exception as e:
            logger.error(f"分析过程出错: {str(e)}")
            return None
    
    def _build_prompt(self, news):
        """
        构建提示词
        
        Args:
            news: 新闻文本
            
        Returns:
            str: 提示词
        """
        today = datetime.now().strftime("%Y年%m月%d日")
        
        prompt = f"""
请你作为一名专业的股票分析师，根据以下{today}的财经新闻，分析A股市场走势，并推荐3-5只值得关注的股票。

新闻内容：
{news}

请提供：
1. 对当前A股市场的整体分析
2. 3-5只值得关注的股票，包括股票名称、代码和推荐理由
3. 你的分析推理过程

请以JSON格式返回结果，格式如下：
```json
{{
  "market_analysis": "市场分析内容",
  "stock_picks": [
    {{
      "name": "股票名称",
      "code": "股票代码",
      "reason": "推荐理由"
    }},
    ...
  ],
  "reasoning": "分析推理过程"
}}
```
"""
        return prompt
    
    def format_for_wechat(self, result):
        """
        将分析结果格式化为微信推送内容
        
        Args:
            result: 分析结果
            
        Returns:
            str: 格式化后的内容
        """
        if not result:
            return "分析失败，无结果"
            
        today = datetime.now().strftime("%Y年%m月%d日")
        
        # 处理市场分析
        market_analysis = result.get("market_analysis", "无市场分析")
        
        # 处理股票推荐
        stock_picks = result.get("stock_picks", [])
        stock_content = ""
        
        if isinstance(stock_picks, list):
            for i, stock in enumerate(stock_picks, 1):
                if isinstance(stock, dict):
                    name = stock.get("name", "未知")
                    code = stock.get("code", "未知")
                    reason = stock.get("reason", "无推荐理由")
                    stock_content += f"### {i}. {name}（{code}）\n{reason}\n\n"
                else:
                    stock_content += f"### {i}. {stock}\n\n"
        else:
            stock_content = "无股票推荐"
            
        # 处理推理过程
        reasoning = result.get("reasoning", "无推理过程")
        
        # 组合内容
        content = f"""## 📊 市场分析
{market_analysis}

## 🔍 推荐关注股票
{stock_content}

## 💡 分析推理
{reasoning}
"""
        
        return content

    def get_hotspot_news(self, sources=None):
        """
        获取热点新闻数据
        
        Args:
            sources: 新闻来源列表
            
        Returns:
            str: 热点新闻文本
        """
        if sources is None:
            sources = ["东方财富"]
            
        try:
            logger.info("获取热点新闻...")
            # 这里可以添加实际的新闻API调用
            # 目前使用模拟数据
            
            # 获取当前日期
            today = datetime.now().strftime("%Y年%m月%d日")
            
            # 模拟热点新闻数据
            news = f"{today}热点概念：\n"
            news += "1. 人工智能：OpenAI发布新一代大模型\n"
            news += "2. 新能源：光伏产业链价格企稳回升\n"
            news += "3. 半导体：国产芯片替代加速\n"
            news += "4. 医药：创新药审批速度加快\n"
            news += "5. 消费电子：苹果发布新产品\n"
            
            logger.info("热点新闻获取成功")
            return news
        except Exception as e:
            logger.error(f"获取热点新闻失败: {str(e)}")
            return f"获取热点新闻失败: {str(e)}"

    def build_hotspot_prompt(self, news):
        """
        构建热点分析提示词
        
        Args:
            news: 热点新闻文本
            
        Returns:
            str: 提示词
        """
        today = datetime.now().strftime("%Y年%m月%d日")
        
        prompt = f"""
请你作为一名专业的股票分析师，根据以下{today}的热点新闻，分析相关概念板块及个股。

新闻内容：
{news}

请提供：
1. 热点概念分析
2. 3-5只相关概念股票推荐，包括：
   - 股票名称、代码
   - 概念相关性
   - 基本面分析（PE、PB、ROE等）
   - 技术面分析（支撑位、压力位、上涨空间）
   - 明日走势预测
3. 综合分析结论

请以JSON格式返回结果，格式如下：
```json
{{
  "hotspot_analysis": "热点概念分析",
  "stock_recommendations": [
    {{
      "name": "股票名称",
      "code": "股票代码",
      "concept": "相关概念",
      "fundamental": "基本面分析",
      "technical": {{
        "support": "支撑位",
        "resistance": "压力位",
        "upside": "上涨空间"
      }},
      "prediction": "明日走势预测"
    }},
    ...
  ],
  "conclusion": "综合分析结论"
}}
```
"""
        return prompt
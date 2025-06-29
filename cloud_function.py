import os
import json
from datetime import datetime
import logging
from stock_analyzer import StockAnalyzer
from wechat_pusher import WechatPusher

# 配置日志（云函数环境）
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def main_handler(event, context):
    """
    云函数入口
    :param event: 触发事件
    :param context: 运行上下文
    :return: 执行结果
    """
    try:
        logger.info("开始执行股票分析任务...")
        
        # 初始化分析器和推送器
        analyzer = StockAnalyzer()
        pusher = WechatPusher()
        
        # 执行分析（非测试模式）
        max_retries = 3
        result = None
        
        for attempt in range(max_retries):
            try:
                result = analyzer.analyze(test_mode=False)
                if result:
                    break
                logger.warning(f"第 {attempt + 1} 次尝试分析失败，准备重试...")
            except Exception as e:
                logger.error(f"第 {attempt + 1} 次分析出错: {e}")
                if attempt < max_retries - 1:
                    continue
                raise
        
        if not result:
            error_msg = "分析失败：无法获取有效结果"
            logger.error(error_msg)
            pusher.push("股票分析失败", f"❌ {error_msg}")
            return {
                "statusCode": 500,
                "body": error_msg
            }
        
        # 格式化结果并推送
        formatted_result = analyzer.format_for_wechat(result)
        push_result = pusher.push_stock_analysis(formatted_result)
        
        if not push_result:
            error_msg = "推送失败：无法发送微信消息"
            logger.error(error_msg)
            return {
                "statusCode": 500,
                "body": error_msg
            }
        
        success_msg = "分析和推送任务完成"
        logger.info(success_msg)
        return {
            "statusCode": 200,
            "body": success_msg
        }
        
    except Exception as e:
        error_msg = f"任务执行出错: {str(e)}"
        logger.error(error_msg)
        try:
            pusher = WechatPusher()
            pusher.push("股票分析任务异常", f"❌ {error_msg}")
        except Exception as push_error:
            logger.error(f"推送错误消息时发生异常: {push_error}")
        return {
            "statusCode": 500,
            "body": error_msg
        }
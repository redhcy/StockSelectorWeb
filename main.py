import schedule
import time
import logging
import os
from datetime import datetime
from stock_analyzer import StockAnalyzer
from wechat_pusher import WechatPusher
from config import ANALYSIS_TIME

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("stock_selector.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("main")

def check_environment():
    """检查环境配置是否正确"""
    from config import DEEPSEEK_API_KEY, SERVERCHAN_KEY
    
    if not DEEPSEEK_API_KEY:
        logger.warning("未配置Deepseek API密钥，请在.env文件中设置DEEPSEEK_API_KEY")
        return False
        
    if not SERVERCHAN_KEY:
        logger.warning("未配置Server酱密钥，请在.env文件中设置SERVERCHAN_KEY")
        return False
        
    return True

def run_analysis():
    """运行股票分析并推送结果"""
    logger.info("开始执行股票分析任务...")
    
    try:
        # 创建股票分析器
        analyzer = StockAnalyzer()
        
        # 分析股票市场
        analysis_result = analyzer.analyze()
        
        if not analysis_result:
            logger.error("分析失败，无法获取结果")
            return
            
        # 格式化结果用于微信推送
        formatted_content = analyzer.format_for_wechat(analysis_result)
        
        # 保存分析结果
        analyzer.save_analysis_result(analysis_result)
        
        # 推送到微信
        pusher = WechatPusher()
        success = pusher.push_stock_analysis(formatted_content)
        
        if success:
            logger.info("股票分析任务完成，结果已推送到微信")
        else:
            logger.error("股票分析任务完成，但推送到微信失败")
            
    except Exception as e:
        logger.error(f"执行股票分析任务时出错: {e}")

def setup_schedule():
    """设置定时任务"""
    schedule.every().day.at(ANALYSIS_TIME).do(run_analysis)
    logger.info(f"已设置定时任务，将在每天 {ANALYSIS_TIME} 执行股票分析")

def main():
    """主函数"""
    logger.info("股票分析器启动...")
    
    # 检查环境配置
    if not check_environment():
        logger.error("环境配置不正确，请检查.env文件")
        return
    
    # 设置定时任务
    setup_schedule()
    
    # 如果是首次运行，立即执行一次分析
    first_run = os.environ.get("FIRST_RUN", "true").lower() == "true"
    if first_run:
        logger.info("首次运行，立即执行分析")
        run_analysis()
    
    # 持续运行，等待定时任务触发
    logger.info("进入定时任务循环，按Ctrl+C退出")
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次是否有待执行的任务
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序运行出错: {e}")
    finally:
        logger.info("股票分析器已停止")

if __name__ == "__main__":
    main()
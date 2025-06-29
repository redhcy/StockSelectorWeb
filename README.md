# StockSelector - 股票分析推荐系统

StockSelector是一个基于大模型的股票分析推荐系统，可以自动分析A股市场走势并推荐值得关注的股票。系统会定期执行分析任务，并通过微信推送结果。

## 功能特点

- 自动获取最新财经新闻
- 利用DeepSeek大模型分析市场走势
- 智能推荐值得关注的股票
- 通过微信推送分析结果
- 支持腾讯云函数部署，实现定时执行

## 系统架构

- `cloud_function.py`: 云函数入口文件
- `stock_analyzer.py`: 股票分析核心逻辑
- `deepseek_api.py`: DeepSeek API调用封装
- `wechat_push.py`: 微信推送功能
- `config.py`: 配置文件

## 部署指南

### 1. 准备工作

- 注册[DeepSeek](https://www.deepseek.com/)账号，获取API密钥
- 注册[Server酱](https://sct.ftqq.com/)账号，获取微信推送密钥

### 2. 腾讯云函数部署

1. 登录[腾讯云函数控制台](https://console.cloud.tencent.com/scf/list)
2. 创建新函数
   - 选择"从头开始"创建
   - 运行环境选择"Python 3.7"
   - 提交方法选择"本地上传zip包"或"本地上传文件夹"

3. 配置环境变量
   - `DEEPSEEK_API_KEY`: DeepSeek API密钥
   - `WECHAT_PUSH_KEY`: Server酱推送密钥

4. 配置触发器
   - 触发方式选择"定时触发"
   - 根据需要设置执行频率，例如每天早上9点执行：`0 0 9 * * * *`

5. 配置函数属性
   - 执行超时时间建议设置为60秒或更长
   - 内存配置建议设置为128MB或更高

### 3. 本地测试

如果需要在本地测试，可以执行以下命令：

```bash
# 设置环境变量
export DEEPSEEK_API_KEY=your_api_key
export WECHAT_PUSH_KEY=your_push_key

# 执行测试
python -c "from cloud_function import main_handler; main_handler({}, {})"
```

## 注意事项

- 确保API密钥和推送密钥的安全，不要泄露
- 云函数执行时间有限制，如果分析过程较长，可能需要增加超时时间
- 定时触发的频率不宜过高，以免超出API调用限制

## 常见问题

1. **推送失败**
   - 检查WECHAT_PUSH_KEY是否正确
   - 检查Server酱账号是否正常

2. **分析结果不准确**
   - 可能是由于新闻数据不足，可以扩充新闻来源
   - 可以调整提示词以获得更精确的分析

3. **云函数执行超时**
   - 增加云函数的超时时间设置
   - 优化代码执行效率
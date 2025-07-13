# 操作日志

## 2025-07-13 - Vercel免费部署方案建议

### 需求
用户希望将StockSelector项目免费部署到云端，要求平台完全免费。

### 解决方案
推荐使用[Vercel](https://vercel.com/)平台，支持Python Serverless Function，部署简单，适合API和轻量Web服务。

### Vercel部署步骤
1. 注册并登录Vercel（支持GitHub账号一键登录）。
2. 新建项目，选择导入GitHub上的StockSelector仓库。
3. 配置项目：
   - 选择Python作为Serverless Function运行环境。
   - 保证`requirements.txt`存在，Vercel会自动安装依赖。
   - 如需Web服务，入口文件命名为`api/index.py`或`api/xxx.py`。
   - 如需定时任务，可用Vercel Cron功能（需在Dashboard设置）。
4. 设置环境变量（如DEEPSEEK_API_KEY、SERVERCHAN_KEY等）。
5. 部署后，Vercel会分配一个免费域名。

### 注意事项
- Vercel免费版Serverless函数有冷启动和执行时间限制，适合API和轻量定时任务。
- 若需长期运行的服务，建议结合Railway等平台。
- 国内访问Vercel速度较快，但API调用需考虑外网访问。

### 状态
- [x] 已推荐Vercel免费部署方案
- [ ] 用户是否需要详细部署教程

--- 

## 2025-07-13 - 腾讯云云开发/云函数免费部署方案建议

### 需求
用户希望将StockSelector项目免费部署到腾讯云，要求平台完全免费。

### 解决方案
推荐使用[腾讯云云开发（CloudBase）](https://cloudbase.net/)或[腾讯云函数（SCF）](https://console.cloud.tencent.com/scf/list)。
- 支持Python运行环境和定时任务，免费额度充足，国内访问速度快。

### 腾讯云云函数部署步骤
1. 注册并登录腾讯云，进入[云函数控制台](https://console.cloud.tencent.com/scf/list)。
2. 新建函数，选择“从头开始创建”，运行环境选择“Python 3.7/3.8/3.9”。
3. 上传代码包（可直接上传本地zip，包含`cloud_function.py`、依赖包等）。
4. 配置环境变量（如DEEPSEEK_API_KEY、SERVERCHAN_KEY等）。
5. 配置定时触发器（Cron表达式如：`0 0 9 * * * *`，每天9点执行）。
6. 保存并部署，支持在线测试。

### 腾讯云云开发部署步骤
1. 注册并登录[腾讯云云开发](https://cloudbase.net/)。
2. 新建环境，选择“云函数”服务。
3. 新建云函数，上传代码包，配置运行环境和环境变量。
4. 可结合云定时器实现定时分析和推送。

### 注意事项
- 免费额度充足，适合个人和小型项目。
- 云函数有执行时间和内存限制，建议优化分析逻辑。
- 需实名认证。
- 代码包需包含所有依赖（可用`pip install -t . 包名`打包依赖）。

### 状态
- [x] 已推荐腾讯云免费部署方案
- [ ] 用户是否需要详细部署教程

--- 
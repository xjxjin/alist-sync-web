import os
import sys
import time
import logging
from datetime import datetime

# 设置时区
os.environ['TZ'] = 'Asia/Shanghai'
if hasattr(time, 'tzset'):
    time.tzset()

# 添加当前目录到PYTHONPATH
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# 配置日志打印到控制台
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 输出启动信息
print(f"Python解释器: {sys.executable}")
print(f"当前工作目录: {os.getcwd()}")
print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"时区设置: {os.environ['TZ']}")

# 导入应用工厂函数
from app import create_app

# 创建应用实例
app = create_app()

# 应用信息
with app.app_context():
    print("\n===== 应用配置信息 =====")
    print(f"SECRET_KEY: {'*' * 8}")
    print(f"DEBUG: {app.config.get('DEBUG')}")
    
    # 检查同步管理器
    if 'SYNC_MANAGER' in app.config:
        sync_manager = app.config['SYNC_MANAGER']
        print("\n===== 调度器任务信息 =====")
        jobs = sync_manager.scheduler.get_jobs()
        print(f"调度器中共有 {len(jobs)} 个任务:")
        
        for job in jobs:
            job_id = job.id
            next_run = job.next_run_time
            print(f" - 任务: {job_id}, 下一次运行: {next_run}")
    else:
        print("同步管理器未初始化！")

if __name__ == '__main__':
    # 读取端口配置，如果没有则使用默认端口5000
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"\n启动Flask应用: http://localhost:{port}")
    print(f"调试模式: {'开启' if debug else '关闭'}")
    
    # 启动应用
    app.run(debug=debug, host='0.0.0.0', port=port) 
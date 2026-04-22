# -*- coding: utf-8 -*-
import sys
import os

# 确保在 GitHub Actions / Linux 下能正确 import 本地模块
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from golden_get import get_gold_price
from gold_notice import send_email

PRICE_FILE = "last_price.txt"


# ======================
# 从环境变量读取配置
# ======================
def get_env_float(key, default=None):
    value = os.environ.get(key)
    if value is None:
        if default is None:
            raise RuntimeError(f"缺少环境变量: {key}")
        return default
    try:
        return float(value)
    except ValueError:
        raise RuntimeError(f"环境变量 {key} 不是合法数字: {value}")


PRICE_UP_THRESHOLD = get_env_float("PRICE_UP_THRESHOLD", 0.0)
PRICE_DOWN_THRESHOLD = get_env_float("PRICE_DOWN_THRESHOLD", 0.0)


# ======================
# 价格文件读写
# ======================
def load_last_price():
    if not os.path.exists(PRICE_FILE):
        print("[DEBUG] 未找到历史价格文件 last_price.txt")
        return None

    with open(PRICE_FILE, "r", encoding="utf-8") as f:
        price = float(f.read())
        print(f"[DEBUG] 读取到历史价格: {price}")
        return price


def save_price(price):
    with open(PRICE_FILE, "w", encoding="utf-8") as f:
        f.write(str(price))
    print(f"[DEBUG] 已保存当前价格: {price}")


# ======================
# 主逻辑
# ======================
def main():
    print("[INFO] 启动黄金价格监控程序")
# test
    try:
        send_email(...)
        print("[SUCCESS] 邮件发送成功")
    except Exception as e:
        print(f"[ERROR] 邮件发送失败: {e}")
        
    try:
        current_price = get_gold_price()
        print(f"[INFO] 当前实时金价: {current_price} 元/克")
    except Exception as e:
        print(f"[FATAL] 获取金价失败: {e}")
        return

    last_price = load_last_price()

    if last_price is None:
        print("[INFO] 首次运行，仅记录价格")
        save_price(current_price)
        return

    diff = current_price - last_price
    print(f"[DEBUG] 价格变化: {diff:.2f} 元")

    if diff >= PRICE_UP_THRESHOLD:
        print("[ACTION] 触发上涨提醒")
        send_email(
            "黄金价格上涨提醒",
            f"当前价格 {current_price} 元/克\n上涨 {diff:.2f} 元"
        )

    elif diff <= -PRICE_DOWN_THRESHOLD:
        print("[ACTION] 触发下跌提醒")
        send_email(
            "黄金价格下跌提醒",
            f"当前价格 {current_price} 元/克\n下跌 {abs(diff):.2f} 元"
        )

    else:
        print("[INFO] 价格波动未达到提醒阈值")

    save_price(current_price)
    print("[INFO] 本次检测完成")


if __name__ == "__main__":
    main()

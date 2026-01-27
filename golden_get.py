# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import akshare as ak


def get_gold_price():
    """
    获取上海黄金交易所 Au99.99 实时价格（人民币/克）
    作为“工商银行如意金条”的基准参考价
    """
    print("[DEBUG] 开始获取 Au99.99 实时行情...")

    try:
        df = ak.spot_quotations_sge(symbol="Au99.99")
        print("[DEBUG] AkShare 接口调用成功")
        
        # 检查数据时效性（假设返回数据包含"日期"和"时间"字段）
        latest_time = df["时间"].iloc[0]  # 或根据实际字段名调整
        print(f"[DEBUG] 最新数据时间: {latest_time}")
        
    except Exception as e:
        print("[ERROR] AkShare 接口调用失败")
        print(f"[ERROR] 异常信息: {e}")
        raise RuntimeError(f"获取黄金行情失败: {e}")
    
    if df is None or df.empty:
        print("no data")
        raise ValueError("未获取到黄金实时行情数据")
    
    print(f"[DEBUG] 获取到行情记录数: {len(df)}")
    print(f"[DEBUG] 字段列表: {list(df.columns)}")

    # 通常最新一条即为实时价格
    latest_row = df.iloc[-1]
    print("[DEBUG] 最新一条行情数据:")
    print(latest_row)

    # AkShare 字段名可能随版本略有差异，做防御式读取
    for col in ["现价", "最新价", "价格"]:
            if col in latest_row:
                print(f"[DEBUG] 尝试使用字段: {col}")
                try:
                    price = float(latest_row[col])
                    print(f"[SUCCESS] 成功解析实时金价: {price} 元/克")
                    return price
                except Exception as e:
                    print(f"[WARN] 字段 {col} 转换失败: {e}")
    raise ValueError("未能解析 Au99.99 实时价格")



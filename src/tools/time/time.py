from datetime import datetime

def get_current_date() -> str:
    current_time_str = datetime.now().strftime("%Y-%m-%d")
    print(f"⌚️ 获取当前时间: {current_time_str}")

    return current_time_str

from datetime import datetime


class Logger:

    @staticmethod
    def info(message):
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"[{current_time}] [INFO] {message}")

    @staticmethod
    def success(message):
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"[{current_time}] [SUCCESS] {message}")

    @staticmethod
    def error(message):
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"[{current_time}] [ERROR] {message}")
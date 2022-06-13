from datetime import datetime
import os
import sys

os.system("color")

class LevelStyles():
    ## 1 if bold else 0;color
    info_color = "0;37m"
    success_color = "1;32m"
    warning_color = "1;33m"
    error_color = "1;31m"

class Logger():
    pref = "\033["
    reset = f"{pref}0m"

    def __init__(self, *, file_path=None):
        self.file_path = f"logs/{file_path}"
        if not file_path:
            self.file_path = f"logs/{datetime.now().strftime('%m%d%H%M%S')}.log"
        self.log_file = open(self.file_path, "w", encoding="utf-8")
    
    def write_log(self, text):
        self.log_file.write(text + "\n")
        self.log_file.flush()
        os.fsync(self.log_file.fileno())

    def success(self, text):
        self.write_log(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' (SUCCESS) ' + text)
        print(f'{self.pref}{LevelStyles.success_color}' + text + self.reset)

    def info(self, text):
        self.write_log(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' (INFO) ' + text)
        print(f'{self.pref}{LevelStyles.info_color}' + text + self.reset)
    
    def warning(self, text):
        self.write_log(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' (WARNING) ' + text)
        print(f'{self.pref}{LevelStyles.warning_color}' + text + self.reset)
    
    def error(self, text):
        self.write_log(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' (ERROR) ' + text)
        print(f'{self.pref}{LevelStyles.error_color}' + text + self.reset)

log = Logger()

def global_error_handler(errtype, value, traceback):
    log.error(f"{errtype}: {value}")
    sys.__excepthook__(errtype, value, traceback)
    sys.exit(1)

sys.excepthook = global_error_handler
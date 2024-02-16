import os
import tkinter as tk
import tkinter.font as tkfont

# 创建并隐藏默认的根窗口
root = tk.Tk()
root.withdraw()

# 获取系统中的字体列表
fonts = tkfont.families()
font_names = [item for item in fonts if '@' not in item]

# 销毁根窗口
root.destroy()

project_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
config_dir = project_dir.replace("/utils", "") + "/config/"  # 配置文件

# 写入文本文件
with open(config_dir + 'font_data.txt', 'w', encoding='utf-8') as file:
    for font in font_names:
        file.write(font + '\n')



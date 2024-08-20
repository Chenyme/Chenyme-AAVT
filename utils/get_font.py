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

path = os.getcwd().replace("utils", "/")

# 写入文本文件
with open(path + '/config/font.txt', 'w', encoding='utf-8') as file:
    for font in font_names:
        file.write(font + '\n')

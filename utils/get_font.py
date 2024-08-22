import os
import platform


def get_font_data():
    system_type = platform.system()

    if system_type == "Windows":

        import re
        import winreg

        fonts = []
        key = r"Software\Microsoft\Windows NT\CurrentVersion\Fonts"
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key, 0, winreg.KEY_READ)
        for i in range(0, winreg.QueryInfoKey(registry_key)[1]):
            font_name, font_path, _ = winreg.EnumValue(registry_key, i)
            clean_font_name = re.sub(r'\s*\(.*?\)\s*', '', font_name).strip()
            fonts.append(clean_font_name)
        winreg.CloseKey(registry_key)
        path = os.getcwd().replace("utils", "/")
        with open(path + '/config/font.txt', 'w', encoding='utf-8') as file:
            for font in fonts:
                file.write(font + "\n")

    elif system_type in ["Darwin"]:
        import subprocess
        import re

        result = subprocess.run(['system_profiler', 'SPFontsDataType'], capture_output=True, text=True)
        output = result.stdout
        fonts = re.findall(r'Full Name: (.+)', output)
        path = os.path.join(os.getcwd().replace("utils", ""), 'config', 'font.txt')
        with open(path, 'w', encoding='utf-8') as file:
            for font in fonts:
                file.write(font + "\n")
                
    elif system_type in ["Linux"]:
        import subprocess
        
        result = subprocess.run(['fc-list', ':', 'family'], capture_output=True, text=True)
        output = result.stdout
        fonts = output.split('\n')
        path = os.path.join(os.getcwd().replace("utils", ""), 'config', 'font.txt')
        with open(path, 'w', encoding='utf-8') as file:
            for font in fonts:
                if font:
                    file.write(font + "\n")

    else:
        print(f"获取字体失败！尚未支持的操作系统: {system_type}")

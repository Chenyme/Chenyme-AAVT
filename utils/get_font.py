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

    elif system_type == "Linux":

        import subprocess
        import re

        result = subprocess.run(['fc-list', ':family'], stdout=subprocess.PIPE, text=True)
        font_lines = result.stdout.splitlines()
        fonts = set()
        for line in font_lines:
            match = re.search(r":\s*([^:]+)", line)
            if match:
                font_name = match.group(1).split(",")[0].strip()
                fonts.add(font_name)
        sorted_fonts = sorted(fonts)
        path = os.path.join(os.getcwd().replace("utils", ""), 'config', 'font.txt')
        with open(path, 'w', encoding='utf-8') as file:
            for font in sorted_fonts:
                file.write(font + "\n")

    elif system_type == "Darwin":
        import AppKit

        font_manager = AppKit.NSFontManager.sharedFontManager()
        font_families = font_manager.availableFontFamilies()

        path = os.path.join(os.getcwd().replace("utils", ""), 'config', 'font.txt')
        with open(path, 'w', encoding='utf-8') as file:
            for family in font_families:
                file.write(family + "\n")

    else:
        print(f"获取字体失败！尚未支持的操作系统: {system_type}")

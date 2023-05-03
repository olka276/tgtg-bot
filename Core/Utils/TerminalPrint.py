from Core.Utils.TerminalColor import TerminalColor


def color_print(color, text):
    print(color.value, text, TerminalColor.ENDC.value)

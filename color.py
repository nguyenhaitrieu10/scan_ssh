class AsciiColor(object):

    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CYAN = '\033[36m',
    MAGENTA = '\033[35m'

    @staticmethod
    def red(text):
        return AsciiColor.RED + text + AsciiColor.ENDC

    @staticmethod
    def blue(text):
        return AsciiColor.BLUE + text + AsciiColor.ENDC

    @staticmethod
    def green(text):
        return AsciiColor.GREEN + text + AsciiColor.ENDC
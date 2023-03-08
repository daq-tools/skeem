from colorama import Fore, Style

from skeem import __version__
from skeem.type import TypeInfo
from skeem.util.platform import about_platform
from skeem.util.report import bullet_list, section, subsection


class AboutReport:
    @staticmethod
    def types():
        section("Skeem")
        print()
        print(f"{Fore.YELLOW + Style.BRIGHT}Version:{Style.RESET_ALL} " f"{Style.BRIGHT}{__version__}{Style.RESET_ALL}")
        print()
        for name, content in TypeInfo.get().items():
            subsection(name)
            print(bullet_list(content))
            print()
        print()

    @staticmethod
    def platform():
        section("Platform")
        print()
        about_platform()
        print()

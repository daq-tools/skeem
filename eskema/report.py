from colorama import Fore, Style

from eskema import __version__
from eskema.type import TypeInfo
from eskema.util.platform import about_platform
from eskema.util.report import bullet_list, section, subsection


class AboutReport:
    @staticmethod
    def types():
        section("Eskema")
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

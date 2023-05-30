from rich.console import Console

class logging:
    def __init__(self) -> None:
        self.console = Console()


    def error(self,msg):
        self.console.print(msg,style = "red")

    def success(self,msg):
        self.console.print(msg,style="green")

    def warning(self,msg):
        self.console.print(msg,style="orange")
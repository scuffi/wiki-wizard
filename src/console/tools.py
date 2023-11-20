from rich.console import Console

console = Console()


def monitor(message: str):
    def inner_function(func):
        def wrapper(*args, **kwargs):
            with console.status(message, spinner="arc"):
                result = func(*args, **kwargs)
            return result

        return wrapper

    return inner_function

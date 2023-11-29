from javascript import require

# * Martian is an external JS package built to convert markdown/text into notion blocks
# https://github.com/tryfabric/martian
# * We have to use an awesome javascript bridge to use this package as there is no python bindings
martian = require("@tryfabric/martian")


def parse2notion(markdown: str):
    """Parse a markdown text string into valid Notion Blocks/JSON API text

    Args:
        markdown (str): The markdown string

    Returns:
        list[any]: The parsed MD text in JSON format
    """
    return martian.markdownToBlocks(markdown).valueOf()

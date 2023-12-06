from dotenv import load_dotenv

load_dotenv()

from pipelines import CompletePipeline

# TODO: Migrate Agents into GPTs in OpenAI, allowing central control & configuration of each agent.
# TODO: See - https://www.youtube.com/watch?v=AVInhYBUnKs&t=479s

# * Project start
if __name__ == "__main__":
    title = "Nim Programming Language"

    page_url = "https://www.notion.so/archief/93992d8440fa4111b06e7cc5748fac5e?v=6429bb958ce6452497c5089c15e9e6f2"

    pipeline = CompletePipeline(page_url)

    pipeline.run(title)

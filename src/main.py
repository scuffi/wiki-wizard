from dotenv import load_dotenv
from tasks import headings

load_dotenv()


# * Project start
print(headings.generate_headings("Toothpaste"))

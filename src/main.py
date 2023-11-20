from dotenv import load_dotenv

load_dotenv()

from tasks import headings


# * Project start
print(headings.generate_headings("RabbitMQ"))

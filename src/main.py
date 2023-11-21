from dotenv import load_dotenv

load_dotenv()

from tasks import writing


# * Project start
# print(headings.generate_headings("RabbitMQ"))
print(writing.write_section())

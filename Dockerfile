FROM python:3.10
WORKDIR /bot
COPY requirements.txt /bot/
RUN pip install -r requirements.txt
COPY /bot /bot
CMD python discordbot.py

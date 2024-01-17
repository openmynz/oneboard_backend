FROM python:3.11.4-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /oneboard_backend


# copy from the current directory of the Dockerfile to /mamba-backend in the image
COPY . .

COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./entrypoint.sh /entrypoint.sh
RUN ls -a
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN chown nobody /entrypoint.sh

CMD ["bash", "/entrypoint.sh"]

EXPOSE 8080
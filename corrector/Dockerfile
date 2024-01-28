FROM python:3-alpine AS src

ENV VERSION 2.1.1

RUN apk add --update --no-cache \
      unzip \
      wget \
 && wget https://grammalecte.net/grammalecte/zip/Grammalecte-fr-v${VERSION}.zip \
 && unzip Grammalecte-fr-v${VERSION}.zip -d /srv

FROM python:3-alpine

COPY --from=src /srv/ /srv

ENV PYTHONUNBUFFERED TRUE

EXPOSE 8080

WORKDIR /srv

ENTRYPOINT ["python3"]

CMD ["grammalecte-server.py","-ht", "0.0.0.0","-p","8080","-t"]

# Create the container with
# `docker build -t grammalecte:latest .`

# Lauch the container with:
# `docker run --rm -p 8080:8080 --name gr grammalecte:latest`

FROM python:3.7-alpine
ENV TZ=Asia/Shanghai

WORKDIR /tmp
COPY ./requirements.txt ./
RUN adduser app -D \
    && apk add --no-cache tzdata \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /tmp/*

WORKDIR /app
COPY index.py ./
COPY dailynotehelper ./dailynotehelper

USER app
CMD [ "python3", "./index.py" ]
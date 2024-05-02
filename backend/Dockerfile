FROM python:3.10.2-slim as base

ENV USER=fpm-mishina \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/src

RUN apt-get update && apt-get install --no-install-recommends -y \
    dumb-init \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && addgroup --system $USER && adduser --system --group $USER

ENV BUILDER_DIR=/usr/src/$USER

FROM base as builder

WORKDIR $BUILDER_DIR

COPY backend/requirements.txt backend/
RUN pip wheel --no-cache-dir --no-deps --wheel-dir "$BUILDER_DIR"/wheels \
    -r backend/requirements.txt

FROM base

ENV HOME_DIR=/home/$USER
ENV APP_DIR=$HOME_DIR/backend/src

WORKDIR $APP_DIR

COPY --from=builder $BUILDER_DIR/wheels /wheels
COPY --from=builder $BUILDER_DIR/backend/requirements.txt $HOME_DIR
RUN pip install --no-cache-dir /wheels/*

COPY ./backend/src $APP_DIR
COPY ../recognizer $HOME_DIR/recognizer

ENV PYTHONPATH=$APP_DIR

RUN chown -R "$USER":"$USER" $APP_DIR
RUN chown -R "$USER":"$USER" /opt

USER $USER

CMD ["bash", "-c", "dumb-init uvicorn driver.main:app --host 0.0.0.0 --port 8000"]

FROM python:3.11-alpine as build

WORKDIR /opt/loader
ENV PATH /opt/loader/.venv/bin/:$PATH

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.7.1 \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi

FROM build AS app

COPY --from=build /opt/loader /opt/loader
COPY . .

RUN chmod +x /opt/loader/entrypoint.sh

ENTRYPOINT ["/opt/loader/entrypoint.sh"]
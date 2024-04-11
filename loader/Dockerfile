FROM python:3.11-alpine as build

WORKDIR /opt/loader

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./

RUN python -m pip install --no-cache-dir -r requirements.txt

FROM build AS app

COPY --from=build /opt/loader /opt/loader
COPY . .

RUN chmod +x /opt/loader/entrypoint.sh

ENTRYPOINT ["/opt/loader/entrypoint.sh"]
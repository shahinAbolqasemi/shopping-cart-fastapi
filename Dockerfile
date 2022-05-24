FROM tiangolo/uvicorn-gunicorn-fastapi AS installer

WORKDIR /builder

RUN pip install -U pip

COPY requirements.txt ./

RUN pip wheel -w /wheelhouse -r requirements.txt

FROM tiangolo/uvicorn-gunicorn-fastapi AS runner

WORKDIR /service

COPY requirements.txt ./
COPY --from=installer /wheelhouse /wheelhouse

RUN pip install --no-index -f /wheelhouse -r requirements.txt

COPY . .

CMD ["sh", "entrypoint.sh"]

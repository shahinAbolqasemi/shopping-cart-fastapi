temp=$PYTHONPATH
export PYTHONPATH=.
python3 app/main.py init
export PYTHONPATH=$temp
gunicorn \
    -w ${NUM_WORKERS:=4} ${RELOAD} --backlog ${BACKLOG:=2048} \
    -b ${BIND_ADDRESS:=0.0.0.0}:${SERVICE_PORT:=8080} -k uvicorn.workers.UvicornWorker \
    --log-level ${LOG_LEVEL:=debug} -t ${WORKER_TIMEOUT:=20} \
    --log-file ${LOG_FILE:=-} \
    --worker-connections ${SIMULTANEOUS_CLIENTS:=1000} \
    app.main:app
FROM public.ecr.aws/lambda/python:3.13

WORKDIR ${LAMBDA_TASK_ROOT}

RUN pip install --no-cache-dir \
    "environs>=14.6.0" \
    "fastapi[standard-no-fastapi-cloud-cli]>=0.133.1" \
    "mangum>=0.21.0" \
    "pandas>=3.0.1" \
    "psycopg2-binary>=2.9.11" \
    "pydantic>=2.11.9" \
    "sqlalchemy>=2.0.47"

COPY core ./core
COPY infrastructure ./infrastructure
COPY service ./service
COPY main.py ./main.py
COPY seed_data.py ./seed_data.py

CMD ["main.handler"]
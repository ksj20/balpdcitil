ARG FUNCTION_DIR="/app"

# Change here (1)
FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.10.2023.10.24.15

# COPY requirements.txt  .
# RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY ${FUNCTION_DIR} ${LAMBDA_TASK_ROOT}${FUNCTION_DIR}/

# COPY requirements.txt  .
# RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Install the function's dependencies
RUN pip install --upgrade pip
# RUN python3.10 -m pip install --target /app awslambdaric

# Change here (2)
RUN python3.10 -m pip install awslambdaric

# Change here (3) aws-lambda-rie-arm64 -> aws-lambda-rie if x86 architecture
RUN mkdir -p /.aws-lambda-rie && curl -Lo /.aws-lambda-rie/aws-lambda-rie \
  https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie-arm64 \
    && chmod +x /.aws-lambda-rie/aws-lambda-rie

ENTRYPOINT [ "/.aws-lambda-rie/aws-lambda-rie","/var/lang/bin/python", "-m", "awslambdaric" ]

CMD [ "app.handler" ]
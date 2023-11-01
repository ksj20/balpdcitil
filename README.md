# Title

Build an AWS Lambda Python Docker container image, and test it locally as if triggering a real AWS Lambda function

# Description 

This AWS Lambda function is a simple Hello World app where it returns somthing like `{"message": "Hello Steve Jobs!"}`

If you want to build it, run 
```bash
$ sh build_run.sh
```

If you want to test it, run
```bash
$ sh curl_test.sh
```

If you want to change the function details, refer to `app/__init__.py`

# Caveats

If necessary, you can change some details:

- If you want to change the version of Python, refer to `Change here (1)` and `Change here (2)` in the `Dockerfile`, and change the version after `public.ecr.aws/lambda/python` to what you want

- If you have a different architecture than `arm64` which is recommended by AWS, you can refer to `Change here (3)` in the `Dockerfile` and change the github link accordingly. (ex) aws-lambda-rie-arm64 -> aws-lambda-rie if x86 architecture
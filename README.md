## ai_linebot
Image AI LINEBot on AWS CloudFormation and CI/CD pipeline

## about

###about product
LINE Bot who analyzes a person's emotions, age, and gender when sent an image

You can try it here!
https://liff.line.me/1645278921-kWRPP32q?accountId=163yiazd&openerPlatform=native&openerKey=talkroom%3Amessage#mst_challenge=b1q1r9yarEAEX4gqFCFLGLddVf1ef9EDcH9jFRAlEmM

###about dev
Using SAM to build and deploy the backend environment.
Using Code Pipeline to set CI/CD with github

### Before you begin
be familiar with AWS Serverless Application Model (AWS SAM) and codepipeline
See https://docs.aws.amazon.com/en_us/codepipeline/latest/userguide/tutorials-serverlessrepo-auto-publish.html for more about these AWS archtecture


### Step 1: Create a buildspec.yml file

example
```
version: 0.2
phases:
  install:
    runtime-versions:
        python: 3.8
  build:
    commands:
      - sam package --template-file template.yml --s3-bucket bucketname --output-template-file packaged-template.yml
artifacts:
  files:
    - packaged-template.yml
```

### Step 2: Create and configure your pipeline

configure your pipeline
https://console.aws.amazon.com/codepipeline/

## ai_linebot
Image AI LINEBot on AWS CloudFormation and CI/CD pipeline


***AWS Used:*** <br>
AWS CodePipeline <br>
AWS Sam <br>
Amazon API Gateway <br>
AWS Lambda <br>
Amazon Rekognition <br>



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


## product like

product like
![S__97501187 (2)](https://user-images.githubusercontent.com/73207535/125492312-94557266-9be6-4404-bb2a-fac4f928353f.jpg)

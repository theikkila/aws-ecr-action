# AWS ECR Action
Converted to python from (https://github.com/kciter/aws-ecr-action) and added tag evaluation feature.

This Action allows you to create Docker images and push into a ECR repository.

## Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `access_key_id` | `string` | | Your AWS access key id |
| `secret_access_key` | `string` | | Your AWS secret access key |
| `account_id` | `string` | | Your AWS Account ID |
| `repo` | `string` | | Name of your ECR repository |
| `region` | `string` | | Your AWS region |
| `tags` | `string` | `latest` | Comma-separated string of ECR image tags (ex latest,1.0.0,) |
| `dockerfile` | `string` | `Dockerfile` | Name of Dockerfile to use |
| `extra_build_args` | `string` | `""` | Extra flags to pass to docker build (see docs.docker.com/engine/reference/commandline/build) |
| `path` | `string` | `.` | Path to Dockerfile, defaults to the working directory |

## Usage
```yaml
jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
    - uses: theikkila/aws-ecr-action@v1
      with:
        access_key_id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        secret_access_key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        account_id: ${{ secrets.AWS_ACCOUNT_ID }}
        repo: docker/repo
        region: ap-northeast-2
        tags: latest,%echo $GITHUB_SHA
        create_repo: true
```

## Reference
* https://github.com/CircleCI-Public/aws-ecr-orb
* https://github.com/elgohr/Publish-Docker-Github-Action

## License
The MIT License (MIT)

Copyright (c) 2020 Teemu Heikkilä

Original:
Copyright (c) 2015 Lee Sun-Hyoup
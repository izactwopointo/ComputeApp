from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_dynamodb as _dynamodb,
    aws_iam as _iam,
    aws_events as _events,
    aws_events_targets as _targets
    )

class S3listDynamodbStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDb
        s3_asset_table = _dynamodb.Table(self,
            "S3AssetTable",
            table_name = "S3AssetTable",
            partition_key=_dynamodb.Attribute(
                name="_id",
                type=_dynamodb.AttributeType.STRING),
            removal_policy = core.RemovalPolicy.DESTROY,
        )

        # Lambda Source code
        try:
            with open("serverless_app_stacks/lambda_source/s3_list.py", mode = "r") as file:
                lambda_code = file.read()
        except OSError:
            print("Unable to find the given file :(")

        # Lambda Function
        S3listDynamodbFunction = _lambda.Function(self,
            "List-S3-Dynamodb-Function",
            description = "This function will list all the S3 buckets into the DynamoDb",
            function_name = "FucntionToListS3Buckets",
            runtime = _lambda.Runtime.PYTHON_3_7,
            handler = "index.lambda_handler",
            code = _lambda.InlineCode(lambda_code),
            timeout = core.Duration.seconds(3),
            reserved_concurrent_executions = 1,
            environment = {
                "LOG_LEVEL" : "INFO"
            }
        )

        # Schedule Event
        Run_every_week = _events.Rule(self,
            "RunEveryWeek",
            schedule = _events.Schedule.cron(
                minute = "0",
                hour = "18",
                month = "*",
                week_day = "MON",
                year = "*"
                )
            )

        Run_every_week.add_target(_targets.LambdaFunction(S3listDynamodbFunction))

        # Add Permissions
        S3listDynamodbFunction.role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3ReadOnlyAccess"))

        s3_asset_table.grant_write_data(S3listDynamodbFunction)


from aws_cdk import (
    core,
    aws_s3 as _s3,
    aws_lambda as _lambda,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_logs as _logs
)

class CustomLambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # try:
        #     with open("serverless_app_stacks/lambda_source/process.py", mode="r") as file:
        #         lambda_code = file.read()
        # except OSError:
        #     print("Unable to read the Lambda Function :( ")
        asset_bkt = _s3.Bucket.from_bucket_attributes(self,
            "AssetBucket",
            bucket_name = "test-assets-bkt"
            )

        test_fn = _lambda.Function(self,
            "Test Function",
            description = "This is test function",
            function_name = "Test_Function",
            runtime = _lambda.Runtime.PYTHON_3_7,
            handler = "process.lambda_handler",
            # code = _lambda.InlineCode(
            #     lambda_code),
            code = _lambda.S3Code(
                bucket = asset_bkt,
                key = 'lambda_source/process.zip'),
            timeout = core.Duration.seconds(3),
            reserved_concurrent_executions = 1,
            environment = {
                'LOG_LEVEL': 'INFO'
            }
            )

        # Run Every day at 18.00 UTC
        six_pm_cron = _events.Rule(
            self,
            "SixPmRule",
            schedule = _events.Schedule.cron(
                    minute = "0",
                    hour = "18",
                    month = "*",
                    week_day = "MON-FRI",
                    year = "*"
                )
            )

        # Run every 1 minute
        run_every_1_minute = _events.Rule(
            self,
            "RunEvery1Minute",
            schedule = _events.Schedule.rate(core.Duration.minutes(1))
            )

        six_pm_cron.add_target(_targets.LambdaFunction(test_fn))
        run_every_1_minute.add_target(_targets.LambdaFunction(test_fn))

        test_log = _logs.LogGroup(self,
            "testLoggroup",
            log_group_name = f"/aws/lambda/{test_fn.function_name}",
            removal_policy = core.RemovalPolicy.DESTROY,
            retention = _logs.RetentionDays.ONE_DAY
            )




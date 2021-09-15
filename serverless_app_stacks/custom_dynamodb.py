from aws_cdk import (
    core,
    aws_dynamodb as _dynamodb
    )

class DynamoDbStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        Test_db = _dynamodb.Table(self,
            "TestDb",
            table_name = "TestDynamoDb",
            partition_key = _dynamodb.Attribute(
                name = "id",
                type = _dynamodb.AttributeType.STRING),
            removal_policy = core.RemovalPolicy.DESTROY,
            server_side_encryption=True
        )

from aws_cdk import core
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_secretsmanager as _secretsmanager

class CustomIamUserStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        user1_pass = _secretsmanager.Secret(
            self,
            "User1Pass",
            description = "Initial Password for User1",
            secret_name = "user1_pass"
            )

        user1 = _iam.User(self,
            "User1",
            user_name = "Avinash",
            password = user1_pass.secret_value)


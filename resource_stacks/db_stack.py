from aws_cdk import (
    core,
    aws_ec2 as _ec2,
    aws_rds as _rds
    )

class RDSDatabaseStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, vpc, asg_security_group, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        test_db = _rds.DatabaseInstance(self,
            "testRdsDb",
            # master_username = "chrisgrey",
            database_name = "test_db",
            engine = _rds.DatabaseInstanceEngine.MYSQL,
            vpc = vpc,
            port = 3306,
            allocated_storage = 30,
            multi_az = False,
            cloudwatch_logs_exports = ["audit", "error", "slowquery"],
            instance_type=_ec2.InstanceType.of(
                _ec2.InstanceClass.BURSTABLE2,
                _ec2.InstanceSize.MICRO
            ),
            removal_policy = core.RemovalPolicy.DESTROY,
            deletion_protection = False,
            delete_automated_backups = True,
            backup_retention = core.Duration.days(7)
            )

        for sg in asg_security_group:
            test_db.connections.allow_default_port_from(sg, "Allow EC2 ASG Access to RDS Mysql")

        Output = core.CfnOutput(self,
            "DatabaseConnectionCommand",
            value = f"mysql -h {test_db.db_instance_endpoint_address} -P 3306 -u admin -p",
            description = "Connect to the database using this command")

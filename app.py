#!/usr/bin/env python3
from aws_cdk import core

from resource_stacks.customvpc_stack import CustomVpcStack
from resource_stacks.iamuser_stack import CustomIamUserStack
from resource_stacks.db_stack import RDSDatabaseStack
from resource_stacks.customalb_stack import ALB_ASGStack

app = core.App()
env = core.Environment(region = "ap-southeast-2", account = "275239396717")

# Custom VPC Stack
Vpc_Stack = CustomVpcStack(app, "Custom-Vpc-Stack")

# Custom ALB and ASG Stack
Alb_Stack = ALB_ASGStack(app, "Custom-ALB-Stack",
    vpc = Vpc_Stack.vpc)

# Database Stack
Db_Stack = RDSDatabaseStack(app, "RDS-Database-Stack",
    vpc = Vpc_Stack.vpc,
    asg_security_group = Alb_Stack.web_server_asg.connections.security_groups,
    description = "Custom RDS DataBase")

app.synth()

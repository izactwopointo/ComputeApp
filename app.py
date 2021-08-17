#!/usr/bin/env python3
import os
from aws_cdk import core

# from resource_stacks.customvpc_stack import CustomVpcStack

from resource_stacks.customec2_stack import CustomEc2Stack

app = core.App()
env = core.Environment(region = "ap-southeast-2", account = "275239396717")

#Custom VPC Stack
# CustomVpcStack(app, "Custom-Vpc-Stack")

#Custom Ec2 Stackd
CustomEc2Stack(app, "Custom-Ec2-Stack", env = env)

app.synth()

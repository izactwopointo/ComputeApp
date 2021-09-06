from aws_cdk import (
    core,
    aws_ec2 as _ec2,
    aws_elasticloadbalancingv2 as _elbv2,
    aws_iam as _iam,
    aws_autoscaling as _autoscaling
    )

class ALB_ASGStack(core.Stack):

    def __init__(self, scope: core.Construct,construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #Reading User Data
        try:
            with open("bootstrap_scripts/db.sh", mode = "r") as file:
                user_data = file.read()
        except OSError:
            print("Unable to find the given file.")

        #Selecting Latest AMI ID
        linux_ami = _ec2.MachineImage.latest_amazon_linux(
                generation = _ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                edition = _ec2.AmazonLinuxEdition.STANDARD,
                storage = _ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
                virtualization = _ec2.AmazonLinuxVirt.HVM
            )

        #Creating Application load balancer
        alb = _elbv2.ApplicationLoadBalancer(self,
            "TestAlb",
            vpc = vpc,
            internet_facing = True,
            load_balancer_name = "WebServerAlb"
            )

        #Allow connection on port 80
        alb.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80),
            description = "Allow Internet Access on port 80")

        #Adding Listener
        listener = alb.add_listener("listenerId",
            port = 80,
            open = True)

        #Creating Webser ag role
        web_server_role = _iam.Role(self, "webServerRoleId",
                                    assumed_by=_iam.ServicePrincipal(
                                        'ec2.amazonaws.com'),
                                    managed_policies=[
                                        _iam.ManagedPolicy.from_aws_managed_policy_name(
                                            'AmazonSSMManagedInstanceCore'
                                        ),
                                        _iam.ManagedPolicy.from_aws_managed_policy_name(
                                            'AmazonS3ReadOnlyAccess'
                                        )
                                    ])

        #Creating Auto Scaling Parameter
        self.web_server_asg = _autoscaling.AutoScalingGroup(self,
            "WebserverAsgId",
            vpc = vpc,
            vpc_subnets = _ec2.SubnetSelection(
                    subnet_type = _ec2.SubnetType.PRIVATE
                ),
            instance_type = _ec2.InstanceType(instance_type_identifier="t2.micro"),
            machine_image = linux_ami,
            role=web_server_role,
            min_capacity = 2,
            max_capacity = 2,
            user_data =  _ec2.UserData.custom(user_data)
            )

        #Allow connection to asg on port 80
        self.web_server_asg.connections.allow_from(alb, _ec2.Port.tcp(80),
            description = "Allow ASG Security Group receive traffic from ALB")

        #Add target to the listener
        listener.add_targets("listenerId", port=80, targets = [self.web_server_asg])

        #Output of the ALB Domain
        OutputALB = core.CfnOutput(self,
            "ALBDomainName",
            value = f"http://{alb.load_balancer_dns_name}",
            description = "Web Server ALB Domain Name")

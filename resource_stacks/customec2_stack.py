from aws_cdk import (
    core,
    aws_ec2 as _ec2,
    aws_iam as _iam
    )

class CustomEc2Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = _ec2.Vpc.from_lookup(self,
                                    "importedVpc",
                                    is_default = True)

        with open("bootstrap_scripts/httpd.sh", mode = "r") as file:
            user_data = file.read()

        Amazon_linux_ami = _ec2.MachineImage.latest_amazon_linux(
                generation = _ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                edition = _ec2.AmazonLinuxEdition.STANDARD,
                storage = _ec2.AmazonLinuxStorage.EBS,
                virtualization = _ec2.AmazonLinuxVirt.HVM
            )

        server = _ec2.Instance(self,
                                "Webserver",
                                instance_type = _ec2.InstanceType(instance_type_identifier="t2.micro"),
                                instance_name = 'TestInstance',
                                # machine_image = _ec2.MachineImage.generic_linux(
                                #     {'ap-southeast-2': "ami-0aab712d6363da7f9"}),
                                machine_image = Amazon_linux_ami,
                                vpc = vpc,
                                vpc_subnets = _ec2.SubnetSelection(
                                    subnet_type = _ec2.SubnetType.PUBLIC),
                                key_name = 'ChrisGrey',
                                user_data =  _ec2.UserData.custom(user_data)
                                )

#Ubuntu Server 20.04 LTS - ami-0567f647e75c7bc05
#Amazon Linux 2 AMI - ami-0aab712d6363da7f9

        server.instance.add_property_override(
            "BlockDeviceMappings",[
                {
                    "DeviceName": "/dev/sdb",
                    "Ebs":{
                        "VolumeSize": "8",
                        "VolumeType": "io1",
                        "Iops": "400",
                        "DeleteOnTermination": "true"
                    }
                }
            ]
            )

        server.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80), description = "Allow web Traffic in 80"
            )

        server.role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMManagedInstanceCore")
            )

        server.role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3ReadOnlyAccess")
            )

        Output = core.CfnOutput(self,
                                "WebserverPublicIp",
                                description = "Webserver server IP address",
                                value = f"http://{server.instance_public_ip}")


from aws_cdk import (
    core,
    aws_ec2 as _ec2)

class CustomVpcStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc_configs = self.node.try_get_context('vpc_configs')
        # print(vpc_configs)

        CutomVpc = _ec2.Vpc(self,
             "customvpcId",
             cidr = vpc_configs['vpc_cidr'],
             max_azs = 2,
             nat_gateways = 1,
             subnet_configuration = [
                _ec2.SubnetConfiguration(
                    name = "PublicSubnet",
                    cidr_mask = vpc_configs['cidr_mask'],
                    subnet_type= _ec2.SubnetType.PUBLIC
                    ),
                _ec2.SubnetConfiguration(
                    name = "PrivateSubnet",
                    cidr_mask = vpc_configs['cidr_mask'],
                    subnet_type= _ec2.SubnetType.PRIVATE
                    ),
                _ec2.SubnetConfiguration(
                    name = "DBSubnet",
                    cidr_mask = vpc_configs['cidr_mask'],
                    subnet_type= _ec2.SubnetType.ISOLATED
                    )
             ]
            )

        Tag =  core.Tags.of(CutomVpc).add('Owner', 'Esakkimuthu')

        Output = core.CfnOutput(self,
            'CutomVpcId',
            value = CutomVpc.vpc_id,
            export_name = 'CutomVpc001')

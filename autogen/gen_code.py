# -*- coding: utf-8 -*-

# INSTRUCTIONS: Format with black
#
# E.g.
# python gen_code.py definition spot-fleet | black -
# diffuse <(python ./autogen/gen_code.py definition spot-fleet | black -) ./nixops_aws/resources/spot_fleet.py

import dataclasses
from resource import Resource
from mypy_boto3_ec2 import EC2Client, type_defs
from pprint import pprint
import sys
from typing import Optional
import gen_definition as definition
import gen_options as options
import gen_nix as nix


def gen_options(r: Resource):
    print(
        f"""
{options.gen_options_imports(r)}

{options.gen_options_types(r)}
""".strip()
    )


def gen_resource(r: Resource):
    print(
        f"""
{definition.gen_resource_imports(r)}


{definition.gen_resource_definition(r)}


{definition.gen_resource_state(r)}
""".strip()
    )


def gen_nix(r: Resource):
    print(
        f"""
{{ config, lib, uuid, name, ... }}:

with lib;

{nix.gen_nix_types(r)}
""".strip()
    )


def gen_example(r: Resource):
    print(
        """
""".strip()
    )


resources = {
    "spot-fleet": Resource(
        resource="spot fleet",
        factory_resource="spot fleet request",
        create_method=EC2Client.request_spot_fleet,
        describe_method=EC2Client.describe_spot_fleet_requests,
        modify_method=EC2Client.modify_spot_fleet_request,
        destroy_method=EC2Client.cancel_spot_fleet_requests,
        create_annotations=type_defs.SpotFleetRequestConfigDataTypeDef.__annotations__,
        create_typedef=type_defs.SpotFleetRequestConfigDataTypeDef,
        describe_typedef=type_defs.DescribeSpotFleetRequestsRequestRequestTypeDef,
        modify_typedef=type_defs.ModifySpotFleetRequestRequestRequestTypeDef,
        destroy_typedef=type_defs.CancelSpotFleetRequestsRequestRequestTypeDef,
        cross_references={
            (None, "iamFleetRole"): ("iamRole", "arn"),
            ("FleetLaunchTemplateSpecification", "launchTemplateId"): (
                "Ec2LaunchTemplate",
                "templateId",
            ),
            # ("EbsBlockDevice", "kmsKeyId"): (),
            # ("EbsBlockDevice", "outpostArn"): (),
            # ("EbsBlockDevice", "snapshotId"): (),
            # ("IamInstanceProfileSpecification", "arn"): (),
            ("InstanceNetworkInterfaceSpecification", "networkInterfaceId"): (
                "vpcNetworkInterface",
                "networkInterfaceId",
            ),
            ("InstanceNetworkInterfaceSpecification", "subnetId"): (
                "vpcSubnet",
                "subnetId",
            ),
            ("GroupIdentifier", "groupId"): ("ec2SecurityGroups", "groupId"),
            # ("SpotFleetLaunchSpecification", "imageId"): (),
            # ("SpotFleetLaunchSpecification", "kernelId"): (),
            # ("SpotFleetLaunchSpecification", "ramdiskId"): (),
            ("SpotFleetLaunchSpecification", "subnetId"): ("vpcSubnet", "subnetId"),
            ("FleetLaunchTemplateSpecification", "launchTemplateId"): (
                "Ec2LaunchTemplate",
                "templateId",
            ),
            # ("FleetLaunchTemplateSpecification", "launchTemplateName"): (
            #     "Ec2LaunchTemplate",
            #     "arn",
            # ),
            ("LaunchTemplateOverrides", "subnetId"): ("vpcSubnet", "subnetId"),
            # ("TargetGroup", "arn"): (),
        },
    ),
    "launch-template": Resource(
        resource="launch template",
        create_method=EC2Client.create_launch_template,
        describe_method=EC2Client.describe_launch_templates,
        modify_method=EC2Client.modify_launch_template,
        destroy_method=EC2Client.delete_launch_template,
        create_annotations=type_defs.CreateLaunchTemplateRequestRequestTypeDef.__annotations__,
        create_typedef=type_defs.CreateLaunchTemplateRequestRequestTypeDef,
        describe_typedef=type_defs.DescribeLaunchTemplatesRequestRequestTypeDef,
        modify_typedef=type_defs.ModifyLaunchTemplateRequestRequestTypeDef,
        destroy_typedef=type_defs.DeleteLaunchTemplateRequestRequestTypeDef,
    ),
    "fleet": Resource(
        resource="fleet",
        managed_resource="instance",
        create_method=EC2Client.create_fleet,
        describe_method=EC2Client.describe_fleets,
        modify_method=EC2Client.modify_fleet,
    ),
    # "vpn-connection-route": Resource(
    #     resource="vpn route",
    #     create_method=EC2Client.create_vpn_connection_route,
    #     describe_method=EC2Client.describe_vpn_connections,
    #     # modify_method=EC2Client.modify_vpn_connection_route,
    #     # delete_method=EC2Client.delete_vpn_connection_route,
    # ),
    "internet-gateway": Resource(
        resource="internet gateway",
        create_method=EC2Client.create_internet_gateway,
        describe_method=EC2Client.describe_internet_gateways,
        # delete_method=EC2Client.delete_internet_gateway,
        # methods = [
        #     EC2Client.attach_internet_gateway
        #     EC2Client.deattach_internet_gateway
        # ]
    ),
}


help_usage = """
USAGE:

\tpython gen_code.py show
\tpython gen_code.py [target] [resource]

----
Resources:
"""


def pprint_resource(r, shorthand):
    pprint(
        {
            k: (
                v
                if k
                not in [
                    "create_annotations",
                    "modify_annotations",
                    "describe_annotations",
                ]
                else "[...]"
            )
            for k, v in dataclasses.asdict(r).items()
        }
    )


def main():
    argv_target = sys.argv[1:2]

    if sys.argv[1:] == []:
        print(help_usage)
        for r in resources.values():
            if r.factory_resource is not None:
                print("\t•", r.resource, "(", r.factory_resource, ")")
            else:
                print("\t•", r.resource)
    elif sys.argv[1:] == ["show", "all"]:
        for r in resources.values():
            pprint_resource(r)
    else:
        argv_resource = sys.argv[2:3]
        resource: Optional[Resource]
        if argv_resource == []:
            resource = list(resources.values())[-1]
        else:
            resource = resources.get(argv_resource[0])
            if resource is None:
                raise Exception("No such resource:", argv_resource[0])
        if argv_target == ["show"]:
            pprint(dataclasses.asdict(resource))
        elif argv_target == ["options"]:
            gen_options(resource)
        elif argv_target == ["definition"]:
            gen_resource(resource)
        elif argv_target == ["nix"]:
            gen_nix(resource)
        elif argv_target == ["example"]:
            gen_example(resource)
        else:
            raise Exception("Unknown arguments", sys.argv[1:])


main()

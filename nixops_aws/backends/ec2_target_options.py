from nixops.backends import MachineOptions
from nixops.resources import ResourceOptions
# from typing import Union
from typing import Optional


# class Ec2TargetInstanceOptions(ResourceOptions):
#     spotInstanceId: str


# class Ec2TargetSpotRequestOptions(ResourceOptions):
#     spotRequestId: str


# class Ec2TargetSpotFleetRequestOptions(ResourceOptions):
#     spotFleetRequestId: str


class Ec2TargetTargetOptions(ResourceOptions):
    spotInstanceId: Optional[str]
    spotRequestId: Optional[str]
    spotFleetRequestId: Optional[str]


class Ec2TargetOptions(ResourceOptions):
    # target: Union[
    #     Ec2TargetInstanceOptions,
    #     Ec2TargetSpotRequestOptions,
    #     Ec2TargetSpotFleetRequestOptions,
    # ]
    # target: str
    target: Ec2TargetTargetOptions


class Ec2TargetMachineOptions(MachineOptions):
    # ec2: Union[Ec2Options, Ec2TargetOptions]
    ec2target: Ec2TargetOptions

from nixops.backends import MachineOptions
from nixops.resources import ResourceOptions
# from typing import Union
from typing import Optional
from ...resources.util.references import ResourceReferenceOption # TODO move util module up


# class Ec2TargetInstanceOptions(ResourceOptions):
#     spotInstanceId: str


# class Ec2TargetSpotRequestOptions(ResourceOptions):
#     spotRequestId: str


# class Ec2TargetSpotFleetRequestOptions(ResourceOptions):
#     spotFleetRequestId: str


class Ec2TargetTargetOptions(ResourceOptions):
    spotInstanceId: Optional[ResourceReferenceOption[str, str]]
    spotRequestId: Optional[ResourceReferenceOption[str, str]]
    spotFleetRequestId: Optional[ResourceReferenceOption[str, str]]


class Ec2TargetOptions(ResourceOptions):
    # target: Union[
    #     Ec2TargetInstanceOptions,
    #     Ec2TargetSpotRequestOptions,
    #     Ec2TargetSpotFleetRequestOptions,
    # ]
    # target: str
    target: Ec2TargetTargetOptions
    privateKey: str


class Ec2TargetMachineOptions(MachineOptions):
    # ec2: Union[Ec2Options, Ec2TargetOptions]
    ec2target: Ec2TargetOptions

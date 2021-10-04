from typing import Union
from typing import Optional
from typing import List
from typing import Mapping
from typing_extensions import Literal
from nixops.resources import ResourceOptions


class Ec2LaunchTemplateOptions(ResourceOptions):
    name: str
    templateId: str
    versionDescription: str
    ebsOptimized: bool
    userData: Optional[str]
    disableApiTermination: bool
    instanceInitiatedShutdownBehavior: Union[
        Literal["stop"],
        Literal["terminate"],
    ]
    networkInterfaceId: str
    privateIpAddresses: Optional[List[str]]
    secondaryPrivateIpAddressCount: Optional[int]
    instanceTags: Mapping[str, str]
    volumeTags: Mapping[str, str]

    # Common EC2 auth options
    accessKeyId: str
    region: str

    # Common EC2 options
    tags: Mapping[str, str]

    # Common EC2 instance options
    zone: str
    monitoring: bool
    tenancy: Union[
        Literal["default"],
        Literal["dedicated"],
        Literal["host"],
    ]
    ebsInitialRootDiskSize: int
    ami: str
    instanceType: str
    instanceProfile: str
    keyPair: str
    securityGroupIds: str
    subnetId: str
    associatePublicIpAddress: bool
    placementGroup: str
    spotInstancePrice: int
    spotInstanceRequestType: Union[
        Literal["one-time"],
        Literal["persistent"],
    ]
    spotInstanceInterruptionBehavior: Union[
        Literal["terminate"],
        Literal["stop"],
        Literal["hibernate"],
    ]
    spotInstanceTimeout: int
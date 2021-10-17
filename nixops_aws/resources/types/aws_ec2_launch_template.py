from typing import Union
from typing import Optional
from typing import Sequence
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
        Literal["stop"], Literal["terminate"],
    ]
    networkInterfaceId: str
    privateIpAddresses: Optional[Sequence[str]]
    secondaryPrivateIpAddressCount: Optional[int]
    instanceTags: Mapping[str, str]
    volumeTags: Mapping[str, str]

    # Common EC2 auth options
    accessKeyId: str
    region: str

    # Common EC2 options
    tags: Mapping[str, str]

    # Common EC2 instance options
    monitoring: bool
    ami: str
    associatePublicIpAddress: bool
    # blockDeviceMapping: Mapping[str, BlockdevicemappingOptions]
    # ebsBoot: bool
    ebsInitialRootDiskSize: int
    # ebsOptimized: bool
    # fileSystems: Optional[Mapping[str, FilesystemsOptions]]
    instanceProfile: str
    instanceType: str
    keyPair: str
    # physicalProperties: Mapping[str, Union[int, str, bool]]
    placementGroup: str
    # privateKey: str
    securityGroupIds: Sequence[str]
    # securityGroups: Sequence[str]
    # sourceDestCheck: bool
    spotInstanceInterruptionBehavior: Union[
        Literal["terminate"], Literal["stop"], Literal["hibernate"],
    ]
    spotInstancePrice: int
    spotInstanceRequestType: Union[
        Literal["one-time"], Literal["persistent"],
    ]
    spotInstanceTimeout: int
    subnetId: str
    tenancy: Union[
        Literal["default"], Literal["dedicated"], Literal["host"],
    ]
    # usePrivateIpAddress: bool
    zone: str

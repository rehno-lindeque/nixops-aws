from typing import Mapping, Sequence, Optional, Union
from typing_extensions import Literal
from nixops.resources import ResourceOptions
from mypy_boto3_ec2 import type_defs


class FleetLaunchTemplateSpecificationOptions(ResourceOptions):
    # launchTemplateId: str # Optional
    launchTemplateName: str  # Optional #  {"max":128,"min":3,"pattern":"[a-zA-Z0-9\\(\\)\\.\\-/_]+"}
    version: str  # Optional


# class PlacementOptions:
#     AvailabilityZone: Optional[String]
#     Affinity: Optional[String]
#     GroupName: Optional[PlacementGroupName]
#     PartitionNumber: Optional[Integer]
#     HostId: Optional[String]
#     Tenancy: Optional[Tenancy]
#     SpreadDomain: Optional[String]
#     HostResourceGroupArn: Optional[String]


class AwsConfig(type_defs.RequestSpotFleetRequestRequestTypeDef, total=False):
    pass


class SpotFleetRequestConfigDataTypeDef(
    type_defs.SpotFleetRequestConfigDataTypeDef, total=False
):
    pass


class SpotMaintenanceStrategiesTypeDef(
    type_defs.SpotMaintenanceStrategiesTypeDef, total=False
):
    pass


class SpotFleetLaunchSpecificationTypeDef(
    type_defs.SpotFleetLaunchSpecificationTypeDef, total=False
):
    pass


class LaunchTemplateConfigTypeDef(type_defs.LaunchTemplateConfigTypeDef, total=False):
    pass


class LoadBalancersConfigTypeDef(type_defs.LoadBalancersConfigTypeDef, total=False):
    pass


class TagSpecificationTypeDef(type_defs.TagSpecificationTypeDef, total=False):
    pass


class LaunchTemplateOverridesOptions(ResourceOptions):
    instanceType: Optional[str]
    spotPrice: Optional[str]
    subnetId: Optional[str]
    availabilityZone: Optional[str]
    weightedCapacity: Optional[float]
    priority: Optional[float]


class LaunchTemplateConfigOptions(ResourceOptions):
    launchTemplateSpecification: FleetLaunchTemplateSpecificationOptions  # Optional
    overrides: Sequence[LaunchTemplateOverridesOptions]


class SpotFleetRequestOptions(ResourceOptions):
    spotFleetRequestId: str
    iamFleetRole: str
    type: Union[
        Literal["request"],
        Literal["maintain"]
        # Literal["instant"] # instant is listed but is not used by Spot Fleet.
    ]
    launchTemplateConfigs: Sequence[LaunchTemplateConfigOptions]
    spotPrice: Optional[str]
    spotMaxTotalPrice: Optional[str]

    # Common EC2 auth options
    accessKeyId: str
    region: str

    # Common EC2 options
    tags: Mapping[str, str]

    # Extra options
    # awsConfig: type_defs.RequestSpotFleetRequestRequestTypeDef
    awsConfig: AwsConfig

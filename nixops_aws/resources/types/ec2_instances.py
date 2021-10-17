from nixops.resources import ResourceOptions

from mypy_boto3_ec2 import type_defs
from typing import Any, Mapping


class BlockDeviceMappingTypeDef(type_defs.BlockDeviceMappingTypeDef, total=False):
    pass


class InstanceIpv6AddressTypeDef(type_defs.InstanceIpv6AddressTypeDef, total=False):
    pass


class RunInstancesMonitoringEnabledTypeDef(
    type_defs.RunInstancesMonitoringEnabledTypeDef, total=False
):
    pass


class PlacementTypeDef(type_defs.PlacementTypeDef, total=False):
    pass


class IamInstanceProfileSpecificationTypeDef(
    type_defs.IamInstanceProfileSpecificationTypeDef, total=False
):
    pass


class InstanceNetworkInterfaceSpecificationTypeDef(
    type_defs.InstanceNetworkInterfaceSpecificationTypeDef, total=False
):
    pass


class ElasticGpuSpecificationTypeDef(
    type_defs.ElasticGpuSpecificationTypeDef, total=False
):
    pass


class ElasticInferenceAcceleratorTypeDef(
    type_defs.ElasticInferenceAcceleratorTypeDef, total=False
):
    pass


class TagSpecificationTypeDef(type_defs.TagSpecificationTypeDef, total=False):
    pass


class LaunchTemplateSpecificationTypeDef(
    type_defs.LaunchTemplateSpecificationTypeDef, total=False
):
    pass


class InstanceMarketOptionsRequestTypeDef(
    type_defs.InstanceMarketOptionsRequestTypeDef, total=False
):
    pass


class CreditSpecificationRequestTypeDef(
    type_defs.CreditSpecificationRequestTypeDef, total=False
):
    pass


class CpuOptionsRequestTypeDef(type_defs.CpuOptionsRequestTypeDef, total=False):
    pass


class CapacityReservationSpecificationTypeDef(
    type_defs.CapacityReservationSpecificationTypeDef, total=False
):
    pass


class HibernationOptionsRequestTypeDef(
    type_defs.HibernationOptionsRequestTypeDef, total=False
):
    pass


class LicenseConfigurationRequestTypeDef(
    type_defs.LicenseConfigurationRequestTypeDef, total=False
):
    pass


class InstanceMetadataOptionsRequestTypeDef(
    type_defs.InstanceMetadataOptionsRequestTypeDef, total=False
):
    pass


class EnclaveOptionsRequestTypeDef(type_defs.EnclaveOptionsRequestTypeDef, total=False):
    pass


class RunInstancesRequestRequestTypeDef(
    type_defs.RunInstancesRequestRequestTypeDef, total=False
):
    pass


class Ec2InstancesOptions(ResourceOptions):
    accessKeyId: str
    # name: str
    region: str

    # Extra options
    # awsConfig: type_defs.RunInstancesRequestRequestTypeDef
    awsConfig: Mapping[str, Any]

# class type_defs.RunInstancesRequestRequestTypeDef

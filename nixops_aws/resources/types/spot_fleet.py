from copy import deepcopy

# from datetime import datetime
import inspect
from itertools import repeat
from nixops.resources import ResourceOptions
from typing import (
    # NoneType,
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Set,
    TYPE_CHECKING,
    Type,
    TypeVar,
    Union,
    overload,
)
from typing_extensions import Concatenate, ParamSpec
from ..util.references import ResourceReferenceOption

if TYPE_CHECKING:
    from mypy_boto3_ec2.type_defs import (
        BlockDeviceMappingTypeDef,
        ClassicLoadBalancerTypeDef,
        ClassicLoadBalancersConfigTypeDef,
        EbsBlockDeviceTypeDef,
        FleetLaunchTemplateSpecificationTypeDef,
        GroupIdentifierTypeDef,
        IamInstanceProfileSpecificationTypeDef,
        InstanceIpv6AddressTypeDef,
        InstanceNetworkInterfaceSpecificationTypeDef,
        Ipv4PrefixSpecificationRequestTypeDef,
        Ipv6PrefixSpecificationRequestTypeDef,
        LaunchTemplateConfigTypeDef,
        LaunchTemplateOverridesTypeDef,
        LoadBalancersConfigTypeDef,
        PrivateIpAddressSpecificationTypeDef,
        SpotCapacityRebalanceTypeDef,
        SpotFleetLaunchSpecificationTypeDef,
        SpotFleetMonitoringTypeDef,
        SpotFleetTagSpecificationTypeDef,
        SpotMaintenanceStrategiesTypeDef,
        SpotPlacementTypeDef,
        TagSpecificationTypeDef,
        TagTypeDef,
        TargetGroupTypeDef,
        TargetGroupsConfigTypeDef,
        SpotFleetRequestConfigDataTypeDef,
        ModifySpotFleetRequestRequestRequestTypeDef,
    )
else:
    BlockDeviceMappingTypeDef = dict
    ClassicLoadBalancerTypeDef = dict
    ClassicLoadBalancersConfigTypeDef = dict
    EbsBlockDeviceTypeDef = dict
    FleetLaunchTemplateSpecificationTypeDef = dict
    GroupIdentifierTypeDef = dict
    IamInstanceProfileSpecificationTypeDef = dict
    InstanceIpv6AddressTypeDef = dict
    InstanceNetworkInterfaceSpecificationTypeDef = dict
    Ipv4PrefixSpecificationRequestTypeDef = dict
    Ipv6PrefixSpecificationRequestTypeDef = dict
    LaunchTemplateConfigTypeDef = dict
    LaunchTemplateOverridesTypeDef = dict
    LoadBalancersConfigTypeDef = dict
    PrivateIpAddressSpecificationTypeDef = dict
    SpotCapacityRebalanceTypeDef = dict
    SpotFleetLaunchSpecificationTypeDef = dict
    SpotFleetMonitoringTypeDef = dict
    SpotFleetTagSpecificationTypeDef = dict
    SpotMaintenanceStrategiesTypeDef = dict
    SpotPlacementTypeDef = dict
    TagSpecificationTypeDef = dict
    TagTypeDef = dict
    TargetGroupTypeDef = dict
    TargetGroupsConfigTypeDef = dict
    SpotFleetRequestConfigDataTypeDef = dict
    ModifySpotFleetRequestRequestRequestTypeDef = dict


# KeyType = TypeVar("KeyType")
# Kwargs = ParamSpec("Kwargs")
# ReturnType = TypeVar("ReturnType")

# MappableResourceOptions = Union[
#     ResourceOptions,
#     Sequence[ResourceOptions],
#     Mapping[Any, ResourceOptions],
#     None,
# ]


# @overload
# def map_resource_options(
#     f: Callable[..., ReturnType],  # TODO: Concatenate[ResourceOptions, Kwargs]
#     options: ResourceOptions,
#     **kwargs,  # TODO: Kwargs
# ) -> ReturnType:
#     ...


# @overload
# def map_resource_options(
#     f: Callable[..., ReturnType],  # TODO: Concatenate[ResourceOptions, Kwargs]
#     options: Sequence[ResourceOptions],
#     **kwargs,  # TODO: Kwargs
# ) -> List[ReturnType]:
#     ...


# @overload
# def map_resource_options(
#     f: Callable[..., ReturnType],  # TODO: Concatenate[ResourceOptions, Kwargs]
#     options: Mapping[KeyType, ResourceOptions],
#     **kwargs,  # TODO: Kwargs
# ) -> Dict[KeyType, ReturnType]:
#     ...


# @overload
# def map_resource_options(
#     f: Callable[..., ReturnType],  # TODO: Concatenate[ResourceOptions, Kwargs]
#     options: None,
#     **kwargs,  # TODO: Kwargs
# ) -> None:
#     ...


# def map_resource_options(
#     f: Callable[..., ReturnType],  # TODO: Concatenate[ResourceOptions, Kwargs]
#     options: MappableResourceOptions,
#     **kwargs,  # TODO: Kwargs
# ) -> Union[ReturnType, List[ReturnType], Mapping[Any, ReturnType], None]:
#     if options is None:
#         return None
#     elif isinstance(options, ResourceOptions):
#         return f(options, **kwargs)
#     elif isinstance(options, Sequence):
#         return [map_resource_options(f, o, **kwargs) for o in options]
#     elif isinstance(options, Mapping):
#         return {k: map_resource_options(f, o, **kwargs) for k, o in options.items()}
#     else:
#         assert False  # Implementation bug: case analysis should match all types in MappableResourceOptions


# class AwsResourceOptions(Resource):
#     def extract_boto_type_def(
#         self: AwsResourceOptions, dest_type: Type, overrides: dict = {}
#     ):
#         def uncapitalize(s: str) -> str:
#             return s[0].lower() + s[1:]

#         # def extract(source: ResourceOptions, dest_type: Type, overrides):
#         #     source_annotations = type(source).__annotations__
#         #     return d

#         # map_resource_options((lambda source: extract(source, dest_type, overrides)), self)

#         d = overrides.copy()
#         for dest_name, dest_type in t.__annotations__.items():
#             source_name = uncapitalize(dest_name)
#             source_type = source_annotations.get(source_name)
#             source_type_origin = typing.get_args(source_type)
#             source_type_args = typing.get_args(source_type)
#             if source_type is None:
#                 continue
#             source_value = getattr(self, source_name)
#             if inspect.isclass(source_type) and issubclass(
#                 source_type, AwsResourceOptions
#             ):
#                 d[dest_name] = source_value.convert_to_aws(dest_type)
#             elif source_type_origin in {Union, Sequence, List}:
#                 if any(
#                     [
#                         inspect.isclass(t) and issubclass(t, AwsResourceOptions)
#                         for t in typing.type_args(source_type)
#                     ]
#                 ):
#                     d[dest_name] = source_value
#             else:
#                 if dest_name not in overrides:
#                     d[dest_name] = source_value
#                 # if isinstance(, AwsResourceOptions):
#             # else:
#             #     d[dest_name] = source._dict[src_name]


class EbsBlockDeviceOptions(ResourceOptions):
    deleteOnTermination: Optional[bool]
    encrypted: Optional[bool]
    iops: Optional[int]
    kmsKeyId: Optional[str]
    outpostArn: Optional[str]
    snapshotId: Optional[str]
    throughput: Optional[int]
    volumeSize: Optional[int]
    volumeType: Optional[Literal["gp2", "gp3", "io1", "io2", "sc1", "st1", "standard"]]


def unpack_ebs_block_device(
    config: EbsBlockDeviceOptions,
) -> EbsBlockDeviceTypeDef:
    r = EbsBlockDeviceTypeDef()
    DeleteOnTermination = config.deleteOnTermination
    if DeleteOnTermination is not None:
        r["DeleteOnTermination"] = DeleteOnTermination
    Encrypted = config.encrypted
    if Encrypted is not None:
        r["Encrypted"] = Encrypted
    Iops = config.iops
    if Iops is not None:
        r["Iops"] = Iops
    KmsKeyId = config.kmsKeyId
    if KmsKeyId is not None:
        r["KmsKeyId"] = KmsKeyId
    OutpostArn = config.outpostArn
    if OutpostArn is not None:
        r["OutpostArn"] = OutpostArn
    SnapshotId = config.snapshotId
    if SnapshotId is not None:
        r["SnapshotId"] = SnapshotId
    Throughput = config.throughput
    if Throughput is not None:
        r["Throughput"] = Throughput
    VolumeSize = config.volumeSize
    if VolumeSize is not None:
        r["VolumeSize"] = VolumeSize
    VolumeType = config.volumeType
    if VolumeType is not None:
        r["VolumeType"] = VolumeType
    return r


class BlockDeviceMappingOptions(ResourceOptions):
    deviceName: Optional[str]
    ebs: Optional[EbsBlockDeviceOptions]
    noDevice: Optional[str]
    virtualName: Optional[str]


def unpack_block_device_mapping(
    config: BlockDeviceMappingOptions,
) -> BlockDeviceMappingTypeDef:
    r = BlockDeviceMappingTypeDef()
    DeviceName = config.deviceName
    if DeviceName is not None:
        r["DeviceName"] = DeviceName
    Ebs = unpack_ebs_block_device(config.ebs)
    if Ebs is not None:
        r["Ebs"] = Ebs
    NoDevice = config.noDevice
    if NoDevice is not None:
        r["NoDevice"] = NoDevice
    VirtualName = config.virtualName
    if VirtualName is not None:
        r["VirtualName"] = VirtualName
    return r


class IamInstanceProfileSpecificationOptions(ResourceOptions):
    arn: Optional[str]
    name: Optional[str]


def unpack_iam_instance_profile_specification(
    config: IamInstanceProfileSpecificationOptions,
) -> IamInstanceProfileSpecificationTypeDef:
    r = IamInstanceProfileSpecificationTypeDef()
    Arn = config.arn
    if Arn is not None:
        r["Arn"] = Arn
    Name = config.name
    if Name is not None:
        r["Name"] = Name
    return r


class SpotFleetMonitoringOptions(ResourceOptions):
    enabled: Optional[bool]


def unpack_spot_fleet_monitoring(
    config: SpotFleetMonitoringOptions,
) -> SpotFleetMonitoringTypeDef:
    r = SpotFleetMonitoringTypeDef()
    Enabled = config.enabled
    if Enabled is not None:
        r["Enabled"] = Enabled
    return r


class Ipv4PrefixSpecificationOptions(ResourceOptions):
    ipv4Prefix: Optional[str]


def unpack_ipv4_prefix_specification(
    config: Ipv4PrefixSpecificationOptions,
) -> Ipv4PrefixSpecificationRequestTypeDef:
    r = Ipv4PrefixSpecificationRequestTypeDef()
    Ipv4Prefix = config.ipv4Prefix
    if Ipv4Prefix is not None:
        r["Ipv4Prefix"] = Ipv4Prefix
    return r


class InstanceIpv6AddressOptions(ResourceOptions):
    ipv6Address: Optional[str]


def unpack_instance_ipv6_address(
    config: InstanceIpv6AddressOptions,
) -> InstanceIpv6AddressTypeDef:
    r = InstanceIpv6AddressTypeDef()
    Ipv6Address = config.ipv6Address
    if Ipv6Address is not None:
        r["Ipv6Address"] = Ipv6Address
    return r


class Ipv6PrefixSpecificationOptions(ResourceOptions):
    ipv6Prefix: Optional[str]


def unpack_ipv6_prefix_specification(
    config: Ipv6PrefixSpecificationOptions,
) -> Ipv6PrefixSpecificationRequestTypeDef:
    r = Ipv6PrefixSpecificationRequestTypeDef()
    Ipv6Prefix = config.ipv6Prefix
    if Ipv6Prefix is not None:
        r["Ipv6Prefix"] = Ipv6Prefix
    return r


class PrivateIpAddressSpecificationOptions(ResourceOptions):
    primary: Optional[bool]
    privateIpAddress: Optional[str]


def unpack_private_ip_address_specification(
    config: PrivateIpAddressSpecificationOptions,
) -> PrivateIpAddressSpecificationTypeDef:
    r = PrivateIpAddressSpecificationTypeDef()
    Primary = config.primary
    if Primary is not None:
        r["Primary"] = Primary
    PrivateIpAddress = config.privateIpAddress
    if PrivateIpAddress is not None:
        r["PrivateIpAddress"] = PrivateIpAddress
    return r


class InstanceNetworkInterfaceSpecificationOptions(ResourceOptions):
    associateCarrierIpAddress: Optional[bool]
    associatePublicIpAddress: Optional[bool]
    deleteOnTermination: Optional[bool]
    description: Optional[str]
    deviceIndex: Optional[int]
    groups: Optional[Sequence[str]]
    interfaceType: Optional[str]
    ipv4PrefixCount: Optional[int]
    ipv4Prefixes: Sequence[Ipv4PrefixSpecificationOptions]
    ipv6AddressCount: Optional[int]
    ipv6Addresses: Sequence[InstanceIpv6AddressOptions]
    ipv6PrefixCount: Optional[int]
    ipv6Prefixes: Sequence[Ipv6PrefixSpecificationOptions]
    networkCardIndex: Optional[int]
    networkInterfaceId: Optional[ResourceReferenceOption[str, str]]
    privateIpAddress: Optional[str]
    privateIpAddresses: Sequence[PrivateIpAddressSpecificationOptions]
    secondaryPrivateIpAddressCount: Optional[int]
    subnetId: Optional[ResourceReferenceOption[str, str]]


def unpack_instance_network_interface_specification(
    config: InstanceNetworkInterfaceSpecificationOptions,
) -> InstanceNetworkInterfaceSpecificationTypeDef:
    r = InstanceNetworkInterfaceSpecificationTypeDef()
    AssociateCarrierIpAddress = config.associateCarrierIpAddress
    if AssociateCarrierIpAddress is not None:
        r["AssociateCarrierIpAddress"] = AssociateCarrierIpAddress
    AssociatePublicIpAddress = config.associatePublicIpAddress
    if AssociatePublicIpAddress is not None:
        r["AssociatePublicIpAddress"] = AssociatePublicIpAddress
    DeleteOnTermination = config.deleteOnTermination
    if DeleteOnTermination is not None:
        r["DeleteOnTermination"] = DeleteOnTermination
    Description = config.description
    if Description is not None:
        r["Description"] = Description
    DeviceIndex = config.deviceIndex
    if DeviceIndex is not None:
        r["DeviceIndex"] = DeviceIndex
    Groups = list(config.groups) if config.groups else None
    if Groups is not None:
        r["Groups"] = Groups
    InterfaceType = config.interfaceType
    if InterfaceType is not None:
        r["InterfaceType"] = InterfaceType
    Ipv4PrefixCount = config.ipv4PrefixCount
    if Ipv4PrefixCount is not None:
        r["Ipv4PrefixCount"] = Ipv4PrefixCount
    Ipv4Prefixes = (
        [unpack_ipv4_prefix_specification(c) for c in config.ipv4Prefixes]
        if config.ipv4Prefixes
        else None
    )
    if Ipv4Prefixes is not None:
        r["Ipv4Prefixes"] = Ipv4Prefixes
    Ipv6AddressCount = config.ipv6AddressCount
    if Ipv6AddressCount is not None:
        r["Ipv6AddressCount"] = Ipv6AddressCount
    Ipv6Addresses = (
        [unpack_instance_ipv6_address(c) for c in config.ipv6Addresses]
        if config.ipv6Addresses
        else None
    )
    if Ipv6Addresses is not None:
        r["Ipv6Addresses"] = Ipv6Addresses
    Ipv6PrefixCount = config.ipv6PrefixCount
    if Ipv6PrefixCount is not None:
        r["Ipv6PrefixCount"] = Ipv6PrefixCount
    Ipv6Prefixes = (
        [unpack_ipv6_prefix_specification(c) for c in config.ipv6Prefixes]
        if config.ipv6Prefixes
        else None
    )
    if Ipv6Prefixes is not None:
        r["Ipv6Prefixes"] = Ipv6Prefixes
    NetworkCardIndex = config.networkCardIndex
    if NetworkCardIndex is not None:
        r["NetworkCardIndex"] = NetworkCardIndex
    NetworkInterfaceId = (
        config.networkInterfaceId.value if config.networkInterfaceId else None
    )
    if NetworkInterfaceId is not None:
        r["NetworkInterfaceId"] = NetworkInterfaceId
    PrivateIpAddress = config.privateIpAddress
    if PrivateIpAddress is not None:
        r["PrivateIpAddress"] = PrivateIpAddress
    PrivateIpAddresses = (
        [unpack_private_ip_address_specification(c) for c in config.privateIpAddresses]
        if config.privateIpAddresses
        else None
    )
    if PrivateIpAddresses is not None:
        r["PrivateIpAddresses"] = PrivateIpAddresses
    SecondaryPrivateIpAddressCount = config.secondaryPrivateIpAddressCount
    if SecondaryPrivateIpAddressCount is not None:
        r["SecondaryPrivateIpAddressCount"] = SecondaryPrivateIpAddressCount
    SubnetId = config.subnetId.value if config.subnetId else None
    if SubnetId is not None:
        r["SubnetId"] = SubnetId
    return r


class SpotPlacementOptions(ResourceOptions):
    availabilityZone: Optional[str]
    groupName: Optional[str]
    tenancy: Optional[Literal["dedicated", "default", "host"]]


def unpack_spot_placement(
    config: SpotPlacementOptions,
) -> SpotPlacementTypeDef:
    r = SpotPlacementTypeDef()
    AvailabilityZone = config.availabilityZone
    if AvailabilityZone is not None:
        r["AvailabilityZone"] = AvailabilityZone
    GroupName = config.groupName
    if GroupName is not None:
        r["GroupName"] = GroupName
    Tenancy = config.tenancy
    if Tenancy is not None:
        r["Tenancy"] = Tenancy
    return r


class GroupIdentifierOptions(ResourceOptions):
    groupId: Optional[ResourceReferenceOption[str, str]]
    groupName: Optional[str]


def unpack_group_identifier(
    config: GroupIdentifierOptions,
) -> GroupIdentifierTypeDef:
    r = GroupIdentifierTypeDef()
    GroupId = config.groupId.value if config.groupId else None
    if GroupId is not None:
        r["GroupId"] = GroupId
    GroupName = config.groupName
    if GroupName is not None:
        r["GroupName"] = GroupName
    return r


class SpotFleetLaunchSpecificationOptions(ResourceOptions):
    addressingType: Optional[str]
    blockDeviceMappings: Sequence[BlockDeviceMappingOptions]
    ebsOptimized: Optional[bool]
    iamInstanceProfile: Optional[IamInstanceProfileSpecificationOptions]
    imageId: Optional[str]
    instanceType: Optional[str]
    kernelId: Optional[str]
    keyName: Optional[str]
    monitoring: Optional[SpotFleetMonitoringOptions]
    networkInterfaces: Sequence[InstanceNetworkInterfaceSpecificationOptions]
    placement: Optional[SpotPlacementOptions]
    ramdiskId: Optional[str]
    securityGroups: Sequence[GroupIdentifierOptions]
    spotPrice: Optional[str]
    subnetId: Optional[ResourceReferenceOption[str, str]]
    # tagSpecifications: Sequence[SpotFleetTagSpecificationOptions]
    userData: Optional[str]
    weightedCapacity: Optional[float]


def unpack_spot_fleet_launch_specification(
    config: SpotFleetLaunchSpecificationOptions,
) -> SpotFleetLaunchSpecificationTypeDef:
    r = SpotFleetLaunchSpecificationTypeDef()
    AddressingType = config.addressingType
    if AddressingType is not None:
        r["AddressingType"] = AddressingType
    BlockDeviceMappings = (
        [unpack_block_device_mapping(c) for c in config.blockDeviceMappings]
        if config.blockDeviceMappings
        else None
    )
    if BlockDeviceMappings is not None:
        r["BlockDeviceMappings"] = BlockDeviceMappings
    EbsOptimized = config.ebsOptimized
    if EbsOptimized is not None:
        r["EbsOptimized"] = EbsOptimized
    IamInstanceProfile = (
        unpack_iam_instance_profile_specification(config.iamInstanceProfile)
        if config.iamInstanceProfile
        else None
    )
    if IamInstanceProfile is not None:
        r["IamInstanceProfile"] = IamInstanceProfile
    ImageId = config.imageId
    if ImageId is not None:
        r["ImageId"] = ImageId
    InstanceType = config.instanceType
    if InstanceType is not None:
        r["InstanceType"] = InstanceType
    KernelId = config.kernelId
    if KernelId is not None:
        r["KernelId"] = KernelId
    KeyName = config.keyName
    if KeyName is not None:
        r["KeyName"] = KeyName
    Monitoring = (
        unpack_spot_fleet_monitoring(config.monitoring) if config.monitoring else None
    )
    if Monitoring is not None:
        r["Monitoring"] = Monitoring
    NetworkInterfaces = (
        [
            unpack_instance_network_interface_specification(c)
            for c in config.networkInterfaces
        ]
        if config.networkInterfaces
        else None
    )
    if NetworkInterfaces is not None:
        r["NetworkInterfaces"] = NetworkInterfaces
    Placement = unpack_spot_placement(config.placement) if config.placement else None
    if Placement is not None:
        r["Placement"] = Placement
    RamdiskId = config.ramdiskId
    if RamdiskId is not None:
        r["RamdiskId"] = RamdiskId
    SecurityGroups = (
        [unpack_group_identifier(c) for c in config.securityGroups]
        if config.securityGroups
        else None
    )
    if SecurityGroups is not None:
        r["SecurityGroups"] = SecurityGroups
    SpotPrice = config.spotPrice
    if SpotPrice is not None:
        r["SpotPrice"] = SpotPrice
    SubnetId = config.subnetId.value if config.subnetId else None
    if SubnetId is not None:
        r["SubnetId"] = SubnetId
    UserData = config.userData
    if UserData is not None:
        r["UserData"] = UserData
    WeightedCapacity = config.weightedCapacity
    if WeightedCapacity is not None:
        r["WeightedCapacity"] = WeightedCapacity
    return r


class FleetLaunchTemplateSpecificationOptions(ResourceOptions):
    launchTemplateId: Optional[ResourceReferenceOption[str, str]]
    launchTemplateName: Optional[str]
    version: Optional[str]


def unpack_fleet_launch_template_specification(
    config: FleetLaunchTemplateSpecificationOptions,
) -> FleetLaunchTemplateSpecificationTypeDef:
    r = FleetLaunchTemplateSpecificationTypeDef()
    LaunchTemplateId = (
        config.launchTemplateId.value if config.launchTemplateId else None
    )
    if LaunchTemplateId is not None:
        r["LaunchTemplateId"] = LaunchTemplateId
    LaunchTemplateName = config.launchTemplateName
    if LaunchTemplateName is not None:
        r["LaunchTemplateName"] = LaunchTemplateName
    Version = config.version
    if Version is not None:
        r["Version"] = Version
    return r


class LaunchTemplateOverridesOptions(ResourceOptions):
    availabilityZone: Optional[str]
    instanceType: Optional[str]
    priority: Optional[float]
    spotPrice: Optional[str]
    subnetId: Optional[ResourceReferenceOption[str, str]]
    weightedCapacity: Optional[float]


def unpack_launch_template_overrides(
    config: LaunchTemplateOverridesOptions,
) -> LaunchTemplateOverridesTypeDef:
    r = LaunchTemplateOverridesTypeDef()
    AvailabilityZone = config.availabilityZone
    if AvailabilityZone is not None:
        r["AvailabilityZone"] = AvailabilityZone
    InstanceType = config.instanceType
    if InstanceType is not None:
        r["InstanceType"] = InstanceType
    Priority = config.priority
    if Priority is not None:
        r["Priority"] = Priority
    SpotPrice = config.spotPrice
    if SpotPrice is not None:
        r["SpotPrice"] = SpotPrice
    SubnetId = config.subnetId.value if config.subnetId else None
    if SubnetId is not None:
        r["SubnetId"] = SubnetId
    WeightedCapacity = config.weightedCapacity
    if WeightedCapacity is not None:
        r["WeightedCapacity"] = WeightedCapacity
    return r


class LaunchTemplateConfigOptions(ResourceOptions):
    launchTemplateSpecification: Optional[FleetLaunchTemplateSpecificationOptions]
    overrides: Sequence[LaunchTemplateOverridesOptions]


def unpack_launch_template_config(
    config: LaunchTemplateConfigOptions,
) -> LaunchTemplateConfigTypeDef:
    r = LaunchTemplateConfigTypeDef()
    LaunchTemplateSpecification = (
        unpack_fleet_launch_template_specification(config.launchTemplateSpecification)
        if config.launchTemplateSpecification
        else None
    )
    if LaunchTemplateSpecification is not None:
        r["LaunchTemplateSpecification"] = LaunchTemplateSpecification
    Overrides = (
        [unpack_launch_template_overrides(c) for c in config.overrides]
        if config.overrides
        else None
    )
    if Overrides is not None:
        r["Overrides"] = Overrides
    return r


class ClassicLoadBalancerOptions(ResourceOptions):
    name: Optional[str]


def unpack_classic_load_balancer(
    config: ClassicLoadBalancerOptions,
) -> ClassicLoadBalancerTypeDef:
    r = ClassicLoadBalancerTypeDef()
    Name = config.name
    if Name is not None:
        r["Name"] = Name
    return r


class ClassicLoadBalancersConfigOptions(ResourceOptions):
    classicLoadBalancers: Sequence[ClassicLoadBalancerOptions]


def unpack_classic_load_balancers_config(
    config: ClassicLoadBalancersConfigOptions,
) -> ClassicLoadBalancersConfigTypeDef:
    r = ClassicLoadBalancersConfigTypeDef()
    ClassicLoadBalancers = (
        [unpack_classic_load_balancer(c) for c in config.classicLoadBalancers]
        if config.classicLoadBalancers
        else None
    )
    if ClassicLoadBalancers is not None:
        r["ClassicLoadBalancers"] = ClassicLoadBalancers
    return r


class TargetGroupOptions(ResourceOptions):
    arn: Optional[str]


def unpack_target_group(
    config: TargetGroupOptions,
) -> TargetGroupTypeDef:
    r = TargetGroupTypeDef()
    Arn = config.arn
    if Arn is not None:
        r["Arn"] = Arn
    return r


class TargetGroupsConfigOptions(ResourceOptions):
    targetGroups: Sequence[TargetGroupOptions]


def unpack_target_groups_config(
    config: TargetGroupsConfigOptions,
) -> TargetGroupsConfigTypeDef:
    r = TargetGroupsConfigTypeDef()
    TargetGroups = (
        [unpack_target_group(c) for c in config.targetGroups]
        if config.targetGroups
        else None
    )
    if TargetGroups is not None:
        r["TargetGroups"] = TargetGroups
    return r


class LoadBalancersConfigOptions(ResourceOptions):
    classicLoadBalancersConfig: Optional[ClassicLoadBalancersConfigOptions]
    targetGroupsConfig: Optional[TargetGroupsConfigOptions]


def unpack_load_balancers_config(
    config: LoadBalancersConfigOptions,
) -> LoadBalancersConfigTypeDef:
    r = LoadBalancersConfigTypeDef()
    ClassicLoadBalancersConfig = (
        unpack_classic_load_balancers_config(config.classicLoadBalancersConfig)
        if config.classicLoadBalancersConfig
        else None
    )
    if ClassicLoadBalancersConfig is not None:
        r["ClassicLoadBalancersConfig"] = ClassicLoadBalancersConfig
    TargetGroupsConfig = (
        unpack_target_groups_config(config.targetGroupsConfig)
        if config.targetGroupsConfig
        else None
    )
    if TargetGroupsConfig is not None:
        r["TargetGroupsConfig"] = TargetGroupsConfig
    return r


class SpotCapacityRebalanceOptions(ResourceOptions):
    replacementStrategy: Optional[Literal["launch"]]


def unpack_spot_capacity_rebalance(
    config: SpotCapacityRebalanceOptions,
) -> SpotCapacityRebalanceTypeDef:
    r = SpotCapacityRebalanceTypeDef()
    ReplacementStrategy = config.replacementStrategy
    if ReplacementStrategy is not None:
        r["ReplacementStrategy"] = ReplacementStrategy
    return r


class SpotMaintenanceStrategiesOptions(ResourceOptions):
    capacityRebalance: Optional[SpotCapacityRebalanceOptions]


def unpack_spot_maintenance_strategies(
    config: SpotMaintenanceStrategiesOptions,
) -> SpotMaintenanceStrategiesTypeDef:
    r = SpotMaintenanceStrategiesTypeDef()
    CapacityRebalance = (
        unpack_spot_capacity_rebalance(config.capacityRebalance)
        if config.capacityRebalance
        else None
    )
    if CapacityRebalance is not None:
        r["CapacityRebalance"] = CapacityRebalance
    return r
    return r


class AwsSpotFleetOptions(ResourceOptions):
    # spotFleetRequestId: str
    iamFleetRole: ResourceReferenceOption[str, str]
    targetCapacity: int
    allocationStrategy: Optional[
        Literal[
            "capacityOptimized",
            "capacityOptimizedPrioritized",
            "diversified",
            "lowestPrice",
        ]
    ]
    # clientToken: Optional[str]
    # context: Optional[str]
    excessCapacityTerminationPolicy: Optional[Literal["default", "noTermination"]]
    fulfilledCapacity: Optional[float]
    instanceInterruptionBehavior: Optional[Literal["hibernate", "stop", "terminate"]]
    instancePoolsToUseCount: Optional[int]
    launchSpecifications: Sequence[SpotFleetLaunchSpecificationOptions]
    launchTemplateConfigs: Sequence[LaunchTemplateConfigOptions]
    loadBalancersConfig: Optional[LoadBalancersConfigOptions]
    onDemandAllocationStrategy: Optional[Literal["lowestPrice", "prioritized"]]
    onDemandFulfilledCapacity: Optional[float]
    onDemandMaxTotalPrice: Optional[str]
    onDemandTargetCapacity: Optional[int]
    replaceUnhealthyInstances: Optional[bool]
    spotMaintenanceStrategies: Optional[SpotMaintenanceStrategiesOptions]
    spotMaxTotalPrice: Optional[str]
    spotPrice: Optional[str]
    # tagSpecifications: Sequence[TagSpecificationOptions]
    terminateInstancesWithExpiration: Optional[bool]
    type: Optional[
        Union[
            Literal["request"],
            Literal["maintain"]
            # Literal["instant"] # instant is listed but is not used by Spot Fleet.
        ]
    ]
    # validFrom: Optional[datetime]
    # validUntil: Optional[datetime]

    # Common EC2 auth options
    accessKeyId: str
    region: str

    # Common EC2 options
    tags: Mapping[str, str]


def unpack_create_spot_fleet_request(
    config: AwsSpotFleetOptions,
) -> SpotFleetRequestConfigDataTypeDef:
    r = SpotFleetRequestConfigDataTypeDef(
        IamFleetRole=config.iamFleetRole.value, TargetCapacity=config.targetCapacity
    )
    AllocationStrategy = config.allocationStrategy
    if AllocationStrategy is not None:
        r["AllocationStrategy"] = AllocationStrategy
    ExcessCapacityTerminationPolicy = config.excessCapacityTerminationPolicy
    if ExcessCapacityTerminationPolicy is not None:
        r["ExcessCapacityTerminationPolicy"] = ExcessCapacityTerminationPolicy
    FulfilledCapacity = config.fulfilledCapacity
    if FulfilledCapacity is not None:
        r["FulfilledCapacity"] = FulfilledCapacity
    InstanceInterruptionBehavior = config.instanceInterruptionBehavior
    if InstanceInterruptionBehavior is not None:
        r["InstanceInterruptionBehavior"] = InstanceInterruptionBehavior
    InstancePoolsToUseCount = config.instancePoolsToUseCount
    if InstancePoolsToUseCount is not None:
        r["InstancePoolsToUseCount"] = InstancePoolsToUseCount
    LaunchSpecifications = (
        [unpack_spot_fleet_launch_specification(c) for c in config.launchSpecifications]
        if config.launchSpecifications
        else None
    )
    if LaunchSpecifications is not None:
        r["LaunchSpecifications"] = LaunchSpecifications
    LaunchTemplateConfigs = (
        [unpack_launch_template_config(c) for c in config.launchTemplateConfigs]
        if config.launchTemplateConfigs
        else None
    )
    if LaunchTemplateConfigs is not None:
        r["LaunchTemplateConfigs"] = LaunchTemplateConfigs
    LoadBalancersConfig = (
        unpack_load_balancers_config(config.loadBalancersConfig)
        if config.loadBalancersConfig
        else None
    )
    if LoadBalancersConfig is not None:
        r["LoadBalancersConfig"] = LoadBalancersConfig
    OnDemandAllocationStrategy = config.onDemandAllocationStrategy
    if OnDemandAllocationStrategy is not None:
        r["OnDemandAllocationStrategy"] = OnDemandAllocationStrategy
    OnDemandFulfilledCapacity = config.onDemandFulfilledCapacity
    if OnDemandFulfilledCapacity is not None:
        r["OnDemandFulfilledCapacity"] = OnDemandFulfilledCapacity
    OnDemandMaxTotalPrice = config.onDemandMaxTotalPrice
    if OnDemandMaxTotalPrice is not None:
        r["OnDemandMaxTotalPrice"] = OnDemandMaxTotalPrice
    OnDemandTargetCapacity = config.onDemandTargetCapacity
    if OnDemandTargetCapacity is not None:
        r["OnDemandTargetCapacity"] = OnDemandTargetCapacity
    ReplaceUnhealthyInstances = config.replaceUnhealthyInstances
    if ReplaceUnhealthyInstances is not None:
        r["ReplaceUnhealthyInstances"] = ReplaceUnhealthyInstances
    SpotMaintenanceStrategies = (
        unpack_spot_maintenance_strategies(config.spotMaintenanceStrategies)
        if config.spotMaintenanceStrategies
        else None
    )
    if SpotMaintenanceStrategies is not None:
        r["SpotMaintenanceStrategies"] = SpotMaintenanceStrategies
    SpotMaxTotalPrice = config.spotMaxTotalPrice
    if SpotMaxTotalPrice is not None:
        r["SpotMaxTotalPrice"] = SpotMaxTotalPrice
    SpotPrice = config.spotPrice
    if SpotPrice is not None:
        r["SpotPrice"] = SpotPrice
    TerminateInstancesWithExpiration = config.terminateInstancesWithExpiration
    if TerminateInstancesWithExpiration is not None:
        r["TerminateInstancesWithExpiration"] = TerminateInstancesWithExpiration
    RequestType = config.type
    if RequestType is not None:
        r["Type"] = RequestType
    return r


# def override(a: Mapping, b: Mapping) -> dict:
#     if a is None:
#         return b
#     elif b is None:
#         return a
#     else:
#         return (
#             {k: a[k] for k in a.keys() - b.keys()}
#             | {k: override(a[k], b[k]) for k in a.keys() & b.keys()}
#             | {k: b[k] for k in b.keys() - a.keys()}
#         )


def unpack_modify_spot_fleet_request(
    config: AwsSpotFleetOptions,
    SpotFleetRequestId: str,
) -> ModifySpotFleetRequestRequestRequestTypeDef:
    r = ModifySpotFleetRequestRequestRequestTypeDef(
        SpotFleetRequestId=SpotFleetRequestId
    )
    ExcessCapacityTerminationPolicy = config.excessCapacityTerminationPolicy
    if ExcessCapacityTerminationPolicy is not None:
        r["ExcessCapacityTerminationPolicy"] = ExcessCapacityTerminationPolicy
    LaunchTemplateConfigs = (
        [unpack_launch_template_config(c) for c in config.launchTemplateConfigs]
        if config.launchTemplateConfigs
        else None
    )
    if LaunchTemplateConfigs is not None:
        r["LaunchTemplateConfigs"] = LaunchTemplateConfigs
    OnDemandTargetCapacity = config.onDemandTargetCapacity
    if OnDemandTargetCapacity is not None:
        r["OnDemandTargetCapacity"] = OnDemandTargetCapacity
    TargetCapacity = config.targetCapacity
    if TargetCapacity is not None:
        r["TargetCapacity"] = TargetCapacity
    return r

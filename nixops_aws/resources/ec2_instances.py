# -*- coding: utf-8 -*-
from . import ec2_common
from .types.ec2_instances import Ec2InstancesOptions, RunInstancesRequestRequestTypeDef

import boto3

import botocore.exceptions

# import nixops.util
import nixops.resources
import nixops_aws.ec2_utils
from mypy_boto3_ec2 import type_defs

# from nixops.state import StateDict

# from nixops_aws.backends import ec2
import nixops_aws.resources.ec2_keypair
import nixops_aws.resources.iam_role
import nixops_aws.resources.ec2_security_group
import nixops_aws.resources.ec2_placement_group
import nixops_aws.resources.ebs_volume
import nixops_aws.resources.elastic_ip
import nixops_aws.resources.vpc_subnet
import nixops_aws.resources.vpc_route
import nixops_aws.resources.elastic_file_system
import nixops_aws.resources.elastic_file_system_mount_target
import typeguard
from typing import Optional, Generic, TypeVar, Any, Mapping

RequestType = TypeVar("RequestType")
ResponseType = TypeVar("ResponseType")


# def check_typeddict(d: RequestType) -> bool:
#     for ann in d.__required_keys__:
#         print(ann)
#     return false

class EC2InstancesDefinition(nixops.resources.ResourceDefinition):
    """Definition of an EC2 instance."""

    config: Ec2InstancesOptions

    @classmethod
    def get_type(cls):
        return "ec2-instances"

    @classmethod
    def get_resource_type(cls):
        return "ec2Instances"

    # def __init__(self, name: str, config):
    #     # print("instances config", config)
    #     nixops.resources.ResourceDefinition.__init__(self, name, config)
    #     # self.instance_name = self.config.name
    #     # self.region = self.config.region
    #     # self.access_key_id = self.config.accessKeyId

    def show_type(self):
        return "{0}".format(self.get_type())
        # return "{0} [{1}]".format(self.get_type(), self.region)


class AwsResourceState(
    nixops.resources.ResourceState,
    Generic[nixops.resources.ResourceDefinitionType],
    ec2_common.EC2CommonState,
):
    """Base class for AWS resource state objects"""

    state = nixops.util.attr_property(
        "state", nixops.resources.ResourceState.MISSING, int
    )
    access_key_id = nixops.util.attr_property("accessKeyId", None)
    region = nixops.util.attr_property("region", None)

    awsConfig = nixops.util.attr_property("awsConfig", {}, "json")

    # TODO: See EC2CommonState ? Needed??
    def get_client(self, service):
        if hasattr(self, "_client"):
            if self._client:
                return self._client

        assert self.region
        (access_key_id, secret_access_key) = nixops_aws.ec2_utils.fetch_aws_secret_key(
            self.access_key_id
        )
        self._client = boto3.session.Session().client(
            service_name=service,
            region_name=self.region,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
        )
        return self._client

    def _exists(self):
        return self.state != self.MISSING

    # TODO: generic create_after using "res-${res._type}-${res._name}
    # create_after()

    def _save_aws_config(
        self, aws_config: Mapping[str, Any], request: RequestType, response: ResponseType
    ):
        (existing_keys, new_keys) = (
            [k for k in self.awsConfig],
            [k for k in aws_config],
        )
        (mutual_keys, missing_from_new, missing_from_existing) = (
            [k for k in existing_keys if k in new_keys],
            [k for k in existing_keys if k not in new_keys],
            [k for k in new_keys if k not in new_keys],
        )

        # # val = config.get(k)
        # # if val:
        # #     if type(val) in (int, float, bool, str):
        # #         self.awsConfig
        # # self.allocationStrategy = config["AllocationStrategy"]
        # # if config["OnDemandAllocationStrategy"] is not None:
        # #     self.onDemandAllocationStrategy = config["OnDemandAllocationStrategy"]
        # # if config["SpotMaintenanceStrategies"] is not None:
        # #     self.spotMaintenanceStrategies = config["SpotMaintenanceStrategies"]
        # # if config["ClientToken"] is not None:
        # #     self.clientToken = config["ClientToken"]
        # # if config["ExcessCapacityTerminationPolicy"] is not None:
        # #     self.excessCapacityTerminationPolicy = (
        # #         config["ExcessCapacityTerminationPolicy"]
        # #     )
        # # if config["FulfilledCapacity"] is not None:
        # #     self.fulfilledCapacity = config["FulfilledCapacity"]
        # # if config["OnDemandFulfilledCapacity"] is not None:
        # #     self.onDemandFulfilledCapacity = config["OnDemandFulfilledCapacity"]
        # self.iamFleetRole = config["IamFleetRole"]
        # # if config["LaunchSpecifications"] is not None:
        # #     self.launchSpecifications = config["LaunchSpecifications"]
        # if config["LaunchTemplateConfigs"] is not None:
        #     self.launchTemplateConfigs = config["LaunchTemplateConfigs"]
        # if config["SpotPrice"] is not None:
        #     self.spotPrice = config["SpotPrice"]
        # self.targetCapacity = config["TargetCapacity"]
        # # if config["OnDemandTargetCapacity"] is not None:
        # #     self.onDemandTargetCapacity = config["OnDemandTargetCapacity"]
        # # if config["OnDemandMaxTotalPrice"] is not None:
        # #     self.onDemandMaxTotalPrice = config["OnDemandMaxTotalPrice"]
        # if config["SpotMaxTotalPrice"] is not None:
        #     self.spotMaxTotalPrice = config["SpotMaxTotalPrice"]
        # # if config["TerminateInstancesWithExpiration"] is not None:
        # #     self.terminateInstancesWithExpiration = (
        # #         config["TerminateInstancesWithExpiration"]
        # #     )
        # if config["Type"] is not None:
        #     self.type = config["Type"]
        # # if config["ValidFrom"] is not None:
        # #     self.validFrom = config["ValidFrom"]
        # # if config["ValidUntil"] is not None:
        # #     self.validUntil = config["ValidUntil"]
        # # if config["ReplaceUnhealthyInstances"] is not None:
        # #     self.replaceUnhealthyInstances = config["ReplaceUnhealthyInstances"]
        # # if config["InstanceInterruptionBehavior"] is not None:
        # #     self.instanceInterruptionBehavior = (
        # #         config["InstanceInterruptionBehavior"]
        # #     )
        # # if config["LoadBalancersConfig"] is not None:
        # #     self.loadBalancersConfig = config["LoadBalancersConfig"]
        # # if config["InstancePoolsToUseCount"] is not None:
        # #     self.instancePoolsToUseCount = config["InstancePoolsToUseCount"]
        # # if config["TagSpecifications"] is not None:
        # #     self.tagSpecifications = config["TagSpecifications"]


class EC2InstancesState(AwsResourceState[EC2InstancesDefinition]):
    """State of an EC2 instance."""

    definition_type = EC2InstancesDefinition

    # access_key_id = nixops.util.attr_property("accessKeyId", None)
    # region = nixops.util.attr_property("region", None)

    # awsConfig: RunInstancesRequestRequestTypeDef
    # awsConfig = nixops.util.attr_property("awsConfig", {}, "json")

    reservationId = nixops.util.attr_property("reservationId", None)
    instanceIds = nixops.util.attr_property("instanceIds", [], "json")

    @classmethod
    def get_type(cls):
        return "ec2-instances"

    def __init__(self, depl, name, id):
        nixops.resources.ResourceState.__init__(self, depl, name, id)

    def show_type(self):
        s = super(EC2InstancesState, self).show_type()
        return s

    @property
    def resource_id(self):
        return self.reservationId

    def create_after(self, resources, defn):
        # EC2 instances can require key pairs, IAM roles, security
        # groups, EBS volumes and elastic IPs.  FIXME: only depend on
        # the specific key pair / role needed for this instance.
        return {
            r
            for r in resources
            if isinstance(r, nixops_aws.resources.ec2_keypair.EC2KeyPairState)
            or isinstance(r, nixops_aws.resources.iam_role.IAMRoleState)
            or isinstance(
                r, nixops_aws.resources.ec2_security_group.EC2SecurityGroupState
            )
            or isinstance(
                r, nixops_aws.resources.ec2_placement_group.EC2PlacementGroupState
            )
            or isinstance(r, nixops_aws.resources.ebs_volume.EBSVolumeState)
            or isinstance(r, nixops_aws.resources.elastic_ip.ElasticIPState)
            or isinstance(r, nixops_aws.resources.vpc_subnet.VPCSubnetState)
            or isinstance(r, nixops_aws.resources.vpc_route.VPCRouteState)
            or isinstance(
                r, nixops_aws.resources.elastic_file_system.ElasticFileSystemState
            )
            or isinstance(
                r,
                nixops_aws.resources.elastic_file_system_mount_target.ElasticFileSystemMountTargetState,
            )
        }

    def create(
        self,
        defn: EC2InstancesDefinition,
        check: bool,
        allow_reboot: bool,
        allow_recreate: bool,
    ):
        self.access_key_id = (
            defn.config.accessKeyId or nixops_aws.ec2_utils.get_access_key_id()
        )
        if not self.access_key_id:
            raise Exception(
                "please set ‘accessKeyId’, $EC2_ACCESS_KEY or $AWS_ACCESS_KEY_ID"
            )

        if self._exists():
            # immutable_values = {
            #     "region": defn.config.region,
            # }
            # immutable_diff = {
            #     k for k in immutable_values if getattr(self, k) != immutable_values[k]
            # }  # TODO dict diff
            # if immutable_diff:
            #     raise Exception(
            #         "changing keys ‘{0}’ (from ‘{1}’ to ‘{2}’) of an existing instance is not supported".format(
            #             immutable_diff,
            #             [getattr(self, k) for k in immutable_diff],
            #             [getattr(defn.config, k) for k in immutable_diff],
            #         )
            #     )

            # mutable_values: Dict[str, Any] = {}
            # mutable_diff = [
            #     k for k in mutable_values if getattr(self, k) != mutable_values[k]
            # ]  # TODO dict diff
            # if mutable_diff:
            #     # request = ModifyInstance...(
            #     # )

            #     self.log(
            #         "modifying instance `{}`... ".format(
            #             self.instanceIds...
            #         )
            #     )
            #     # self._modify_instance(request)

            #     # TODO stop & modify the instance
            #     # TODO update tags
            raise Exception("TODO")

        if self.state == self.MISSING:
            self.log(
                "creating instance with target capacity of ‘{0}’...".format(
                    # self.targetCapacity
                    0
                )
            )
            # The region may only be set once, when a new instance is being requested
            with self.depl._db:
                self.region = defn.config.region

            # Save request to deployment state (TODO: improve)
            request = self._to_run_instances_request(defn.config)
            self._save_aws_config(
                defn.config.awsConfig,
                request=request,
                response=self._run_instances(request),
            )

    def check(self):
        if self.reservationId is None:
            self.state = self.MISSING
            return

        response = self._describe_instances(
            type_defs.DescribeInstancesRequestRequestTypeDef(
                InstanceIds=self.instanceIds
            )
        )

        # TODO handle state
        # self.warn()

        return

    def destroy(self, wipe=False):
        if not self._exists():
            return True

        # self.log("canceling instances with ids ‘{0}’...".format(self.instanceIds))
        # try:
        #     self._cancel_instances(
        #         CancelInstanceRequestsRequestRequestTypeDef(
        #             InstanceRequestIds=[self.instanceId], TerminateInstances=True,
        #         )
        #     )
        # except botocore.exceptions.ClientError as e:
        #     if e.response["Error"]["Code"] == "ResourceNotFoundException":
        #         self.warn(
        #             "instance with id {0} was already deleted".format(self.instanceId)
        #         )
        #     else:
        #         raise e
        raise Exception("TODO: destroy")

        return True

    # Boto3 helpers

    # def _to_resource_state(self, state: BatchStateType) -> int:
    #     if state == "active":
    #         return self.UP
    #     elif state == "cancelled":
    #         return self.MISSING
    #     elif state == "cancelled_running":
    #         return self.MISSING
    #     elif state == "cancelled_terminating":
    #         return self.MISSING
    #     elif state == "failed":
    #         return self.MISSING
    #     elif state == "modifying":
    #         return self.UP
    #     elif state == "submitted":
    #         return self.UP
    #     else:
    #         return self.UNKNOWN

    # def _to_launch_template_overrides(
    #     self, overrides
    # ) -> LaunchTemplateOverridesTypeDef:
    #     result = LaunchTemplateOverridesTypeDef()
    #     if overrides.instanceType:
    #         result["InstanceType"] = overrides.instanceType
    #     if overrides.spotPrice:
    #         result["SpotPrice"] = overrides.spotPrice
    #     if overrides.subnetId:
    #         result["SubnetId"] = overrides.subnetId
    #     if overrides.availabilityZone:
    #         result["AvailabilityZone"] = overrides.availabilityZone
    #     if overrides.weightedCapacity:
    #         result["WeightedCapacity"] = overrides.weightedCapacity
    #     if overrides.priority:
    #         result["Priority"] = overrides.priority
    #     return result

    def _to_run_instances_request(self, config) -> RunInstancesRequestRequestTypeDef:
        # tags = dict(config.tags)
        # tags.update(self.get_common_tags())

        # # # TODO instance tags
        # # instance_tags = dict(config.tags)
        # # instance_tags.update(self.get_common_tags())

        # launch_template_configs = [
        #     LaunchTemplateConfigTypeDef(
        #         LaunchTemplateSpecification=FleetLaunchTemplateSpecificationTypeDef(
        #             # LaunchTemplateId: str
        #             LaunchTemplateName=template_config.launchTemplateSpecification.launchTemplateName,
        #             Version=template_config.launchTemplateSpecification.version,
        #         ),
        #         Overrides=[
        #             self._to_launch_template_overrides(overrides)
        #             for overrides in template_config.overrides
        #         ],
        #     )
        #     for template_config in config.launchTemplateConfigs
        # ]

        request = type_defs.RunInstancesRequestRequestTypeDef(**config.awsConfig)  # type: ignore
        # if config.spotPrice:
        #     request["InstanceRequestConfig"]["SpotPrice"] = config.spotPrice
        # if config.spotMaxTotalPrice:
        #     request["InstanceRequestConfig"][
        #         "SpotMaxTotalPrice"
        #     ] = config.spotMaxTotalPrice
        typeguard.check_type(type_defs.RunInstancesRequestRequestTypeDef.__name__, request, type_defs.RunInstancesRequestRequestTypeDef)
        return request

    # def _arn_from_role_name(self, role_name):
    #     if role_name.startswith("arn:aws:iam"):
    #         return role_name

    #     role_arn = self.get_client("iam").get_role(RoleName=role_name)
    #     return role_arn["Role"]["Arn"]

    # def _save_tags(self, tags: List[TagTypeDef]):
    #     pass

    # Boto3 wrappers

    def _describe_instances(
        self, request: type_defs.DescribeInstancesRequestRequestTypeDef
    ) -> Optional[type_defs.DescribeInstancesResultTypeDef]:

        # TODO type check request

        def check_response_field(name, value, expected_value):
            if value != expected_value:
                raise Exception(
                    "Unexpected value ‘{0} = {1}’ in response, expected ‘{0} = {2}’".format(
                        name, value, expected_value
                    )
                )

        def check_response_field_in(name, value, expected_values):
            if not (value in expected_values):
                raise Exception(
                    "Unexpected value ‘{0} = {1}’ in response, expected one of ‘{2}’".format(
                        name, value, expected_values
                    )
                )

        try:
            response: type_defs.DescribeInstancesResultTypeDef
            response = self.get_client("ec2").describe_instances(**request)

            for reservation in response["Reservations"]:
                check_response_field(
                    "ReservationId", reservation["ReservationId"], self.reservationId,
                )

                for instance in reservation["Instances"]:
                    check_response_field_in(
                        "InstanceId", instance["InstanceId"], self.instanceIds
                    )

                    # TODO save remaining fields...

                    # TODO save instance resource
                    # instance["State"]
                    #     'Code': 123,
                    #     'Name': 'pending'|'running'|'shutting-down'|'terminated'|'stopping'|'stopped'

                if not request.get("DryRun"):
                    with self.depl._db:
                        # # Update deployment state from response
                        # self.state = self._to_resource_state(
                        #     config["InstanceRequestState"]
                        # )
                        # self._save_config_data(config["InstanceRequestConfig"])
                        # self._save_tags(config["Tags"])
                        pass

            return response
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                self.state = self.MISSING
                return None
            else:
                raise e

    def _run_instances(
        self, request: RunInstancesRequestRequestTypeDef
    ) -> type_defs.ReservationResponseMetadataTypeDef:
        response = self.get_client("ec2").run_instances(**request)

        if not request.get("DryRun"):
            with self.depl._db:
                # self.state = self.UP

                # Save response to deployment state
                self.reservationId = response["ReservationId"]
                self.instanceIds = [
                    instance["InstanceId"] for instance in response["Instances"]
                ]

                # ReservationResponseMetadataTypeDef
                # Groups: List[GroupIdentifierTypeDef]
                # Instances: List[InstanceTypeDef]
                # OwnerId: str
                # RequesterId: str
                # ReservationId: str
                # ResponseMetadata: ResponseMetadataTypeDef
                pass

        return response

    # def _modify_instance(
    #     self, request: ModifyInstanceRequestTypeDef
    # ) -> Optional[ModifyInstanceTypeDef]:
    #     try:
    #         response = self.get_client("ec2").modify_instance_request(
    #             # **dataclasses.asdict(request)
    #             **request
    #         )

    #         if response.Return:
    #             with self.depl._db:
    #                 # Save request to deployment state
    #                 # if request.ExcessCapacityTerminationPolicy is not None:
    #                 #     self.excessCapacityTerminationPolicy = (
    #                 #         request.ExcessCapacityTerminationPolicy
    #                 #     )
    #                 # if request.LaunchTemplateConfigs is not None:
    #                 #     self.launchTemplateConfigs = request.LaunchTemplateConfigs
    #                 if request["TargetCapacity"] is not None:
    #                     self.targetCapacity = request["TargetCapacity"]
    #                 if request["OnDemandTargetCapacity"] is not None:
    #                     self.onDemandTargetCapacity = request["OnDemandTargetCapacity"]

    #         return response

    #     except botocore.exceptions.ClientError as e:
    #         if e.response["Error"]["Code"] == "ResourceNotFoundException":
    #             with self.depl._db:
    #                 self.state = self.MISSING
    #             return None
    #         else:
    #             raise e

    # def _cancel_instance(
    #     self, request: CancelInstanceRequestsRequestRequestTypeDef
    # ) -> CancelInstanceRequestsResponseTypeDef:
    #     response = self.get_client("ec2").cancel_instance_requests(
    #         # **dataclasses.asdict(request)
    #         **request
    #     )

    #     def check_response_field(name, value, expected_value):
    #         if value != expected_value:
    #             raise Exception(
    #                 "Unexpected value ‘{0} = {1}’ in response, expected ‘{0} = {2}’".format(
    #                     name, value, expected_value
    #                 )
    #             )

    #     for item in response["SuccessfulFleetRequests"]:
    #         check_response_field(
    #             "InstanceRequestId",
    #             item["InstanceRequestId"],
    #             self.instanceId,
    #         )
    #         self.state = self._to_resource_state(item["CurrentInstanceRequestState"])

    #     for item in response["UnsuccessfulFleetRequests"]:
    #         check_response_field(
    #             "InstanceRequestId",
    #             item["InstanceRequestId"],
    #             self.instanceId,
    #         )
    #         self.warn(
    #             "instance with id ‘{0}’ cancelation failed with error ‘{1}: {2}’".format(
    #                 self.instanceId,
    #                 response["Error"]["Code"],
    #                 response["Error"]["Message"],
    #             )
    #         )
    #         self.state = self.UNKNOWN

    #     return response

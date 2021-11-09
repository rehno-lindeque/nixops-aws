# -*- coding: utf-8 -*-

# Automatic provisioning of spot fleets.

import boto3
import botocore
import inspect
import json
from nixops.diff import Handler
import nixops.resources
import nixops.util
from nixops_aws.resources.ec2_common import EC2CommonState
import nixops_aws.ec2_utils
import time
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Literal,
    Optional,
    Type,
    TYPE_CHECKING,
    TypedDict,
    TypeVar,
)
from . import ec2_common
from .aws_ec2_launch_template import Ec2LaunchTemplateState
from .definition import AwsResourceDefinition
from .ec2_security_group import EC2SecurityGroupState
from .iam_role import IAMRoleState
from .state import AwsResourceState
from .util.references import ResourceReferenceOption, Unresolved
from .types.spot_fleet import (
    AwsSpotFleetOptions,
    unpack_create_spot_fleet_request,
    unpack_modify_spot_fleet_request,
)
from .vpc_network_interface import VPCNetworkInterfaceState
from .vpc_subnet import VPCSubnetState
from ..boto_clients import BotoClients

if TYPE_CHECKING:
    from mypy_boto3_ec2.literals import BatchStateType
    from mypy_boto3_ec2.type_defs import (
        RequestSpotFleetRequestRequestTypeDef,
        RequestSpotFleetResponseTypeDef,
        SpotFleetRequestConfigDataTypeDef,
        DescribeSpotFleetRequestsRequestRequestTypeDef,
        DescribeSpotFleetRequestsResponseTypeDef,
        ModifySpotFleetRequestRequestRequestTypeDef,
        ModifySpotFleetRequestResponseTypeDef,
        CancelSpotFleetRequestsRequestRequestTypeDef,
        CancelSpotFleetRequestsResponseTypeDef,
        LaunchTemplateConfigTypeDef,
        FleetLaunchTemplateSpecificationTypeDef,
        LaunchTemplateOverridesTypeDef,
        TagSpecificationTypeDef,
        TagTypeDef,
    )
else:
    BatchStateType = object
    RequestSpotFleetRequestRequestTypeDef = dict
    RequestSpotFleetResponseTypeDef = dict
    SpotFleetRequestConfigDataTypeDef = dict
    DescribeSpotFleetRequestsRequestRequestTypeDef = dict
    DescribeSpotFleetRequestsResponseTypeDef = dict
    ModifySpotFleetRequestRequestRequestTypeDef = dict
    ModifySpotFleetRequestResponseTypeDef = dict
    CancelSpotFleetRequestsRequestRequestTypeDef = dict
    CancelSpotFleetRequestsResponseTypeDef = dict
    LaunchTemplateConfigTypeDef = dict
    FleetLaunchTemplateSpecificationTypeDef = dict
    LaunchTemplateOverridesTypeDef = dict
    TagSpecificationTypeDef = dict
    TagTypeDef = dict

T = TypeVar("T")


class AwsSpotFleetDefinition(AwsResourceDefinition[AwsSpotFleetOptions]):
    """Definition of a spot fleet."""

    config: AwsSpotFleetOptions
    config_type: Type = AwsSpotFleetOptions

    @classmethod
    def get_type(cls):
        return "aws-spot-fleet"

    @classmethod
    def get_resource_type(cls):
        return "awsSpotFleets"

    def __init__(self, name: str, config: nixops.resources.ResourceEval):
        # def unpack(resource_eval: nixops.resources.ResourceEval, options_type: Type):
        #     keys = {k for k in resource_eval}
        #     annotations = options_type.__annnotations__
        #     subtype_keys = {
        #         k: annotations[k]
        #         for k in annotations
        #         if annotations[k]
        #     }
        #     print("...................", subtype_keys)

        # print("DEBUG:", name, config)
        # updated_config = {}
        # for k in self.config_type.__annotations__:
        #     print(
        #         "!!!!",
        #         # self.config_type,
        #         k,
        #         self.config_type.__annotations__[k],
        #         inspect.isclass(self.config_type.__annotations__[k]) and issubclass(
        #             self.config_type.__annotations__[k], nixops.resources.ResourceEval
        #         )
        #     )

        # aws_config = dict(**config["awsConfig"])
        # aws_config["DryRun"] = False
        # updated_config = {
        #     k: config[k] for k in config if k != "awsConfig"
        # }
        # updated_config["awsConfig"] = type_defs.RequestSpotFleetRequestRequestTypeDef(aws_config, total=False)
        # nixops.resources.ResourceDefinition.__init__(self, name, ResourceEval(updated_config))
        super().__init__(name, config)

    def show_type(self):
        return "{0}".format(self.get_type())


class AwsSpotFleetState(AwsResourceState[AwsSpotFleetOptions], EC2CommonState):
    """State of a spot fleet."""

    definition_type = AwsSpotFleetDefinition

    _clients: BotoClients

    state = nixops.util.attr_property(
        "state", nixops.resources.ResourceState.MISSING, int
    )
    access_key_id = nixops.util.attr_property("accessKeyId", None)
    _reserved_keys = EC2CommonState.COMMON_EC2_RESERVED + [
        "spotFleetId",
        "spotFleetRequestId",
    ]

    # # region = nixops.util.attr_property("region", None)

    # spotFleetRequestId = nixops.util.attr_property("spotFleetRequestId", None)
    # allocationStrategy = nixops.util.attr_property("allocationStrategy", None)
    # # allocationStrategy: Optional[Union[
    # #    Literal["lowestPrice"],
    # #    Literal["diversified"],
    # #    Literal["capacityOptimized"],
    # #    Literal["capacityOptimizedPrioritized"]
    # # ]],
    # # clientToken: Optional[str]
    # # excessCapacityTerminationPolicy: Optional[Union[
    # #    Literal["noTermination"],
    # #    Literal["default"]
    # # ]],
    # # fulfilledCapacity: Optional[float]

    # iamFleetRole = nixops.util.attr_property("iamFleetRole", None)

    # # instanceInterruptionBehavior: Optional[Union[
    # #     Literal["hibernate"],
    # #     Literal["top"],
    # #     Literal["terminate"]
    # # ]],
    # # instancePoolsToUseCount: Optional[int]
    # # launchSpecifications = nixops.util.attr_property("launchSpecifications", [], "json")
    # launchTemplateConfigs = nixops.util.attr_property(
    #     "launchTemplateConfigs", [], "json"
    # )
    # # loadBalancersConfig: Optional[List[LoadBalancersConfigOptions]]
    # # onDemandAllocationStrategy: Optional[Union[
    # #    Literal["lowestPrice"],
    # #    Literal["prioritized"]
    # # ]]
    # # onDemandFulfilledCapacity: Optional[float]
    # # onDemandMaxTotalPrice: Optional[str] # todo: price
    # # onDemandTargetCapacity: Optional[int]
    # # replaceUnhealthyInstances: Optional[bool]
    # # spotMaintenaneStrategies: Optional[SpotMaintenanceStrategiesOptions]
    # spotMaxTotalPrice = nixops.util.attr_property("spotMaxTotalPrice", None)
    # spotPrice = nixops.util.attr_property("spotPrice", None)
    # # # tagSpecifications / tags = Mapping[str, str]
    # targetCapacity = nixops.util.attr_property("targetCapacity", 0, int)
    # # terminateInstancesWithExpiration: Optional[bool]
    # type = nixops.util.attr_property("type", None)
    # # validFrom: Optional[Timestamp]
    # # validUntil: Optional[Timestamp]

    def get_client(self, service: Literal["ec2", "iam"], region: Optional[str] = None):
        # Test if the region has changed, and reset clients if so
        client_region = self._state.get("region")
        if region is not None and region != client_region:
            if self.state != self.MISSING:
                raise Exception("can't change the region of an active resource")
            self._clients = BotoClients()
            client_region = region
            with self.depl._db:
                self._state["region"] = client_region

        if client_region is None:
            raise Exception("no region has been assigned for AWS clients")

        client = self._clients.get(service)
        if client:
            return client

        access_key_id = (
            self.get_defn().config.accessKeyId if self.depl.definitions else None  # type: ignore
        ) or nixops_aws.ec2_utils.get_access_key_id()
        if access_key_id is not None:
            self.access_key_id = access_key_id
        if self.access_key_id is None:
            raise Exception(
                "please set 'accessKeyId', $EC2_ACCESS_KEY or $AWS_ACCESS_KEY_ID"
            )
        (access_key_id, secret_access_key) = nixops_aws.ec2_utils.fetch_aws_secret_key(
            self.access_key_id
        )
        # if self._state["region"] is  None:
        #     self_
        # region: str = self._state["region"]
        client = boto3.session.Session().client(
            service_name=service,
            region_name=client_region,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
        )
        self._clients[service] = client
        return client

    def __init__(self, depl, name, id):
        nixops.resources.DiffEngineResourceState.__init__(self, depl, name, id)
        self._clients = BotoClients()
        # self.spot_fleet_request_id = self._state.get("spotFleetRequestId", None)
        self.handle_create_spot_fleet = Handler(
            [
                # immutable options
                "allocationStrategy",
                "fulfilledCapacity",
                "iamFleetRole",
                "instanceInterruptionBehavior",
                "instancePoolsToUseCount",
                "launchSpecifications",
                "loadBalancersConfig",
                "onDemandAllocationStrategy",
                "onDemandFulfilledCapacity",
                "onDemandMaxTotalPrice",
                "region",
                "replaceUnhealthyInstances",
                "spotMaintenanceStrategies",
                "spotMaxTotalPrice",
                "spotPrice",
                "terminateInstancesWithExpiration",
                "type",
                "validFrom",
                "validUntil",
                # modifiable options
                "excessCapacityTerminationPolicy",
                "launchTemplateConfigs",
                "onDemandTargetCapacity",
                "targetCapacity",
            ],
            handle=self.realize_create_spot_fleet,
        )
        self.handle_modify_spot_fleet = Handler(
            [
                "excessCapacityTerminationPolicy",
                "launchTemplateConfigs",
                "onDemandTargetCapacity",
                "targetCapacity",
            ],
            after=[self.handle_create_spot_fleet],
            handle=self.realize_modify_spot_fleet,
        )
        self.handle_tag_update = Handler(
            ["tags"],
            after=[self.handle_create_spot_fleet],
            handle=self.realize_update_tag,
        )

    @classmethod
    def get_type(cls):
        return "aws-spot-fleet"

    # def _exists(self):
    #    return self.state != self.MISSING

    def show_type(self):
        s = super(AwsSpotFleetState, self).show_type()
        region = self._state.get("region")
        if region is not None:
            s = "{0} [{1}]".format(s, region)
        return s

    @property
    def resource_id(self) -> Optional[str]:
        return self._state.get("spotFleetRequestId")

    def prefix_definition(self, attr):
        return {("resources", "awsSpotFleets"): attr}

    def get_physical_spec(self):
        return {
            "spotFleetRequestId": self._state.get("spotFleetRequestId"),
        }

    def get_definition_prefix(self):
        return "resources.awsSpotFleets."

    def create_after(self, resources, defn):
        return {r for r in self.resolve_resource_dependencies(defn.config)}

    def destroy_before(self, resources):
        return {
            r
            for r in resources
            if isinstance(r, Ec2LaunchTemplateState)
            or isinstance(r, VPCSubnetState)
            or isinstance(r, VPCNetworkInterfaceState)
            or isinstance(r, EC2SecurityGroupState)
        }

    # FIXME: No need to implement create, it's already taken care of by the handler
    # def create(
    #     self,
    #     defn: AwsSpotFleetDefinition,
    #     check: bool,
    #     allow_reboot: bool,
    #     allow_recreate: bool,
    # ):
    #     nixops.resources.DiffEngineResourceState.create(
    #         self, defn, check, allow_reboot, allow_recreate
    #     )
    #     self.ensure_spot_fleet_up(check)

    #     # self.access_key_id = (
    #     #     defn.config.accessKeyId or nixops_aws.ec2_utils.get_access_key_id()
    #     # )
    #     # if not self.access_key_id:
    #     #     raise Exception(
    #     #         "please set ‘accessKeyId’, $EC2_ACCESS_KEY or $AWS_ACCESS_KEY_ID"
    #     #     )

    #     # if self._exists():
    #     #     immutable_values = {
    #     #         "region": defn.config.region,
    #     #         "type": defn.config.type,
    #     #         "iamFleetRole": self._arn_from_role_name(defn.config.iamFleetRole),
    #     #     }
    #     #     immutable_diff = {
    #     #         k for k in immutable_values if getattr(self, k) != immutable_values[k]
    #     #     }  # TODO dict diff
    #     #     if immutable_diff:
    #     #         raise Exception(
    #     #             "changing keys ‘{0}’ (from ‘{1}’ to ‘{2}’) of an existing spot fleet request is not supported".format(
    #     #                 immutable_diff,
    #     #                 [getattr(self, k) for k in immutable_diff],
    #     #                 [getattr(defn.config, k) for k in immutable_diff],
    #     #             )
    #     #         )

    #     #     mutable_values = {
    #     #         # "excessCapacityTerminationPolicy",
    #     #         # "launchTemplateConfigs",
    #     #         "targetCapacity": 0,  # defn.config.targetCapacity
    #     #         # "onDemandTargetCapacity",
    #     #     }
    #     #     mutable_diff = [
    #     #         k for k in mutable_values if getattr(self, k) != mutable_values[k]
    #     #     ]  # TODO dict diff
    #     #     if mutable_diff:
    #     #         request = ModifySpotFleetRequestRequestRequestTypeDef(
    #     #             # ExcessCapacityTerminationPolicy=
    #     #             # LaunchTemplateConfigs=
    #     #             SpotFleetRequestId=self.spotFleetRequestId,
    #     #             TargetCapacity=mutable_values["targetCapacity"]
    #     #             # OnDemandTargetCapacity=
    #     #         )

    #     #         self.log(
    #     #             "modifying spot fleet request `{}`... ".format(
    #     #                 self.spotFleetRequestId
    #     #             )
    #     #         )
    #     #         self._modify_spot_fleet_request(request)

    #     #         # TODO update tags?

    #     # if self.state == self.MISSING:
    #     #     self.log(
    #     #         "creating spot fleet request with target capacity of ‘{0}’...".format(
    #     #             # self.targetCapacity
    #     #             0
    #     #         )
    #     #     )
    #     #     # The region may only be set once, when a new spot fleet is being requested
    #     #     with self.depl._db:
    #     #         self.region = defn.config.region

    #     #     self._request_spot_fleet(self._to_spot_fleet_request(defn.config))

    # def check(self):
    #     if self.spotFleetRequestId is None:
    #         self.state = self.MISSING
    #         return

    #     self._describe_spot_fleet_requests(
    #         DescribeSpotFleetRequestsRequestRequestTypeDef(
    #             # DryRun=None,
    #             # MaxResults=None,
    #             # NextToken=None,
    #             SpotFleetRequestIds=[self.spotFleetRequestId]
    #         )
    #     )

    #     # TODO handle state
    #     # self.warn()

    #     return

    def _destroy(self):
        if self.state is self.MISSING:
            return
        self.log(
            "canceling spot fleet request `{0}`".format(
                self._state["spotFleetRequestId"]
            )
        )
        try:
            self._retry(
                lambda: self._cancel_spot_fleet_requests(
                    TerminateInstances=True,
                )
            )
        except botocore.exceptions.ClientError as error:
            # TODO
            # if error.response["Error"]["Code"] == "ResourceNotFoundException":
            #     self.warn(
            #         "spotFleetRequestId `{}` was already deleted".format(
            #             self.spot_fleet_id
            #         )
            #     )
            # else:
            #     raise error
            raise error

        with self.depl._db:
            self.state = self.MISSING
            self._state["spotFleetRequestId"] = None

    def destroy(self, wipe=False):
        self._destroy()
        return True

    # def destroy(self, wipe=False):
    #     if not self._exists():
    #         return True

    #     self.log(
    #         "canceling spot fleet request with id ‘{0}’...".format(
    #             self.spotFleetRequestId
    #         )
    #     )
    #     try:
    #         self._cancel_spot_fleet_requests(
    #             CancelSpotFleetRequestsRequestRequestTypeDef(
    #                 SpotFleetRequestIds=[self.spotFleetRequestId],
    #                 TerminateInstances=True,
    #             )
    #         )
    #     except botocore.exceptions.ClientError as e:
    #         if e.response["Error"]["Code"] == "ResourceNotFoundException":
    #             self.warn(
    #                 "spot fleet request with id {0} was already deleted".format(
    #                     self.spotFleetRequestId
    #                 )
    #             )
    #         else:
    #             raise e

    #     return True

    # Synchronize state changes

    def wait_for_spot_fleet_request_available(self):
        def check_response_field(name, value, expected_value):
            if value != expected_value:
                raise Exception(
                    "Unexpected value ‘{0} = {1}’ in response, expected ‘{0} = {2}’".format(
                        name, value, expected_value
                    )
                )

        with self.depl._db:
            self.state = self.UNKNOWN
        while self.state != self.UP:
            response = self._describe_spot_fleet_requests()
            for config in response["SpotFleetRequestConfigs"]:
                check_response_field(
                    "SpotFleetRequestId",
                    config["SpotFleetRequestId"],
                    self._state["spotFleetRequestId"],
                )
                if config.get("ActivityStatus") == "error":
                    self.warn(
                        "spot fleet activity status is {}, please investigate...".format(
                            config["ActivityStatus"]
                        )
                    )
                with self.depl._db:
                    self.state = self.resource_state_from_boto(
                        config["SpotFleetRequestState"]
                    )
            if self.state not in {self.UP, self.STARTING}:
                raise Exception(
                    "spot fleet request {0} is in an unexpected state {1}".format(
                        self._state["spotFleetRequestId"],
                        config["SpotFleetRequestState"],
                    )
                )
            # if len(response["SpotFleets"]) == 1:
            #     spot_fleet = response["SpotFleets"][0]
            # else:
            #     raise Exception(
            #         "couldn't find spot fleet request `{}`, please run deploy with --check".format(
            #             spotFleetId
            #         )
            #     )
            self.log_continue(".")
            time.sleep(1)
        self.log_end("done")

        # # Save additional data from last response if necessary
        # with self.depl._db:
        #     TODO


    def ensure_spot_fleet_up(self, check):
        defn: AwsSpotFleetDefinition = self.get_defn()
        self._state["region"] = defn.config.region

        if self._state.get("spotFleetRequestId", None):
            if check:
                try:
                    self.get_client("ec2").describe_spot_fleet_requests(
                        spotFleetRequestIds=[self._state["spotFleetRequestId"]]
                    )
                except botocore.exceptions.ClientError as error:
                    errorNotFound = "InvalidSpotFleetRequestId.NotFound"  # TODO: Check
                    if error.response["Error"]["Code"] == errorNotFound:
                        # TODO: recreate?
                        self.warn(
                            "TODO: "
                            "spotFleetId `{}` was deleted from outside nixops,"
                            " recreating ...".format(self._state["spotFleetRequestId"])
                        )
                        # self.realize_create_spot_fleet(allow_recreate = True)
                        # ...
                    else:
                        raise error
            if self.state != self.UP:
                self.wait_for_spot_fleet_request_available()

    # Realize state changes

    def realize_create_spot_fleet(self, allow_recreate):
        defn: AwsSpotFleetDefinition = self.get_defn()
        if self.state == self.UP:
            if not allow_recreate:
                raise Exception(
                    "spot fleet request `{}` definition changed and it needs to be recreated"
                    " use --allow-recreate if you want to create a new one".format(
                        self._state["spotFleetRequestId"]
                    )
                )
            self.warn("spot fleet definition changed, recreating...")
            self._destroy()

        self.log("creating spot fleet request")
        response = self._request_spot_fleet()
        print("!!!RESPONSE", "request_spot_fleet", response)

        # Save essential state
        with self.depl._db:
            self.state = self.UNKNOWN
            self._state["spotFleetRequestId"] = response["SpotFleetRequestId"]

        # Save non-essential state
        with self.depl._db:
            # Unmodifiable keys
            self._state["allocationStrategy"] = defn.config.allocationStrategy
            self._state["fulfilledCapacity"] = defn.config.fulfilledCapacity
            self._state["iamFleetRole"] = json.dumps(defn.config.iamFleetRole, cls=nixops.util.NixopsEncoder)
            self._state["instanceInterruptionBehavior"] = defn.config.instanceInterruptionBehavior
            self._state["instancePoolsToUseCount"] = defn.config.instancePoolsToUseCount
            self._state["launchSpecifications"] = json.dumps(defn.config.launchSpecifications, cls=nixops.util.NixopsEncoder)
            self._state["loadBalancersConfig"] = defn.config.loadBalancersConfig
            self._state["onDemandAllocationStrategy"] = defn.config.onDemandAllocationStrategy
            self._state["onDemandFulfilledCapacity"] = defn.config.onDemandFulfilledCapacity
            self._state["onDemandMaxTotalPrice"] = defn.config.onDemandMaxTotalPrice
            self._state["region"] = defn.config.region
            self._state["replaceUnhealthyInstances"] = defn.config.replaceUnhealthyInstances
            self._state["spotMaintenanceStrategies"] = defn.config.spotMaintenanceStrategies
            self._state["spotMaxTotalPrice"] = defn.config.spotMaxTotalPrice
            self._state["spotPrice"] = defn.config.spotPrice
            self._state["terminateInstancesWithExpiration"] = defn.config.terminateInstancesWithExpiration
            self._state["type"] = defn.config.type
            # self._state["validFrom"] = defn.config.validFrom
            # self._state["validUntil"] = defn.config.validUntil
            # Modifiable keys
            self._state["excessCapacityTerminationPolicy"] = defn.config.excessCapacityTerminationPolicy
            self._state["launchTemplateConfigs"] = json.dumps(defn.config.launchTemplateConfigs, cls=nixops.util.NixopsEncoder)
            self._state["onDemandTargetCapacity"] = defn.config.onDemandTargetCapacity
            self._state["targetCapacity"] = defn.config.targetCapacity

        def tag_updater(tags):
            self.get_client("ec2").create_tags(
                Resources=[self._state["spotFleetRequestId"]],
                Tags=[{"Key": k, "Value": tags[k]} for k in tags],
            )

        self.update_tags_using(tag_updater, user_tags=defn.config.tags, check=True)

        self.wait_for_spot_fleet_request_available()

    def realize_modify_spot_fleet(self, allow_recreate):
        self.log(
            "modifying spot fleet request `{0}`".format(
                self._state["spotFleetRequestId"]
            )
        )
        self._modify_spot_fleet_request()

        self.wait_for_spot_fleet_request_available()

        # with self.depl._db:
        #     self._state["policy"] = defn.config.policy
        #     self._state["routeTableIds"] = new_rtbs

    def realize_update_tag(self, allow_recreate):
        # TODO
        # config: AwsSpotFleetDefinition = self.get_defn()
        # tags = {k: v for k, v in config.config.tags.items()}
        # tags.update(self.get_common_tags())
        # self.get_client("ec2").create_tags(
        #     Resources=[self._state["spotFleetRequestId"]],
        #     Tags=[{"Key": k, "Value": tags[k]} for k in tags],
        # )
        pass

    def resource_state_from_boto(self, state: BatchStateType) -> int:
        if state == "active":
            return self.UP
        elif state == "cancelled":
            return self.MISSING
        elif state == "cancelled_running":
            return self.MISSING
        elif state == "cancelled_terminating":
            return self.MISSING
        elif state == "failed":
            return self.MISSING
        elif state == "modifying":
            return self.STARTING
        elif state == "submitted":
            return self.STARTING
        else:
            return self.UNKNOWN

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

    # def _to_spot_fleet_request(self, config):
    #     tags = dict(config.tags)
    #     tags.update(self.get_common_tags())

    #     # # TODO instance tags
    #     # instance_tags = dict(config.tags)
    #     # instance_tags.update(self.get_common_tags())

    #     launch_template_configs = [
    #         LaunchTemplateConfigTypeDef(
    #             LaunchTemplateSpecification=FleetLaunchTemplateSpecificationTypeDef(
    #                 # LaunchTemplateId: str
    #                 LaunchTemplateName=template_config.launchTemplateSpecification.launchTemplateName,
    #                 Version=template_config.launchTemplateSpecification.version,
    #             ),
    #             Overrides=[
    #                 self._to_launch_template_overrides(overrides)
    #                 for overrides in template_config.overrides
    #             ],
    #         )
    #         for template_config in config.launchTemplateConfigs
    #     ]

    #     request = RequestSpotFleetRequestRequestTypeDef(
    #         SpotFleetRequestConfig=SpotFleetRequestConfigDataTypeDef(
    #             # AllocationStrategy=
    #             # OnDemandAllocationStrategy=
    #             # SpotMaintenanceStrategies=
    #             # ClientToken=
    #             # ExcessCapacityTerminationPolicy=
    #             # FulfilledCapacity=
    #             # OnDemandFulfilledCapacity=
    #             IamFleetRole=self._arn_from_role_name(config.iamFleetRole),
    #             # LaunchSpecifications=
    #             LaunchTemplateConfigs=launch_template_configs,
    #             TargetCapacity=1,  # TODO
    #             # OnDemandTargetCapacity=
    #             # OnDemandMaxTotalPrice=
    #             # TerminateInstancesWithExpiration=
    #             Type=config.type,
    #             # ValidFrom=
    #             # ValidUntil=
    #             # ReplaceUnhealthyInstances=
    #             # InstanceInterruptionBehavior=
    #             # LoadBalancersConfig=
    #             # InstancePoolsToUseCount=
    #             TagSpecifications=[
    #                 TagSpecificationTypeDef(
    #                     ResourceType="spot-fleet-request",
    #                     Tags=[TagTypeDef(Key=k, Value=tags[k]) for k in tags],
    #                 )
    #             ],
    #         )
    #     )
    #     if config.spotPrice:
    #         request["SpotFleetRequestConfig"]["SpotPrice"] = config.spotPrice
    #     if config.spotMaxTotalPrice:
    #         request["SpotFleetRequestConfig"][
    #             "SpotMaxTotalPrice"
    #         ] = config.spotMaxTotalPrice
    #     return request

    # def _arn_from_role_name(self, role_name):
    #     if role_name.startswith("arn:aws:iam"):
    #         return role_name

    #     role_arn = self.get_client("iam").get_role(RoleName=role_name)
    #     return role_arn["Role"]["Arn"]

    # def _save_config_data(self, config: SpotFleetRequestConfigDataTypeDef):
    #     if config.get("AllocationStrategy") is not None:
    #         self.allocationStrategy = config["AllocationStrategy"]
    #     # if config["OnDemandAllocationStrategy"] is not None:
    #     #     self.onDemandAllocationStrategy = config["OnDemandAllocationStrategy"]
    #     # if config["SpotMaintenanceStrategies"] is not None:
    #     #     self.spotMaintenanceStrategies = config["SpotMaintenanceStrategies"]
    #     # if config["ClientToken"] is not None:
    #     #     self.clientToken = config["ClientToken"]
    #     # if config["ExcessCapacityTerminationPolicy"] is not None:
    #     #     self.excessCapacityTerminationPolicy = (
    #     #         config["ExcessCapacityTerminationPolicy"]
    #     #     )
    #     # if config["FulfilledCapacity"] is not None:
    #     #     self.fulfilledCapacity = config["FulfilledCapacity"]
    #     # if config["OnDemandFulfilledCapacity"] is not None:
    #     #     self.onDemandFulfilledCapacity = config["OnDemandFulfilledCapacity"]
    #     self.iamFleetRole = config["IamFleetRole"]
    #     # if config["LaunchSpecifications"] is not None:
    #     #     self.launchSpecifications = config["LaunchSpecifications"]
    #     if config["LaunchTemplateConfigs"] is not None:
    #         self.launchTemplateConfigs = config["LaunchTemplateConfigs"]
    #     if config["SpotPrice"] is not None:
    #         self.spotPrice = config["SpotPrice"]
    #     self.targetCapacity = config["TargetCapacity"]
    #     # if config["OnDemandTargetCapacity"] is not None:
    #     #     self.onDemandTargetCapacity = config["OnDemandTargetCapacity"]
    #     # if config["OnDemandMaxTotalPrice"] is not None:
    #     #     self.onDemandMaxTotalPrice = config["OnDemandMaxTotalPrice"]
    #     if config["SpotMaxTotalPrice"] is not None:
    #         self.spotMaxTotalPrice = config["SpotMaxTotalPrice"]
    #     # if config["TerminateInstancesWithExpiration"] is not None:
    #     #     self.terminateInstancesWithExpiration = (
    #     #         config["TerminateInstancesWithExpiration"]
    #     #     )
    #     if config["Type"] is not None:
    #         self.type = config["Type"]
    #     # if config["ValidFrom"] is not None:
    #     #     self.validFrom = config["ValidFrom"]
    #     # if config["ValidUntil"] is not None:
    #     #     self.validUntil = config["ValidUntil"]
    #     # if config["ReplaceUnhealthyInstances"] is not None:
    #     #     self.replaceUnhealthyInstances = config["ReplaceUnhealthyInstances"]
    #     # if config["InstanceInterruptionBehavior"] is not None:
    #     #     self.instanceInterruptionBehavior = (
    #     #         config["InstanceInterruptionBehavior"]
    #     #     )
    #     # if config["LoadBalancersConfig"] is not None:
    #     #     self.loadBalancersConfig = config["LoadBalancersConfig"]
    #     # if config["InstancePoolsToUseCount"] is not None:
    #     #     self.instancePoolsToUseCount = config["InstancePoolsToUseCount"]
    #     # if config["TagSpecifications"] is not None:
    #     #     self.tagSpecifications = config["TagSpecifications"]

    # def _save_tags(self, tags: List[TagTypeDef]):
    #     pass

    # Boto wrappers

    def _request_spot_fleet(self, **kwargs) -> RequestSpotFleetResponseTypeDef:
        defn: AwsSpotFleetDefinition = self.get_defn()
        response = self.get_client("ec2", region=defn.config.region).request_spot_fleet(
            SpotFleetRequestConfig=unpack_create_spot_fleet_request(
                config = self.resolve_config(defn),
            ),
            **kwargs,
        )

        # if not kwargs.get("DryRun"):
        #     with self.depl._db:
        #         self.state = self.UP

        #         # Save response to deployment state
        #         self.spotFleetRequestId = response["SpotFleetRequestId"]

        #         # Save request to deployment state
        #         self._save_config_data(request["SpotFleetRequestConfig"])

        return response

    def _describe_spot_fleet_requests(
        # self, request: DescribeSpotFleetRequestsRequestRequestTypeDef
        self,
        **kwargs,
    ) -> DescribeSpotFleetRequestsResponseTypeDef:
        response = self.get_client("ec2").describe_spot_fleet_requests(
            SpotFleetRequestIds=[self._state["spotFleetRequestId"]], **kwargs
        )
        # def check_response_field(name, value, expected_value):
        #     if value != expected_value:
        #         raise Exception(
        #             "Unexpected value ‘{0} = {1}’ in response, expected ‘{0} = {2}’".format(
        #                 name, value, expected_value
        #             )
        #         )

        # try:
        #     for config in response["SpotFleetRequestConfigs"]:
        #         check_response_field(
        #             "SpotFleetRequestId",
        #             config["SpotFleetRequestId"],
        #             self.spotFleetRequestId,
        #         )

        #         # TODO:
        #         # Why is activity status not always present?
        #         # Is it due to spot fleet being canceled without any instances?
        #         if response.get("ActivityStatus") == "error":
        #             self.warn(
        #                 "spot fleet activity status is {}, please investigate...".format(
        #                     response["ActivityStatus"]
        #                 )
        #             )

        #         if not request.get("DryRun"):
        #             with self.depl._db:
        #                 # Update deployment state from response
        #                 self.state = self._to_resource_state(
        #                     config["SpotFleetRequestState"]
        #                 )
        #                 self._save_config_data(config["SpotFleetRequestConfig"])
        #                 self._save_tags(config["Tags"])

        #     return response
        # except botocore.exceptions.ClientError as e:
        #     if e.response["Error"]["Code"] == "ResourceNotFoundException":
        #         self.state = self.MISSING
        #         return None
        #     else:
        #         raise e
        return response

    def _modify_spot_fleet_request(
        # self, request: ModifySpotFleetRequestRequestRequestTypeDef
        self,
        **kwargs,
    ) -> Optional[ModifySpotFleetRequestResponseTypeDef]:
        defn: AwsSpotFleetDefinition = self.get_defn()
        response = self.get_client("ec2").modify_spot_fleet_request(
            **unpack_modify_spot_fleet_request(
                self.get_defn().config,
                SpotFleetRequestId=self._state["spotFleetRequestId"],
            ),
            **kwargs,
        )
        # try:
        #     response = self.get_client("ec2").modify_spot_fleet_request(
        #         # **dataclasses.asdict(request)
        #         **request
        #     )

        #     if response.Return:
        #         with self.depl._db:
        #             # Save request to deployment state
        #             # if request.ExcessCapacityTerminationPolicy is not None:
        #             #     self.excessCapacityTerminationPolicy = (
        #             #         request.ExcessCapacityTerminationPolicy
        #             #     )
        #             # if request.LaunchTemplateConfigs is not None:
        #             #     self.launchTemplateConfigs = request.LaunchTemplateConfigs
        #             if request["TargetCapacity"] is not None:
        #                 self.targetCapacity = request["TargetCapacity"]
        #             if request["OnDemandTargetCapacity"] is not None:
        #                 self.onDemandTargetCapacity = request["OnDemandTargetCapacity"]

        #     return response

        # except botocore.exceptions.ClientError as e:
        #     if e.response["Error"]["Code"] == "ResourceNotFoundException":
        #         with self.depl._db:
        #             self.state = self.MISSING
        #         return None
        #     else:
        #         raise e
        return response

    def _cancel_spot_fleet_requests(
        # self, request: CancelSpotFleetRequestsRequestTypeDef,
        self,
        **kwargs,
    ) -> CancelSpotFleetRequestsResponseTypeDef:
        response = self.get_client("ec2").cancel_spot_fleet_requests(
            SpotFleetRequestIds=[self._state["spotFleetRequestId"]],
            **kwargs,
        )

        # def check_response_field(name, value, expected_value):
        #     if value != expected_value:
        #         raise Exception(
        #             "Unexpected value ‘{0} = {1}’ in response, expected ‘{0} = {2}’".format(
        #                 name, value, expected_value
        #             )
        #         )

        # for item in response["SuccessfulFleetRequests"]:
        #     check_response_field(
        #         "SpotFleetRequestId",
        #         item["SpotFleetRequestId"],
        #         self.spotFleetRequestId,
        #     )
        #     self.state = self._to_resource_state(item["CurrentSpotFleetRequestState"])

        # for item in response["UnsuccessfulFleetRequests"]:
        #     check_response_field(
        #         "SpotFleetRequestId",
        #         item["SpotFleetRequestId"],
        #         self.spotFleetRequestId,
        #     )
        #     self.warn(
        #         "spot fleet request with id ‘{0}’ cancelation failed with error ‘{1}: {2}’".format(
        #             self.spotFleetRequestId,
        #             response["Error"]["Code"],
        #             response["Error"]["Message"],
        #         )
        #     )
        #     self.state = self.UNKNOWN

        return response

    def resolve_resource(
        self, ref: Optional[Unresolved], resource_type, state_type: Type[T]
    ) -> Optional[T]:
        if isinstance(ref, str) and ref.startswith("res-"):
            return self.depl.get_typed_resource(
                ref[4:].split(".")[0], resource_type, state_type
            )
        else:
            return None

    def resolve_state(
        self, ref: Optional[Unresolved], resource_type, state_type: Type, field: str
    ):
        resource = self.resolve_resource(ref, resource_type, state_type)
        if resource is not None:
            return resource._state[field]
        else:
            return None

    # def resolve_state_references(self) -> dict:
    #     def debug(x):
    #         return x

    #     defn: AwsSpotFleetDefinition = self.get_defn()
    #     return {
    #         "IamFleetRole": self.resolve_resource(
    #             defn.config.iamFleetRole, "iam-role", IAMRoleState
    #         ).arn
    #         if defn.config.iamFleetRole
    #         else None,
    #         "LaunchTemplateConfigs": [
    #             {
    #                 "LaunchTemplateSpecification": {
    #                     "LaunchTemplateId": debug(
    #                         self.resolve_resource(
    #                             c.launchTemplateSpecification.launchTemplateId,
    #                             "ec2-launch-template",
    #                             Ec2LaunchTemplateState,
    #                         ).templateId
    #                     )
    #                 }
    #                 if c.launchTemplateSpecification
    #                 else None,
    #                 "Overrides": [
    #                     {
    #                         "SubnetId": self.resolve_state(
    #                             c.subnetId,
    #                             "vpc-subnet",
    #                             VPCSubnetState,
    #                             "subnetId",
    #                         )
    #                     }
    #                     for c in c.overrides
    #                 ]
    #                 if c.overrides
    #                 else None,
    #             }
    #             for c in defn.config.launchTemplateConfigs
    #         ]
    #         if defn.config.launchTemplateConfigs
    #         else None,
    #         "LaunchSpecifications": [
    #             {
    #                 "NetworkInterfaces": [
    #                     {
    #                         "NetworkInterfaceId": self.resolve_state(
    #                             c.networkInterfaceId,
    #                             "vpc-network-interface",
    #                             VPCNetworkInterfaceState,
    #                             "networkInterfaceId",
    #                         ),
    #                         "SubnetId": self.resolve_state(
    #                             c.subnetId,
    #                             "vpc-subnet",
    #                             VPCSubnetState,
    #                             "subnetId",
    #                         ),
    #                     }
    #                     for c in c.networkInterfaces
    #                 ]
    #                 if c.networkInterfaces
    #                 else None,
    #                 "SecurityGroups": [
    #                     {
    #                         "GroupId": self.resolve_state(
    #                             c.groupId,
    #                             "ec2-security-group",
    #                             EC2SecurityGroupState,
    #                             "groupId",
    #                         )
    #                     }
    #                     for c in c.securityGroups
    #                 ]
    #                 if c.securityGroups
    #                 else None,
    #             }
    #             for c in defn.config.launchSpecifications
    #         ]
    #         if defn.config.launchSpecifications
    #         else None,
    #     }

    def resolve_resource_dependencies(
        self, config
    ) -> List[nixops.resources.ResourceState]:
        def resolve_each():
            yield self.resolve_resource(config.iamFleetRole.value, "iam-role", IAMRoleState)
            for template_config in config.launchTemplateConfigs or []:
                if template_config.launchTemplateSpecification:
                    if template_config.launchTemplateSpecification.launchTemplateId is not None:
                        yield self.resolve_resource(
                            template_config.launchTemplateSpecification.launchTemplateId.value,
                            "ec2-launch-template",
                            Ec2LaunchTemplateState,
                        )
                for override in template_config.overrides:
                    if override.subnetId is not None:
                        yield self.resolve_resource(
                            override.subnetId.value, "vpc-subnet", VPCSubnetState
                        )
            for spec in config.launchSpecifications:
                for interface in spec.networkInterfaces or []:
                    if interface.networkInterfaceId is not None:
                        yield self.resolve_resource(
                            interface.networkInterfaceId.value,
                            "vpc-network-interface",
                            VPCNetworkInterfaceState,
                        )
                    if interface.subnetId is not None:
                        yield self.resolve_resource(
                            interface.subnetId.value, "vpc-subnet", VPCSubnetState
                        )
                for group in spec.securityGroups or []:
                    if group.groupId is not None:
                        yield self.resolve_resource(
                            group.groupId.value, "ec2-security-group", EC2SecurityGroupState
                        )

        return [r for r in resolve_each() if r is not None]

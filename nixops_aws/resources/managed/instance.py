# -*- coding: utf-8 -*-

# Tracking of instances.

import boto3
import botocore
from mypy_boto3_ec2.literals import InstanceStateNameType
from nixops.deployment import Deployment
from nixops.logger import MachineLogger
import nixops.resources
from nixops.state import RecordId
import nixops_aws.ec2_utils
from typing import Literal, Dict, Any
from ..state import AwsManagedResourceState, ManagedResourceStatus
from ..definition import AwsManagedResourceDefinition
from ...boto_clients import BotoClients


class AwsEc2InstanceDefinition(AwsManagedResourceDefinition):
    """Definition of a instance."""

    # TODO
    # @classmethod
    # def get_type(cls):
    #     return "aws-ec2-instance"
    # def __init__(self, name):
    #     super().__init__(name)


# TODO: inherit from ResourceState/ImplicitResourceState/ManagedResourceState
class AwsEc2InstanceState(AwsManagedResourceState):
    """State of a instance."""

    definition_type = AwsEc2InstanceDefinition

    _clients: BotoClients

    # state = nixops.util.attr_property(
    #     "state", nixops.resources.ResourceState.MISSING, int
    # )
    # access_key_id = nixops.util.attr_property("accessKeyId", None)

    def __init__(
        self,
        depl: Deployment,
        name: str,
        id: RecordId,
        initial_state: Dict[str, Any] = {},
    ):
        super().__init__(depl, name, id)
        self._clients = BotoClients()
        for k, v in initial_state.items():
            self._state[k] = initial_state[k]

    def get_client(self, service: Literal["ec2", "iam"]):
        client = self._clients.get(service)
        if client:
            return client

        access_key_id = (
            # TODO: self.get_defn().config.accessKeyId if self.depl.definitions else None  # type: ignore
            None
        ) or nixops_aws.ec2_utils.get_access_key_id()
        # TODO
        # if access_key_id is not None:
        #     self.access_key_id = access_key_id
        # if self.access_key_id is None:
        #     raise Exception(
        #         "please set 'accessKeyId', $EC2_ACCESS_KEY or $AWS_ACCESS_KEY_ID"
        #     )
        (access_key_id, secret_access_key) = nixops_aws.ec2_utils.fetch_aws_secret_key(
            # TODO self.access_key_id
            access_key_id
        )
        # region: str = self._state["region"]
        client = boto3.session.Session().client(
            service_name=service,
            # region_name=region,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
        )
        self._clients[service] = client
        return client

    def _check(self):
        self.state = self.UNKNOWN
        response = self._describe_instances()
        if (
            len(response["Reservations"]) == 1
            and len(response["Reservations"][0]["Instances"]) == 1
        ):
            instance = response["Reservations"][0]["Instances"][0]
        else:
            assert len(response["Reservations"]) == 0 or (
                len(response["Reservations"]) == 1
                and len(response["Reservations"][0]["Instances"]) == 0
            )
            self.reset_state()
            return

        self.state = self.resource_status_from_boto(instance["State"]["Name"])
        self._state["privateIpAddress"] = instance["PrivateIpAddress"]
        self._state["publicIpAddress"] = instance["PublicIpAddress"]
        self._state["zone"] = instance["Placement"]["AvailabilityZone"]
        self._state["instanceType"] = instance["InstanceType"]

    def _destroy(self):
        if self.state not in {self.UP, self.STARTING}:
            return
        self.logger.log("deleting instance `{0}`".format(self._state["instanceId"]))
        self._terminate_instances()

        with self.depl._db:
            self.state = self.MISSING
            self._state["instanceId"] = None

    def destroy(self, wipe=False):
        self._destroy()
        return True

    def _describe_instances(self, **kwargs):
        response = self.get_client("ec2").describe_instances(
            InstanceIds=[self._state["instanceId"]],
            **kwargs,
        )

        return response

    def _terminate_instances(self, **kwargs):
        response = self.get_client("ec2").terminate_instances(
            InstanceIds=[self._state["instanceId"]],
            **kwargs,
        )

        return response

    # Synchronize state changes
    def reset_state(self):
        with self.depl._db:
            self.state = self.MISSING
            self._state["instanceId"] = None
            self._state["publicIpAddress"] = None

    def resource_status_from_boto(
        self, state: InstanceStateNameType
    ) -> ManagedResourceStatus:
        if state == "pending":
            return self.STARTING
        elif state == "running":
            return self.UP
        elif state == "shutting-down":
            return self.MISSING
        elif state == "stopped":
            return self.STOPPED
        elif state == "stopping":
            return self.STOPPING
        elif state == "terminated":
            return self.MISSING
        else:
            return self.UNKNOWN

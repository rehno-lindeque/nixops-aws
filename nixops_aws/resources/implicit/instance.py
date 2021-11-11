# -*- coding: utf-8 -*-

# Tracking of instances.

import boto3
import botocore
from nixops.deployment import Deployment
from nixops.logger import MachineLogger
import nixops.resources
from nixops.state import RecordId
import nixops_aws.ec2_utils
from typing import Literal, Dict, Any
from ..state import AwsManagedResourceState
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

    state = nixops.util.attr_property(
        "state", nixops.resources.ResourceState.MISSING, int
    )
    # access_key_id = nixops.util.attr_property("accessKeyId", None)

    def __init__(self, depl: Deployment, name: str, id: RecordId, initial_state: Dict[str, Any] = {}):
        super().__init__(depl, name, id)
        self._clients = BotoClients()
        for k, v in initial_state.items():
            self._state[k] = initial_state[k]

    def get_client(self, service: Literal["ec2", "iam"]):
        client = self._clients.get(service)
        if client:
            return client

        # new_access_key_id = (
        #     self.get_defn().config.accessKeyId if self.depl.definitions else None  # type: ignore
        # ) or nixops_aws.ec2_utils.get_access_key_id()
        # if new_access_key_id is not None:
        #     self.access_key_id = new_access_key_id
        # if self.access_key_id is None:
        #     raise Exception(
        #         "please set 'accessKeyId', $EC2_ACCESS_KEY or $AWS_ACCESS_KEY_ID"
        #     )
        (access_key_id, secret_access_key) = nixops_aws.ec2_utils.fetch_aws_secret_key(
            # self.access_key_id
            ""
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
        response = self._describe_instances()
        print("!!!!!!!", "DESCRIBE INSTANCES", response)

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

        #         )
        #     )

        # return self._cached_instance

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

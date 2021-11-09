# -*- coding: utf-8 -*-

from typing import TypedDict
import mypy_boto3_ec2
import mypy_boto3_iam


class BotoClients(TypedDict, total=False):
    ec2: mypy_boto3_ec2.EC2Client
    iam: mypy_boto3_iam.IAMClient

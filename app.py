#!/usr/bin/env python3
import os

import aws_cdk as cdk

from etl.etl_stack import EtlStack
from aws_cdk import App

app = App()
EtlStack(app, "EtlStack",)

app.synth()

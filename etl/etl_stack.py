from aws_cdk import (
    Duration,
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_events as events,
    aws_events_targets as targets
)
from constructs import Construct
from step_function.step_function import ValidateTransformUserStepFunction

class EtlStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3 buckets
        raw_data_bucket = s3.Bucket(self, "RawDataBucket")
        user_valid_bucket = s3.Bucket(self, "UserValidBucket")
        user_final_bucket = s3.Bucket(self, "UserFinalS3")

        # IAM Role for Step Functions
        role = iam.Role(self, "StepFunctionsRole",
                        assumed_by=iam.ServicePrincipal("states.amazonaws.com"),
                        managed_policies=[
                            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaRole"),
                            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
                        ])
                        

        # Lambda function for validate_user_data
        validate_user_lambda = _lambda.Function(self, "ValidateUserData",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="validate_user_profile.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                'USER_VALID_BUCKET': user_valid_bucket.bucket_name
            }
            role=lambda_role
        )

        # Lambda function for validate_user_data
        transform_user_lambda = _lambda.Function(self, "TransforUserData",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="transfer_user_profile.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                'USER_FINAL_BUCKET': user_final_bucket.bucket_name
            }
            role=lambda_role
        )

        # Step Function Construct
        step_function = ValidateTransformUserStepFunction(self, "ValidateTransformUserStepFunction",
                                                          validate_user_lambda=validate_user_lambda,
                                                          transform_user_lambda=transform_user_lambda,
                                                          raw_data_bucket=raw_data_bucket,
                                                          user_valid_bucket=user_valid_bucket,
                                                          final_data_bucket=user_final_bucket)

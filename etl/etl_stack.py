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


class EtlStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3 buckets
        raw_data_bucket = s3.Bucket(self, "RawDataBucket")
        user_valid_bucket = s3.Bucket(self, "UserValidBucket")

        # Lambda function for validation
        validate_lambda = _lambda.Function(self, "ValidateDataFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="validate_data.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                'USER_VALID_BUCKET': user_valid_bucket.bucket_name
            }
            # TODO: Write a trigger here
        )

        # Permissions for Lambda
        user_valid_bucket.grant_read_write(validate_lambda)
        raw_data_bucket.grant_read(validate_lambda)

        # # Step Function Tasks
        # validate_task = tasks.LambdaInvoke(self, "Validate Data",
        #     lambda_function=validate_lambda,
        #     output_path="$.Payload"
        # )

        # # Step Function Definition
        # definition = validate_task

        # # Step Function
        # etl_state_machine = sfn.StateMachine(self, "ETLStateMachine",
        #     definition=definition,
        #     timeout=Duration.minutes(5)
        # )

        # # Grant permissions to the Step Function to invoke Lambda
        # validate_lambda.grant_invoke(etl_state_machine.role)

        # # Create EventBridge rule to trigger the Step Function
        # rule = events.Rule(self, "Rule",
        #     event_pattern={
        #         "source": ["aws.s3"],
        #         "detail_type": ["Object Created"],
        #         "detail": {
        #             "bucket": {
        #                 "name": [raw_data_bucket.bucket_name]
        #             },
        #             "object": {
        #                 "key": [{"prefix": ""}]  # Match all objects
        #             }
        #         }
        #     }
        # )
        # rule.add_target(targets.SfnStateMachine(etl_state_machine))

        # # Add policy to allow EventBridge to start the Step Function
        # etl_state_machine.add_to_role_policy(iam.PolicyStatement(
        #     actions=["states:StartExecution"],
        #     resources=[etl_state_machine.state_machine_arn]
        # ))
from aws_cdk import (
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
)
from constructs import Construct


class ValidateTransformUserStepFunction(Construct):

    def __init__(self, scope: Construct, id: str, validate_user_lambda: _lambda.Function, transform_user_lambda: _lambda.Function, raw_data_bucket: s3.Bucket, user_valid_bucket:s3.Bucket, final_data_bucket: s3.Bucket, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Step Functions Tasks
        get_s3_object = sfn.Pass(self, "GetS3Object",
                                 result=sfn.Result.from_object({
                                     "Bucket": raw_data_bucket.bucket_name,
                                     "Key": "path/to/your/data.json"
                                 }),
                                 result_path="$.S3Data")

        invoke_validate_user_lambda = tasks.LambdaInvoke(self, "InvokeValidateUserLambda",
                                                         lambda_function=validate_user_lambda,
                                                         input_path="$.S3Data",
                                                         result_path="$.ValidateUserResult",
                                                         output_path="$.ValidateUserResult.Payload")

        check_validation_result = sfn.Choice(self, "CheckValidationResult")
        
        invoke_transform_user_lambda = tasks.LambdaInvoke(self, "InvokeTransformUserLambda",
                                                          lambda_function=transform_user_lambda,
                                                          input_path="$",
                                                          result_path="$.TransformUserResult",
                                                          output_path="$.TransformUserResult.Payload")

        validation_failed = sfn.Fail(self, "ValidationFailed",
                                     error="ValidationFailed",
                                     cause="User validation failed.")

        # State Machine Definition
        definition = get_s3_object.next(invoke_validate_user_lambda).next(
            check_validation_result
            .when(sfn.Condition.number_equals("$.statusCode", 200), invoke_transform_user_lambda)
            .otherwise(validation_failed)
        )

        # State Machine
        self.state_machine = sfn.StateMachine(self, "ValidateTransformUserStateMachine",
                                              definition=definition)

    def get_state_machine(self):
        return self.state_machine

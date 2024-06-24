from aws_cdk import (
    aws_lambda as _lambda,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    
)

from constructs import Construct

class StepFunction(Construct):

    def __init__(self, scope: Construct, id: str, validate_user_profile_lambda: _lambda.Function, transfer_user_profile_lambda: _lambda.Function, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        validate_user_profile_task = tasks.LambdaInvoke(self, "Validate User Profile",
            lambda_function=validate_user_profile_lambda,
            output_path="$.Payload"
        )

        transfer_user_profile_task = tasks.LambdaInvoke(self, "Transfer User Profile",
            lambda_function=transfer_user_profile_lambda,
            output_path="$.Payload"
        )

        definition = validate_user_profile_task.next(transfer_user_profile_task)

        self.state_machine = sfn.StateMachine(self, "StateMachine",
            definition=definition,
            timeout=Construct.Duration.minutes(5)
        )

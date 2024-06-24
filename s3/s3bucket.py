from aws_cdk import (
    aws_s3 as s3,
    
)

from constructs import Construct

class S3Bucket(Construct):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.bucket = s3.Bucket(self, "CommonBucket",
            versioned=kwargs["versioned"], #parameter and defaulf value
            removal_policy=Construct.RemovalPolicy.DESTROY,
            auto_delete_objects=kwargs["auto_delete_objects"]
        )

#bucket name ID as a parameter
# all should default parameter

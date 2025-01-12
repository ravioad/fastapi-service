from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_ecs_patterns as patterns,
    # Dration,
    # aws_sqs as sqs,
)
from constructs import Construct


class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC
        vpc = ec2.Vpc(self, "FastAPIVPC", max_azs=2)

        # Create an ECS cluster
        cluster = ecs.Cluster(self, "FastAPICluster", vpc=vpc)

        # Replace the repository name with your ECR repository
        repository = ecr.Repository.from_repository_name(
            self, "FastAPIRepository", "fastapi-service"
        )

        # Use the ECR image in your Fargate service
        fargate_service = patterns.ApplicationLoadBalancedFargateService(
            self,
            "FastAPIService",
            cluster=cluster,
            task_image_options={
                "image": ecs.ContainerImage.from_ecr_repository(repository, "latest"),
                "container_port": 8000,  # The port your FastAPI app listens on
            },
            memory_limit_mib=256,
            cpu=256,
            runtime_platform=ecs.RuntimePlatform(
                operating_system_family=ecs.OperatingSystemFamily.LINUX,
                cpu_architecture=ecs.CpuArchitecture.X86_64,  # `amd64` maps to `X86_64`
            ),
        )
        # Configure health check for the ALB
        fargate_service.target_group.configure_health_check(path="/docs")

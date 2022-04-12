from fargate_ssh import FargateSsh
import os
import sys

cluster = sys.argv[1]
app_name = sys.argv[2]

def ssh():
    fg = FargateSsh(
        cluster,
        app_name,
    )
    sa = fg.get_service_arn()
    service = fg.get_service(sa)
    task_definition_arn = fg.get_task_definition_arn(service)
    task_definition = fg.describe_task_definition(task_definition_arn)
    container_name = fg.get_container_name(task_definition)
    task = fg.get_task_id(service)
    command = fg.ecs_execute_command(task, container_name)
    os.system(command)

ssh()


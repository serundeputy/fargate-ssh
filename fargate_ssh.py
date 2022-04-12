from http import client
import boto3

"""
" I know the AWS ecs cluster.
" I can go to the AWS console, ecs, click on the cluster, find the service
" click on the Service Name, then click the tasks tab to see the active task.
" Then I can click on the task and see the taskId.
"
" From this info I can 'ssh' into the fargate container via:
" aws ecs exectute-task --cluster <cluster> --task <taskId> --container <containerName> --interactive --command "bash"
"""


class FargateSsh:
    def __init__(self, cluster, app_name):
        self.cluster = cluster
        self.app_name = app_name
        self.client = boto3.client('ecs')


    def get_service_arn(self):
        service_arn = ''
        lsRes = self.client.list_services(
            cluster=self.cluster,
            launchType='FARGATE',
            maxResults=100,
        )

        # Get the serviceArn that contains app_name
        for service in lsRes['serviceArns']:
            if self.app_name in service:
                service_arn = service
        
        return service_arn


    def get_service(self, service_arn):
        services = self.client.describe_services(
            cluster=self.cluster,
            services=[
                service_arn,
            ],
        )

        return services['services'][0]


    def get_task_definition_arn(self, service):
        task_definition = service['taskDefinition']

        return task_definition


    def describe_task_definition(self, task_definition):
        task_definition_res = self.client.describe_task_definition(
            taskDefinition=task_definition,
        )

        return task_definition_res['taskDefinition']


    def get_container_name(self, task_definition):
        container_name = ''
        for container in task_definition['containerDefinitions']:
            if 'name' in container:
                if '-app' in container['name']:
                    container_name = container['name']
                elif 'newrelic' not in container['name'] and 'redis' not in container['name']:
                    container_name = container['name']

        return container_name


    def get_task_id(self, service):
        tasks = self.client.list_tasks(
            cluster=self.cluster,
            serviceName=service['serviceName'],
        )

        return tasks['taskArns'][0].split('/')[2]


    def ecs_execute_command(self, task_id, container_name):
        command = 'aws ecs execute-command --cluster {} --task {} --container {} --interactive --command "bash"'.format(
            self.cluster,
            task_id,
            container_name,
        )

        return command



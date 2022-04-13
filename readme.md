# Fargate SSH

SSH into AWS fargate containers.

## Prerequisites

* aws cli
* samlutil
* AWS account and permissions to the resources

## Usage

Clone the repo to your local machine. Then you can either run it via python or make an alias in your .bashrc or .zshrc file.

via python:
```bash
python /path/to/app.py <cluster> <app_name>
```

via alias:
```bash
gfssh <cluster> <app_name>
```
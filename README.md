# Context Group for AWS CDK Python

## Introduction

**Background:** The AWS CDK provides the context to cache useful information about your CDK app and its resources. The context can also be used to store custom values for use throughout your stacks.

**What this solves:** `ContextGroup` is a simple Python class that establishes a convention for working with context values as a hierarchy organized using a naming scheme -- for example by environment name. This can be one way of using per environment configuration in your project.

This was designed in connection with client projects where we are using the CDK and Python to build out AWS deployments. Even though the context is relatively simple to work with, packaging the extra handling into a Python module ensures the same behavior can be consistently applied across many CDK projects.

_Collaborators:_ Mike Rose (@mike-cumulus)

## How to use

1. Add the module to your project with one of the following methods: 
   * **curl:** `curl -O https://raw.githubusercontent.com/cloudmation-llc/cdk-context-group/master/ContextGroup.py`
   * **wget:** `wget https://raw.githubusercontent.com/cloudmation-llc/cdk-context-group/master/ContextGroup.py`

2. Add a `contextGroup` key to `cdk.json`, set up a default group name _(optional)_, and add named groups.
 
The default group name is used if you do not specify a group name when running CDK commands.

Example:

```json
{
  "context": {
    "@aws-cdk/core:enableStackNameDuplicates": "true",
    "aws-cdk:enableDiffNoFail": "true",
    "@aws-cdk/core:stackRelativeExports": "true",
    "contextGroups": {
      "default": "dev",
      "dev": {
        "account_id": "****",
        "em_instance_type": "t3.large",
        "vpc_id": "vpc-*****************"
      },
      "prod": {
        "account_id": "****",
        "em_instance_type": "r5.large",
        "vpc_id": "vpc-*****************"        
      } 
    }
  }
}
```

3. Import and use the module in your CDK project.

For example, in `app.py` you can do the following:

```python
from ContextGroup import *

# Define new CDK application
app = core.App()

# Load the context group
context_group = ContextGroup(app)

# Context variables within group name as loaded as attribute onto ContextGroup object
print(context_group.account_id)
print(context_group.vpc_id)

# Pass the group to print() or other string functions to see all of the group variables
print(context_group)

# Pass the entire object around your CDK application
MyStack(app, 'my-stack', context_group=context_group)
```

4. When running CDK commands, pass the command line flag `-c ctxgroup=group_name_here` to activate a specific context group. If you do not specify one, then the default configured in `cdk.json` is used as the fallback.

    If you did not provide a default name, and did not specify one on the command line, then an error condition is raised.
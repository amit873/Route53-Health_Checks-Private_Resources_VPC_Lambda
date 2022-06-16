## Performing Route 53 health checks on private resources in a VPC with AWS Lambda and Amazon CloudWatch
https://aws.amazon.com/blogs/networking-and-content-delivery/performing-route-53-health-checks-on-private-resources-in-a-vpc-with-aws-lambda-and-amazon-cloudwatch/

## Create Lambda Policy
Name - nv-lambda-policy
Use policy.json

## Create Lambda Role
Name - nv-lambda-role
Policy - nv-lambda-policy

## Security Group for Lambda
Security group name - nv-lambda-sg
VPC - nv-vpc

## Lambda Function 
Function Name - nv-lambda-function
Runtime - python 3.6
Execution Role - nv-lambda-role
# Enable VPC -
VPC - nv-vpc
Subnets - nv-private-subnet
Security groups - nv-lambda-sg

# Lambda Environment Variable
cfResourceIPaddress = nv-LB-1190207452.us-east-1.elb.amazonaws.com
cfpath = 
cfport = 80
cfprotocol = HTTP
cfstackname = amit-project

# Lambda Function will create Metrics
# Create Alarm using above metrics
Name - nv-alarm

# Create Route 53 Health Check
Name - nv-health-check
What to monitor - State of CloudWatch alarm
CloudWatch region - us-east-1
CloudWatch alarm  - nv-alarm

## Event Bridge
Create Event Bridge - New Rule
Name - nv-eventbridge
Rule type - Schedule
A schedule that runs at a regular rate, such as every 10 minutes - 2 minutes
Select a target - Lambda Function
Function Name - nv-lambda-role
Create Rule
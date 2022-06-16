import requests
import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

def lambda_handler(event, context):
    cloudwatch = boto3.client('cloudwatch')
    lambdah = boto3.client('lambda')
    protocol = os.environ['cfprotocol']
    healthcheckname = os.environ['cfstackname']
    domainname = os.environ['cfResourceIPaddress']
    port = os.environ['cfport']
    path = os.environ['cfpath']
    url = str("http://" + domainname + ":"+ port + "/" + path)
    
    try:
        internettest = requests.get("http://amazon.com", timeout=2)
    
    except requests.exceptions.ConnectionError as e:
        if "timed out" in str(e):
            print ("The Lambda function does not have internet access because it is not in a private subnet with internet access provided by a NAT Gateway or NAT instance. The HTTP GET request might be successful but Lambda will not be able to push metrics to Cloudwatch and the Route 53 health check will always be unhealthy.")
    
    try:
        r = requests.get(url, timeout=2)
        if r.status_code >= 200 and r.status_code <= 399:
            metric = 1
            print ("The HTTP GET Request to " + domainname +  " was successful.")
            print ("The HTTP response code is " + str(r.status_code))
            response = cloudwatch.put_metric_data(Namespace = 'Route53PrivateHealthCheck', MetricData = [{'MetricName': 'HTTP: ' + healthcheckname + ' (Health Check for resource ' + domainname + ')', 'Dimensions': [{'Name': 'HTTP Health Check','Value': 'HTTP Health Check'}], 'Unit': 'None','Value': metric},])
           
            
        else:
            metric = 0
            print ("The HTTP GET Request to " + domainname +  " was not successful because it received a HTTP Client Side or Server Side Error Code.")
            print ("The HTTP response code is " + str(r.status_code))
            response = cloudwatch.put_metric_data(Namespace = 'Route53PrivateHealthCheck', MetricData = [{'MetricName': 'HTTP: ' + healthcheckname + ' (Health Check for resource ' + domainname + ')', 'Dimensions': [{'Name': 'HTTP Health Check','Value': 'HTTP Health Check'}], 'Unit': 'None','Value': metric},])
    
    except requests.exceptions.ConnectionError as e:
        metric = 0
        response = cloudwatch.put_metric_data(Namespace = 'Route53PrivateHealthCheck', MetricData = [{'MetricName': 'HTTP: ' + healthcheckname + ' (Health Check for resource ' + domainname + ')', 'Dimensions': [{'Name': 'HTTP Health Check','Value': 'HTTP Health Check'}], 'Unit': 'None','Value': metric},])
        
        
        if "Name or service not known" in str(e):
            print ("The domain name " + domainname + " does not resolve to an IP address. Kindly ensure the domain name resolves in the VPC.")
        elif "refused" in str(e):
            print ("The HTTP connection was refused by the endpoint. Please check if the endpoint is listening for HTTP connections on the correct port.")
        elif "timed out" in str(e):
            print ("The HTTP connection timed out because a HTTP response was not received within the 2 seconds timeout period.")
        else:
            logger.error("Error: " + str(e))
            
    except:
        metric = 0
        response = cloudwatch.put_metric_data(Namespace = 'Route53PrivateHealthCheck', MetricData = [{'MetricName': 'HTTP: ' + healthcheckname + ' (Health Check for resource ' + domainname + ')', 'Dimensions': [{'Name': 'HTTP Health Check','Value': 'HTTP Health Check'}], 'Unit': 'None','Value': metric},])
        logger.error("An error occurred while performing the health check.")
        
    
   
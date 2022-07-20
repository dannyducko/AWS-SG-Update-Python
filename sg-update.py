from urllib import response
import requests
import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')
my_ip = ""

def myip():
    global my_ip
    ## call the api on my-ip.io
    url = "https://api.my-ip.io/ip"
    ip_response = requests.request("GET", url)
    my_ip = (ip_response.text + "/32")

def des_sg(ip):
    ## Replace the sgr with the security group rule containing your IP you SSH from.
    sg_rules_list = [{'SecurityGroupRuleId': 'sgr-123456789abcd',
                  'SecurityGroupRule': {
                      'IpProtocol': 'tcp',
                      'FromPort': 22,
                      'ToPort': 22,
                      'CidrIpv4': f'{ip}',
                      'Description': 'Added SSH port via script'
                  }
                  }
                 ]
    try:
        ## replace the below with the security group ID that contains the SG Rule
        response = ec2.modify_security_group_rules(GroupId='sg-123456789abcd', SecurityGroupRules=sg_rules_list)
        print(f"Response code = {response['ResponseMetadata']['HTTPStatusCode']}")
    except ClientError as e:
        print(e)

def run_sg_replace():
    myip()
    sg_question = input(f"Would you like to replace your SG Rule to {my_ip}? (y or n)\n... ")
    if sg_question == "y" or "Y":
        des_sg(my_ip)
        #print("Successfully added")
    else:
        print("Closing...")
        exit()

run_sg_replace()
exit()

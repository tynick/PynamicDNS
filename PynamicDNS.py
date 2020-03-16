import requests
import boto3
import sys
# the purpose of this script is to change an AWS DNS record to match your current public ip

# script should be run like this...
# python3 pynamic_dns.py <DNS_RECORD> <HOSTED_ZONE_ID>
# python3 pynamic_dns.py pynamicdns.tynick.com X0XXXXXX000X0

try:
    # make sure it exists already or it will make it and the script will fail on first run.
    # example... home.example.com
    DNS_RECORD = sys.argv[1]
    # aws hosted zone id for your domain
    ZONE_ID = sys.argv[2]
except:
    print('FAILED - check that you are launching the script with the proper arguments')

try:
    client = boto3.client('route53')
except:
    print('FAILED - Check that boto3 is installed and that you populated your ~/.aws/ credentials and config files')
    sys.exit()

# get your public ip
def get_public_ip():
    public_ip = requests.get('https://api.ipify.org').text
    return public_ip

# get the value of your DNS record from Route53
def get_record_value():
    # attempt to get value of DNS record
    try:
        response = client.test_dns_answer(
            HostedZoneId=ZONE_ID,
            RecordName=DNS_RECORD,
            RecordType='A',
        )
    except:
        response = 'FAILED'

    try:
        # make sure we got a 200 from aws
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            # parse out the value and assume there is only 1 value in the list
            response = response['RecordData'][0]
        else:
            response = 'FAILED'
    except:
        # this means response['ResponseMetadata']['HTTPStatusCode'] didnt exist
        response = 'FAILED - Check ZONE_ID and DNS_RECORD in AWS'
    return response

def change_record_value(public_ip):
    # attempt to change the value of the Route53 DNS record
    try:
        response = client.change_resource_record_sets(
            HostedZoneId=ZONE_ID,
            ChangeBatch={
                'Comment': 'PynamicDNS Change',
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': DNS_RECORD,
                        'Type': 'A',
                        'TTL': 300,
                        'ResourceRecords': [
                                {
                                    'Value': public_ip
                                },
                            ],
                        }
                    },
                ]
            }
        )
    except:
        response = 'FAILED'

    # make sure we got a 200 from aws
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        response = 'DNS CHANGE SUCCESSFUL'
    else:
        # something went wrong and response['ResponseMetadata']['HTTPStatusCode'] didnt exist. 
        response = 'FAILED'

    return response

public_ip = get_public_ip()
record_value = get_record_value()
# this just formats some output and assumes DNS_RECORD+2 is more chars than 'Public IP: '
padding = len(DNS_RECORD) + 2 - len('Public IP: ')
print('---------------------------')
print('Public IP: {0}{1}'.format(padding * ' ', public_ip))
print('{0}: {1}'.format(DNS_RECORD, record_value))
print('---------------------------')

# if IP changed, change the Route53 record
# if not, do nothing
if public_ip != record_value:
    print("DNS VALUE DOES NOT MATCH PUBLIC IP")
    # change record value to current public_ip
    print(change_record_value(public_ip))
else:
    print("NO CHANGE NEEDED")

import boto3
import sys, traceback
from datetime import datetime
from time import sleep

def stop_ec2_instances():
    start_time = datetime.now()

    # starting ec2 client
    ec2_client = boto3.client('ec2')

    regions = ec2_client.describe_regions()

    for region in regions['Regions']:
        try:
            print("Region: " + str(region['RegionName']))
            ec2_client = boto3.client('ec2', region_name=region['RegionName'])
            instances = ec2_client.describe_instances()
            instanceIds = list()
            
            for reservation in instances['Reservations']:
                for instance in reservation['Instances']:
                    if instance['State']['Name'] == "running" and not instance['Tags'] is None : 
                        for tag in instance['Tags']:
                            try:
                                if tag['Key'] == 'ScheduledStartStop' and tag['Value'] == 'True'    :
                                    instanceIds.append(instance['InstanceId'])
                            except:
                                print "Not expected error: ", traceback.print_exc()
                      
            if len(instanceIds) > 0 : 
                print "Stopping instances: " + str(instanceIds)
                ec2_client.stop_instances(InstanceIds=instanceIds, Force=False)                                                   
                                                            
        except:
            print "Not expected error:", traceback.print_exc()
                                                           
    end_time = datetime.now()
    took_time = end_time - start_time
    print "Total time of execution: " + str(took_time)    

def lambda_handler(event, context):
    print('Stopping instances... ')
    stop_ec2_instances()

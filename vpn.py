import boto3
import json
import sys

class VPN:
	def __init__(self):
		self.get_config()

		self.client = boto3.client(
				'ec2',
				region_name = self.config['AWS_DEFAULT_REGION'],
				aws_access_key_id = self.config['AWS_ACCESS_KEY_ID'],
				aws_secret_access_key = self.config['AWS_SECRET_ACCESS_KEY']
			)
		
	def get_config(self):
		try:
			configFile = open('config.json') 
			self.config = json.load(configFile) 
		except: 
			print("Error, no config file found")
			sys.exit()


	def stop(self):
		response = self.client.stop_instances(InstanceIds=[self.config['VPN_INSTANCE_ID']], Hibernate=False, DryRun=False, Force=False)

	def start(self):
		response = self.client.start_instances(InstanceIds=[self.config['VPN_INSTANCE_ID']], DryRun=False)

	def state(self):
		myec2 = self.client.describe_instances(InstanceIds=[self.config['VPN_INSTANCE_ID']])
		for reservation in myec2['Reservations']:
			for instance in reservation['Instances']:
					if instance['InstanceId'] == self.config['VPN_INSTANCE_ID']:
						return instance['State']['Name']
		return False

	def isStateTransition(self):
		return self.state() in ['pending', 'shutting-down', 'rebooting', 'stopping']

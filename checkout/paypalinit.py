import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment

class PayPalClient:
	def __init__(self):
		self.client_id = "Ad578eVwBNx76nWxGcIqY9qW4UKe2o69F5GsCuR099rA9oCtY59C6Rl8Hg2A_Ft6wQpZE4cf4mjN7Pye"
		self.client_secret = "EHwDvmu-V0NQd8EcoRZ1w_Ky_bdEhCyxGPQ-b6P90r4KVvXhU3VFljQ2Dhk4Xcg683ODf9LTRSVaUURF"
		self.environment = SandboxEnvironment(client_id = self.client_id, client_secret = self.client_secret)
		self.client = PayPalHttpClient(self.environment)
import boto3
import accesoAWS
import time

class Manager:
  def __init__(self) -> None:
    self.pool = []
    self.ec2 = boto3.resource('ec2', 
                              aws_access_key_id =  accesoAWS.aws_access_key_id,
                              aws_secret_access_key = accesoAWS.aws_secret_access_key, 
                              aws_session_token = accesoAWS.aws_session_token, 
                              region_name = 'us-east-1')

  def crearInstanciaEC2(self, amiImage):
    instancia = self.ec2.create_instances(
      ImageId = amiImage, 
      MinCount = 1, 
      MaxCount = 1,
      InstanceType = 't2.micro', 
      KeyName = "vockey",
      )
    time.sleep(3)
    instancia[0].reload()
    self.pool.append((instancia[0].id, instancia[0].public_ip_address))
    return instancia
  
  def eliminarInstanciaEC2(self, instanceId):
    instancia = self.ec2.Instance(instanceId)
    instancia.terminate()
    return instancia

  def verPool(self):
    print(self.pool)
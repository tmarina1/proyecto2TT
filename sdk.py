import boto3
from datetime import datetime
from Monitor.clases_ec2 import Manager

def conexionEC2():
  global ec2
  #ec2 = boto3.resource('ec2')

  session = boto3.Session(
    aws_access_key_id='YOUR_ACCESS_KEY_ID',
    aws_secret_access_key='YOUR_SECRET_ACCESS_KEY'
  ) 
  ec2 = session.client('ec2')

def crearInstancia(amiImage):
  try:
    ec2.create_instances(
      ImageId = amiImage, 
      InstanceType = 't2.micro', 
      MinCount = 1, 
      MaxCount = 1,
      KeyName = "vockey",
      )
    return 'Creada correctamente'
  except:
    return 'No se puso crear'

def eliminarInstancia(instanceId):
  instancia = ec2.instances.filter(InstanceIds = instanceId).terminate()
  return instancia

if __name__=='__main__':
  manager = Manager(1, 1)
  #manager.crearInstanciaEC2('ami-0b6c5e19de6b71814')
  #manager.verPool()
  print(manager.eliminarInstanciaEC2('i-095e58de4d8482fcb'))

'''
def verificarEstado(instanceId):
  instance = ec2.Instance(instanceId)
  return instance.instance.state["Name"]

def verificarUso(instanceId):
  client = boto3.client('cloudwatch')
  response = client.get_metric_statistics(
    Namespace='AWS/EC2',
    MetricName='CPUUtilization',
    Dimensions=[
        {
            'Name': 'InstanceId',
            'Value': instanceId
        },
    ],
    StartTime=datetime(2023, 4, 6),
    EndTime=datetime(2023, 4, 7),
    Period = 60,
    Statistics = [
        'Average',
    ],
    Unit = 'Percent'
  )

  return response['MetricDataResults'][0]['Values'][0]

'''
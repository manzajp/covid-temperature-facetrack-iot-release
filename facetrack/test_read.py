import time
from smbus2 import SMBus
from mlx90614 import MLX90614

temp = []
for y in range(5):
  sensor = MLX90614(SMBus(1), address=0x5A)
  print (time.asctime())
  temp.append(round(sensor.get_object_1(),2))
  #print ("Ambient Temperature : ", sensor.get_ambient())
  print ("Object Temperature : ", round(sensor.get_object_1(),2))
  if len(temp) == 5:
    average = 0.0
    for x in temp:
      average += float(x)
    print ("Average Temperature: ", round((average/5),2))
  SMBus(1).close()
  time.sleep(1)


import time
from machine import I2C

#i2c obj
i2c=I2C(1,13,12)

#shtc3 init addr-0x70
def shtc3_init():	
  buf0=bytearray([0x35,0x17])
  i2c.writeto(0x70,buf0)
  time.sleep_ms(500)
  buf=bytearray([0xEF,0xC8])
  i2c.writeto(0x70,buf)
  i2c.readfrom_into(0x70,buf)
  num=int.from_bytes(buf,'big')
  print('I2C device shtc3 init and id is %d'%num)

def get_temperature_humidity(echo=False, ret=True):
  buf=bytearray([0x7C, 0xA2])
  i2c.writeto(0x70, buf)
  buf2=bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
  i2c.readfrom_into(0x70, buf2)
  temp = (buf2[1] | (buf2[0] << 8)) * 175 / 65536.0 - 45.0
  humi = (buf2[4] | (buf2[3] << 8)) * 100 / 65536.0
  echo_Arg='shtc3: Temperature='+str(temp)+', Humidity='+str(humi)
  ret_Arg={}
  ret_Arg['temp']=temp
  ret_Arg['humi']=humi
  return _answer(echo, ret, echo_Arg, ret_Arg)
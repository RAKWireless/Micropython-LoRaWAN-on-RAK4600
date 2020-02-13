
import time
from machine import I2C

#i2c obj
i2c=I2C(1,13,12)

#lis3dh init addr-0x19
def lis3dh_init():	
  buf=bytearray([0x57])
  i2c.writeto_mem(0x19,0x20,buf)
  buf=bytearray([0x08])
  i2c.writeto_mem(0x19,0x23,buf)
  lis3dh_id=i2c.readfrom_mem(0x19,0x0F,1)
  lis3dh_id=''.join(['%02X' %x  for x in lis3dh_id])
  print('I2C device lis3dh init and id is 0x',lis3dh_id)

def get_acceleration(echo=False, ret=True):
  x_l=i2c.readfrom_mem(0x19, 0x28, 1)
  x_h=i2c.readfrom_mem(0x19, 0x29, 1)
  y_l=i2c.readfrom_mem(0x19, 0x2a, 1)
  y_h=i2c.readfrom_mem(0x19, 0x2b, 1)
  z_l=i2c.readfrom_mem(0x19, 0x2c, 1)
  z_h=i2c.readfrom_mem(0x19, 0x2d, 1)
  x= (x_h[0]<<8) | x_l[0]
  y= (y_h[0]<<8) | y_l[0]
  z= (z_h[0]<<8) | z_l[0]
  if x < 0x8000:
    x=x
  else:
    x=x-0x10000
  if y < 0x8000:
    y=y
  else:
    y=y-0x10000
  if z < 0x8000:
    z=z
  else:
    z=z-0x10000
  acc_x=(x*4000)/65536.0
  acc_y=(y*4000)/65536.0
  acc_z=(z*4000)/65536.0
  echo_Arg='lis3dh: acc_x='+str(acc_x)+', acc_y='+str(acc_y)+', acc_z='+str(acc_z)
  ret_Arg={}
  ret_Arg['x']=acc_x
  ret_Arg['y']=acc_y
  ret_Arg['z']=acc_z
  return _answer(echo, ret, echo_Arg, ret_Arg)
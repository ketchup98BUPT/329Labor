import pyvisa
import time

rm = pyvisa.ResourceManager()
resource_list=rm.list_resources()
print(resource_list)
tunable_laser=rm.open_resource('GPIB0::1::INSTR')
MPM_210=rm.open_resource('GPIB0::16::INSTR')

# print(MPM_210.query('TRIG?'))  # check connect

tunable_laser.write(':SYST:COMM:COD 1')
tunable_laser.write(':POW:ATT:AUT 1')
tunable_laser.write(':POW 10dBm')
tunable_laser.write(':POW:STAT 1')
tunable_laser.write(':WAV 1550nm')

# # test section
# # the MPM sometime get error and give wrong result, just restart it !
# MPM_210.write('WMOD CONST2')
# MPM_210.write('WAV','1550')
# time.sleep(1)
# MPM_210.write('MEAS')
# print(MPM_210.query('READ? 0'))
# print(MPM_210.query('READ? 1'))


# logging section

avg_time = 0.05
logging_point = 400  # < 100,0000
MPM_210.write('ZERO')
MPM_210.write('AVG 0.05')
MPM_210.write('LOGN 40')
MPM_210.write('WAV 1550.0')
MPM_210.write('TRIG 1')
MPM_210.write('WMOD FREERUN')
MPM_210.write('LEV 1')
MPM_210.write('MEAS')
MPM_210.write('STOP')
# logging = MPM_210.query_binary_values('LOGG? 1,1',header_fmt='ieee',expect_termination='LF',chunk_size=256,datatype='d')
# logging = MPM_210.query_binary_values('LOGG? 1,1',header_fmt='ieee')
MPM_210.write('LOGG? 1,1')
logging = MPM_210.read_raw()
# logging = MPM_210.read_raw()
print('logging:',logging)

MPM_210.write('LOGG? 1,2')
logging = MPM_210.read_raw()
print('logging2:',logging)

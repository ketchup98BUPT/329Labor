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

avg_time = 10  # unit: ms
logging_point = 8  # < 100,0000
MPM_210.write('ZERO')
time.sleep(3)
tunable_laser.write(':POW:STAT 1')
MPM_210.write('AVG '+str(avg_time))
MPM_210.write('LOGN '+str(logging_point))
MPM_210.write('WAV 1550.0')
MPM_210.write('TRIG 1')
MPM_210.write('WMOD FREERUN')
MPM_210.write('LEV 1')
MPM_210.write('MEAS')

sleep_time = 3+avg_time*logging_point/1000
print('sleep_time',sleep_time)
time.sleep(sleep_time)

MPM_210.write('STOP')

MPM_210.write('LOGG? 1,1')
logging2 = MPM_210.read_raw()


data_length=logging_point*4
n_data = len(str(data_length))
n_digits = len(str(n_data))
headlength = 1 + n_digits + n_data

print('headlength:', headlength)

count = 0
sample_bank = []

sample_point = []
for log_byte in logging2:
    if count < headlength:
        print('char:',chr(log_byte))
    else:
        # print(log_byte)
        bin_byte = bin(log_byte)[2:]
        byte_str = bin_byte.zfill(8)
        print(log_byte,bin_byte.zfill(8))
        sample_point.insert(0,byte_str)
        if len(sample_point)==4:
            print(sample_point)
            sign_value = sample_point[0][0]
            exp_value = sample_point[0][1:]+sample_point[1][0]
            frac_value = sample_point[1][1:]+sample_point[2]+sample_point[3]
            print(sign_value,exp_value,frac_value)
            sign_value = int(sign_value,base=2)
            exp_value = int(exp_value,base=2)
            frac_value = int(frac_value,base=2)
            # print(sign_value, exp_value, frac_value)
            point_vale = ((-1)**sign_value)*(2**(exp_value-127))*(1+frac_value*(2**-23))
            sample_bank.insert(0,point_vale)
            sample_point = []
    count += 1

print('byte_count:',count)
print(sample_bank)
print(len(sample_bank))

tunable_laser.write(':POW:STAT 0')


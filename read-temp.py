#!/usr/bin/env python
 
import os
import time
import keen

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

keen.project_id = os.environ.get('PROJECT_ID')
keen.write_key = os.environ.get('WRITE_KEY')
keen.read_key = os.environ.get('READ_KEY')
keen.master_key = os.environ.get('MASTER_KEY')

temp_sensor = '/sys/bus/w1/devices/28-00043359d9ff/w1_slave'

def temp_raw():
	f = open(temp_sensor, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines = temp_raw()
	while lines[0].strip()[-3:] !='YES':
		time.sleep(0.2)
		lines = temp_raw()

	temp_output = lines[1].find('t=')

	if temp_output != -1:
		temp_string = lines[1].strip()[temp_output+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 +32.0
		
		json_temp = {
			'celcius' : temp_c,
			'fahrenheit' : temp_f
			}
		return json_temp

# while reading the temp from the sensor write the result to a file in json format, wait a second then write again
while True:
	print(read_temp())
	keen.add_event("temp_reading", read_temp())
	time.sleep(1)




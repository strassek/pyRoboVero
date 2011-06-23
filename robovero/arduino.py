"""Defines an API similar to the Arduino standard library.
"""

from lpc17xx_gpio import * # bad form!
from lpc17xx_adc import *  #
from LPC17xx import *      #
from lpc_types import *    #
from time import sleep

__author__ =			"Neil MacMunn"
__email__ =				"neil@gumstix.com"
__copyright__ = 	"Copyright 2010, Gumstix Inc"
__license__ = 		"BSD 2-Clause"
__version__ =			"0.1"

########################################################################
# Digital I/O
########################################################################

# modes
INPUT =			"INPUT"
OUTPUT = 		"OUTPUT"
modes = 		{INPUT:0, OUTPUT:1}
# values
LOW = 			"LOW"
HIGH = 			"HIGH"
values = 		{LOW:0, HIGH:1}
# PCB labels
P0_4 =			"P0_4"
P0_5 =			"P0_5"
P0_19 =			"P0_19"
P1_27 =			"P1_27"
P3_25 =			"P3_25"
P2_10 =			"P2_10"
P0_20 =			"P0_20"
P0_8 =			"P0_8"
P4_28 =			"P4_28"
P4_29 =			"P4_29"
P2_6 =			"P2_6"
P2_3 =			"P2_3"
P2_4 =			"P2_4"
BTN = 			"BTN"
LED = 			"LED"

class DigitalPin(object):
	"""Need the port and pin numbers to configure digital IO."""
	def __init__(self, portnum, pinnum):
		self.portnum = portnum
		self.pinnum = pinnum

digital_pins = {
	P0_4:DigitalPin(0,4),
	P0_5:DigitalPin(0,5),
	P0_19:DigitalPin(0,19),
	P1_27:DigitalPin(1,27),
	P3_25:DigitalPin(3,25),
	P2_10:DigitalPin(2,10),
	P0_20:DigitalPin(0,20),
	P0_8:DigitalPin(0,8),
	P4_28:DigitalPin(4,28),
	P4_29:DigitalPin(4,29),
	P2_6:DigitalPin(2,6),
	P2_3:DigitalPin(2,3),
	P2_4:DigitalPin(2,4),
	BTN:DigitalPin(2,10),
	LED:DigitalPin(3,25)
	}


def pinMode(pin, mode):
	"""Configures the specified pin to behave either as an input or an
	output."""
	global digital_pins, modes
	
	if pin not in digital_pins:
		print "Pin must be one of:"
		for key in digital_pins:
			print key
		exit(1)
		
	if mode not in modes:
		print "Mode must be one of:",
		for key in modes:
			print key,
		exit(1)
	
	GPIO_SetDir(digital_pins[pin].portnum,
							(1 << digital_pins[pin].pinnum),
							modes[mode]);


def digitalWrite(pin, value):
	"""Write a HIGH or a LOW value to a digital pin."""
	global digital_pins, values
	
	if pin not in digital_pins:
		print "Pin must be one of:"
		for key in digital_pins:
			print key
		exit(1)
	
	if value in values.keys():
		value = values[value]
	elif value not in values.values():
		print "Value must be one of:", values.items()
		exit(1)
	
	if value:	
		GPIO_SetValue(digital_pins[pin].portnum, (1 << digital_pins[pin].pinnum))
	else:
		GPIO_ClearValue(digital_pins[pin].portnum, (1 << digital_pins[pin].pinnum))


def digitalRead(pin):
	"""Reads the value from a specified digital pin, either HIGH or 
	LOW."""
	global digital_pins
	
	if pin not in digital_pins:
		print "Pin must be one of:"
		for key in digital_pins:
			print key
		exit(1)
	
	if (GPIO_ReadValue(digital_pins[pin].portnum) & (1 << digital_pins[pin].pinnum)):
		return 1
	else:
		return 0


########################################################################
# Analog I/O
########################################################################

references = 	{}

AD0_0 =				"AD0_0"
AD0_1 =				"AD0_1"
AD0_2 =				"AD0_2"
AD0_3 =				"AD0_3"
AD0_5 =				"AD0_5"
AD0_6 =				"AD0_6"
AD0_7 =				"AD0_7"

PWM1 =				"PWM1"
PWM2 =				"PWM2"
PWM3 =				"PWM3"
PWM4 =				"PWM4"
PWM5 =				"PWM5"
PWM6 =				"PWM6"

class AnalogPin(object):
	def __init__(self, channel, interrupt):
		self.channel = channel
		self.interrupt = interrupt

class PWMPin(object):
	def __init__(self):
		#TODO
		pass
		
analog_pins = {
	AD0_0:AnalogPin(ADC_CHANNEL_SELECTION.ADC_CHANNEL_0, ADC_TYPE_INT_OPT.ADC_ADINTEN0),
	AD0_1:AnalogPin(ADC_CHANNEL_SELECTION.ADC_CHANNEL_1, ADC_TYPE_INT_OPT.ADC_ADINTEN1),
	AD0_2:AnalogPin(ADC_CHANNEL_SELECTION.ADC_CHANNEL_2, ADC_TYPE_INT_OPT.ADC_ADINTEN2),
	AD0_3:AnalogPin(ADC_CHANNEL_SELECTION.ADC_CHANNEL_3, ADC_TYPE_INT_OPT.ADC_ADINTEN3),
	AD0_5:AnalogPin(ADC_CHANNEL_SELECTION.ADC_CHANNEL_5, ADC_TYPE_INT_OPT.ADC_ADINTEN5),
	AD0_6:AnalogPin(ADC_CHANNEL_SELECTION.ADC_CHANNEL_6, ADC_TYPE_INT_OPT.ADC_ADINTEN6),
	AD0_7:AnalogPin(ADC_CHANNEL_SELECTION.ADC_CHANNEL_7, ADC_TYPE_INT_OPT.ADC_ADINTEN7),
}

#~ pwm_pins = {
	#~ PWM1:Pin(1, 18),
	#~ PWM2:Pin(1, 20),
	#~ PWM3:Pin(3, 26),
	#~ PWM4:Pin(1, 23),
	#~ PWM5:Pin(1, 24),
	#~ PWM6:Pin(2, 5),
#~ }


def analogReference(reference):
	"""Configures the reference voltage used for analog input."""
	# TODO
	pass


def analogRead(pin):
	"""Reads the value from the specified analog pin. Assumes that 
	extras.roboveroConfig() has been called to initialize the ADC."""
	global analog_pins
	
	if pin not in analog_pins:
		print "Pin must be one of:"
		for key in analog_pins:
			print key
		exit(1)
		
	ADC_StartCmd(LPC_ADC, ADC_START_OPT.ADC_START_NOW)
	while not ADC_ChannelGetStatus(LPC_ADC, analog_pins[pin].channel, ADC_DATA_STATUS.ADC_DATA_DONE):
		sleep(0)
	adc_value = ADC_ChannelGetData(LPC_ADC, analog_pins[pin].channel)

	return adc_value


def analogWrite(pin, value):
	"""Writes an analog value (PWM wave) to a pin."""
	global pwm_pins
	# TODO: configure a PWM pin with duty cycle to generate pseudo analog
	#				output




#!/usr/bin/env python

# Before you run this:
# sudo apt-get install python-pip python-tk && pip install xpect

import serial
import expect

device = "/dev/ttyUSB0"

def setup(pirate):
  pirate.sendln("i")
  raw_info = pirate.iostream.read(1000)
  info = raw_info.split('\r\n')
  device_line = info[1]
  firmware_line = info[2]

  pirate.send("\n")
  pirate.expect(">")

  # Set 2WIRE mode
  pirate.sendln("m")
  pirate.expect("2WIRE")
  pirate.sendln("6")
  pirate.expect("Set speed")
  pirate.sendln("2")
  pirate.expect("Select output type")
  pirate.sendln("1")

  pirate.expect("2WIRE>")

  pirate.sendln("L")
  pirate.expect("LSB set")

  pirate.sendln("W")
  #pirate.expect("Power supplies ON") #FIXME: Why does this fail?

  pirate.sendln("P")
  pirate.expect("Pull-up resistors ON")

  pirate.sendln("C")
  pirate.expect("2WIRE>")

  return (device_line, firmware_line)


def get_atr(pirate):
  pirate.send("\n")
  pirate.expect("2WIRE>")
  pirate.sendln("(1)")

  atr_bytes = None
  line = ""
  pirate.iostream.readline()
  while line != '\r\n':
    line = pirate.iostream.readline()
    if line.startswith('ISO 7816-3 reply'):
      atr_bytes = line.split()[7:11]

  return atr_bytes

def read_card(pirate):
  # flush the input buffer
  pirate.iostream.flushInput()

  pirate.send("\n")
  pirate.expect("2WIRE>")

  pirate.sendln("{0x30 0 0xff}\ r:256 r:10")

  # ignore lines before the data output
  for i in range(10):
    data = pirate.iostream.readline()
    if len(data) > 250:
      break

  hex_string = data.split()[1:257]

  pirate.iostream.readline()
  return hex_string

def hex_to_bytes(hex_str):
  output = ""
  for group in hex_str:
    output += chr(int(group[-2:], 16))
  return output


def update_card(pirate, address, data):
    # Instruction: 0x38 <address> <data>
    raise NotImplemented()

def read_protection_memory(pirate):
    # 0x34 0 0
    raise NotImplemented()

def write_protection_memory(pirate, address, data):
    # 0x3c <address> <data>
    raise NotImplemented()

def read_security_memory():
    # 0x31 0 0
    raise NotImplemented()

def update_security_memory():
    # 0x39 <address> <data>
    raise NotImplemented()

def compare_verification_data():
    # 0x33 <address> <data>
    raise NotImplemented()

def get_device():
  ser = serial.Serial(device, 115200, timeout=1)
  pirate = expect.Handler(ser, print_output=False)

  pirate.send("\n")
  try:
    pirate.expect("2WIRE>", timeout=1)
  except expect.BreakConditionError:
    setup(pirate)

  return pirate

if __name__ == '__main__':
  with serial.Serial(device, 115200, timeout=1) as ser:
    pirate = expect.Handler(ser)

    pirate.send("\n")
    try:
      pirate.expect("2WIRE>", timeout=1)
    except expect.BreakConditionError:
      setup(pirate)

    while True:
      a = input("Press enter to read card, or anything else to quit > ")
      if a != '':
        ser.close()
        exit()

      ATR = get_atr(pirate)
      print(ATR)

      hex_data = read_card(pirate)
      print(hex_data)








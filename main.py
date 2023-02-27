import numpy as np
import serial

def translate_units(units: str) -> str:
    if units == "M":
        return "metres/second"
    elif units == "N":
        return "knots"
    elif units == "P":
        return "miles/hour"
    elif units == "K":
        return "kilometres/hour"
    elif units == "F":
        return "feets/minute"
    else:
        raise ValueError("Invalid unit value")

ser = serial.Serial('/dev/ttyUSB0', baudrate=9600,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE)

print("Wind direction, wind speed, units")

while True:
    try:
        line = str(ser.readline(), 'utf-8').strip()
        data_values=line.split(',')

        wind_direction=np.nan
        if data_values[1] != '':
            wind_direction=float(data_values[1])

        wind_speed=float(data_values[2])
        units=data_values[3]
        status=data_values[4]

        if status == '00':
            print("wd:",wind_direction,"ws:",wind_speed,"units:",translate_units(units))
        else:
            print("wd:",wind_direction,"ws:",wind_speed,"units:",translate_units(units))
    except:
        print("keyboard interrupt")
        break
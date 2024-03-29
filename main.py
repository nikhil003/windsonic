import numpy as np
import serial
from waggle.plugin import Plugin
from argparse import ArgumentParser


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


def main(*args, **kwargs):
    ser = serial.Serial(args[0], baudrate=args[1],
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE)

    #print("Wind direction, wind speed, units")

    data_names = {"wind_speed": "env.wind.magnitude",
                  "wind_direction": "env.wind.direction"}

    meta = {"sensor": "windsonic60"}

    with Plugin() as plugin:
        while True:
            try:
                line = str(ser.readline(), 'utf-8').strip()
                data_values = line.split(',')

                wind_direction = -9999.0
                if data_values[1] != '':
                    wind_direction = float(data_values[1])

                wind_speed = float(data_values[2])
                units = data_values[3]
                status = data_values[4]

                if kwargs.get('debug', False):
                    print(wind_speed, wind_direction, translate_units(units))

                if status == '00':
                    plugin.publish(data_names['wind_speed'], wind_speed,
                                   meta={"units": translate_units(units),
                                         "missing": "-9999.0", **meta})
                    plugin.publish(data_names['wind_direction'],
                                   wind_direction,
                                   meta={"units": "degree",
                                         "orientation": "from",
                                         "missing": "-9999.0",
                                         **meta})
                else:
                    plugin.publish(data_names['wind_speed'], -9999.0,
                                   meta={"units": translate_units(units),
                                         "missing": "-9999.0", **meta})
                    plugin.publish(data_names['wind_direction'],
                                   wind_direction,
                                   meta={"units": "degree",
                                         "orientation": "from",
                                         "missing": "-9999.0",
                                         **meta})
            except Exception as e:
                print("keyboard interrupt")
                print(e)
                break

    if not ser.closed:
        ser.close()


if __name__ == "__main__":
    parser = ArgumentParser(
        description="plugin for pushing windsonic 2d anemometer data through WSN")

    parser.add_argument('--device', type=str, dest='device',
                        default='/dev/ttyUSB5', help='device to read')
    parser.add_argument('--baud_rate', type=int, dest='baud_rate',
                        default=9600, help='baud rate for the device')
    parser.add_argument('--debug', action='store_true', dest='debug',
                        help='command to run script in debug mode')

    args = parser.parse_args()

    main(args.device, args.baud_rate, debug=args.debug)

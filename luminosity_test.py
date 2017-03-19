from tsl2561 import TSL2561


luminosity_sensor = TSL2561(debug=1)

def read_luminosity():
    print(int(luminosity_sensor.lux()))


def main():
    while(True):
        read_luminosity()


if __name__ == "__main__":
    main()

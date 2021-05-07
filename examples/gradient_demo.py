from syringe_pumps.pump_control import pump_code_pack
import time


def gradient(
    port, address_1, address_2, address_3, total_flow_rate, total_flow_rate_units
):
    ##### set up serial connection and define pumps #####
    # set up serial connection:

    sc_com4 = pump_code_pack.SerialConnection(port)

    # # define first pump
    pump_2000_1 = pump_code_pack.Pump2000(sc_com4, address_1, name="PHD2000_1")

    # # define second pump
    pump_2000_2 = pump_code_pack.Pump2000(sc_com4, address_2, name="PHD2000_2")

    # # define third pump
    pump_2000_3 = pump_code_pack.Pump2000(sc_com4, address_3, name="PHD2000_3")

    sleep_time = 1
    rounds_per_gradient = 20
    min_flow_percent = float(0.25)
    percent_1 = float(0.333)
    percent_2 = float(0.333)
    percent_3 = float(0.333)

    # percent_1 = float(percent_1)
    # percent_2 = float(percent_2)
    # percent_3 = float(percent_3)
    diff = (2 * (min_flow_percent) - percent_1) / rounds_per_gradient

    total_flow_rate = float(total_flow_rate)

    total_percents = percent_1 + percent_2 + percent_3

    infuse_rate_1 = total_flow_rate * percent_1 / total_percents
    pump_2000_1.set_infuse_rate(infuse_rate_1, total_flow_rate_units)

    infuse_rate_2 = total_flow_rate * percent_2 / total_percents
    pump_2000_2.set_infuse_rate(infuse_rate_2, total_flow_rate_units)

    infuse_rate_3 = total_flow_rate * percent_3 / total_percents
    pump_2000_3.set_infuse_rate(infuse_rate_3, total_flow_rate_units)

    # run pump to infuse
    pump_2000_1.set_irun()
    pump_2000_2.set_irun()
    pump_2000_3.set_irun()
    time.sleep(sleep_time)

    for x in range(rounds_per_gradient):
        print(x)
        percent_1 = percent_1 + diff
        percent_2 = percent_2 - (diff / 2)
        percent_3 = percent_3 - (diff / 2)
        total_percents = percent_1 + percent_2 + percent_3

        infuse_rate_2 = total_flow_rate * percent_2 / total_percents
        pump_2000_2.set_infuse_rate(infuse_rate_2, total_flow_rate_units)
        infuse_rate_3 = total_flow_rate * percent_3 / total_percents
        pump_2000_3.set_infuse_rate(infuse_rate_3, total_flow_rate_units)
        infuse_rate_1 = total_flow_rate * percent_1 / total_percents
        pump_2000_1.set_infuse_rate(infuse_rate_1, total_flow_rate_units)

        time.sleep(sleep_time)

    print("DONE WITH FIRST LOOP ")
    for x in range(rounds_per_gradient):
        print(x)
        percent_1 = percent_1 - (diff)
        percent_2 = percent_2 + (diff)
        total_percents = percent_1 + percent_2 + percent_3

        infuse_rate_1 = total_flow_rate * percent_1 / total_percents
        pump_2000_1.set_infuse_rate(infuse_rate_1, total_flow_rate_units)

        infuse_rate_2 = total_flow_rate * percent_2 / total_percents
        pump_2000_2.set_infuse_rate(infuse_rate_2, total_flow_rate_units)

        time.sleep(sleep_time)

    print("DONE WITH SECOND LOOP ")

    for x in range(rounds_per_gradient):
        print(x)
        percent_2 = percent_2 - diff
        percent_3 = percent_3 + diff
        total_percents = percent_1 + percent_2 + percent_3

        infuse_rate_2 = total_flow_rate * percent_2 / total_percents
        pump_2000_2.set_infuse_rate(infuse_rate_2, total_flow_rate_units)

        infuse_rate_3 = total_flow_rate * percent_3 / total_percents
        pump_2000_3.set_infuse_rate(infuse_rate_3, total_flow_rate_units)

        time.sleep(sleep_time)

    print("DONE WITH THIRD LOOP ")

    for x in range(rounds_per_gradient):
        print(x)
        percent_1 = percent_1 + (diff / 2)
        percent_2 = percent_2 + (diff / 2)
        percent_3 = percent_3 - (diff)
        total_percents = percent_1 + percent_2 + percent_3

        infuse_rate_3 = total_flow_rate * percent_3 / total_percents
        pump_2000_3.set_infuse_rate(infuse_rate_3, total_flow_rate_units)

        infuse_rate_1 = total_flow_rate * percent_1 / total_percents
        pump_2000_1.set_infuse_rate(infuse_rate_1, total_flow_rate_units)

        infuse_rate_2 = total_flow_rate * percent_2 / total_percents
        pump_2000_2.set_infuse_rate(infuse_rate_2, total_flow_rate_units)

        time.sleep(sleep_time)

    print("DONE WITH FOURTH LOOP ")

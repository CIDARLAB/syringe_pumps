from syringe_pumps.pump_control import pump_code_pack
import logging

##### add this to for logging functionality#####
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    filename="example.log",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)


##### set up serial connection and define pumps #####
# set up serial connection:
sc_com4 = pump_code_pack.SerialConnection("COM4")

# define first pump
address_1 = 0
pump_2000_1 = pump_code_pack.Pump2000(sc_com4, address_1, name="PHD2000")

# define second pump
address_2 = 1
pump_2000_2 = pump_code_pack.Pump2000(sc_com4, address_2, name="PHD2000")


##### run first pump to  infuse indefinitely #####

# set syringe diameter
diameter = 9.52
pump_2000_1.set_dia(diameter)

# set pump to pump mode (infuse indefinitely)
pump_2000_1.set_pump_mode()

# set infuse rate with infuse rate units
infuse_rate_1 = 10
infuse_rate_units_1 = "ul/min"
pump_2000_1.set_infuse_rate(infuse_rate_1, infuse_rate_units_1)

# run pump to infuse
pump_2000_1.set_irun()


##### run second pump to  infuse indefinitely #####

# set syringe diameter
diameter = 9.52
pump_2000_2.set_dia(diameter)

# set pump to pump mode (infuse indefinitely)
pump_2000_2.set_pump_mode()


# set infuse rate with infuse rate units
infuse_rate_2 = 12
infuse_rate_units_2 = "ul/min"
pump_2000_2.set_infuse_rate(infuse_rate_2, infuse_rate_units_2)

# run pump to infuse
pump_2000_2.set_irun()


### ... wait around... then run the stop code below ####


##### stop first pump #####
pump_2000_1.set_stop()

##### stop second pump #####
pump_2000_2.set_stop()


##### close serial connection #####
sc_com4.close()

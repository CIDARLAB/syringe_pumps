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


##### stop first pump #####
pump_2000_1.set_stop()

##### stop second pump #####
pump_2000_2.set_stop()


##### close serial connection #####
sc_com4.close()

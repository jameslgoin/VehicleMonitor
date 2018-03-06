#!/bin/bash

#python3 server/VehicleMonitor.py "candump -L can1 | /home/pi/vehicle_monitor/CAN_dbc_filter/socketcanDecodeSignal /home/pi/vehicle_monitor/dbcFiles/GM_HS.dbc /home/pi/vehicle_monitor/signalsFiltered"
#python3 server/VehicleMonitor.py "python3 ./server/test.py"
#candump -L can1 | /home/pi/vehicle_monitor/CAN_dbc_filter/socketcanDecodeSignal /home/pi/vehicle_monitor/dbcFiles/GM_HS.dbc /home/pi/vehicle_monitor/signalsFiltered
python3 server/VehicleMonitor.py "./getCAN.sh"

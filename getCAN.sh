#!/bin/bash
candump -L can1 | /home/pi/vehicle_monitor/CAN_dbc_filter/socketcanDecodeSignal /home/pi/vehicle_monitor/dbcFiles/GM_HS.dbc signalsFiltered

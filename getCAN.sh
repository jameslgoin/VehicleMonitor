#!/bin/bash
candump -L can1 | ./CAN_dbc_filter/socketcanDecodeSignal ./dbcFiles/GM_HS.dbc ./signalsFiltered

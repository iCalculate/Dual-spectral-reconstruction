# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 21:10:33 2023

@author: ywang
"""
import LakeShoreM335


Model335_GPIB_Addr = 12


Md335 = LakeShoreM335.Model335('GPIB0::' + str(Model335_GPIB_Addr) + '::INSTR')
TempA = Md335.read_temperature(mode = 'A')
TempB = Md335.read_temperature(mode = 'B')

Md335.set_heater_range(1,3)   #Set the heater of output 1 as medium(3) range
Md335.set_temperature(1, 300)   #set the temperature of output 1 as 40K






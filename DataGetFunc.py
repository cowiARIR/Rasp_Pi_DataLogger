# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 09:14:50 2018

@author: arir
"""
from sense_hat import SenseHat
from random import uniform
import RTIMU

def PressureTake():

    
    sense = SenseHat()
    sense.clear
    
    return sense.get_pressure()


def TempFromHumidityTake():
    sense = SenseHat()
    sense.clear
    
    return sense.get_temperature()

def TempFromPressureTake():
    sense = SenseHat()
    sense.clear
    
    return sense.get_temperature_from_pressure()

def HumidityTake():
    
    sense = SenseHat()
    sense.clear()
    
    return sense.get_humidity()

def OrientationTake():
    sense = SenseHat()
    sense.clear()
    
    orient = sense.get_orientation()
    pitch = orient["pitch"]
    roll = orient["roll"]
    yaw = orient["yaw"]
    
    return pitch, roll, yaw

def AccelTake():
    sense = SenseHat()
    sense.clear
    
    acceleration = sense.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']
    
    return x, y, z

def randomNum():
    return uniform(-10,40)


class AccelPiSense():
    
    def __init__(self, settingsfile = 'RTIMU_settings'):
        
        RTIMU_Settings = RTIMU.Settings(settingsfile)
        self.imu = RTIMU.RTIMU(RTIMU_Settings)
        self.imu.IMUInit()
        print("IMU: " + self.imu.IMUName() + " initalized")
        self.data = (0,0,0)
        self.internal_samp_period = self.imu.IMUGetPollInterval()/1000
        print('Minimum sampling period: ' + str(self.internal_samp_period))
    
    
    def all_accel_take(self):
        if self.imu.IMURead():
            self.data = self.imu.getAccel()
        else:
            print('Warning: Sampling too fast')
            self.data = (None, None, None)
            
    def x_accel_take(self, fetch_new_data = True):
        self.all_accel_take()
        xx = self.data[0]
        return xx 
        
    def y_accel_take(self, fetch_new_data = False):
        self.all_accel_take()
        yy = self.data[1]
        return yy     
        
    def z_accel_take(self,fetch_new_data = False):
        self.all_accel_take()
        zz = self.data[2]
        return zz
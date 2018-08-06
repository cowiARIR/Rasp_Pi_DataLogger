# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 16:03:12 2018
@author: ARIR

Main Data Logger thread:
    Gets data with a sampling frequency of 10Hz, max file size of 50 lines, 
    with a timeout of 10s
    Currently only runs a ticker thread and acquisition 19/6/2018
"""
import DataGetFunc2 as dataGetFunc
from ticker_example import ticker
import threading

# Define classes used in core threads
import acquisition_system as acqSys
import pre_processor as prePro

#import RTIMU
from DataGetFunc2 import RTIMU
import liveFeed
#%% start of main code

#### Inputs
s = RTIMU.Settings('RTIMU_settings')
imu = RTIMU.RTIMU(s) 
print("IMU Name: " + imu.IMUName())

if (not imu.IMUInit()): 
    print("IMU Init Failed!!!!")
    print("Using fake IMU")
    fake_IMU = True
else: 
    print("IMU Init Succeeded")
    fake_IMU = False



reader = dataGetFunc.AccelReader(imu, fake_IMU)
    
samplingFunctions = [lambda :reader.x_accel_take(fetch_new_data = True), 
                     lambda :reader.y_accel_take(),
                     lambda :reader.z_accel_take()] 
maxCacheSize = 50.0 
fs = 16; T = 1/fs
timeOut = 10.0
fig_length = 30

draw_funcs = {'Ch0':liveFeed.line_chart,  
              'Ch1':liveFeed.line_chart,  
              'Ch2':liveFeed.line_chart}  
   
dsp_raw_channels = []  
dsp_processed_channels = ['Ch0','Ch1'] 



def addition_1(xx):
    yy = xx + 1
    return yy
    
def subtract_1(xx):
    yy = xx - 1
    return yy

def do_nothing(xx):
    return xx

pre_process_func = [[do_nothing],[do_nothing],[do_nothing]]
layover_size = 20

#Creates an AcquisitionSystem 
ASys = acqSys.AcquisitionSystem(samplingFunctions)

#Creates a PreProcessor
PrePross = prePro.PreProcessor(pre_process_func,   
                               draw_funcs,   
                               dsp_raw_channels,   
                               dsp_processed_channels,
                               fig_x_len = fig_length,
                               layover_size = layover_size) 


#Creates events
eventGoGetData = threading.Event()
eventFileReady = threading.Event() 
event_ticker_timeout = threading.Event()

#Define and start threads
ticker_thread = threading.Thread(name= 'ticker', 
                                 target = ticker, 
                                 args = (eventGoGetData,), 
                                 kwargs = {'timeout':timeOut, 
                                           'T':T, 
                                           'tick_timeout':event_ticker_timeout})

Acq_thread = threading.Thread(name = 'Acquisition',
                               target = acqSys.runAcquisition,
                               args=(eventGoGetData, 
                                     eventFileReady, 
                                     ASys, 
                                     event_ticker_timeout),
                               kwargs={'maxCacheSize':maxCacheSize})
                               
PreProcess_thread = threading.Thread(name = 'Pre-Processor',
                                     target = prePro.run_pre_processor,
                                     args=(PrePross,
                                           eventFileReady, 
                                           event_ticker_timeout))


ticker_thread.start()
Acq_thread.start()
PreProcess_thread.start()



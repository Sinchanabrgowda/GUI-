import tkinter as tk
from tkinter import ttk
import socket
import datetime

functions_path = "functions.lua"  # This file holds the set of TSP (Lua-based) functions

def load_functions(s):
    # This function opens the scanFunctions.lua file in the same directory
    # as the Python script and transfers its contents to the DAQ6510
    # internal memory. All the functions defined in the file are callable
    # by the controlling program.
    func_file = open(functions_path, "r")
    contents = func_file.read()
    func_file.close()
    
    s.send("if loadfuncs ~= nil then script.delete('loadfuncs') end\n".encode())
    s.send("loadscript loadfuncs\n{0}\nendscript\n".format(contents).encode())
    s.send("loadfuncs()\n".encode())
    print(s.recv(100).decode())

def send_reset(s):
    # This function issues the reset that clears all existing
    # instrument settings.
    s.send("rst()\n".encode())
    s.recv(10)

def send_cnfgSpeedScan(s, fnc, scanList, rng, nplc, cnt, s2sInt):
    # This function configures the speed scan setup as
    # defined by the passed parameters.
    sndBuffer = "cnfgSpeedScan({0},{1},{2},{3},{4},{5})\n".format(fnc, scanList, rng, nplc, cnt, s2sInt)
    s.send(sndBuffer.encode())
    s.recv(10)

def send_init(s):
    # This function issues the reset that clears all existing
    # instrument settings.
    s.send("init()\n".encode())
    s.recv(10)

def send_waitForScan(s):
    # This function issues the reset that clears all existing
    # instrument settings.
    s.send("chkTrgMdl()\n".encode())
    response = (int)(s.recv(10))
    while (response == 1):
        s.send("chkTrgMdl()\n".encode())
        response = (int)(s.recv(10))

def get_ScanData(s):
    # This function extracts the scanned readings
    # from the DAQ6510
    s.send("getRdgs()\n".encode())
    response = s.recv(1024).decode()
    return response

def connect_daq():
    global s
    global ip_entry, window, frame2

    ip_address = ip_entry.get()

    # Create a new socket for each connection
    s = socket.socket()
    s.connect((ip_address, 5025))

    # Load functions and configure the DAQ6510
    load_functions(s)
    send_reset(s)
    dcvScanList = '\'101\''
    rng =10000
    send_cnfgSpeedScan(s, 2, dcvScanList, rng, 0.001, 1, 0)
    
    # Switch to the second page
    frame2.tkraise()
def measure_daq_values():
    global s, label, resistor_entry, capacitor_entry

    given_resistor_value = resistor_entry.get()
    given_capacitor_value = capacitor_entry.get()

    if given_resistor_value:
        try:
            given_resistor_value = float(given_resistor_value)
            send_init(s)
            send_waitForScan(s)
            reading = get_ScanData(s)
            daq_resistor_value = float(reading.strip())  # Assuming the DAQ value is returned as a string

            result_resistor = "Pass" if abs(given_resistor_value - daq_resistor_value) < 100 else "Fail"
            label.config(text=f"DAQ6510 Resistor Value: {daq_resistor_value} - Result: {result_resistor}")
        except ValueError:
            label.config(text="Invalid resistor value. Please enter a valid number.")
    elif given_capacitor_value:
        try:
            given_capacitor_value = float(given_capacitor_value)
            send_init(s)
            send_waitForScan(s)
            reading = get_ScanData(s)
            daq_capacitor_value = float(reading.strip())  # Assuming the DAQ value is returned as a string

            result_capacitor = "Pass" if abs(given_capacitor_value - daq_capacitor_value) < 0.000001 else "Fail"
            label.config(text=f"DAQ6510 Capacitor Value: {daq_capacitor_value} - Result: {result_capacitor}")
        except ValueError:
            label.config(text="Invalid capacitor value. Please enter a valid number.")
    else:
        label.config(text="Please enter either a resistor or a capacitor value.")

# Create the main window
window = tk.Tk()
window.title("DAQ6510 Value Display GUI")

# Create the first frame (Connection Page)
frame1 = ttk.Frame(window, padding="20")
frame1.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create IP Address Entry on the first page
ip_label = ttk.Label(frame1, text="Enter IP Address:")
ip_label.grid(row=0, column=0, sticky=tk.W)
ip_entry = ttk.Entry(frame1)
ip_entry.grid(row=0, column=1, sticky=tk.W)

# Create Connect Button on the first page
connect_button = ttk.Button(frame1, text="Connect", command=connect_daq)
connect_button.grid(row=1, column=0, columnspan=2, sticky=tk.W)

# Create the second frame (Settings Page)
frame2 = ttk.Frame(window, padding="10")
frame2.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create Resistor Entry on the second page
resistor_label = ttk.Label(frame2, text="Enter Resistor Value:")
resistor_label.grid(row=0, column=0, sticky=tk.W)
resistor_entry = ttk.Entry(frame2)
resistor_entry.grid(row=0, column=1, sticky=tk.W)

# Create Capacitor Entry on the second page
capacitor_label = ttk.Label(frame2, text="Enter Capacitor Value:")
capacitor_label.grid(row=1, column=0, sticky=tk.W)
capacitor_entry = ttk.Entry(frame2)
capacitor_entry.grid(row=1, column=1, sticky=tk.W)

# Create Measure Button on the second page
measure_button = ttk.Button(frame2, text="Measure DAQ Values", command=measure_daq_values)
measure_button.grid(row=2, column=0, columnspan=2, sticky=tk.W)

# Create a Label to display the obtained DAQ6510 values on the second page
label = ttk.Label(frame2, text="DAQ6510 Values: ")
label.grid(row=3, column=0, columnspan=2, sticky=tk.W)

# Initial display: Show the first page
frame1.tkraise()

window.mainloop()

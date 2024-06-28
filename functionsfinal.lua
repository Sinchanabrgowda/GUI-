function rst()
    -- Call reset w/ reduced number of character
    reset()
    print("OK")
end

function cnfgFunc(fnc, chLst)
    -- Set the measurement functions for the scan
    if fnc == 0 then
     -- Scan Temperature
        channel.setdmm(chLst, dmm.ATTR_MEAS_FUNCTION, dmm.FUNC_TEMPERATURE) 
        channel.setdmm(chLst, dmm.ATTR_MEAS_REF_JUNCTION, dmm.REFJUNCT_INTERNAL)
        channel.setdmm(chLst, dmm.ATTR_MEAS_THERMOCOUPLE, dmm.THERMOCOUPLE_K)
    elseif fnc == 1 then 
     -- Scan DC Volts
        channel.setdmm(chLst, dmm.ATTR_MEAS_FUNCTION, dmm.FUNC_DC_VOLTAGE)
    elseif fnc == 2 then
     -- Scan 2-Wire Resistance
        channel.setdmm(chLst, dmm.ATTR_MEAS_FUNCTION, dmm.FUNC_RESISTANCE)
    elseif fnc == 3 then 
     -- Scan 4-Wire Resistance
        channel.setdmm(chLst, dmm.ATTR_MEAS_FUNCTION, dmm.FUNC_4W_RESISTANCE)
    elseif fnc == 4 then
     -- Scan DC Amps
        channel.setdmm(chLst, dmm.ATTR_MEAS_FUNCTION, dmm.FUNC_DC_CURRENT)
    elseif fnc == 5 then
     -- Scan Capacitor
        channel.setdmm(chLst, dmm.ATTR_MEAS_FUNCTION, dmm.FUNC_CAPACITANCE)
    end
end

function cnfgSetRng(chLst, rng)
    -- Set the measurement function range
        channel.setdmm(chLst, dmm.ATTR_MEAS_RANGE, rng)
end

function cnfgSetNplc(chLst, nplc)
    -- Set the measurement integration time via NPLCs
    channel.setdmm(chLst, dmm.ATTR_MEAS_NPLC, nplc)
end

function enblAZero(chLst, state)
    -- Set the state of Auto Zero
    if state == 0 then
        channel.setdmm(chLst, dmm.ATTR_MEAS_AUTO_ZERO, dmm.OFF)
    else
        channel.setdmm(chLst, dmm.ATTR_MEAS_AUTO_ZERO, dmm.ON)
    end
end

function enblADelay(chLst, state)
    if state == 0 then
        channel.setdmm(chLst, dmm.ATTR_MEAS_AUTO_DELAY, dmm.DELAY_OFF)
    else
        channel.setdmm(chLst, dmm.ATTR_MEAS_AUTO_DELAY, dmm.DELAY_ON)
    end
end
    
function enblLimit(chLst, use1, use2)
    if use1 == 0 then
        channel.setdmm(chLst, dmm.ATTR_MEAS_LIMIT_ENABLE_1, dmm.OFF)
    else
        channel.setdmm(chLst, dmm.ATTR_MEAS_LIMIT_ENABLE_1, dmm.ON)
    end

    if use2 == 0 then
        channel.setdmm(chLst, dmm.ATTR_MEAS_LIMIT_ENABLE_2, dmm.OFF)
    else
        channel.setdmm(chLst, dmm.ATTR_MEAS_LIMIT_ENABLE_2, dmm.ON)
    end
end

function enblLineSync(chLst, state)
    if state == 0 then
        channel.setdmm(chLst, dmm.ATTR_MEAS_LINE_SYNC, dmm.OFF)
    else
        channel.setdmm(chLst, dmm.ATTR_MEAS_LINE_SYNC, dmm.ON)
    end
end
    
function setScanList(chLst)
        scan.create(chLst)
end
    
function setScanCount(cnt)
        scan.scancount = cnt
end
    
function setScn2Scn(stosIntvl)
        scan.scaninterval = stosIntvl
end
    
function scanInit()
        trigger.model.initiate()
end
   
function cnfgSpeedScan(fnc, chLst, rng, nplc, cnt, s2sInt)
    -- Apply the measure function
    cnfgFunc(fnc, chLst)
    -- Set the measure range; not for Temp which is fixed
    if fnc ~= 0 then
        cnfgSetRng(chLst, rng)
    end
        -- Set the measure integration rate
    cnfgSetNplc(chLst, nplc)
        -- Disable auto zero
    enblAZero(chLst, 0)
        -- Disable auto delay
    enblADelay(chLst, 0)
        -- Disable limits checking
    enblLimit(chLst, 0, 0)
        -- Disable line synchronization
    enblLineSync(chLst, 0)
        -- Set the scan list
    setScanList(chLst)
        -- Set the scan count
    setScanCount(cnt)
    -- Set the scan to scan interval
    setScn2Scn(s2sInt)
    -- Ensure that all setup operations have completed
    opc()
    print("OK")
end 

function init()
    trigger.model.initiate()
    opc()
    print("OK")
end

function chkTrgMdl()
    present_state, n = trigger.model.state() -- state, present block number
    if (present_state == trigger.STATE_RUNNING) or (present_state == trigger.STATE_WAITING) then 
        print("1")
    else
        print("0")
    end
end 

function getRdgs()
    printbuffer(1, defbuffer1.n, defbuffer1)
end

print("functions loaded")

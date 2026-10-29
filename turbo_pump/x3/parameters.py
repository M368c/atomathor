from turbo_pump.x3.data_type import DataType
from enum import Enum


class Parameters(Enum):
    def __new__(cls, value: int, description: str, access: str, data_type: str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        obj.is_readable = "R" in access
        obj.is_writeable = "W" in access
        obj.data_type = data_type
        return obj

    Heating = (1, "Heating", "RW", DataType.BooleanOld)
    StandBy = (2, "Stand-By", "RW", DataType.BooleanOld)
    RUTimeCtrl = (4, "Run-up time monitoring", "RW", DataType.BooleanOld)
    ErrorAckn = (9, "Malfunction acknowledgement", "W", DataType.BooleanOld)
    PumpgStatn = (10, "Pumping station", "RW", DataType.BooleanOld)
    EnableVent = (12, "Enable venting", "RW", DataType.BooleanOld)
    CfgSpdSwPt = (
        17,
        "Rotation speed switchpoint configuration",
        "RW",
        DataType.UShortInt,
    )
    CfgDO2 = (19, "Output DO2 configuration", "RW", DataType.UShortInt)
    MotorPump = (23, "Motor pump", "RW", DataType.BooleanOld)
    CfgDO1 = (24, "Output DO1 configuration", "RW", DataType.UShortInt)
    OpModeBKP = (25, "Backing pump operating mode", "RW", DataType.UShortInt)
    SpdSetMode = (26, "Rotation speed setting mode", "RW", DataType.UShortInt)
    GasMode = (27, "Gas mode", "RW", DataType.UShortInt)
    VentMode = (30, "Venting mode", "RW", DataType.UShortInt)
    CfgAccA1 = (35, "Configuration accessory connection A1", "RW", DataType.UShortInt)
    CfgAccB1 = (36, "Configuration accessory connection B1", "RW", DataType.UShortInt)
    Press1HVen = (
        41,
        "Release HV sensor integrated (only IKT)",
        "RW",
        DataType.UShortInt,
    )
    SealingGas = (50, "Sealing gas", "RW", DataType.BooleanOld)
    CfgAO1 = (55, "Output AO1 configuration", "RW", DataType.UShortInt)
    TmpMgtMode = (58, "Temperature management configuration", "RW", DataType.UShortInt)
    CtrlViaInt = (60, "Operate via interface", "RW", DataType.UShortInt)
    IntSelLckd = (61, "Interface selection locked", "RW", DataType.BooleanOld)
    CfgDI1 = (62, "Input DI1 configuration", "RW", DataType.UShortInt)
    CfgDI2 = (63, "Input DI2 configuration", "RW", DataType.UShortInt)
    CfgAccC1 = (68, "Configuration accessory connection C1", "RW", DataType.UShortInt)
    CfgAccD1 = (69, "Configuration accessory connection D1", "RW", DataType.UShortInt)
    RemotePrio = (300, "Remote priority", "R", DataType.BooleanOld)
    SpdSwPtAtt = (302, "Rotation speed switchpoint reached", "R", DataType.BooleanOld)
    ErrorCode = (303, "Error code", "R", DataType.String)
    OvTempElec = (304, "Excess temperature electronics", "R", DataType.BooleanOld)
    OvTempPump = (305, "Excess temperature pump", "R", DataType.BooleanOld)
    SetSpdAtt = (306, "Set rotation speed reached", "R", DataType.BooleanOld)
    PumpAccel = (307, "Pump accelerating", "R", DataType.BooleanOld)
    SetRotSpd = (308, "Set rotation speed (Hz)", "R", DataType.UInteger)
    ActualSpd = (309, "Actual rotational speed (Hz)", "R", DataType.UInteger)
    DrvCurrent = (310, "Drive current", "R", DataType.UReal)
    OpHrsPump = (311, "Pump operating hours", "R", DataType.UInteger)
    FwVersion = (312, "Drive electronics software version", "R", DataType.String)
    DrvVoltage = (313, "Drive voltage", "R", DataType.UReal)
    OpHrsElec = (314, "Drive electronics operating hours", "R", DataType.UInteger)
    NominalSpd = (315, "Nominal rotation speed (Hz)", "R", DataType.UInteger)
    DrvPower = (316, "Drive power", "R", DataType.UInteger)
    PumpCycles = (319, "Pump cycles", "R", DataType.UInteger)
    TmpPwrStg = (324, "Temperature power stage", "R", DataType.UInteger)
    TempElec = (326, "Electronics temperature", "R", DataType.UInteger)
    TempPmpBot = (330, "Pump lower part temperature", "R", DataType.UInteger)
    AccelDecel = (336, "Acceleration/deceleration", "R", DataType.UInteger)
    ElecName = (349, "Electronic drive unit designation", "R", DataType.String)
    HWVersion = (354, "Hardware version drive electronics", "R", DataType.String)
    SerialNo = (355, "Serial number", "R", DataType.String16)
    ErrHist1 = (360, "Error code history, item 1", "R", DataType.String)
    ErrHist2 = (361, "Error code history, item 2", "R", DataType.String)
    ErrHist3 = (362, "Error code history, item 3", "R", DataType.String)
    ErrHist4 = (363, "Error code history, item 4", "R", DataType.String)
    ErrHist5 = (364, "Error code history, item 5", "R", DataType.String)
    ErrHist6 = (365, "Error code history, item 6", "R", DataType.String)
    ErrHist7 = (366, "Error code history, item 7", "R", DataType.String)
    ErrHist8 = (367, "Error code history, item 8", "R", DataType.String)
    ErrHist9 = (368, "Error code history, item 9", "R", DataType.String)
    ErrHist10 = (369, "Error code history, item 10", "R", DataType.String)
    TempRotor = (384, "Rotor temperature", "R", DataType.UInteger)
    OrderCode = (388, "Order number", "R", DataType.String16)
    AddID = (396, "Pump ID", "R", DataType.UInteger)
    SetRotSpdRpm = (397, "Set rotation speed (rpm)", "R", DataType.UInteger)
    ActualSpdRpm = (398, "Actual rotational speed (rpm)", "R", DataType.UInteger)
    NominalSpdRpm = (399, "Nominal rotation speed (rpm)", "R", DataType.UInteger)
    RUTimeSVal = (700, "Set value run-up time", "RW", DataType.UInteger)
    SpdSwPt1 = (701, "Rotation speed switch point 1", "RW", DataType.UInteger)
    SpdSVal = (707, "Set value in rotation speed setting mode", "RW", DataType.UReal)
    PwrSVal = (708, "Set value power consumption", "RW", DataType.UShortInt)
    SwOffBKP = (
        710,
        "Backing pump switch-off threshold for intermittent operation",
        "RW",
        DataType.UInteger,
    )
    SwOnBKP = (
        711,
        "Backing pump switch-on threshold for intermittent operation",
        "RW",
        DataType.UInteger,
    )
    StdbySVal = (
        717,
        "Rotation speed set value in stand-by operation",
        "RW",
        DataType.UReal,
    )
    SpdSwPt2 = (719, "Rotation speed switch point 2", "RW", DataType.UInteger)
    VentSpeed = (
        720,
        "Venting at rotation speed, delayed venting",
        "RW",
        DataType.UShortInt,
    )
    VentTime = (721, "Venting time, delayed venting", "RW", DataType.UInteger)
    MxPweOutTm = (
        726,
        "Max time for the output voltage in power back-up mode",
        "RW",
        DataType.UInteger,
    )
    FanOnTemp = (
        728,
        "Start-up temperature of the fan in temperature-controlled mode",
        "RW",
        DataType.UInteger,
    )
    PrsSwPt1 = (730, "Pressure switch point 1", "RW", DataType.Exponential)
    PrsSwPt2 = (732, "Pressure switch point 2", "RW", DataType.Exponential)
    PwrOutColt = (733, "Output voltage in power back-up mode", "RW", DataType.UReal)
    PwrOutThrs = (
        734,
        "Power threshold from which the voltage is output from P733 (PwrOutVolt)",
        "RW",
        DataType.UInteger,
    )
    PrsSn1Name = (739, "Name sensor 1", "R", DataType.String)
    Pressure1 = (740, "Pressure value 1", "RW", DataType.Exponential)
    PrsCorrPi1 = (742, "Correction factor 1", "RW", DataType.UReal)
    PrsSn2Name = (749, "Name sensor 2", "R", DataType.String)
    Pressure2 = (750, "Pressure value 2", "RW", DataType.Exponential)
    PrsCorrPi2 = (752, "Correction factor 2", "RW", DataType.UReal)
    NomSpdConf = (
        777,
        "Confirmation on nominal rotation speed",
        "RW",
        DataType.UInteger,
    )
    RS485Adr = (797, "RS-485 Interface address", "RW", DataType.UInteger)
    Pressure = (340, "Actual pressure value (ActiveLine)", "R", DataType.UShortInt)
    CtrName = (350, "Control unit type", "R", DataType.String)
    CtrSofrware = (351, "Control unit software version", "R", DataType.String)
    GaugeType = (738, "Type of pressure gauge", "RW", DataType.String)
    ParamSet = (794, "Parameter set", "RW", DataType.UShortInt)
    ServiceLin = (795, "Insert service line", "RW", DataType.UShortInt)

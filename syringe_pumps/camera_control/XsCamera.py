###############################################################################
#   XsCamera.py - Python wrapper class for IDT cameras
#   Version 2.15.00
#   Copyright (C) 2000-2019 Integrated Design Tools, Inc.
#   ALL RIGHTS RESERVED
###############################################################################

import ctypes
import sys
import types
import ctypes.util

###############################################################################
# Loading library

if sys.platform.startswith("win"):
    _library_loader = ctypes.windll
    CALLBACK_TYPE = ctypes.WINFUNCTYPE
else:
    _library_loader = ctypes.cdll
    CALLBACK_TYPE = ctypes.CFUNCTYPE


def FindLibrary(library_name="XStreamDrv", library_loader=_library_loader):
    library_path = ctypes.util.find_library(library_name)
    if library_path:
        return library_loader.LoadLibrary(library_path)
    else:
        return library_loader.XStreamDrv


class LibraryNotLoadedException(Exception):
    pass


class LibraryAlreadyLoadedException(Exception):
    pass


class DelayedLoadLibrary:
    def __init__(self, library_loader):
        self.library_loader = library_loader
        self.library = None

    def LoadLibrary(self, library_name):
        self.library = FindLibrary(library_name, self.library_loader)

    def Call(self, function_name, *params, **kw):
        if self.library:
            return self.library.__getattr__(function_name)(*params, **kw)
        else:
            raise LibraryNotLoadedException()

    def __getattr__(self, function_name):
        return DelayedLoadFunction(self, function_name)


class DelayedLoadFunction:
    def __init__(self, library, function_name):
        self.library = library
        self.function_name = function_name

    def __call__(self, *params, **kw):
        return self.library.Call(self.function_name, *params, **kw)


def LoadLibrary(library_name="XStreamDrv"):
    global XStreamDrv
    if XStreamDrv.__class__ is DelayedLoadLibrary:
        XStreamDrv.LoadLibrary(library_name)
    else:
        raise LibraryAlreadyLoadedException(
            "Dynamic library was loaded on module import and can not be changed"
        )


try:
    XStreamDrv = FindLibrary()
except:
    XStreamDrv = DelayedLoadLibrary(_library_loader)

XSUINT64 = ctypes.c_uint64
XSINT64 = ctypes.c_int64
XSULONG32 = ctypes.c_uint32
XSLONG32 = ctypes.c_int32

PXSUINT64 = ctypes.POINTER(XSUINT64)
PXSINT64 = ctypes.POINTER(XSINT64)
PXSULONG32 = ctypes.POINTER(XSULONG32)
PXSLONG32 = ctypes.POINTER(XSLONG32)

###############################################################################
# Constant Definitions

# Camera Model
class XS_CAM_MODEL(XSULONG32):
    XS_CM_UNKNOWN = 0  # Unknown type
    XS_CM_MP_X1 = 1  # X-Stream XS3
    XS_CM_MP_X4 = 2  # MotionPro HS4/X4
    XS_CM_MP_X3 = 3  # MotionPro HS3/X3
    XS_CM_MP_X5 = 4  # MotionPro XS6/X5
    XS_CM_MP_X2 = 5  # MotionPro HS2
    XS_CM_MP_M3 = 6  # MotionScope M3
    XS_CM_MP_M4 = 7  # MotionScope M4
    XS_CM_MP_M5 = 8  # MotionScope M5
    XS_CM_MP_Y3 = 9  # MotionPro Y3
    XS_CM_MP_Y4 = 10  # MotionPro Y4
    XS_CM_MP_Y5 = 11  # MotionPro Y5
    XS_CM_HG_100K = 12  # MotionXtra HG-100K
    XS_CM_HG_LE = 13  # MotionXtra HG-LE
    XS_CM_HG_TH = 14  # MotionXtra HG-TH
    XS_CM_HG_2K = 15  # MotionXtra HG-2000
    XS_CM_CR_2K = 16  # MotionXtra CR-2000
    XS_CM_TX_2K = 17  # MotionXtra TX-2000
    XS_CM_MP_N3 = 18  # MotionPro N3
    XS_CM_MP_N4 = 19  # MotionPro N4
    XS_CM_MP_N5 = 20  # MotionPro N5
    XS_CM_MP_Y6 = 21  # MotionPro Y6
    XS_CM_MP_Y7 = 22  # MotionPro Y7
    XS_CM_MP_N7 = 23  # MotionXtra NR7/NX7
    XS_CM_MP_Y8 = 24  # MotionPro Y8
    XS_CM_MP_N8 = 25  # MotionXtra NX8
    XS_CM_MP_Y10 = 26  # MotionXtra Y10
    XS_CM_MP_O9 = 27  # MotionXtra Os9
    XS_CM_MP_O4 = 28  # MotionXtra Os4
    XS_CM_MP_O5 = 29  # MotionXtra Os5
    XS_CM_MP_O10 = 30  # MotionXtra Os10
    XS_CM_MP_O7 = 31  # MotionXtra Os7
    XS_CM_MP_O8 = 32  # MotionXtra Os8
    XS_CM_CC_1060 = 33  # CrashCam 1060
    XS_CM_CC_1520 = 34  # CrashCam 1520
    XS_CM_CC_1540 = 35  # CrashCam 1540
    XS_CM_CC_4010 = 36  # CrashCam 4010
    XS_CM_CC_M1510 = 37  # CrashCam Mini 1510
    XS_CM_CC_2020 = 38  # CrashCam 2020
    XS_CM_CC_M5K05 = 39  # CrashCam Mini 5K05
    XS_CM_MP_O3 = 40  # MotionXtra Os3
    XS_CM_CC_M1520 = 41  # CrashCam Mini 1520
    XS_CM_CC_M3510 = 42  # CrashCam Mini 3510
    XS_CM_MINI_HD = 43  # Mini HD
    XS_CM_CC_M1540 = 44  # CrashCam Mini 1540
    XS_CM_CC_M3525 = 45  # CrashCam Mini 3525
    XS_CM_PCIE_X7 = 46  # PCIe X-Stream 720p
    XS_CM_PCIE_X14 = 47  # PCIe X-Stream 1440p
    XS_CM_XSM_1540 = 48  # TB X-Stream Mini 1540
    XS_CM_XSM_3520 = 49  # TB X-Stream Mini 3520
    XS_CM_XSS_1310 = 50  # TB X-Stream Stick 1310
    XS_CM_R_HD = 55  # R-series HD


# camera name max lenght
L_CAMNAME = 128

# max number of frames that can be acquired by old design N3 and N4 cameras
MAX_N_ACQ_FRAMES = 16352

# Enumeration filter
class XS_ENUM_FLT(XSULONG32):
    XS_EF_USB_X = 0x00000001  # MotionPro XS/HS/X (USB 2.0)
    XS_EF_GE_X = 0x00000002  # MotionPro X (Giga-Ethernet)
    XS_EF_HG = 0x00000004  # MotionXtra HG (Giga-Ethernet)
    XS_EF_CL = 0x00000008  # MotionScope M (Camera-Link)
    XS_EF_USB_Y = 0x00000010  # MotionPro Y (USB 2.0)
    XS_EF_GE_Y = 0x00000020  # MotionPro Y (Giga-Ethernet)
    XS_EF_LG_RL = 0x00000040  # Legacy MotionXtra
    XS_EF_GE_N = 0x00000080  # MotionXtra N/NR/NX/O (Giga-Ethernet)
    XS_EF_GE_NO = 0x00000080  # see above
    XS_EF_PCI_X = 0x00000100  # X-Stream PCIe/Thunderbolt
    XS_EF_VCAM = 0x00010000  # Virtual camera (RAW sequence)
    XS_EF_VSSD = 0x00020000  # Virtual camera (removable SSD, SD card)
    #
    XS_EF_ALL = 0x000001FF  # mask


# Link type
class XS_LINK_TYPE(XSULONG32):
    XS_LT_USB20 = 0  # USB 2.0
    XS_LT_GIGAETH = 1  # Giga Ethernet
    XS_LT_CAMLINK = 2  # Camera Link
    XS_LT_SDCARD = 3  # SD card/SSD (virtual camera)
    XS_LT_RAWFILE = 4  # RAW file (virtual camera)
    XS_LT_WIFI = 5  # WiFi
    XS_LT_PCIE = 6  # PCI express
    XS_LT_TB = 7  # Thunderbolt


# Frame Grabber Type (Camera Link only)
class XS_FG_TYPE(XSULONG32):
    XS_FG_COR_X64CL = 0  # Dalsa-Coreco X64 Xcelera-CL PX4
    XS_FG_NI_PCIE1429 = 1  # National Instruments PCIe-1429
    XS_FG_MATROX_HS = 2  # Matrox Helios/Solios
    XS_FG_EPIXCI_E4 = 3  # Epix PIXCI E4
    XS_FG_BF_KARBON = 4  # Bitflow Karbon CL


# Sensor type (monochrome/color)
class XS_SNS_TYPE(XSULONG32):
    XS_ST_MONOCHROME = 0  # monochrome sensor (gray scale color)
    XS_ST_COLOR = 1  # color sensor (bayer pattern color)


# CFA Bayer Pattern
class XS_CFA_PATTERN(XSULONG32):
    XS_CFAP_GRBG = 0
    XS_CFAP_BGGR = 1
    XS_CFAP_RGGB = 2
    XS_CFAP_GBRG = 3


# Sensor Model
class XS_SNS_MODEL(XSULONG32):
    XS_SM_UNKNOWN = 0  # Unknown model
    XS_SM_MV13 = 1  # MV-13 (XS3)
    XS_SM_MV02 = 2  # MV-02 (X4)
    XS_SM_RL_LEGACY = 3  # Redlake legacy (HG-2000, CR, TX)
    XS_SM_MAKO = 4  # MAKO (HG100K, LE, TH)
    XS_SM_SIRIUS = 5  # Sirius (X3, M3, Y3)
    XS_SM_ORION = 6  # Orion (X5, M5, Y5, N5)
    XS_SM_ORION_II = 7  # Orion II (Y5, N5)
    XS_SM_NORTH_STAR = 8  # North Star (Y4)
    XS_SM_NORTH_STAR_II = 9  # North Star II (Y4, N4)
    XS_SM_NOZOMI = 10  # Nozomi (Y6)
    XS_SM_PEGASUS = 11  # Pegasus (Y10/O10)
    XS_SM_SIRIUS_II = 12  # Sirius II (O7)
    XS_SM_GEMINI = 13  # Gemini (O9)
    XS_SM_LEO = 14  # Leo (CCM4K)
    XS_SM_STK = 15  # Stick sensor
    XS_SM_RCHD = 16  # R-HD sensor


# Camera Revisions
class XS_REVISION(XSULONG32):
    XS_REV_A = 0
    XS_REV_B = 1
    XS_REV_C = 2
    XS_REV_D = 3
    XS_REV_E = 4
    XS_REV_F = 5
    XS_REV_G = 6
    XS_REV_H = 7
    XS_REV_I = 8
    XS_REV_J = 9


# Miscellaneous capabilities
class XS_MISC_CAPS(XSULONG32):
    XS_CAP_NR = 0x00000001  # the camera is NR
    XS_CAP_NX = 0x00000002  # the camera is NX
    XS_CAP_NXT = 0x00000004  # the camera is NXTra
    XS_CAP_NXA = 0x00000008  # the camera is NXAir
    XS_CAP_DNR2 = 0x00000010  # the camera supports DNR2
    XS_CAP_HWBROC = 0x00000020  # the camera supports HW BROC
    XS_CAP_JPEG = 0x00000040  # the camera supports JPEG
    XS_CAP_1PPS = 0x00000080  # the camera supports 1PPS sync mode (in and out)
    XS_CAP_BATSTS = 0x00000100  # the camera supports battery status read
    XS_CAP_FBCAM = 0x00000200  # the camera is FB cam (Forward Bay Camera)
    XS_CAP_PIV = 0x00000400  # the camera is PIV ready
    XS_CAP_OS = 0x00000800  # the camera is Os (sealed)
    XS_CAP_GPSMOD = 0x00001000  # the camera has internal GPS module
    XS_CAP_INX = 0x00002000  # the camera is iNdustrial camera
    XS_CAP_JPLROC = 0x00004000  # the camera is JPL ROC
    XS_CAP_PTP = 0x00008000  # the camera supports PTP
    XS_CAP_IS1024 = 0x00010000  # the camera is Y4,N4,NR4 or NX4 that supports 1024x1024 resolution (not only 1016x1016)
    XS_CAP_OS3 = 0x00020000  # the camera is Os3 (Os-series version 3)
    XS_CAP_OSA = 0x00040000  # the camera is OsA (Airborne)
    XS_CAP_PLL = 0x00080000  # the camera supports Phase Lock Loop (PLL)
    XS_CAP_IRIGMD = 0x00100000  # the camera has internal IRIG module
    XS_CAP_SDI_FW = 0x00200000  # the camera has a special firmware for SDI


def CAP_IS_NR(c):
    return (c) & XS_CAP_NR


def CAP_IS_NX(c):
    return (c) & XS_CAP_NX


def CAP_IS_NTRA(c):
    return (c) & XS_CAP_NXT


def CAP_IS_NAIR(c):
    return (c) & XS_CAP_NXA


def CAP_IS_FBCAM(c):
    return ((c) & XS_CAP_FBCAM).value


def CAP_IS_OS(c):
    return ((c) & XS_CAP_OS).value


def CAP_IS_INX(c):
    return ((c) & XS_CAP_INX).value


def CAP_IS_ROC(c):
    return ((c) & XS_CAP_JPLROC).value


def CAP_IS_OS3(c):
    return ((c) & XS_CAP_OS3).value


def CAP_IS_OSA(c):
    return ((c) & XS_CAP_OSA).value


# pre config parameters
class XS_PRE_PARAM(XSULONG32):
    XSPP_IP_ADDRESS = 0  # camera IP address
    XSPP_NET_AD_IP = 1  # network adapter IP address (all cameras)
    XSPP_IP_ADD_EX = 2  # camera IP address when the camera is not enumerated
    XSPP_CAM_CMD_PORT = 3  # camera command UDP port (listening)
    XSPP_NET_AD_CMD_PORT = 4  # local application command UDP port (sending)
    XSPP_GET_IP_ADDRESS = 5  # get ip address and network mask (HG only)
    XSPP_DB_FOLDER = 6  # DB folder, for RAW virtual cameras detection
    XSPP_CAM_DFL_GW = 7  # camera Default Gateway
    XSPP_DISABLE_1024 = 8  # disable 1024x1024 resolution on new Y4,N4,NR4,NX4 cameras
    XSPP_REBOOT_FW = 9  # reboot camera firmware
    XSPP_PCIX_DMASIZE = 10  # configure size of DMA buffer of PCIe camera


# camera status
class XS_STATUS(XSULONG32):
    XSST_UNKNOWN = 0  # unknown status
    XSST_IDLE = 1  # the camera is idle (no op)
    XSST_LIVE = 2  # the camera is in live mode (HG-only)
    XSST_REC_PRETRG = 3  # the camera is recording before trigger
    XSST_REC_POSTRG = 4  # the camera is recording after trigger
    XSST_REC_DONE = 5  # the camera has recorded (HG-only)
    XSST_DOWNLOAD = 6  # the camera is downloading (HG-only)
    XSST_DISCONNECT = 7  # the camera is disconnected
    XSST_DWL_SD = 8  # the camera is downloading memory into SD card
    XSST_DWLUPL_SSD = 8  # the camera is downloading/uploading from/to SSD
    XSST_VPB_ON_COFF = 9  # Video Playback is on but HDMI cable is disconnected
    XSST_VPB_ON_CON = 10  # Video Playback is on and HDMI cable is on
    XSST_PLAYBACK = 11  # the camera is in automatic playback mode (Mini HD)


# Exposure mode
class XS_EXP_MODE(XSULONG32):
    XS_EM_SINGLE_EXP = 0  # single exposure
    XS_EM_DOUBLE_EXP = 1  # double exposure
    XS_EM_EDR = 2  # Extended Dynamic Range (Y4,N4 cameras)
    XS_EM_XDR = 3  # eXtended Dynamic Range (all cameras)


# Record mode
class XS_REC_MODE(XSULONG32):
    XS_RM_NORMAL = 0  # Normal mode (fills the memory segment and stop)
    XS_RM_CIRCULAR = 1  # Circular mode (fills the memory segment and restart)
    XS_RM_BROC = 2  # Burst Record On Command (HG-only)
    XS_RM_ROC = 3  # Record On Command (HG-only)
    XS_RM_READY = 4  # Ready (HG-only)


# Sync In configuration (on 2 BNC cameras it configures the trigger also)
class XS_SYNCIN_CFG(XSULONG32):
    # internal
    XS_SIC_INTERNAL = 0  # acquisition is synchronized by internal clock
    # external
    XS_SIC_EXT_EDGE_HI = 1  # acquisition is synchronized by trigger edge
    XS_SIC_EXT_EDGE_LO = 2
    XS_SIC_EXT_PULSE_HI = 3  # acquisition is synchronized pulse size
    XS_SIC_EXT_PULSE_LO = 4
    # IRIG/DTS/STP
    XS_SIC_IRIG_DTS_EXT = (
        5  # acquisition is synced by IRIG GPS signal with external 1pps generation
    )
    XS_SIC_IRIG_DTS_INT = 6  # acquisition is synced by IRIG GPS signal with internal 1pps generation (N-only)
    XS_SIC_1PPS = (
        7  # acquisition is synced by 1PPS signal entering from the sync in connector
    )
    XS_SIC_PTP = 8  # acquisition is synced by Precision Time Protocol
    XS_SIC_EPLL_EDGE_HI = 20  # external edge high - phase lock loop
    XS_SIC_EPLL_EDGE_LO = 21  # external edge low - phase lock loop
    XS_SIC_EDYN_PULSE_HI = 22  # external pulse high - dynammic (pulse width changes)
    XS_SIC_EDYN_PULSE_LO = 23  # external pulse low - dynamic (pulse width changes)


# Sync Out configuration
class XS_SYNCOUT_CFG(XSULONG32):
    XS_SOC_DFL = 0  # default cfg: sync out follows rate and exposure
    XS_SOC_DFL_INV = 1  # the default sync out signal is inverted
    XS_SOC_CFGWID = 2  # the sync out width is configurable
    XS_SOC_CFGWID_INV = (
        3  # the sync out width is configurable and the signal is inverted
    )
    XS_SOC_DISABLED = 4  # the sync out signal is disabled
    XS_SOC_DBLEXP = 5  # sync out reflects the double exposure
    XS_SOC_1PPS = 6  # sync out signal is a 1 PPS signal


# Sync Out alignment
class XS_SYNCOUT_ALIGN(XSULONG32):
    XS_SOA_EXP = 0  # default cfg: sync out is aligned to exposure
    XS_SOA_SYNC_IN = 1  # sync out is aligned to sync-in


# Trigger Configuration (external trigger-in signal on 3 BNC camera models)
class XS_TRIGIN_CFG(XSULONG32):
    XS_TIC_EDGE_HI = 0  # Trigger starts on edge high
    XS_TIC_EDGE_LO = 1  # Trigger starts on egge low
    XS_TIC_SWC = 2  # Trigger starts on switch closure
    XS_TIC_GATE_HI = 3  # Trigger acts as a gate on high level
    XS_TIC_GATE_LO = 4  # Trigger acts as a gate on low level
    XS_TIC_DISABLED = 5  # Trigger is disabled


# Motion Trigger Mode
class XS_MTRIG_CFG(XSULONG32):
    XS_MT_DISABLED = 0  # Motion Trigger disabled
    XS_MT_AVG_CHG = 1  # Trigger if average brightness changes
    XS_MT_AVG_INCR = 2  # Trigger if average brightness increases
    XS_MT_AVG_DECR = 3  # Trigger if average brightness decreases
    XS_MT_MOTION = 4  # Trigger if simple motion is detected (no change of intensity)


# Image format
class XS_IMG_FMT(XSULONG32):
    XS_IF_GRAY8 = 0  # Gray 8: data is bytes
    XS_IF_BAYER8 = 0  # Bayer pattern 8 bit: data is bytes
    XS_IF_GRAY16 = 1  # Gray 16: data is word, LSB aligned
    XS_IF_BAYER16 = 1  # Bayer pattern 16: data is 16 bit word, LSB aligned
    XS_IF_BGR24 = 2  # Windows 24 bit BGR
    XS_IF_BGRA32 = 3  # Windows 32 bit BGRA (A is not used)
    XS_IF_ARGB32 = 4  # MAC 32 bit ARGB (A is not used)
    XS_IF_GRAY8X = 5  # Gray 8 set from RGB
    XS_IF_GRAY16X = 6  # Gray 16 set from RGB
    XS_IF_BGR48 = 7  # Windows 48 bit BGR: each component is 16 bit word, LSB aligned


# color interpolation mode
class XS_CI_MODE(XSULONG32):
    XS_CIM_BILINEAR = 0  # bilinear demosaic
    XS_CIM_ADVANCED = 1  # advanced demosaic
    XS_CIM_AHD = 2  # AHD demosaic


# sensor digital gain
class XS_SENSOR_GAIN(XSULONG32):
    XS_SG_1_00 = 0  # no gain (gain = 1.00)
    XS_SG_1_41 = 1  # sqrt(2) (gain = 1.44)
    XS_SG_2_00 = 2  # 2 (gain = 2.00)
    XS_SG_2_82 = 3  # 2*sqrt(2) (gain = 2.82)


# Pixel Gain
class XS_PIXEL_GAIN(XSULONG32):
    XS_PG_1X = 0  # Bits 2-9 (upper)
    XS_PG_2X = 1  # Bits 1-8 (middle)
    XS_PG_4X = 2  # Bits 0-7 (lower)


# Lookup Table
class XS_LUT(XSULONG32):
    XS_LUT_OFF = 0  # Disabled LUT
    XS_LUT_USER = 1  # User-defined LUT
    XS_LUT_A = 2  # Pre-defined LUT: A
    XS_LUT_B = 3  # Pre-defined LUT: B
    XS_LUT_C = 4  # Pre-defined LUT: C
    XS_LUT_D = 5  # Pre-defined LUT: D
    XS_LUT_E = 6  # Pre-defined LUT: E


# Lut channels mask
class XS_LUT_MASK(XSULONG32):
    XS_LUTMSK_OFF = 0x00000000  # disabled channels
    XS_LUTMSK_R = 0x00000001  # enable red channel
    XS_LUTMSK_G = 0x00000002  # enable green channel
    XS_LUTMSK_B = 0x00000004  # enable blue channel
    XS_LUTMSK_ALL = 0x00000007  # neable all channels


# Binning
class XS_BINNING(XSULONG32):
    XS_BIN_1X1 = 0  # Binning 1x1
    XS_BIN_2X2 = 1  # Binning 2x2
    XS_BIN_3X3 = 2  # Binning 3x3
    XS_BIN_4X4 = 3  # Binning 4x4


# HDMI mode (Y cameras)
class XS_HDMI_MODE(XSULONG32):
    XS_HDMI_OFF = 0  # HDMI is off
    XS_HDMI_ON = (
        1  # HDMI is on, read frame and live are done to both PC and HDMI output)
    )
    XS_HDMI_TRANSFER = 2  # HDMI is on, read fram and live are done to HDMI output only (PC output is disabled)
    XS_HDMI_INDEPENDENT = (
        3  # HDMI is on and independent from PC (new designed cameras only)
    )


# Video Output mode (X,HG legacy,Y and O cameras)
class XS_VIDEO_MODE(XSULONG32):
    XS_VM_X_PAL = 0  # X/HG camera: PAL output
    XS_VM_Y_720P_60HZ = 0  # Y camera: 720p 60 Hz
    XS_VM_X_NTSC = 1  # X/HG camera: NTSC output
    XS_VM_Y_1080_60HZ = 1  # Y camera: 1080p 60 Hz
    XS_VM_O_1080P_50HZ = 1  # O camera: 1080p 50 Hz
    XS_VM_Y_1080_25HZ = 2  # Y camera: 1080p 25 Hz
    XS_VM_O_1080P_30HZ = 2  # O camera: 1080p 30 Hz
    XS_VM_Y_1080_24HZ = 3  # Y camera: 1080p 24 Hz
    XS_VM_O_1080P_25HZ = 3  # O camera: 1080p 25 Hz
    XS_VM_Y_1080_30HZ = 4  # Y camera: 1080p 30 Hz
    XS_VM_O_1080P_24HZ = 4  # O camera: 1080p 24 Hz
    XS_VM_O_720P_60HZ = 5  # O camera: 720p 60 Hz
    XS_VM_O_720P_50HZ = 6  # O camera: 720p 50 Hz
    XS_VM_O_720P_30HZ = 7  # O camera: 720p 30 Hz
    XS_VM_O_720P_25HZ = 8  # O camera: 720p 25 Hz
    XS_VM_O_720P_24HZ = 9  # O camera: 720p 24 Hz


# Video playback modes (Y cameras)
class XS_VIDEO_PB(XSULONG32):
    XS_VPB_OFF = 0  # video playback off
    XS_VPB_FWD = 1  # video playback forward
    XS_VPB_REW = 2  # video playback rewind


# Preview Modes (Y and N/NR/NX cameras)
class XS_PREV_MODE(XSULONG32):
    XS_PM_FULL_RES = 0  # full resolution preview
    XS_PM_LOW_RES = 1  # low resolution preview


# Live commands (Y and Os cameras)
class XS_LIVE(XSULONG32):
    XS_LIVE_STOP = 0  # stop live
    XS_LIVE_START = 1  # start live


# Callback Flag
class XS_CALLBACK_FLAGS(XSULONG32):
    XS_CF_DONE = 1  # the callback is called if the operation is successfull
    XS_CF_FAIL = 2  # the callback is called if the operation is NOT successfull
    XS_CF_CBONLY = 4  # install callback only and do not start grab


# Calibration op codes
class XS_CALIB_OPCODE(XSULONG32):
    XS_C_BKG_ALL = (
        0  # Calibrate background in all conditions (don't overwrite factory file)
    )
    XS_C_FILE_RELOAD = 1  # Load factory calibration file
    XS_C_FILE_DOWNLOAD = 2  # Download calibration file from the camera to the disk
    XS_C_CURRENT_BKG = 3  # Calibrate background in current conditions
    XS_C_CURRENT_PSC = 4  # Calibrate pixel sensitivity correction in current conditions
    XS_C_CURRENT_RESET = 5  # Reset current conditions coefficients and delete file
    XS_C_ABORT = 100  # Abort any of the above procedures


# GE datagram sizes
class XS_DGR_SIZE(XSULONG32):
    XS_DGR_1448 = 0  # default: regular datagram size
    XS_DGR_2888 = 1
    XS_DGR_4328 = 2
    XS_DGR_5768 = 3
    XS_DGR_7208 = 4
    XS_DGR_8648 = 5  # jumbo packet max size


# Post record operation (operation performed after a recording)
class XS_PR_OP(XSULONG32):
    XS_PR_NOTHING = 0  # do nothing
    XS_PR_DWL_SD = 1  # download to SD card in IRIG-Flash module
    XS_PR_SSD_STREAM = 2  # download to SSD in stream mode, synchronous (O-series)
    XS_PR_RESERVED1 = 3  # reserved
    XS_PR_RESERVED2 = 4  # reserved
    XS_PR_SSD_BACKUP = 5  # download to SSD in backup mode, asynchronous (O-series)


# Marker Configuration
class XS_MARKER_CFG(XSULONG32):
    XS_MRK_OFF = 0  # disabled
    XS_MRK_SYNCIN = 1  # enabled on sync in
    XS_MRK_TRIGIN = 2  # enabled on trigger in


# Clock speed
class XS_CLOCK_SPEED(XSULONG32):
    XS_CLS_LOWER = 0  # Lower speed - better image quality
    XS_CLS_MIDDLE = 1  # Middle speed - average image quality
    XS_CLS_HIGHER = 2  # Higher speed - lower image quality


# pre-defined ROI for HD cameras (different meanings)
class XS_HD_ROI(XSULONG32):  #   Y3-HD   * Y5/N5/Os5 * Y3C/N3S1-2 *    Y6     * Os10/O10
    XSHD_RES_00 = 0  # 1920x1080      -           -             -           -
    XSHD_RES_01 = 1  #  1280x720      -           -             -           -
    XSHD_RES_02 = 2  #     -       2560x1920   1504x1128    1600x1200   2560x1600
    XSHD_RES_03 = 3  #     -       2560x1440       -        1920x1080   2560x1440
    XSHD_RES_04 = 4  #     -       2560x1080       -            -       1920x1080
    XSHD_RES_05 = 5  #     -           -           -            -        1280x720


# digital zoom factors for HD cameras
class XS_HD_ZOOM(XSULONG32):
    XSHD_Z_100 = 0  #  1X
    XSHD_Z_125 = 1  #  1.25X
    XSHD_Z_150 = 2  #  1.50X
    XSHD_Z_200 = 3  #  2X
    XSHD_Z_300 = 4  #  3X
    XSHD_Z_400 = 5  #  4X
    XSHD_Z_500 = 6  #  5X
    XSHD_Z_600 = 7  #  6X
    XSHD_Z_700 = 8  #  7X
    XSHD_Z_800 = 9  #  8X
    XSHD_Z_900 = 10  #  9X
    XSHD_Z_1000 = 11  # 10X
    XSHD_Z_1200 = 12  # 12X
    XSHD_Z_1400 = 13  # 14X
    XSHD_Z_1600 = 14  # 16X


# rotation angle
class XS_ROT_ANGLE(XSULONG32):
    XS_ROT_0 = 0
    XS_ROT_90 = 1
    XS_ROT_180 = 2
    XS_ROT_270 = 3


# image flip
class XS_FLIP(XSULONG32):
    XS_FLIP_NONE = 0
    XS_FLIP_HORZ = 1
    XS_FLIP_VERT = 2
    XS_FLIP_BOTH = 3


# JPEG Compression
class XS_JPEG(XSULONG32):
    XS_JPEG_OFF = 0  # disable JPEG
    XS_JPEG_CVT = 1  # enable uncompressed JPEG (JPEG is downloaded from camera and decompressed in the driver)
    XS_JPEG_RAW = (
        2  # enable compressed JPEG (JPEG is downloaded from camera and read from SDK)
    )


# battery status (NX cameras)
class XS_BATTERY(XSULONG32):
    XS_BAT_LEVEL_MASK = 0x000000FF  # battery level mask 0..100
    XS_BAT_STATE_MASK = 0x00000F00  # battery state mask
    XS_BAT_STATE_DISCHARGING = (
        0x00000000  # power supply is not connected, running on battery
    )
    XS_BAT_STATE_CHARGING = 0x00000100  # power supply is connected, battery is charging
    XS_BAT_STATE_FULLY_CHARGED = (
        0x00000200  # power supply is connected, battery is fully charged
    )
    XS_BAT_DISABLED = 0x00008000  # the battery is connected but it's disabled
    XS_BAT_UNKNOWN = (
        0xFFFFFFFF  # no battery installed or problem communicating with battery
    )


# Return Codes
class XS_ERROR(XSULONG32):
    XS_SUCCESS = 0  # OK!!!
    #
    XS_E_GENERIC_ERROR = 1  # Generic error
    #
    XS_E_NOT_SUPPORTED = 2  # Function is not supported for this device
    XS_E_INVALID_VALUE = 3  # Invalid parameter value
    XS_E_INVALID_CFG = 4  # Invalid XS_SETTINGS struct
    XS_E_INVALID_HANDLE = 5  # Invalid XS_HANDLE
    XS_E_INVALID_CAMERA_ID = 6  # Invalid camera id used in XsOpenCamera
    XS_E_INVALID_ARGUMENTS = 7  # Invalid function arguments
    XS_E_READONLY = 8  # the parameter is read-only
    XS_E_CAM_ALREADY_OPEN = 9  # camera is already open
    #
    XS_E_HARDWARE_FAULT = 10  # Hardware fault (severe)
    XS_E_BUSY = 11  # The camera is busy
    XS_E_QUEUE_FULL = 12  # Cannot queue more items, queue is full
    XS_E_BUFFER_TOO_SMALL = 13  # The buffer is too small for an acquisition
    XS_E_TIMEOUT = 14  # Operation time-out
    XS_E_NOT_RECORDING = 15  # the camera is not in record mode
    XS_E_MALLOC = 16  # error allocating memory
    XS_E_ABORTED = 17  # error because a procedure has been aborted
    XS_E_NOT_IN_FLASH = 18  # the requested information is not stored in flash memory
    XS_E_EXP_LICENSE = 19  # the time limited license is expired
    XS_E_W2D_OVERRUN = 20  # write to disk overrun (O-series)
    XS_E_DMA_OVERRUN = 21  # DMA overrun error (PCIe)


# Camera Parameters Index
class XS_PARAM(XSULONG32):
    XSP_GAIN = 0  # Camera sensor gain
    XSP_EXPOSURE = 1  # Exposure in nanoseconds
    XSP_IMG_FORMAT = 2  # Image format (See XS_IMG_FMT)
    XSP_PIX_DEPTH = 3  # Pixel depth: 8 to 36
    XSP_PIX_GAIN = 4  # Pixel gain (see XS_PIXEL_GAIN)
    XSP_SYNCIN_CFG = 5  # Trigger mode (see XS_SYNCIN_CFG)
    XSP_REC_MODE = 6  # Trigger Source (see XS_REC_MODE)
    XSP_EXP_MODE = 7  # Exposure Mode (see XS_EXP_MODE)
    XSP_BINNING = 8  # Binning (See XS_BINNING)
    XSP_CI_MODE = 9  # Color interpolation mode (see XS_CI_MODE)
    XSP_TRIGIN_CFG = 10  # trigger in configuration (see XS_TRIGIN_CFG)
    #
    XSP_MAX_WIDTH = 11  # Maximum image width
    XSP_MAX_HEIGHT = 12  # Maximum image height
    XSP_ROIX = 13  # Upper left X of ROI
    XSP_ROIY = 14  # Upper left Y of ROI
    XSP_ROIWIDTH = 15  # Width of ROI, in pixels
    XSP_ROIHEIGHT = 16  # Height of ROI, in pixels
    XSP_PERIOD = 17  # acquisition period in nanoseconds (inverse of rate)
    XSP_PERIOD_MIN = 18  # computes the minimum acquisition period in the current cfg (inverse of max rate)
    XSP_IRIG = 19  # enables/disables IRIG
    XSP_SYNCOUT_CFG = 20  # sync out cfg (see XS_SYNCOUT_CFG)
    XSP_TRIGIN_DEB = 21  # trigger in debounce lenght [ns]
    XSP_TRIGIN_DEL = 22  # trigger in delay [ns]
    XSP_SYNCOUT_WID = 23  # sync out width [ns]
    XSP_SYNCOUT_DEL = 24  # sync out delay [ns]
    XSP_SYNCIN_DEB = 25  # sync in debounce lenght [ns]
    XSP_SYNCIN_DEL = 26  # sync in delay [ns]
    XSP_HDMI_MODE = 27  # HDMI output mode (see XS_HDMI_MODE)
    XSP_PREV_MODE = 28  # preview mode (0:full res 1:1/4th of res)
    #
    XSP_NOISE_RED = 30  # background noise removal (from factory calibration file)
    XSP_NOISE_SENS = 31  # pixel sensitivity correction (from factory calibration file)
    XSP_NOISE_DKCOL = 32  # use dark columns to reduce noise
    XSP_NOISE_AUTO = 33  # auto calibration background (from current conditions)
    #
    XSP_VIDEO_MODE = 34  # Video mode (0:PAL 1:NTSC) or HDMI (0:1280x720p 1:1920x1080p 2:1280x720p decimated)
    XSP_NET_PERFORM = 35  # network performance
    XSP_PLUS = 36  # plus mode (double speed)
    XSP_GAMMA = 37  # gamma correction (0..30)
    XSP_FRAMES = 38  # acquired frames (latest acquisition)
    XSP_PRE_TRIG = 39  # acquired pre-trig frames (latest acquisition)
    XSP_BROC_LEN = 40  # BROC lenght (HG-only)
    XSP_FRAME_CAP = 41  # Frame capacity in current conditions
    XSP_1ST_FRM_IDX = 42  # Index of first frame (latest acquisition)
    XSP_STARTADDRLO = 43  # Latest acquisition's address (low part)
    XSP_STARTADDRHI = 44  # Latest acquisition's address (high part)

    XSP_NOISE_APSC = 45  # auto PSC (from current conditions)

    XSP_EXT_PERIOD = 46  # External sync period in nanoseconds (read-only)
    XSP_EXT_PULSE_WIDTH = 47  # External sync pulse width in nanoseconds (read-only)
    XSP_CMP_RATIO = 48  # compression ratio (40% to 100%, N cameras only)
    XSP_FRAME_SIZE = 49  # frame size in camera memory [bytes]
    XSP_EXPOSURE_MAX = 50  # max allowed exposure in current conditions [ns] (read-only)
    XSP_EXPOSURE_DBL = 51  # value of second exposure in dbl exp mode

    XSP_XDR_RATIO = 52  # XDR ratio (2 to 8)
    XSP_XDR_CONTRAST = 53  # XDR contrast (1 to 100)
    XSP_DYNAMIC_NR = 54  # dynamic noise reduction [0 to 30] dfl = camera dependent
    XSP_SHARPEN = 55  # sharpening [0 to 10] dfl = 0
    XSP_BRIGHTNESS = 56  # brightness [0 to 50] dfl = 25
    XSP_CONTRAST = 57  # contrast [0 to 20] dfl = 10
    XSP_HUE = 58  # hue [0 to 360] dfl = 180
    XSP_SATURATION = 59  # saturation [0 to 20] dfl = 10

    XSP_WB_11 = 60  # White Balance Matrix value 1,1 (Blue Gain)
    XSP_WB_12 = 61  # White Balance Matrix value 1,2
    XSP_WB_13 = 62  # White Balance Matrix value 1,3
    XSP_WB_21 = 63  # White Balance Matrix value 2,1
    XSP_WB_22 = 64  # White Balance Matrix value 2,2 (Green Gain)
    XSP_WB_23 = 65  # White Balance Matrix value 2,3
    XSP_WB_31 = 66  # White Balance Matrix value 3,1
    XSP_WB_32 = 67  # White Balance Matrix value 3,2
    XSP_WB_33 = 68  # White Balance Matrix value 3,3 (Red Gain)

    XSP_BOARD_TEMP = (
        69  # board temperature in hundreds of deg C (Y-redesigned cameras only)
    )

    XSP_MT_CFG = 70  # Motion Trigger mode (see XS_MTRIG_CFG)
    XSP_MT_THRESHOLD = 71  # Motion Trigger threshold
    XSP_MT_ROIX = 72  # Upper left X of Motion Trigger ROI
    XSP_MT_ROIY = 73  # Upper left Y of Motion Trigger ROI
    XSP_MT_ROIWIDTH = 74  # Width of Motion Trigger ROI, in pixels
    XSP_MT_ROIHEIGHT = 75  # Height of Motion Trigger ROI, in pixels

    XSP_DGR_SIZE = 76  # Configurable Datagram size (GE only)

    XSP_AE_ENABLE = 77  # enable auto-exposure (0-1)
    XSP_AE_ROIX = 78  # Auto-exposure RO - X origin
    XSP_AE_ROIY = 79  # Auto-exposure RO - Y origin
    XSP_AE_ROIWIDTH = 80  # Auto-exposure RO - Width
    XSP_AE_ROIHEIGHT = 81  # Auto-exposure RO - Height
    XSP_AE_REFERENCE = 82  # luminance reference [20..200]
    XSP_AE_SPEED = 83  # Auto-exposure speed (reaction to intensity change)
    XSP_AE_EXPOSURE = 84  # read the current value of exposure (read-only)

    XSP_PROP = 85  # Post recording operation (see XS_PR_OP);
    XSP_PROP_WR_BLK = 86  # Post rec Op: blocks of 512 bytes to write in the device (SD card, Net disk)
    XSP_PROP_ABORT = (
        87  # Post rec Op: if the value is non 0, the Post-Rec opearation is aborted.
    )

    XSP_SYNCOUT_ALIGN = 88  # sync out align (see XS_SYNCOUT_ALIGN)
    XSP_MARKER_CFG = 89  # enable marker (see XS_MARKER_CFG)
    XSP_MARKER_VAL = 90  # return current marker value (0 or 1)
    XSP_CI_THR = 91  # color interpolation threshold
    XSP_CLOCK_SPEED = 92  # clock speed read-only (see XS_CLOCK_SPEED)
    XSP_HD_ROI = 93  # pre-defined ROI for HD cameras (see XS_HD_ROI)
    XSP_GAUSS_FLT = 94  # Gaussian Filter
    XSP_ROT_ANGLE = 95  # rotation angle (see XS_ROT_ANGLE)
    XSP_FLIP = 96  # image flip (see XS_FLIP)
    XSP_LUT = 97  # Lookup Table (see XS_LUT)
    XSP_LUT_CHN_MASK = 98  # Lookup Table RGB channels mask (see XS_LUT_MASK)

    XSP_HDMI_OVERLAY = 99  # Enable HDMI overlay (0=Disable, 1=Enable)
    XSP_WBTBL_TEMP = 100  # color balance table temperature (for display on HDMI)
    XSP_HD_ZOOM = 101  # digital zoom for HD cameras (see XS_HD_ZOOM)
    XSP_HD_ZOOM_X = 102  # X coord of origin in digital zoom
    XSP_HD_ZOOM_Y = 103  # Y coord of origin in digital zoom
    XSP_SHARPEN_THR = 104  # sharpening threshold
    XSP_SYNCIN_INV = 105  # Sync in polarity inversion
    XSP_DYNAMIC_NR2 = 106  # additional dynamic noise reduction [0 to 30]
    XSP_JPEG = 107  # Enable/Disable JPEG compression
    XSP_IMG_ZOOM = 108  # image zoom (resize image factor)
    XSP_IMG_ZOOM_WID = 109  # image width after zoom (read only)
    XSP_IMG_ZOOM_HGT = 110  # image height after zoom (read only)
    XSP_AE_CUR_LUMA = 111  # Calculates current luma in AE window (read only - the camera must be in rec mode)
    XSP_BROC_TOT_LEN = 112  # Broc total number of frames
    XSP_BROC_CURR_SECT = 113  # Current recording BROC section index (read-only)
    XSP_HD_ZOOM_2R = 114  # Disable magnification and take ROI
    XSP_FRAME_SIZE_IMG = 115  # Size of a frame if saved to disk as image (read-only)
    XSP_SYNC_COUNT = 116  # total number of sync counts in latest acquisition
    XSP_AE_MIN_EXP = 117  # set the value of min exposure in Auto-Exposure mode
    XSP_AE_MAX_EXP = 118  # set the value of max exposure in Auto-Exposure mode
    XSP_BATTERY_STATUS = (
        119  # battery status (see XS_BATTERY, read-only, NX cameras only)
    )
    XSP_JPEG_QUAL = 120  # jpeg quality (1 to 100, dfl 90)
    XSP_SSD_STRM_PER = 121  # inverse of maximum streaming speed to SSD (O-series)
    XSP_SSD_MAX_FRMS = (
        122  # max number of frames that can be stored in SSD without overrun
    )
    XSP_GAMMA_LEVEL = 123  # Gamma Level
    XSP_GAMMA1 = 124  # Gamma 1
    XSP_GAMMA_LEVEL1 = 125  # Gamma level 1
    XSP_MISS_STEP_CNT = (
        126  # Number of mission steps that have been configured (readonly)
    )
    XSP_EXEC_STEP_CNT = (
        127  # Number of mission steps that have been executed (readonly)
    )
    XSP_EXT_FREQ = 128  # External sync frequency [Hz] (read-only)
    XSP_SSD_WRITE_PERC = 129  # Percentage of data written in the SSD
    XSP_RAW_RD_TSTAMP = 130  # Enable fast read of time stamp from RAW data
    XSP_NET_SPEED = 131  # Network speed for HG (0:automatic, 1:100Mbps, 2:1000 Mbps)
    XSP_AE_EXP_STEP = 132  # Auto-exposure step size (exposure change)
    XSP_SYNCIN_JITTER = 133  # sync in jitter in external pll mode
    XSP_SYNCIN_DIV = 134  # sync in period divider/freq multiplier in external pll mode
    XSP_IRIG_GPS_JITT = 135  # jitter tolarance for IRIG/GPS
    XSP_LENS_POSITION = 136  # lens position (16 bit)
    XSP_IRIS_POSITION = 137  # iris position (16 bit)
    XSP_RAW_MIN_IDX = 138  # index of first frame in a raw sequence
    XSP_SHOCK_THR = 139  # Impact sensor shock threshold level (in multiples of 0.016 g)
    XSP_SHOCK_TIME = (
        140  # Impact sensor shock maximum duration (in multiples of 744 us)
    )
    XSP_LATEST_FRM_IDX = 141  # index of the latest acquired frame (read-only)
    XSP_ZOOM_POSITION = 142  # zoom position in motorized lens
    XSP_PAINT_GAIN_R = 143  # Paint parameter: Gain - R component
    XSP_PAINT_GAIN_G = 144  # Paint parameter: Gain - G component
    XSP_PAINT_GAIN_B = 145  # Paint parameter: Gain - B component
    XSP_PAINT_OFFS_R = 146  # Paint parameter: Offset - R component
    XSP_PAINT_OFFS_G = 147  # Paint parameter: Offset - G component
    XSP_PAINT_OFFS_B = 148  # Paint parameter: Offset - B component
    XSP_DEFLICKER = 149  # Deflicker
    XSP_PTP_MODE = 150  # PTP mode (0:ethernet 1:UDP)
    XSP_DEFLICKER_THR = 151  # Deflicker Threshold


# attribute types
class XS_ATTRIBUTE(XSULONG32):
    XS_ATTR_MIN = 0  # minimum value of the attribute
    XS_ATTR_MAX = 1  # maximum value of the attribute
    XS_ATTR_READONLY = 2  # the attribute is read-only
    XS_ATTR_DEFAULT = 3  # the default value of the parameter


# info values
class XS_INFO(XSULONG32):
    # general
    XSI_CAMERA_MODEL = 0  # Camera Model (see XS_CAM_MODEL)
    XSI_CAMERA_ID = 1  # Camera ID (see XS_ENUMITEM)
    XSI_FW_VERSION = 2  # EEPROM Firmware version
    XSI_MEMORY = 3  # Amount of memory installed on the camera [pixels]
    XSI_REC_SIZE_SELECTABLE = 4  # User can select amount of memory to be recorded
    XSI_COOLED = 5  # the camera is cooled
    XSI_SERIAL = 6  # serial number
    XSI_REVISION = 7  # camera revision (A, B, C, etc.)
    XSI_DACS_COUNT = 8  # number of Digital to Analog Converters
    XSI_INT_CLOCK = 9  # internal clock rate in Hz
    XSI_EXTRA_ROWS = 10  # extra rows in read-out
    XSI_ROW_CLOCKS = 11  # number of clocks for each row readout
    XSI_SNS_TYPE = 12  # Sensor type (see XS_SNS_TYPE)
    XSI_SNS_MODEL = 13  # Sensor model (see XS_SNS_MODEL)
    XSI_SNS_WIDTH = 14  # Sensor Maximum width [pixels]
    XSI_SNS_HEIGHT = 15  # sensor Maximum height [pixels]
    XSI_CFW_VERSION = 16  # Controller Firmware Version
    XSI_LIVE_WHILE_REC = 17  # the camera supports Live while record
    XSI_SOFT_TRIGGER = 18  # the camera supports software trigger
    XSI_FCAL_FILE_ON = 19  # the factory calibration file is installed on the hard disk
    XSI_IRIG = 20  # the camera supports IRIG
    XSI_BNC_CONNECTORS = 21  # the number of BNC connectors on camera (2 or 3)
    XSI_EXP_STEPS = 22  # number of exposure steps
    XSI_INTENSIFIED = 23  # the camera is intensified
    XSI_LINK = 24  # the camera link (USB 2.0, GEthernet)
    XSI_MIN_EXP = 25  # minimum exposure (1 us or 100 ns)
    XSI_CFW_CLK_0 = 26  # controller firmware clock 0 value
    XSI_CFW_CLK_1 = 27  # controller firmware clock 1 value
    XSI_INT_REG_0 = 28  # camera internal register 0 (model-dependent)
    XSI_INT_REG_1 = 29  # camera internal register 1 (model-dependent)
    XSI_LIGHT = 30  # the camera is light (reduced capabilities)
    XSI_GIGA_ETHERNET = 31  # the camera has Giga-ethernet support
    XSI_FLASH_MEMORY = 32  # internal flash memory size (MB)
    XSI_VIDEO_MODE = 33  # the camera supports video mode
    XSI_PLUS = 34  # the camera supports the plus mode (double speed)
    XSI_CAMERA_NAME = 35  # camera name (string)
    XSI_LINK_FW_VER = 36  # Link (USB/GE firmware version)
    XSI_CFW2_VERSION = 37  # Second Controller Firmware Version
    XSI_ROI_MIN = 38  # Minimum allowed ROI (X, Y)
    XSI_ROI_STEP = 39  # ROI Step size (X,Y)
    XSI_FG_TYPE = 40  # Frame grabber type (see XS_FG_TYPE)
    XSI_CCAL_FILE_ON = (
        41  # the calibration file with current conditions is installed on the hard disk
    )
    XSI_FCAL_FILE_FLASH = (
        42  # the factory calibration file is stored in camera flash memory
    )
    XSI_CAL_PATH = 43  # path to the camera calibration files folder (directory)
    XSI_CFA_PATTERN = 44  # CFA Bayer pattern of color sensor (see XS_CFA_PATTERN)
    XSI_MAX_FRM_SIZE = 45  # Maximum frame size in camera memory (or computer) [bytes]
    XSI_NEW_DESIGN = (
        46  # The camera hardware is redesigned (with internal image processing)
    )
    XSI_CAL_NAME = 47  # the camera calibration file name
    XSI_MOTION_TRIG = 48  # the camera supports motion trigger
    XSI_WRITE_2_DISK = 49  # the camera supports direct write to disk (M2D only)
    XSI_COMPRESSION = 50  # the camera supports data compression (N cameras)
    XSI_DGR_SIZE = 51  # the camera supports configurable datagram size
    XSI_AUTO_EXPOSURE = 52  # the camera supports the auto exposure
    XSI_POST_REC_OP = (
        53  # the camera supports post-recording operation (write to SD card)
    )
    XSI_MARKER = 54  # the camera supports the marker option
    XSI_SUB_MODEL = 55  # the camera sub-model
    XSI_SNS_PIX_DEPTH = 56  # the sensor pixel depth (12,10 or 8)
    XSI_XDR_SUPPORT = 57  # the camera supports XDR
    XSI_EDR_SUPPORT = 58  # the camera supports EDR
    XSI_LIVE_BUF_SIZE = 59  # minimum buffer in camera memory to avoid overwrite of acquisition during live
    XSI_RESIZE = 60  # the camera supports image resize for fast thumbnail live.
    XSI_HW_BOARDS = (
        61  # number of boards in hardware configuration (0 if not supported)
    )
    XSI_HW_INFO = 62  # information about boards of Hw configuration ()
    XSI_TNR_SUPPORT = 63  # the camera supports TNR
    XSI_PIV_READY = (
        64  # the camera is PIV ready (timing signals on the status connector)
    )
    XSI_CUR_CAL = 65  # the camera supports the current conditions calibration procedure
    XSI_JPEG_SUPPORT = 66  # the camera supports JPEG compression on images
    XSI_DNR2_SUPPORT = 67  # the camera support TNR and DNR together
    XSI_HW_BROC_SUPPORT = 68  # the camera support HW BROC
    XSI_ASYNC_VIDEO_PB = 69  # the camera supports asynchronous video (HDMI) playback
    XSI_EX_ROI_CNT = 70  # number of extended ROI the camera supports
    XSI_EX_ROI_MAX_WID = 71  # extended ROI maximum width
    XSI_EX_ROI_MAX_HGT = 72  # extended ROI maximum height
    XSI_1PPS_SYNC_SUPPORT = 73  # the camera suports the 1 PPS on sync in and sync out
    XSI_BATTERYSTS_SUPPORT = 74  # the camera supports battery status and level readout
    XSI_SSD_SIZE = 75  # size of onboard SSD
    XSI_FAST_LIVE = 76  # the camera supports the XsLive routine for fast live display
    XSI_PTP_SUPPORT = 77  # the camera supports PTP
    XSI_TEMP_SUPPORT = 78  # the camera supports temperature read [hundreds of deg C]
    XSI_CI_THR_SUPPORT = (
        79  # the camera supports the Color Interpolation threshold value
    )
    XSI_SI_PLL_SUPPORT = 80  # the camera supports Phase lock loop sync in
    XSI_SI_DPULSE_SUPPORT = 81  # the camera supports dynamic pulse sync in
    XSI_LENS_SUPPORT = 82  # the camera supports motorized lens control
    XSI_BATTERY_INFO = 83  # battery information (manufacturing date)
    XSI_SHOCK_SNS_SUPPORT = 84  # impact shock sensor
    XSI_PAINT_SUPPORT = 85  # the camera supports paint parameters (gain/offset)
    XSI_DEFLICKER_SUPPORT = 86  # the camera supports deflicker
    XSI_PTP_MODE_SUPPORT = 87  # the camera supports PTP mode configuration

    # USB specific
    XSI_USB_VID = 100  # USB vendor ID
    XSI_USB_PID = 101  # USB product ID
    XSI_USB_PORT = 102  # USB port number

    # Gigabit Ethernet specific
    XSI_GE_CAM_MACADD = 200  # camera MAC address
    XSI_GE_CAM_IPADD = 201  # camera IP address
    XSI_GE_ADP_MACADD = 202  # adapter MAC address
    XSI_GE_ADP_IPADD = 203  # adapter IP address
    XSI_GE_ADP_NETMASK = 204  # adapter network mask
    XSI_GE_CAM_NETMASK = 205  # camera network mask
    XSI_GE_ADP_MTU = 206  # adapter MTU


###############################################################################
# Data structures and types

# camera object handle
class XS_HANDLE(ctypes.c_void_p):
    def __repr__(self):
        return self.__class__.__name__ + "(" + hex(self.value) + ")"


# Camera Enumeration Item
class XS_ENUMITEM(ctypes.Structure):
    _fields_ = [
        ("cbSize", XSULONG32),  # size of this structure
        # general
        ("nCameraId", XSULONG32),  # camera ID
        ("nCameraModel", XSULONG32),  # camera model (XS-3, etc.)
        ("nSensorType", XSULONG32),  # sensor type (monochrome/color)
        ("nSensorModel", XSULONG32),  # sensor model (XS-3, etc.)
        ("nSerial", XSULONG32),  # serial number
        ("nRevision", XSULONG32),  # camera revision
        ("nEFWVersion", XSULONG32),  # EEPROM Firmware version
        ("nCFWVersion", XSULONG32),  # controller Firmware version
        ("bIsOpen", XSULONG32),  # 1 if already open
        ("nLinkType", XSULONG32),  # link type (USB 2.0, Giga-Ethernet, Camera-Link)
        ("bIRIG", XSULONG32),  # the camera has IRIG
        ("bIntensified", XSULONG32),  # the camera is intensified
        ("nIntClock", XSULONG32),  # internal clock frequency [Hz]
        ("nLicInfo", XSULONG32),  # License information
        ("nSubModel", XSULONG32),  # camera sub-model
        ("bEDR", XSULONG32),  # the camera supports EDR
        ("nMinExp", XSULONG32),  # minimum allowed exposure in ns (1000 or 100)
        ("nGeAdpMTU", XSULONG32),  # Network Adapter maximum transmission unit
        ("nMiscCaps", XSULONG32),  # miscellaneous capabilities (see XS_MISC_CAPS)
        (
            "bDgrSize",
            XSULONG32,
        ),  # the camera supports configurable datagram size (jumbo packets)
        (
            "bNewDesign",
            XSULONG32,
        ),  # the camera is redesigned (Y with on-board image processing)
        ("bLight", XSULONG32),  # the camera is alight version (reduced capabilities)
        ("bPlus", XSULONG32),  # the camera is a plus model (double speed)
        ("bGigaEth", XSULONG32),  # the camera has Giga-ethernet link (and USB 2.0)
        # USB-specific
        ("nUsbVID", XSULONG32),  # Vendor ID
        ("nUsbPID", XSULONG32),  # Product ID
        ("nUsbPort", XSULONG32),  # USB port number
        # gigabit ethernet specific
        ("nGeCamMACAddLo", XSULONG32),  # Camera MAC address (low part)
        ("nGeCamMACAddHi", XSULONG32),  # Camera MAC address (high part)
        ("nGeCamIPAdd", XSULONG32),  # Camera IP address
        ("nGeCamNetMask", XSULONG32),  # Camera subnet mask
        ("nGeCamDfltGw", XSULONG32),  # Camera default gateway
        ("nGeCamCmdPort", XSULONG32),  # Camera Command UDP Port
        ("nGeAdpMACAddLo", XSULONG32),  # Adapter MAC address (low part)
        ("nGeAdpMACAddHi", XSULONG32),  # Adapter MAC address (high part)
        ("nGeAdpIPAdd", XSULONG32),  # Adapter IP address
        ("nGeAdpNetMask", XSULONG32),  # Adapter subnet mask
        ("szCameraName", ctypes.c_char * L_CAMNAME),  # camera name
        ("nCFW2Version", XSULONG32),  # second controller Firmware version
        # camera link specific
        ("nFGType", XSULONG32),  # frame grabber type (see XS_FG_TYPE)
        # Hardware config info
        ("nCFW3Version", XSULONG32),  # controller Firmware version 3 (build number)
        ("nCFAPattern", XSULONG32),  # Color filter array pattern (see XS_CFA_PATTERN)
        ("nSSDSizeLo", XSULONG32),  # SSD size (lo word)
        ("nSSDSizeHi", XSULONG32),  # SSD size (hi word)
        ("nBatteryInfo", XSULONG32),  # Battery info (production date)
        ("anFill", XSULONG32 * 12),  # fill parameters, for future use
    ]

    def __init__(self):
        super(self.__class__, self).__init__()
        self.cbSize = ctypes.sizeof(self)


PXS_ENUMITEM = ctypes.POINTER(XS_ENUMITEM)


# Camera opaque configuration structure
class XS_SETTINGS(ctypes.Structure):
    _fields_ = [
        ("cbSize", XSULONG32),  # size of this structure
        ("nData", XSULONG32 * 255),  # reserved data array
    ]

    def __init__(self):
        super(self.__class__, self).__init__()
        self.cbSize = ctypes.sizeof(self)


PXS_SETTINGS = ctypes.POINTER(XS_SETTINGS)

#
# For calls to Grab routines
#
# These fields must be filled before the Api call:
#        pBuffer
#        nBufSize
#        nImages
#
# These fields are set by the dll during the Api call:
#        nFormat
#        nWidth
#        nHeight
#        nBitDepth
#        nErrorCode
#
class XS_FRAME(ctypes.Structure):
    _fields_ = [
        ("pBuffer", ctypes.c_void_p),  # Image buffer, 4-byte aligned
        ("nBufSize", XSULONG32),  # Length of buffer, in BYTES
        ("nImages", XSULONG32),  # 1 in single exposure, 2 in double exposure
        ("nFormat", XSULONG32),  # Image Format
        ("nWidth", XSULONG32),  # Image width [pels]
        ("nHeight", XSULONG32),  # Image height [pels]
        ("nPixDepth", XSULONG32),  # Pixel depth
        ("nErrorCode", XSULONG32),  # XS_ERROR code for this frame
    ]


PXS_FRAME = ctypes.POINTER(XS_FRAME)

# XsGetBrocparameters BROC section
class XS_BROC_SECTION(ctypes.Structure):
    _fields_ = [
        ("nStartAddrLo", XSULONG32),  # section start address (LSW)
        ("nStartAddrHi", XSULONG32),  # section start address (MSW)
        ("n1stFrmIdx", XSULONG32),  # index of first frame
        ("nTrgTime", XSULONG32),  # time from trigger
    ]


PXS_BROC_SECTION = ctypes.POINTER(XS_BROC_SECTION)

# BROC array of sections
class XS_BROC(ctypes.Structure):
    _fields_ = [("nData", XSULONG32 * 1024)]  # array of 256*4 uint


PXS_BROC = ctypes.POINTER(XS_BROC)

# GPS/IRIG structure
class XS_GPSTIMING(ctypes.Structure):
    _fields_ = [
        ("nSignalPresent", XSULONG32),
        ("nYear", XSULONG32),
        ("nDayOfYear", XSULONG32),
        ("nHours", XSULONG32),
        ("nMinutes", XSULONG32),
        ("nSeconds", XSULONG32),
        ("nMicroSeconds", XSULONG32),
        ("nFlags", XSULONG32),
    ]


PXS_GPSTIMING = ctypes.POINTER(XS_GPSTIMING)

###############################################################################
# Callback prototype

XS_AsyncCallback = CALLBACK_TYPE(
    None,  # No return is expected from callback
    ctypes.c_void_p,  # User defined variable
    XS_ERROR,  # Error code
    XSULONG32,  # Combination of XS_CALLBACK_FLAGS
)

XS_ProgressCallback = CALLBACK_TYPE(
    None,  # No return is expected from callback
    ctypes.c_void_p,  # User defined variable
    XSULONG32,  # Current progress count
    XSULONG32,  # Total progess count
)

# announcements callback
XS_AnnouncementCallback = CALLBACK_TYPE(
    None,  # No return is expected from callback
    ctypes.c_void_p,  # User defined variable
    ctypes.c_char_p,  # Announcements string
)

###############################################################################
# Auxilary functions

# convert an IP address string into a 32 bit number
def _ip_param_to_num(ip_param):
    if type(ip_param) == types.StringType:
        ip = ip_param.split(".")
        return (int(ip[3]) << 24) | (int(ip[2]) << 16) | (int(ip[1]) << 8) | int(ip[0])
    else:
        return int(ip_param)


###############################################################################
# Error management

# check if any error occured
def _xs_error_check(result, func=None, args=None):
    if result:
        if type(result) == XS_ERROR:
            raise CameraError.Create(result.value)
        else:
            raise CameraError.Create(result)


class CameraError(Exception):
    error_code_details = {}  # TBD later in the code

    def __init__(self, code):
        self.code = code
        if self.error_code_details.has_key(code):
            descr = self.error_code_details[code][1]
        else:
            descr = "Unknown error type"
        super(CameraError, self).__init__(descr)

    @classmethod
    def Create(cls, code):
        if cls.error_code_details.has_key(code):
            return cls.error_code_details[code][0](code)
        else:
            return cls(code)


class XS_SUCCESS(CameraError):
    pass


class XS_E_GENERIC_ERROR(CameraError):
    pass


class XS_E_NOT_SUPPORTED(CameraError):
    pass


class XS_E_INVALID_VALUE(CameraError):
    pass


class XS_E_INVALID_CFG(CameraError):
    pass


class XS_E_INVALID_HANDLE(CameraError):
    pass


class XS_E_INVALID_CAMERA_ID(CameraError):
    pass


class XS_E_INVALID_ARGUMENTS(CameraError):
    pass


class XS_E_READONLY(CameraError):
    pass


class XS_E_CAM_ALREADY_OPEN(CameraError):
    pass


class XS_E_HARDWARE_FAULT(CameraError):
    pass


class XS_E_BUSY(CameraError):
    pass


class XS_E_QUEUE_FULL(CameraError):
    pass


class XS_E_BUFFER_TOO_SMALL(CameraError):
    pass


class XS_E_TIMEOUT(CameraError):
    pass


class XS_E_NOT_RECORDING(CameraError):
    pass


class XS_E_MALLOC(CameraError):
    pass


class XS_E_ABORTED(CameraError):
    pass


class XS_E_NOT_IN_FLASH(CameraError):
    pass


class XS_E_EXP_LICENSE(CameraError):
    pass


CameraError.error_code_details = {
    XS_ERROR.XS_SUCCESS: (XS_SUCCESS, "OK"),
    #
    XS_ERROR.XS_E_GENERIC_ERROR: (XS_E_GENERIC_ERROR, "Generic error"),
    #
    XS_ERROR.XS_E_NOT_SUPPORTED: (
        XS_E_NOT_SUPPORTED,
        "Function is not supported for this device",
    ),
    XS_ERROR.XS_E_INVALID_VALUE: (XS_E_INVALID_VALUE, "Invalid parameter value"),
    XS_ERROR.XS_E_INVALID_CFG: (XS_E_INVALID_CFG, "Invalid XS_SETTINGS struct"),
    XS_ERROR.XS_E_INVALID_HANDLE: (XS_E_INVALID_HANDLE, "Invalid XS_HANDLE"),
    XS_ERROR.XS_E_INVALID_CAMERA_ID: (
        XS_E_INVALID_CAMERA_ID,
        "Invalid camera id used in XsOpenCamera",
    ),
    XS_ERROR.XS_E_INVALID_ARGUMENTS: (
        XS_E_INVALID_ARGUMENTS,
        "Invalid function arguments",
    ),
    XS_ERROR.XS_E_READONLY: (XS_E_READONLY, "the parameter is read-only"),
    XS_ERROR.XS_E_CAM_ALREADY_OPEN: (XS_E_CAM_ALREADY_OPEN, "camera is already open"),
    #
    XS_ERROR.XS_E_HARDWARE_FAULT: (XS_E_HARDWARE_FAULT, "Hardware fault"),
    XS_ERROR.XS_E_BUSY: (XS_E_BUSY, "The camera is busy"),
    XS_ERROR.XS_E_QUEUE_FULL: (
        XS_E_QUEUE_FULL,
        "Cannot queue more items, queue is full",
    ),
    XS_ERROR.XS_E_BUFFER_TOO_SMALL: (
        XS_E_BUFFER_TOO_SMALL,
        "The buffer is too small for an acquisition",
    ),
    XS_ERROR.XS_E_TIMEOUT: (XS_E_TIMEOUT, "Operation time-out"),
    XS_ERROR.XS_E_NOT_RECORDING: (
        XS_E_NOT_RECORDING,
        "the camera is not in record mode",
    ),
    XS_ERROR.XS_E_MALLOC: (XS_E_MALLOC, "error allocating memory"),
    XS_ERROR.XS_E_ABORTED: (XS_E_ABORTED, "error because a procedure has been aborted"),
    XS_ERROR.XS_E_NOT_IN_FLASH: (
        XS_E_NOT_IN_FLASH,
        "the requested information is not stored in flash memory",
    ),
    XS_ERROR.XS_E_EXP_LICENSE: (
        XS_E_EXP_LICENSE,
        "the time limited license is expired",
    ),
}

###############################################################################
# Function prototypes

# *****************************************************************************
# *
# *  XsGetVersion
# *
# * Descr: Read the version of the SDK.
# *
# * Ret:   Tuple (pVersionMS, pVersionLS, pIsDemo)
# *        pVersionMS: the most significant 32 bit of the version number
# *        pVersionLS: the least significant 32 bit of the version number
# *        pIsDemo: if the driver is demo the returned value is 1, otherwise 0
# *
# * Exception:
# *        XS_E_GENERIC_ERROR: Could not extract version numbers from the driver.
# *
# *****************************************************************************
#
def XsGetVersion():
    pVersionMS = PXSULONG32(XSULONG32())
    pVersionLS = PXSULONG32(XSULONG32())
    pIsDemo = PXSULONG32(XSULONG32())
    error = XStreamDrv.XsGetVersion(pVersionMS, pVersionLS, pIsDemo)
    _xs_error_check(error)
    return (
        pVersionMS.contents.value,
        pVersionLS.contents.value,
        pIsDemo.contents.value,
    )


# *****************************************************************************
# *
# *  XsLoadDriver
# *
# * Descr: Loads the camera driver
# *
# * Param: nUSBNotify: activates or deactivates the USB notification
# *
# * Ret:   None
# *
# * Exception:
# *        XS_E_DRIVER_ALREADY_LOADED: the driver is already loaded
# *        XS_E_OUT_OF_MEMORY: could not allocate enough memory for the driver
# *        XS_E_NO_DRIVER: the driver could not be found.
# *        XS_E_HARDWARE_FAULT: error using usb driver (SEVERE error)
# *
# *****************************************************************************
#
def XsLoadDriver(nUSBNotify):
    error = XStreamDrv.XsLoadDriver(nUSBNotify)
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsUnloadDriver
# *
# * Descr: Closes the Driver and releases any resources used by the driver.
# *
# * Param: None
# *
# * Ret:   None
# *
# *****************************************************************************
#
def XsUnloadDriver():
    XStreamDrv.XsUnloadDriver()


# *****************************************************************************
# *
# *  XsEnumCameras
# *
# * Descr: List all the cameras accessible to the driver.
# *
# * Param: nEnumFilter: enumeration filter (see XS_ENUM_FLT).
# *
# * Ret:   List of XS_ENUMITEM enumerating sructures
# *
# * Exception:
# *        XS_E_HARDWARE_FAULT: error using driver (SEVERE error)
# *
# *****************************************************************************
#
def XsEnumCameras(nEnumFilter):
    ITEM_LIST_SIZE = 1024
    XS_ENUMITEM_ARRAY = XS_ENUMITEM * ITEM_LIST_SIZE
    c_item_list = XS_ENUMITEM_ARRAY()
    c_item_count = XSULONG32(ITEM_LIST_SIZE)
    error = XStreamDrv.XsEnumCameras(
        c_item_list, ctypes.byref(c_item_count), nEnumFilter
    )
    _xs_error_check(error)
    # converting C-array into Python list
    py_item_list = map((lambda idx: c_item_list[idx]), range(c_item_count.value))
    return py_item_list


# *****************************************************************************
# *
# *  XsPreConfigCamera
# *
# * Descr: configures a camera parameter before the camera is open
# *
# * Param: nCameraId - camera ID
# *        nParamKey - XS_PRE_PARAM parameter index
# *        value     - the value to write
# *
# * Exception:
# *        XS_E_INVALID_CAMERA_ID - invalid camera id
# *        XS_E_CAM_ALREADY_OPEN - the camera is already open
# *        XS_E_NOT_SUPPORTED - not supported nParamKey
# *
# *****************************************************************************
#


def XsPreConfigCamera(nCameraId, nParamKey, *value):
    nValueLo = ctypes.c_void_p()
    nValueHi = ctypes.c_void_p()
    if nParamKey == XS_PRE_PARAM.XSPP_IP_ADDRESS:
        nValueLo.value = _ip_param_to_num(value[0])
        nValueHi.value = _ip_param_to_num(value[1])
    elif nParamKey == XS_PRE_PARAM.XSPP_IP_ADD_EX:
        nValueLo.value = _ip_param_to_num(value[0])
        nValueHi = ctypes.c_char_p(value[1])
    elif nParamKey in [XS_PRE_PARAM.XSPP_NET_AD_IP, XS_PRE_PARAM.XSPP_CAM_DFL_GW]:
        nValueLo.value = _ip_param_to_num(value[0])
    elif nParamKey in [
        XS_PRE_PARAM.XSPP_CAM_CMD_PORT,
        XS_PRE_PARAM.XSPP_NET_AD_CMD_PORT,
    ]:
        nValueLo.value = int(value[0])
    elif nParamKey == XS_PRE_PARAM.XSPP_DB_FOLDER:
        nValueLo = ctypes.c_char_p(value[0])
    elif nParamKey == XS_PRE_PARAM.XSPP_GET_IP_ADDRESS:
        nIPAddr = ctypes.c_uint()
        nIPMask = ctypes.c_uint()
        nValueLo = ctypes.pointer(nIPAddr)
        nValueHi = ctypes.pointer(nIPMask)
    elif nParamKey in [XS_PRE_PARAM.XSPP_DISABLE_1024, XS_PRE_PARAM.XSPP_REBOOT_FW]:
        nValueLo.value = _ip_param_to_num(value[0])
    else:
        raise XS_ERROR(XS_ERROR.XS_E_NOT_SUPPORTED)

    error = XStreamDrv.XsPreConfigCamera(nCameraId, nParamKey, nValueLo, nValueHi)
    _xs_error_check(error)

    if nParamKey == XS_PRE_PARAM.XSPP_GET_IP_ADDRESS:
        return (nIPAddr.value, nIPMask.value)


# *****************************************************************************
# *
# *  XsOpenCamera
# *
# * Descr: opens the camera with the nCameraId ID and returns the handle to that
# *        camera. The available cameras ID can be retrieved by using the
# *        XsEnumCameras routine
# *
# * Param: nCameraId - camera ID
# *
# * Ret:   camera handle used in any further camera operation.
# *
# * Exception:
# *        XS_E_INVALID_CAMERA_ID - invalid camera id
# *        XS_E_CAM_ALREADY_OPEN - the camera is already open
# *        XS_E_HARDWARE_FAULT: error using driver (SEVERE error)
# *
# *****************************************************************************
#
def XsOpenCamera(nCameraId):
    handle = XS_HANDLE()
    error = XStreamDrv.XsOpenCamera(nCameraId, ctypes.byref(handle))
    _xs_error_check(error)
    return handle


# *****************************************************************************
# *
# *  XsOpenRawCamera
#
# * Descr: opens the raw file as a virtual camera and returns the handle
# *
# * Param: lpszRawFilePath - full path to the rawfile.xml or to the directory that
#                           contains the file
#                           (ex: c:/Images/acq01 or c:/images/acq01/rawfile.xml)
# * Ret:   virtual camera handle used in any further operation.
# *
# * Exception:
# *        XS_E_INVALID_CAMERA_ID - invalid path
# *        XS_E_CAM_ALREADY_OPEN - the camera is already open
# *
# *****************************************************************************
#
def XsOpenRawCamera(lpszRawFilePath):
    handle = XS_HANDLE()
    error = XStreamDrv.XsOpenRawCamera(lpszRawFilePath, ctypes.byref(handle))
    _xs_error_check(error)
    return handle


# *****************************************************************************
# *
# *  XsCloseCamera
# *
# * Descr: closes a camera previously open. After that the handle is no longer
# *        valid.
# *
# * Param: hCamera - hadle to an open camera.
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *
# *****************************************************************************
#
def XsCloseCamera(hCamera):
    error = XStreamDrv.XsCloseCamera(hCamera)
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsGetCameraInfo
# *
# * Descr: gets a camera information value
# *
# * Param: hCamera - handle to an open camera
# *        nInfoKey - index to the information you need (see XS_INFO values)
# *
# * Ret:   Tuple (nValueLo, nValueHi)
# *        nValueLo, nValueHi -  the value of the requested parameter.
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_NOT_SUPPORTED - not supported info key value
# *
# *****************************************************************************
#
def XsGetCameraInfo(hCamera, nInfoKey):
    pnValueLo = PXSULONG32(XSULONG32())
    pnValueHi = PXSULONG32(XSULONG32())
    rettype = PXSULONG32
    if nInfoKey in [
        XS_INFO.XSI_CAMERA_NAME,
        XS_INFO.XSI_CAL_PATH,
        XS_INFO.XSI_CAL_NAME,
    ]:
        pnValueLo = ctypes.create_string_buffer(1024)
        rettype = ctypes.c_char_p
    elif nInfoKey == XS_INFO.XSI_HW_INFO:
        _xs_error_check(XS_ERROR.XS_E_NOT_SUPPORTED)
    error = XStreamDrv.XsGetCameraInfo(hCamera, nInfoKey, pnValueLo, pnValueHi)
    _xs_error_check(error)
    if rettype == ctypes.c_char_p:
        return (pnValueLo.value, pnValueHi.contents.value)
    return (pnValueLo.contents.value, pnValueHi.contents.value)


# *****************************************************************************
# *
# *  XsSetCameraInfo
# *
# * Descr: sets a camera information value
# *
# * Param: hCamera - handle to an open camera
# *        nInfoKey - index to the information you need (see XS_INFO values)
# *        nValueLo,nValueHi - the value to set.
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_NOT_SUPPORTED - not supported info key value
# *        XS_E_INVALID_VALUE - the info values are not valid
# *        XS_E_INVALID_ARGUMENTS - invalid function arguments
# *
# *****************************************************************************
#
def XsSetCameraInfo(hCamera, nInfoKey, nValueLo, nValueHi):
    error = XStreamDrv.XsSetCameraInfo(hCamera, nInfoKey, nValueLo, nValueHi)
    _xs_error_check(error)


##################################################
# Camera configuration routines
# the dll can read the parameter from the camera or default and fill the XS_SETTINGS structure.
# the parameters values can be read or written calling the getParameter or SetParameter routines
# Then the routine RefreshCameraSettings must be called to make the changes effective in the camera
##################################################


# *****************************************************************************
# *
# *  XsReadDefaultSettings
# *
# * Descr: Reads the default settings from the camera and returns the XS_SETTINGS
# *        structure
# *
# * Param: hCamera - handle to an open camera
# *
# * Ret:   XS_SETTINGS structure
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_INVALID_CFG - invalid XS_SETTINGS struct. Make sure that the
# *                           cbSize field has been set.
# *
# *****************************************************************************
#
def XsReadDefaultSettings(hCamera):
    cfg = XS_SETTINGS()
    error = XStreamDrv.XsReadDefaultSettings(hCamera, ctypes.byref(cfg))
    _xs_error_check(error)
    return cfg


# *****************************************************************************
# *
# *  XsReadCameraSettings
# *
# * Descr: Reads the current camera configuration structure
# *
# * Param: hCamera - handle to an open camera
# *
# * Ret:   XS_SETTINGS structure
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_INVALID_CFG - invalid XS_SETTINGS struct. Make sure that the
# *                           cbSize field has been set.
# *
# *****************************************************************************
#
def XsReadCameraSettings(hCamera):
    cfg = XS_SETTINGS()
    error = XStreamDrv.XsReadCameraSettings(hCamera, ctypes.byref(cfg))
    _xs_error_check(error)
    return cfg


# *****************************************************************************
# *
# *  XsRefreshCameraSettings
# *
# * Descr: Send the configuration structure to the camera and refresh the camera
# *        status. All the changes to the XS_SETTINGS structure will take effect
# *        after this routine is called
# *
# * Param: hCamera - handle to an open camera
# *        cfg - XS_SETTINGS structure
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_INVALID_CFG - invalid XS_SETTINGS struct. Make sure that the
# *                           cbSize field has been set.
# *        XS_E_BUSY - the operation cannot be completed because the cmera is busy
# *
# *****************************************************************************
#
def XsRefreshCameraSettings(hCamera, cfg):
    error = XStreamDrv.XsRefreshCameraSettings(hCamera, ctypes.byref(cfg))
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsQueueCameraSettings
# *
# * Descr: Queue up a change to the camera state. This function returns immediately.
# *        When the camera state has changed, you will receive a callback if desired.
# *
# * Param: hCamera - handle to an open camera
# *        cfg - XS_SETTINGS structure
# *        pfnCallback - callback routine pointer - may be None
# *        nFlags - XS_CALLBACK_FLAGS callback flags
# *        pUserData - a parameter passed back in the callback. may be a pointer
# *                    to user data.
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_INVALID_CFG - invalid XS_SETTINGS struct. Make sure that the
# *                           cbSize field has been set.
# *        XS_E_QUEUE_FULL - nothing more can be added to the queue.
# *        XS_E_HARDWARE_FAULT - error using driver (SEVERE error)
# *
# *****************************************************************************
#
def XsQueueCameraSettings(
    hCamera, cfg, pfnCallback=None, nFlags=XS_CALLBACK_FLAGS(), pUserData=None
):
    error = XStreamDrv.XsQueueCameraSettings(
        hCamera, ctypes.byref(cfg), pfnCallback, nFlags, pUserData
    )
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsValidateCameraSettings
# *
# * Descr: Validates camera settings. Not all the combinations of parameters
# *        values are allowed. The routine fixes the structure
# *
# * Param: hCamera - handle to an open camera
# *        cfg - XS_SETTINGS structure
# *
# * Ret:   cfg - updated XS_SETTINGS structure
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_INVALID_CFG - invalid XS_SETTINGS struct. Make sure that the
# *                           cbSize field has been set.
# *
# *****************************************************************************
#
def XsValidateCameraSettings(hCamera, cfg):
    error = XStreamDrv.XsValidateCameraSettings(hCamera, ctypes.byref(cfg))
    _xs_error_check(error)
    return cfg


# *****************************************************************************
# *
# *  XsReadSettingsFromFlash
# *
# * Descr: Read camera settings from camera flash memory, if available
# *
# * Param: hCamera - handle to an open camera
# *
# * Ret:   XS_SETTINGS structure
# *
# * Exceptions:
# *        XS_E_NOT_SUPPORTED - not supported or not flash memory
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_INVALID_ARGUMENTS - invalid funcion arguments
# *        XS_E_INVALID_CFG - invalid XS_SETTINGS struct. Make sure that the
# *                           cbSize field has been set.
# *        XS_E_NOT_IN_FLASH - the configuration is not stored in flash memory
# *
# *****************************************************************************
#
def XsReadSettingsFromFlash(hCamera):
    cfg = XS_SETTINGS()
    error = XStreamDrv.XsReadSettingsFromFlash(hCamera, ctypes.byref(cfg))
    _xs_error_check(error)
    return cfg


# *****************************************************************************
# *
# *  XsWriteSettingsToFlash
# *
# * Descr: Writes camera settings to camera flash memory, if available
# *
# * Param: hCamera - handle to an open camera
# *        cfg - XS_SETTINGS structure
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_NOT_SUPPORTED - not supported or not flash memory
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_INVALID_ARGUMENTS - invalid funcion arguments
# *        XS_E_INVALID_CFG - invalid XS_SETTINGS struct. Make sure that the
# *                           cbSize field has been set.
# *
# *****************************************************************************
#
def XsWriteSettingsToFlash(hCamera, cfg):
    error = XStreamDrv.XsWriteSettingsToFlash(hCamera, ctypes.byref(cfg))
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsReadCameraSettingsArray
# *
# * Descr: Reads the current camera configuration structure
# *
# * Param: hCamera - handle to an open camera
# *        pCfgList - pointer to a XS_SETTINGS structure array
# *        pBrocList - pointer to a XS_BROC structure array (it may be NULL)
# *        pCfgCnt: [in]  pointer to the number of structures in the array
# *                 [out] pointer to number of configurations read
# *
# * Ret:   XS_SUCCESS - configuration array successfully read.
# *        XS_E_NOT_SUPPORTED - the routine is not supported
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *
# *****************************************************************************
#
def XsReadCameraSettingsArray(hCamera, nOption, pCfgList, pBrocList, pnCfgCnt):
    error = XStreamDrv.XsReadCameraSettingsArray(
        hCamera, nOption, pCfgList, pBrocList, pnCfgCnt
    )
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsGetParameterAttribute
# *
# * Descr: Gets the minimum value for a parameter
# *
# * Param: hCamera - handle to an open camera
# *        cfg - a valid XS_SETTINGS structure
# *        nParamKey - XS_PARAM parameter index
# *        nParamAttr - XS_ATTRIBUTE parameter attribute index
# *
# * Ret:   the attribute value
# *
# * Exceptions:
# *        XS_E_NOT_SUPPORTED - the parameter is not supported on this camera cfg.
# *        XS_E_INVALID_CFG - invalid XS_SETTINGS structure.
# *
# *****************************************************************************
#
def XsGetParameterAttribute(hCamera, cfg, nParamKey, nParamAttr):
    nAttrValue = XSULONG32()
    error = XStreamDrv.XsGetParameterAttribute(
        hCamera, ctypes.byref(cfg), nParamKey, nParamAttr, ctypes.byref(nAttrValue)
    )
    _xs_error_check(error)
    return nAttrValue.value


# *****************************************************************************
# *
# *  XsGetParameter
# *
# * Descr: Gets a parameter from the configuration structure.
# *
# * Param: hCamera - handle to an open camera
# *        cfg - XS_SETTINGS structure
# *        nParamKey - parameter index
# *
# * Ret:   the parameter value
# *
# * Exceptions:
# *        XS_E_NOT_SUPPORTED - the parameter is not supported on this camera cfg.
# *        XS_E_INVALID_CFG - invalid XS_SETTINGS structure.
# *
# *****************************************************************************
#
def XsGetParameter(hCamera, cfg, nParamKey):
    nValue = XSULONG32()
    error = XStreamDrv.XsGetParameter(
        hCamera, ctypes.byref(cfg), nParamKey, ctypes.byref(nValue)
    )
    _xs_error_check(error)
    return nValue.value


# *****************************************************************************
# *
# *  XsSetParameter
# *
# * Descr: sets a parameter into the configuration structure
# *
# * Param: hCamera - handle to an open camera
# *        cfg - XS_SETTINGS structure
# *        nParamKey - parameter index
# *        nValue - the value to write
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_NOT_SUPPORTED - the parameter is not supported on this camera cfg.
# *        XS_E_READONLY - the parameter is read-only and cannot be changed
# *        XS_E_INVALID_VALUE - the parameter value is not valid
# *        XS_E_INVALID_CFG - invalid XS_SETTINGS structure.
# *
# *****************************************************************************
#
def XsSetParameter(hCamera, cfg, nParamKey, nValue):
    error = XStreamDrv.XsSetParameter(hCamera, ctypes.byref(cfg), nParamKey, nValue)
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsReadUserDataFromFlash
# *
# * Descr: Read user data from the camera flash memory, if available
# *
# * Param: hCamera - handle to an open camera
# *        nType - destination ( 0=internal flash, 1=internal memory)
# *        nDataID - data unique ID (identifies user data) or start address (expressed in number of 2048 bytes blocks)
# *        nSize - size of data [bytes]
# *        pDataBuf - pointer to data buffer
# *
# * Ret:   size read
# *
# * Exceptions:
# *        XS_E_NOT_SUPPORTED - not supported or not flash memory
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_NOT_IN_FLASH - the user data is not stored in flash memory
# *        XS_E_HARDWARE_FAULT - error on driver
# *
# *****************************************************************************
#
def XsReadUserDataFromFlash(hCamera, nType, nDataIDOrOffset, nSize, pDataBuf):
    nSizeCopy = XSULONG32(nSize)
    error = XStreamDrv.XsReadUserDataFromFlash(
        hCamera, nType, nDataIDOrOffset, ctypes.byref(nSizeCopy), pDataBuf
    )
    _xs_error_check(error)
    return nSizeCopy.value


# *****************************************************************************
# *
# *  XsWriteUserDataToFlash
# *
# * Descr: Writes user data to camera flash memory
# *
# * Param: hCamera - handle to an open camera
# *        nType - destination ( 0=internal flash, 1=internal memory)
# *        nDataID - data unique ID (identifies user data) or start address (expressed in number of 2048 bytes blocks)
# *        nSize - size of data [bytes]
# *        pDataBuff - pointer to data buffer
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_NOT_SUPPORTED - not supported or not flash memory
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_HARDWARE_FAULT - error on driver
# *
# *****************************************************************************
#
def XsWriteUserDataToFlash(hCamera, nType, nDataIDOrOffset, nSize, pDataBuf):
    error = XStreamDrv.XsWriteUserDataToFlash(
        hCamera, nType, nDataIDOrOffset, nSize, pDataBuf
    )
    _xs_error_check(error)


# **************************************************************************************************
# * Preview Mode Grab Routines: grab and transfer to the PC memory like traditional cameras
# **************************************************************************************************

# *****************************************************************************
# *
# *  XsSynchGrab
# *
# * Descr: acquires one or more frames synchronously and returns when the frames
# *        have been acquired or an error occurs.
# *
# * Param: hCamera  - handle to an open camera
# *        frame - a valid XS_FRAME structure.
# *        nTimeOut - acquisition time out [ms]
# *
# * Ret:   XS_FRAME structure with the frame
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_BUFFER_TOO_SMALL - the buffer is too small for an acquisition
# *        XS_E_BUSY - the camera is busy
# *        XS_E_HARDWARE_FAULT: error using usb driver (SEVERE error)
# *
# *****************************************************************************
#
def XsSynchGrab(hCamera, frame, nTimeOut):
    error = XStreamDrv.XsSynchGrab(hCamera, ctypes.byref(frame), nTimeOut)
    _xs_error_check(error)
    return frame


# *****************************************************************************
# *
# *  XsAbort
# *
# * Descr: any queued operation is aborted. The frame and settings queues are
# *        cleared.
# *
# * Param: hCamera - handle to an open camera
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *
# *****************************************************************************
#
def XsAbort(hCamera):
    error = XStreamDrv.XsAbort(hCamera)
    _xs_error_check(error)


##################################################
# Camera memory acquisition routines
##################################################

# *****************************************************************************
# *
# *  XsMemoryStartGrab
# *
# * Descr: starts an acquisition in the camera memory. This function returns
# *        immediately. When the acquisition has been performed, you will
# *        receive a callback, if desired.
# *
# * Param: hCamera - handle to an open camera
# *        nStartAddLo - starting address in camera memory - low order XSULONG32
# *        nStartAddHi - starting address in camera memory - high order XSULONG32
# *        nFrames - number of frames to read
# *        nPreTrigFrames - number of frames to be acquired before the trigger
# *                         (valid in single trigger burst mode only)
# *        pfnCallback - callback routine pointer - can be NULL
# *        nFlags - callback flags
# *        pUserData - a parameter passed back in the callback. may be a pointer
# *                    to user data.
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_HARDWARE_FAULT: error using usb driver (SEVERE error)
# *
# *****************************************************************************
#
def XsMemoryStartGrab(
    hCamera,
    nStartAddLo,
    nStartAddHi,
    nFrames,
    nPreTrigFrames,
    pfnCallback,
    nFlags,
    pUserData,
):
    error = XStreamDrv.XsMemoryStartGrab(
        hCamera,
        nStartAddLo,
        nStartAddHi,
        nFrames,
        nPreTrigFrames,
        pfnCallback,
        nFlags,
        pUserData,
    )
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsMemoryStopGrab
# *
# * Descr: stops the current acquisition in the camera memory.
# *
# * Param: hCamera - handle to an open camera
# *
# * Ret:   the number of frames acquired so far
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *
# *****************************************************************************
#
def XsMemoryStopGrab(hCamera):
    nAcqFrames = XSULONG32()
    error = XStreamDrv.XsMemoryStopGrab(hCamera, ctypes.byref(nAcqFrames))
    _xs_error_check(error)
    return nAcqFrames.value


# *****************************************************************************
# *
# *  XsMemoryPreview
# *
# * Descr: previews the latest acquired frame during an acquisition
# *
# * Param: hCamera - handle to an open camera
# *        frame - a valid XS_FRAME structure
# *
# * Ret:   tuple (frame, nFrameIndex)
# *        frame - filled XS_FRAME structure
# *        nFrameIndex - the latest acquired frame index [0..n-1]
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_INVALID_ARGUMENTS - invalid arguments
# *        XS_E_BUSY - camera is busy
# *        XS_E_HARDWARE_FAULT - camera hardware fault
# *
# *****************************************************************************
#
def XsMemoryPreview(hCamera, frame):
    nFrameIndex = XSULONG32()
    error = XStreamDrv.XsMemoryPreview(
        hCamera, ctypes.byref(frame), ctypes.byref(nFrameIndex)
    )
    _xs_error_check(error)
    return (frame, nFrameIndex.value)


# *****************************************************************************
# *
# *  XsMemoryReadFrame
# *
# * Descr: reads one image frame from the camera memory.
# *
# * Param: hCamera - handle to an open camera
# *        nStartAddLo - starting address in camera memory - low order XSULONG32
# *        nStartAddHi - starting address in camera memory - high order XSULONG32
# *        nFrameIdxOrSize - index of the frame (all cams) or frame size (N-cams)
# *        pDataBuff - pointer to data buffer
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_HARDWARE_FAULT - camera hardware fault
# *
# *****************************************************************************
#
def XsMemoryReadFrame(hCamera, nStartAddLo, nStartAddHi, nFrameIdxOrSize, pDataBuf):
    error = XStreamDrv.XsMemoryReadFrame(
        hCamera, nStartAddLo, nStartAddHi, nFrameIdxOrSize, pDataBuf
    )
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsMemoryReadFromDisk
# *
# * Descr: reads a frame from the camera memory.
# *
# * Param: hCamera - handle to an open camera
# *        nMemDstAddLo, nMemDstAddHi - destination address in camera memory
# *        nDiskSrcAddLo, nDiskSrcAddHi - source address in camera disk
# *        nStartIdx - index of the first image to transfer
# *        nStopIdx - index of the last image to transfer
# *        pfnCallback - callback routine pointer - may be NULL
# *        pUserData - a parameter passed back in the callback. may be a pointer
# *                    to user data.
# *
# * Ret:   XS_SUCCESS - frames successfully read
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_NOT_SUPPORTED - the routine is not supported
# *        XS_E_HARDWARE_FAULT - camera hardware fault
# *
# *****************************************************************************
#
def XsMemoryReadFromDisk(
    hCamera,
    nMemDstAddLo,
    nMemDstAddHi,
    nDiskSrcAddLo,
    nDiskSrcAddHi,
    nStartIdx,
    nStopIdx,
    pfnCallback,
    pUserData,
):
    error = XStreamDrv.XsMemoryReadFromDisk(
        hCamera,
        nMemDstAddLo,
        nMemDstAddHi,
        nDiskSrcAddLo,
        nDiskSrcAddHi,
        nStartIdx,
        nStopIdx,
        pfnCallback,
        pUserData,
    )
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsMemoryDownloadRawFrame
# *
# * Descr: downloads one image frame from the camera memory to a RAW file.
# *
# * Param: hCamera - handle to an open camera
# *        szRawFilePath - full path of the raw file (without extension)
# *        nStartAddLo - starting address in camera memory - low order XSULONG32
# *        nStartAddHi - starting address in camera memory - high order XSULONG32
# *        nFrameIdx - index of the frame in camera memory (position)
# *        nPageIdx - index of the image in the file (0 to N-1)
# *        nTotFrames - total number of frames to download
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_BUSY - the camera is busy and cannot donwload
# *        XS_E_HARDWARE_FAULT - camera hardware fault
# *
# *****************************************************************************
#
def XsMemoryDownloadRawFrame(
    lpszRawFilePath, nStartAddLo, nStartAddHi, nFrameIdx, nPageIdx, nTotFrames
):
    error = XStreamDrv.XsMemoryDownloadRawFrame(
        lpszRawFilePath, nStartAddLo, nStartAddHi, nFrameIdx, nPageIdx, nTotFrames
    )


# *****************************************************************************
# *
# *  XsMemoryReadTriggerPosition
# *
# * Descr: reads the trigger position from the camera.
# *
# * Param: hCamera - handle to an open camera
# *        pnTriggerPosLo - pointer to the trigger position - low order XSULONG32
# *        pnTriggerPosHi - pointer to the trigger position - high order XSULONG32
# *        pnTriggerIndex - pointer to the trigger position - frame index
# *        pnTriggerTime - pointer to the trigger position - relative to sync period start [ns]
# *         If the trigger source is a single pulse and the number of pre-trigger
# *         frames is not 0, we need to know where is located the frame acquired
# *         when the pulse comes.
# *
# * Ret:   tuple of (nTriggerPos, nTriggerIndex, nTriggerTime)
# *        nTriggerPos - the trigger position
# *        nTriggerIndex - the trigger position - frame index
# *        nTriggerTime - the trigger position - relative to sync period start [ns]
# *         If the trigger source is a single pulse and the number of pre-trigger
# *         frames is not 0, we need to know where is located the frame acquired
# *         when the pulse comes.
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_HARDWARE_FAULT - the status cannot be read
# *
# *****************************************************************************
#
def XsMemoryReadTriggerPosition(hCamera):
    nTriggerPosLo = XSULONG32()
    nTriggerPosHi = XSULONG32()
    nTriggerIndex = XSULONG32()
    nTriggerTime = XSULONG32()
    error = XStreamDrv.XsMemoryReadTriggerPosition(
        hCamera,
        ctypes.byref(nTriggerPosLo),
        ctypes.byref(nTriggerPosHi),
        ctypes.byref(nTriggerIndex),
        ctypes.byref(nTriggerTime),
    )
    _xs_error_check(error)
    trigger_pos = (nTriggerPosHi.value << 32) | nTriggerPosLo.value
    return (trigger_pos, nTriggerIndex.value, nTriggerTime.value)


# *****************************************************************************
# *
# *  XsEraseMemory
# *
# * Descr: Erases the camera memory
# *
# * Param: hCamera - handle to an open camera
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_HARDWARE_FAULT - error on driver
# *
# *****************************************************************************
#
def XsEraseMemory(hCamera):
    error = XStreamDrv.XsEraseMemory(hCamera)
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsEraseDisk
# *
# * Descr: Erases the camera disk (O-series only)
# *
# * Param: hCamera - handle to an open camera
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_NOT_SUPPORTED - the routine is not supported
# *        XS_E_HARDWARE_FAULT - error on driver
# *
# *****************************************************************************
#
def XsEraseDisk(hCamera):
    error = XStreamDrv.XsEraseDisk(hCamera)
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsTrigger
# *
# * Descr: Issues a software trigger to the camera.
# *
# * Param: hCamera - handle to an open camera
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_NOT_SUPPORTED - the API si not supported
# *        XS_E_NOT_RECORDING - the camera is not in record mode
# *        XS_E_BUSY - the camera is busy
# *        XS_E_HARDWARE_FAULT: error using usb driver (SEVERE error)
# *
# *****************************************************************************
#
def XsTrigger(hCamera):
    error = XStreamDrv.XsTrigger(hCamera)
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsGetHardwareError
# *
# * Descr: returns last encountered vendor specific hardware error.
# *
# * Param: hCamera - handle to an open camera
# *
# * Ret:   tuple (error_code, error_descr)
# *        error_code - error code
# *        error_descr - description string
# *
# *****************************************************************************
#
def XsGetHardwareError(hCamera):
    nSize = 1024
    pszBuffer = ctypes.create_string_buffer(nSize)
    error = XStreamDrv.XsGetHardwareError(hCamera, pszBuffer, nSize)
    return (error, pszBuffer.value)


# *****************************************************************************
# *
# *  XsCalibrateNoiseReduction
# *
# * Descr: calibrates the camera, reduces the fixed noise pattern and
# *        reduces differences due to pixel sensitivity
# *
# * Param: hCamera - handle to an open camera
# *        nOpCode - operation code (see XS_CALIB_OPCODE)
# *        pfnCallback - callback routine pointer - may be None
# *        pUserData - a parameter passed back in the callback. may be a pointer
# *                    to user data.
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_NOT_SUPPORTED - the routine is not supported
# *        XS_E_HARDWARE_FAULT - the status cannot be read
# *        XS_E_NOT_IN_FLASH - if the opcode is XS_C_FILE_DOWNLOAD, the file
# *                            is not stored in flash memory.
# *        XS_E_ABORTED - the procedure has been aborted.
# *
# *****************************************************************************
#
def XsCalibrateNoiseReduction(hCamera, nOpCode, pfnCallback, pUserData):
    error = XStreamDrv.XsCalibrateNoiseReduction(
        hCamera, nOpCode, pfnCallback, pUserData
    )
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsReadGPSTiming
# *
# * Descr: Reads GPS/IRIG timing info from the current frame or from the camera
# *
# * Param: hCamera - handle to an open camera
# *        nOption - 0: read from current frame, 1: read from camera
# *
# * Ret:   IRIG string
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_INVALID_VALUE - invalid parameter
# *        XS_E_NOT_SUPPORTED - the routine is not supported
# *
# *****************************************************************************
#
def XsReadGPSTiming(hCamera, nOption):
    nSize = 1024
    pszBuffer = ctypes.create_string_buffer(nSize)
    error = XStreamDrv.XsReadGPSTiming(hCamera, nOption, pszBuffer)
    return pszBuffer.value


# *****************************************************************************
# *
# *  XsReset
# *
# * Descr: resets the camera
# *
# * Param: hCamera - handle to an open camera
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_HARDWARE_FAULT - the status cannot be read
# *
# *****************************************************************************
#
def XsReset(hCamera):
    error = XStreamDrv.XsReset(hCamera)
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsEnableDiagnosticTrace
# *
# * Descr: enables/disables the diagnostic trace
# *
# * Param: hCamera - handle to an open camera
# *        pszTraceFilePath - full path of the trace file (text)
# *        nEnable - enable (1) disable (0) flag
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *
# *****************************************************************************
#
def XsEnableDiagnosticTrace(hCamera, pszTraceFilePath, nEnable):
    error = XStreamDrv.XsEnableDiagnosticTrace(hCamera, pszTraceFilePath, nEnable)
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsEnableRawMode
# *
# * Descr: enables/disables the raw data mode
# *
# * Param: hCamera - handle to an open camera
# *           nEnable - enable (1) disable (0) flag
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *
# *****************************************************************************
#
def XsEnableRawMode(hCamera, nEnable):
    error = XStreamDrv.XsEnableRawMode(hCamera, nEnable)
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsGetCameraStatus
# *
# * Descr: Reads the camera status
# *
# * Param: hCamera - handle to an open camera
# *
# * Ret:   tuple (nIsBusy, nStatus, nErrCode, nInfo[3])
# *        pnIsBusy - busy (0 or 1)
# *        pnStatus - status
# *        pnErrCode - error code
# *        pnInfo[0,1,2] - information variables
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_INVALID_ARGUMENTS - invalid arguments
# *        XS_E_HARDWARE_FAULT - error on driver
# *
# *****************************************************************************
#
def XsGetCameraStatus(hCamera):
    nIsBusy = XSULONG32()
    nStatus = XSULONG32()
    nErrCode = XSULONG32()
    nInfo1 = XSULONG32()
    nInfo2 = XSULONG32()
    nInfo3 = XSULONG32()
    error = XStreamDrv.XsGetCameraStatus(
        hCamera,
        ctypes.byref(nIsBusy),
        ctypes.byref(nStatus),
        ctypes.byref(nErrCode),
        ctypes.byref(nInfo1),
        ctypes.byref(nInfo2),
        ctypes.byref(nInfo3),
    )
    _xs_error_check(error)
    return (
        nIsBusy.value,
        nStatus.value,
        nErrCode.value,
        (nInfo1.value, nInfo2.value, nInfo3.value),
    )


# *****************************************************************************
# *
# *  XsSetAnnouncementCallback
# *
# * Descr: Sets the announcement callback
# *
# * Param: hCamera - handle to an open camera
# *        pfnCallback - callback routine pointer - can be NULL
# *        pUserData - a parameter passed back in the callback. may be a pointer
# *                    to user data.
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_HARDWARE_FAULT - error on driver
# *
# *****************************************************************************
#
def XsSetAnnouncementCallback(hCamera, pfnCallback, pUserData):
    error = XStreamDrv.XsSetAnnouncementCallback(hCamera, pfnCallback, pUserData)
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsReadBorderData
# *
# * Descr: Reads the border data (HG-only)
# *
# * Param: hCamera - handle to an open camera
# *        pDataBuff - pointer to the border data buffer
# *        nSize - size of the border data buffer
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_HARDWARE_FAULT - error on driver
# *
# *****************************************************************************
#
def XsReadBorderData(hCamera):
    nSize = 256
    pszBuffer = ctypes.create_string_buffer(nSize)
    error = XStreamDrv.XsReadBorderData(hCamera, pszBuffer)
    _xs_error_check(error)
    return pszBuffer.value


# *****************************************************************************
# *
# *  XsAttach
# *
# * Descr: Attach to camera. Handle simultaneous connection from different
# *        computers. For Y and HG cameras only
# *
# * Param: hCamera - handle to an open camera
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_HARDWARE_FAULT - the status cannot be read
# *
# *****************************************************************************
#
def XsAttach(hCamera):
    error = XStreamDrv.XsAttach(hCamera)
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsGetAddressList
# *
# * Descr: reads last acquisition's list of frames' addresses.
# *
# * Param: hCamera - handle to an open camera
# *        nStartIdx - starting frame index
# *        nAddressCount - number of addresses to read
# *
# * Ret:   addresses list
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_HARDWARE_FAULT - camera hardware fault
# *
# *****************************************************************************
#
def XsGetAddressList(hCamera, nStartIdx, nAddressCount):
    pnAddressList = (XSUINT64 * nAddressCount)()
    error = XStreamDrv.XsGetAddressList(
        hCamera, nStartIdx, nAddressCount, pnAddressList
    )
    _xs_error_check(error)
    return pnAddressList[:]


# *****************************************************************************
# *
# *  XsConfigureWriteToDisk
# *
# * Descr: configures the disk recording parameters.
# *
# * Param: hCamera - handle to an open camera
# *        nEnable - on/off flag
# *        lpszDiskDrives - zero terminated array of disk drives (A,B,C...)
# *        lpszDirectory - path to acquisition directory
# *        nRamBufferSize - size of RAM buffer used for acquisition [MB]
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_NOT_SUPPORTED - the option is not supported
# *
# *****************************************************************************
#
def XsConfigureWriteToDisk(
    hCamera, nEnable, lpszDiskDrives, lpszDirectory, nRamBufferSize
):
    error = XStreamDrv.XsConfigureWriteToDisk(
        hCamera, nEnable, lpszDiskDrives, lpszDirectory, nRamBufferSize
    )
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsReadToVideo
# *
# * Descr: sends a command to the HDMI output to read a frame and display it.
# *
# * Param: hCamera - handle to an open camera
# *        nStartAddLo - starting address in camera memory - low order XSULONG32
# *        nStartAddHi - starting address in camera memory - high order XSULONG32
# *        nFrameIdx - index of the frame (if 0xFFFFFFF it snaps an image)
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_NOT_SUPPORTED - the option is not supported
# *        XS_E_BUSY - the operation cannot be completed because the camera is busy
# *        XS_E_HARDWARE_FAULT - camera hardware fault
# *
# *****************************************************************************
#
def XsReadToVideo(hCamera, nStartAddLo, nStartAddHi, nFrameIdx):
    error = XStreamDrv.XsReadToVideo(hCamera, nStartAddLo, nStartAddHi, nFrameIdx)
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsLoadLookupTable
# *
# * Descr: Loads a custom Lookup Table.
# *
# * Param: hCamera - handle to an open camera
# *        table - lookup table (array of numbers)
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_INVALID_ARGUMENTS - invalid arguments
# *
# *****************************************************************************
#
def XsLoadLookupTable(hCamera, table):
    nSize = len(table)
    pnTable = (ctypes.c_ushort * nSize)()
    pnTable[:] = table
    error = XStreamDrv.XsLoadLookupTable(hCamera, pnTable, nSize)
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsGetBrocParameters
# *
# * Descr: reads addresses and indexes of current BROC sections
# *        For cameras that support hardware BROC (Y,NR,NX).
# *
# * Param: hCamera  - handle to an open camera
# *        pBrocSectArray - array of XS_BROC_SECTION items
# *        nSize - number of items in the array
# *
# * Ret:   XS_SUCCESS - resizer successfully activated
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_INVALID_ARGUMENTS - invalid arguments
# *        XS_E_NOT_SUPPORTED - the routine is not supported
# *
# *****************************************************************************
#
def XsGetBrocParameters(hCamera, nSize):
    brocArray = (XS_BROC_SECTION * nSize)()
    error = XStreamDrv.XsGetBrocParameters(hCamera, brocArray, nSize)
    _xs_error_check(error)
    return brocArray[:]


# *****************************************************************************
# *
# *  XsVideoPlayback
# *
# * Descr: starts or stops fast playback on the HDMI output
# *
# * Param: hCamera  - handle to an open camera
# *        nOption - 0:stop,  1:forward, 2:rewind (see XS_VIDEO_PB)
# *        nStartAddLo - starting address in camera memory - low order XSULONG32
# *        nStartAddHi - starting address in camera memory - high order XSULONG32
# *        nFrames - number of frames to play back
# *        nStartFrameIdx - index of first frame.
# *        nStopFrameIdx - index of last frame.
# *
# * Ret:   None
# *
# * Exceptions:
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_INVALID_ARGUMENTS - invalid arguments
# *        XS_E_NOT_SUPPORTED - the routine is not supported
# *        XS_E_HARDWARE_FAULT - the command returns error
# *
# *****************************************************************************
#
def XsVideoPlayback(
    hCamera, nOption, nStartAddLo, nStartAddHi, nFrames, nStartFrameIdx, nStopFrameIdx
):
    error = XStreamDrv.XsVideoPlayback(
        hCamera,
        nOption,
        nStartAddLo,
        nStartAddHi,
        nFrames,
        nStartFrameIdx,
        nStopFrameIdx,
    )
    _xs_error_check(error)


# *****************************************************************************
# *
# *  XsLive
# *
# * Descr: starts/stop acquisition of live images
# *
# * Param: hCamera  - handle to an open camera
# *        nCmd - 1=start 0=stop (see XS_LIVE)
# *
# * Ret:   XS_SUCCESS - frames successfully acquired
# *        XS_E_INVALID_HANDLE - invalid camera handle
# *        XS_E_NOT_SUPPORTED  - function is not supported
# *        XS_E_INVALID_ARGUMENTS - invalid function arguments
# *        XS_E_HARDWARE_FAULT - camera hardware fault
# *
# *****************************************************************************
#
def XsLive(hCamera, nCmd):
    error = XStreamDrv.XsLive(hCamera, nCmd)
    _xs_error_check(error)

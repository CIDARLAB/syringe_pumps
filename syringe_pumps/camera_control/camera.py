from syringe_pumps.camera_control import XsCamera

# load the driver
XsCamera.XsLoadDriver(0)

ef = XsCamera.XS_ENUM_FLT()
py_item_list = XsCamera.XsEnumCameras(ef)

# Open the first camera in the list.
handle = XsCamera.XsOpenCamera(py_item_list[0])

cfg = XsCamera.XsReadCameraSettings(handle)

xs_param_key = XsCamera.XS_PARAM()

nValue = 1000000 # Exposure in nanoseconds
XsCamera.XsSetParameter(handle, cfg, xs_param_key.XSP_EXPOSURE, nValue)

nValue = 10000000 # acquisition period in nanoseconds (inverse of rate)
XsCamera.XsSetParameter(handle, cfg, xs_param_key.XSP_PERIOD, nValue)

xs_info_key = XsCamera.XS_INFO()
# Sensor type (see XS_SNS_TYPE)
value_lo, value_hi = XsCamera.XsGetCameraInfo(handle, xs_info_key.XSI_SNS_TYPE)

# Width of ROI, in pixels
width_pixels = XsCamera.XsGetParameter(handle, cfg, xs_param_key.XSP_ROIWIDTH)

# Height of ROI, in pixels
height_pixels = XsCamera.XsGetParameter(handle, cfg, xs_param_key.XSP_ROIHEIGHT)

nValue = 24 # Pixel depth: 8 to 36
XsCamera.XsSetParameter(handle, cfg, xs_param_key.XSP_PIX_DEPTH, nValue)

# Trigger Source (see XS_REC_MODE)
nValue = 0 # Normal mode (fills the memory segment and stop)
XsCamera.XsSetParameter(handle, cfg, xs_param_key.XSP_REC_MODE, nValue)

XsCamera.XsRefreshCameraSettings(handle, cfg)


nImgSize = nW*nH*nPD/8

# Im not sure how this part will work... 
char *pBuf = (char *)malloc(nImgSize) # i dont think I need this part ... 
memset(pBuf, 0, nImgSize) 


xs_frame_c = XsCamera.XS_FRAME()
xs_frame_c.pBuffer

# minimum buffer in camera memory to avoid overwrite of acquisition during live
 
nAddLo, nAddHi = XsCamera.XsGetCameraInfo(handle, xs_info_key.XSI_LIVE_BUF_SIZE)

nFrames = 100 # number of frames to read
nPreTrigFrames = 0 # number of frames to be acquired before the trigger
pfnCallback = NULL # callback routine pointer - can be NULL
nFlags = 0 # callback flags
pUserData = 0 # a parameter passed back in the callback. may be a pointerto user data.
XsCamera.XsMemoryStartGrab(handle, nAddLo, nAddHi, nFrames, nPreTrigFrames, pfnCallback, nFlags, pUserData)

# add while loop in here 
nIsBusy, nStatus, nErrCode, nInfo1, nInfo2, nInfo3 = XsCamera.XsGetCameraStatus(handle)


### NEED THE pBuf FROM MALLOC.... BUT UNSURE HOW TO GET THAT RIGHT NOW
# read 10 frames
for x in range(10):
	XsCamera.XsMemoryReadFrame(handle, nAddLo, nAddHi, x, pBuf)

# free the memory
free(pBuf)

XsCamera.XsCloseCamera(handle)

XsCamera.XsUnloadDriver()




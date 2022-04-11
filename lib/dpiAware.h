#ifndef DPIAWARE_H
#define DPIAWARE_H
#include <windef.h>
#ifndef DPI_AWARENESS_CONTEXT_UNAWARE
DECLARE_HANDLE(DPI_AWARENESS_CONTEXT);
#define DPI_AWARENESS_CONTEXT_UNAWARE ((DPI_AWARENESS_CONTEXT)-1)
#define DPI_AWARENESS_CONTEXT_SYSTEM_AWARE ((DPI_AWARENESS_CONTEXT)-2)
#define DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE ((DPI_AWARENESS_CONTEXT)-3)
#define DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 ((DPI_AWARENESS_CONTEXT)-4)
#define DPI_AWARENESS_CONTEXT_UNAWARE_GDISCALED ((DPI_AWARENESS_CONTEXT)-5)
#endif

typedef enum MONITOR_DPI_TYPE_ {
    MDT_EFFECTIVE_DPI = 0,
    MDT_ANGULAR_DPI = 1,
    MDT_RAW_DPI = 2,
    MDT_DEFAULT
} MONITOR_DPI_TYPE_;
typedef BOOL(WINAPI *SetProcessDpiAwarenessContextProc)(DPI_AWARENESS_CONTEXT);
typedef LRESULT(WINAPI *GetDpiForMonitorProc)(HMONITOR, MONITOR_DPI_TYPE_, UINT *, UINT *);
typedef UINT(WINAPI *GetDpiForWindowProc)(HWND);
#endif
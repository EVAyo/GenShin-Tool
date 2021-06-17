// ���� ifdef ���Ǵ���ʹ�� DLL �������򵥵�
// ��ı�׼�������� DLL �е������ļ��������������϶���� CVAUTOTRACK_EXPORTS
// ���ű���ġ���ʹ�ô� DLL ��
// �κ���Ŀ�ϲ�Ӧ����˷��š�������Դ�ļ��а������ļ����κ�������Ŀ���Ὣ
// CVAUTOTRACK_API ������Ϊ�Ǵ� DLL ����ģ����� DLL ���ô˺궨���
// ������Ϊ�Ǳ������ġ�
#ifdef CVAUTOTRACK_EXPORTS
#define CVAUTOTRACK_API __declspec(dllexport)
#else
#define CVAUTOTRACK_API __declspec(dllimport)
#endif

// �����Ǵ� dll ������
class CcvAutoTrack {
public:
	CcvAutoTrack(void);
	~CcvAutoTrack(void);
	
	bool init();
	bool GetTransforn(float &x, float &y, float &a);
	bool GetUID(int &uid);
	int GetLastError();
	bool uninit();

private:
	void* _giMatchResource = nullptr;
	
private:
	int error_code = 0;

private:
	bool is_init_end = false;

private:
	int minHessian = 400;
	float ratio_thresh = 0.66f;
	float mapScale = 1.3f;//1.3;
	int someSizeR = 106;
	float MatchMatScale = 2.0;
private:
	//cv::Ptr<cv::xfeatures2d::SURF>
	void* _detectorAllMap = nullptr;
	//cv::Ptr<cv::xfeatures2d::SURF>
	void* _detectorSomeMap = nullptr;
	//std::vector<cv::KeyPoint>
	void* _KeyPointAllMap = nullptr;
	//std::vector<cv::KeyPoint>
	void* _KeyPointSomeMap = nullptr;
	//std::vector<cv::KeyPoint>
	void* _KeyPointMiniMap = nullptr;
	//cv::Mat
	void* _DataPointAllMap = nullptr;
	//cv::Mat
	void* _DataPointSomeMap = nullptr;
	//cv::Mat
	void* _DataPointMiniMap = nullptr;

private:
	bool isContinuity = false;
	//std::vector<cv::Point>
	void* _TransfornHistory = nullptr;
	//cv::Point*
	void** __TransfornHistory = nullptr;

private:
	//HWND
	void* _giHandle = nullptr;
	//RECT
	void* _giRect = nullptr;
	//RECT
	void* _giClientRect = nullptr;
	//cv::Size
	void* _giClientSize = nullptr;
	//cv::Mat
	void* _giFrame = nullptr;
	//cv::Mat
	void* _giPaimonRef = nullptr;
	//cv::Mat
	void* _giMiniMapRef = nullptr;
	//cv::Mat
	void* _giUIDRef = nullptr;

private:
	bool getGengshinImpactWnd();
	void getGengshinImpactRect();
	void getGengshinImpactScreen();
	void getPaimonRefMat();
	void getMiniMapRefMat();
	void getUIDRefMat();
};

extern "C" __declspec(dllexport) bool __stdcall init();
extern "C" __declspec(dllexport) bool __stdcall GetTransforn(float &x, float &y, float &a);
extern "C" __declspec(dllexport) bool __stdcall GetUID(int &uid);
extern "C" __declspec(dllexport) int __stdcall GetLastErr();
extern "C" __declspec(dllexport) bool __stdcall uninit();
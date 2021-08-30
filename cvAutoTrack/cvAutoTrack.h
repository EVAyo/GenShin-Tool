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

// �����ѵ����ĺ�����
extern "C" CVAUTOTRACK_API bool init();
extern "C" CVAUTOTRACK_API bool SetHandle(long long int handle);
extern "C" CVAUTOTRACK_API bool SetWorldCenter(double x, double y);
extern "C" CVAUTOTRACK_API bool SetWorldScale(double scale);
extern "C" CVAUTOTRACK_API bool GetTransform(float &x, float &y, float &a);
extern "C" CVAUTOTRACK_API bool GetPosition(double &x, double &y);
extern "C" CVAUTOTRACK_API bool GetDirection(double &a);
extern "C" CVAUTOTRACK_API bool GetRotation(double &a);
extern "C" CVAUTOTRACK_API bool GetUID(int &uid);

extern "C" CVAUTOTRACK_API bool GetInfoLoadPicture(char* path, int &uid, double &x, double &y, double &a);
extern "C" CVAUTOTRACK_API bool GetInfoLoadVideo(char* path, char* pathOutFile);

extern "C" CVAUTOTRACK_API int GetLastErr();
extern "C" CVAUTOTRACK_API const char* GetLastErrStr();

extern "C" CVAUTOTRACK_API bool startServe();
extern "C" CVAUTOTRACK_API bool stopServe();

#ifdef _DEBUG

	//void testLocalVideo(std::string path);

#endif
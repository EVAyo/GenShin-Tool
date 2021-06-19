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
extern "C" CVAUTOTRACK_API bool GetTransform(float &x, float &y, float &a);
extern "C" CVAUTOTRACK_API bool GetUID(int &uid);
extern "C" CVAUTOTRACK_API int GetLastErr();
extern "C" CVAUTOTRACK_API bool uninit();
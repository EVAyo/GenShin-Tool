#include "pch.h"
#include "GenshinImpactScreen.h"

GenshinImpactScreen::GenshinImpactScreen()
{
	getNowTimeMs();
	updateTime();
}

GenshinImpactScreen * GenshinImpactScreen::getInstance()
{
	static GenshinImpactScreen GIS_Instance = GenshinImpactScreen();
	return &GIS_Instance;
}

Mat GenshinImpactScreen::getGenshinImpactScreen()
{
	getNowTimeMs();
	if (NowTimeMs - LastTimeMs >= 24)
	{
		
		return getGenshinImpactScreen_NewGet();
	}
	else
	{
		return getGenshinImpactScreen_GetAfter();
	}

}

void GenshinImpactScreen::updateTime()
{
	LastTimeMs = NowTimeMs;
}

void GenshinImpactScreen::getNowTimeMs()
{
	NowTimeMs = clock();
}

Mat GenshinImpactScreen::getGenshinImpactScreen_GetAfter()
{
	return Screen;
}

Mat GenshinImpactScreen::getGenshinImpactScreen_NewGet()
{
	static HBITMAP	hBmp;
	BITMAP bmp;
	Mat giFarme;

	DeleteObject(hBmp);

	if (giHandle == NULL)
	{
		err = 12;//���ھ��ʧЧ
		return false;
	}
	if (!IsWindow(giHandle))
	{
		err = 12;//���ھ��ʧЧ
		return false;
	}
	//��ȡĿ�����Ĵ��ڴ�СRECT
	GetWindowRect(giHandle, &giRect);/* ��ԭ�񴰿ڵĲ��� */

	//��ȡĿ������DC
	HDC hScreen = GetDC(giHandle);/* ��ԭ�񴰿ڵĲ��� */
	HDC hCompDC = CreateCompatibleDC(hScreen);

	//��ȡĿ�����Ŀ�Ⱥ͸߶�
	int	nWidth = (int)((screen_scale) * (giRect.right - giRect.left));
	int	nHeight = (int)((screen_scale) * (giRect.bottom - giRect.top));

	//����Bitmap����
	hBmp = CreateCompatibleBitmap(hScreen, nWidth, nHeight);//�õ�λͼ

	SelectObject(hCompDC, hBmp); //��д��ȫ��
	BitBlt(hCompDC, 0, 0, nWidth, nHeight, hScreen, 0, 0, SRCCOPY);

	//�ͷŶ���
	DeleteDC(hScreen);
	DeleteDC(hCompDC);

	//����ת��
	//�����ȡλͼ�Ĵ�С��Ϣ,��ʵ��Ҳ�Ǽ���DC��ͼ����ķ�Χ
	GetObject(hBmp, sizeof(BITMAP), &bmp);

	int nChannels = bmp.bmBitsPixel == 1 ? 1 : bmp.bmBitsPixel / 8;
	int depth = bmp.bmBitsPixel == 1 ? IPL_DEPTH_1U : IPL_DEPTH_8U;

	//mat����
	giFrame.create(cv::Size(bmp.bmWidth, bmp.bmHeight), CV_MAKETYPE(CV_8U, nChannels));

	GetBitmapBits(hBmp, bmp.bmHeight*bmp.bmWidth*nChannels, giFrame.data);

	giFrame = giFrame(cv::Rect(giClientRect.left, giClientRect.top, giClientSize.width, giClientSize.height));

	if (giFrame.empty())
	{
		err = 3;
		return giFrame;
	}
	return giFrame;
}

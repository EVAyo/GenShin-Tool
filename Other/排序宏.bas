Attribute VB_Name = "ģ��1"
Sub ����()
Attribute ����.VB_ProcData.VB_Invoke_Func = " \n14"
'
' �� ��
'

    ' ����A-D���ǽ�ɫ
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Clear
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add2 Key:=Range("D2:D209") _
        , SortOn:=xlSortOnValues, Order:=xlDescending, DataOption:=xlSortNormal
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("A2:A209"), _
        xlSortOnFontColor, xlDescending, , xlSortNormal).SortOnValue.Color = RGB(112, _
        48, 160)
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("A2:A209"), _
        xlSortOnFontColor, xlDescending, , xlSortNormal).SortOnValue.Color = RGB(255, 0 _
        , 0)
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("B2:B209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(174, _
        170, 170)
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("B2:B209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(198, _
        224, 180)
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("B2:B209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(155, _
        194, 230)
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("B2:B209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(237, _
        111, 231)
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("B2:B209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(242, _
        161, 106)
    With ActiveWorkbook.Worksheets("��Ըͳ��").Sort
        .SetRange Range("A2:D209")
        .Header = xlGuess
        .MatchCase = False
        .Orientation = xlTopToBottom
        .SortMethod = xlPinYin
        .Apply
    End With
    
    
    
    ' ����F-J��������
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Clear
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add2 Key:=Range("J2:J207") _
        , SortOn:=xlSortOnValues, Order:=xlDescending, DataOption:=xlSortNormal
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("F2:F207"), _
        xlSortOnFontColor, xlDescending, , xlSortNormal).SortOnValue.Color = RGB(255, 0 _
        , 0)
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("G2:G207"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(174, _
        170, 170)
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("G2:G207"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(198, _
        224, 180)
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("G2:G207"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(155, _
        194, 230)
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("G2:G207"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(237, _
        111, 231)
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("G2:G207"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(242, _
        161, 106)
    With ActiveWorkbook.Worksheets("��Ըͳ��").Sort
        .SetRange Range("F2:J207")
        .Header = xlGuess
        .MatchCase = False
        .Orientation = xlTopToBottom
        .SortMethod = xlPinYin
        .Apply
    End With
    
    
    
    ' ����L-O���ǽ�ɫ
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Clear
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add2 Key:=Range("O2:O209") _
        , SortOn:=xlSortOnValues, Order:=xlDescending, DataOption:=xlSortNormal
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("L2:L209"), _
        xlSortOnFontColor, xlDescending, , xlSortNormal).SortOnValue.Color = RGB(112, _
        48, 160)
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("L2:L209"), _
        xlSortOnFontColor, xlDescending, , xlSortNormal).SortOnValue.Color = RGB(255, 0 _
        , 0)
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("M2:M209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(174, _
        170, 170)
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("M2:M209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(198, _
        224, 180)
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("M2:M209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(155, _
        194, 230)
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("M2:M209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(237, _
        111, 231)
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("M2:M209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(242, _
        161, 106)
    With ActiveWorkbook.Worksheets("��Ըͳ��").Sort
        .SetRange Range("L2:O209")
        .Header = xlGuess
        .MatchCase = False
        .Orientation = xlTopToBottom
        .SortMethod = xlPinYin
        .Apply
    End With
    
    
    
    ' ����Q-T��������
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Clear
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add2 Key:=Range("T2:T209") _
        , SortOn:=xlSortOnValues, Order:=xlDescending, DataOption:=xlSortNormal
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("R2:R209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(174, _
        170, 170)
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("R2:R209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(198, _
        224, 180)
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("R2:R209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(155, _
        194, 230)
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("R2:R209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(237, _
        111, 231)
    ActiveWorkbook.Worksheets("��Ըͳ��").Sort.SortFields.Add(Range("R2:R209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(242, _
        161, 106)
    With ActiveWorkbook.Worksheets("��Ըͳ��").Sort
        .SetRange Range("Q2:T209")
        .Header = xlGuess
        .MatchCase = False
        .Orientation = xlTopToBottom
        .SortMethod = xlPinYin
        .Apply
    End With


End Sub

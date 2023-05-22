Attribute VB_Name = "模块1"
Sub 排序()
Attribute 排序.VB_ProcData.VB_Invoke_Func = " \n14"
'
' 宏 宏
'

    ' 处理A-D五星角色
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Clear
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add2 Key:=Range("D2:D209") _
        , SortOn:=xlSortOnValues, Order:=xlDescending, DataOption:=xlSortNormal
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("A2:A209"), _
        xlSortOnFontColor, xlDescending, , xlSortNormal).SortOnValue.Color = RGB(112, _
        48, 160)
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("A2:A209"), _
        xlSortOnFontColor, xlDescending, , xlSortNormal).SortOnValue.Color = RGB(255, 0 _
        , 0)
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("B2:B209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(174, _
        170, 170)
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("B2:B209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(198, _
        224, 180)
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("B2:B209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(155, _
        194, 230)
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("B2:B209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(237, _
        111, 231)
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("B2:B209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(242, _
        161, 106)
    With ActiveWorkbook.Worksheets("祈愿统计").Sort
        .SetRange Range("A2:D209")
        .Header = xlGuess
        .MatchCase = False
        .Orientation = xlTopToBottom
        .SortMethod = xlPinYin
        .Apply
    End With
    
    
    
    ' 处理F-J五星武器
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Clear
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add2 Key:=Range("J2:J207") _
        , SortOn:=xlSortOnValues, Order:=xlDescending, DataOption:=xlSortNormal
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("F2:F207"), _
        xlSortOnFontColor, xlDescending, , xlSortNormal).SortOnValue.Color = RGB(255, 0 _
        , 0)
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("G2:G207"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(174, _
        170, 170)
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("G2:G207"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(198, _
        224, 180)
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("G2:G207"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(155, _
        194, 230)
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("G2:G207"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(237, _
        111, 231)
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("G2:G207"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(242, _
        161, 106)
    With ActiveWorkbook.Worksheets("祈愿统计").Sort
        .SetRange Range("F2:J207")
        .Header = xlGuess
        .MatchCase = False
        .Orientation = xlTopToBottom
        .SortMethod = xlPinYin
        .Apply
    End With
    
    
    
    ' 处理L-O四星角色
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Clear
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add2 Key:=Range("O2:O209") _
        , SortOn:=xlSortOnValues, Order:=xlDescending, DataOption:=xlSortNormal
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("L2:L209"), _
        xlSortOnFontColor, xlDescending, , xlSortNormal).SortOnValue.Color = RGB(112, _
        48, 160)
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("L2:L209"), _
        xlSortOnFontColor, xlDescending, , xlSortNormal).SortOnValue.Color = RGB(255, 0 _
        , 0)
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("M2:M209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(174, _
        170, 170)
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("M2:M209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(198, _
        224, 180)
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("M2:M209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(155, _
        194, 230)
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("M2:M209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(237, _
        111, 231)
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("M2:M209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(242, _
        161, 106)
    With ActiveWorkbook.Worksheets("祈愿统计").Sort
        .SetRange Range("L2:O209")
        .Header = xlGuess
        .MatchCase = False
        .Orientation = xlTopToBottom
        .SortMethod = xlPinYin
        .Apply
    End With
    
    
    
    ' 处理Q-T四星武器
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Clear
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add2 Key:=Range("T2:T209") _
        , SortOn:=xlSortOnValues, Order:=xlDescending, DataOption:=xlSortNormal
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("R2:R209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(174, _
        170, 170)
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("R2:R209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(198, _
        224, 180)
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("R2:R209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(155, _
        194, 230)
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("R2:R209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(237, _
        111, 231)
    ActiveWorkbook.Worksheets("祈愿统计").Sort.SortFields.Add(Range("R2:R209"), _
        xlSortOnCellColor, xlAscending, , xlSortNormal).SortOnValue.Color = RGB(242, _
        161, 106)
    With ActiveWorkbook.Worksheets("祈愿统计").Sort
        .SetRange Range("Q2:T209")
        .Header = xlGuess
        .MatchCase = False
        .Orientation = xlTopToBottom
        .SortMethod = xlPinYin
        .Apply
    End With


End Sub

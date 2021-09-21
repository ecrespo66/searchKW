from iBott.excel_activities import Excel

wb = Excel('/Users/enriquecrespodebenito/Desktop/pájaros.xlsx')
i = 1
keywords =[]
while True:
    data = wb.readCell(f"A{i}")
    if data is None:
        break
    else:
        keywords.append(data)
    i += 1

print(keywords)
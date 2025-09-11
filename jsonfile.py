import pandas as pd

df = pd.read_excel("baseSep.xlsx")  #   基本檔
dfA = pd.read_excel('asaysisProfile.xlsx')  #   提示內容
dfE = pd.read_excel("eldlyD.xlsx")  #   老人
dfAbx = pd.read_excel("abx.xlsx")   #   抗生素

col = ['藥品代碼', '商品名稱', '腎功能不良劑量調整', '小兒建議劑量', '頻次說明']
dfX = df[col]

#   '腎功能不良劑量調整', '小兒建議劑量', '提示內容'
dfC = pd.merge(dfX, dfA[['藥品代碼', '提示內容']], how="left")
dfC["提示內容"] = dfC["提示內容"].str.replace(r'\n', r"<br>", regex=True)
dfC["小兒建議劑量"] = dfC["小兒建議劑量"].str.replace(r'\n', r"<br>", regex=True)
dfC["小兒建議劑量"] = dfC["小兒建議劑量"].str.replace(r'<br>\s?[(<br>)]+', r"<br>")
dfC["腎功能不良劑量調整"] = dfC["腎功能不良劑量調整"].str.replace(r'\n', r"<br>", regex=True)

#   老年人潛在性不當用藥
# dfEX = dfE[['藥品代碼', 'Unnamed: 9']]
dfEX = dfE[['藥品代碼', '提示內容']]
dfEX.columns=['藥品代碼', '老人用藥建議']
dfEX["老人用藥建議"] = dfEX["老人用藥建議"].str.replace(r'\n', r"<br>", regex=True)

#   抗生素手冊
col_abx = ['drug_id', '抗生素手冊']
abx = dfAbx[col_abx]
abx.fillna("暫無資料", inplace=True)
abx['抗生素手冊'] = abx['抗生素手冊'].str.replace(r'@ ', r'<br>')

# data cleaning
def change (da):
    da["腎功能不良劑量調整"] = da["腎功能不良劑量調整"].str.replace(r'(ml/min/[\w]).+[$(73 m2)]', r"", regex=True)
    da["腎功能不良劑量調整"] = da["腎功能不良劑量調整"].str.replace(r'(\d+)\.(\d+)', r"\1@\2", regex=True)
    da["腎功能不良劑量調整"] = da["腎功能不良劑量調整"].str.replace(r'[Mm][Aa][Xx]\.', r"Max@", regex=True)
    da["腎功能不良劑量調整"] = da["腎功能不良劑量調整"].str.replace(r'S\.', r"S@", regex=True)
    da["腎功能不良劑量調整"] = da["腎功能不良劑量調整"].str.replace(r'\.|。', r"<br>")
    da["腎功能不良劑量調整"] = da["腎功能不良劑量調整"].str.replace(r'@', r".")
    da["腎功能不良劑量調整"] = da["腎功能不良劑量調整"].str.replace(r'([^(>H)])\[', r"\1<br>[")
    da["腎功能不良劑量調整"] = da["腎功能不良劑量調整"].str.replace(r'Q([\d])H(ESRD)', r"Q\1H<br>\2")
    da["腎功能不良劑量調整"] = da["腎功能不良劑量調整"].str.replace(r'\s(HEMO)', r"<br>\1")
    da["腎功能不良劑量調整"] = da["腎功能不良劑量調整"].str.replace(r'(\d)([Hh])\[(\d)', r"\1\2<br>[\3")
    da["腎功能不良劑量調整"] = da["腎功能不良劑量調整"].str.replace(r'([Ddh])(HEMO)', r"\1<br>\2")
    da["腎功能不良劑量調整"] = da["腎功能不良劑量調整"].str.replace(r'~[^\[\d]\s', r"<br>[")
    da["腎功能不良劑量調整"] = da["腎功能不良劑量調整"].str.replace(r'([DdHh])\[(Clcr)', r"\1<br>[\2")
    da["腎功能不良劑量調整"] = da["腎功能不良劑量調整"].str.replace(r'([hH])(C)([lR])', r"\1<br>\2\3")
    da["腎功能不良劑量調整"] = da["腎功能不良劑量調整"].str.replace(r'<br>\s?(<br>)*', r"<br>")
    return da

dfCR = change(dfC)
dfCX = pd.merge(dfCR, dfEX, how='left', on='藥品代碼')
dfCM = pd.merge(dfCX, abx, how='left', left_on='藥品代碼', right_on='drug_id')
dfCM.set_index("藥品代碼", inplace=True)
dfCM.fillna("暫無資料", inplace=True)
dfCM.drop("drug_id", axis=1, inplace=True)
dfCM.to_json("drugs_2025.json", orient="index", force_ascii=False)
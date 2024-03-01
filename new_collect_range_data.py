import pandas as pd
def collect_range_data(file):
    range_data = pd.read_excel(file, sheet_name='Sheet1', usecols='K:L')
    range_data.fillna(value=0)
    add4_gains = [float(range_data.iloc[25,0]), float(range_data.iloc[25,1])]
    add3_gains = [float(range_data.iloc[9,0]), float(range_data.iloc[9,1])]
    add1_gains = [float(range_data.iloc[18,0]), float(range_data.iloc[18,1])]
    adc_gains = [float(range_data.iloc[11,0]), float(range_data.iloc[11,1])]
    dac_dict = {'ADD1': add1_gains[0], 'ADD3': add3_gains[0], 'ADD4': add4_gains[0]}
    adc_dict = {'ADD1': add1_gains[1], 'ADD3': add3_gains[1], 'ADD4': add4_gains[1], 'LTC': adc_gains[1]}
    # print(dac_dict, adc_dict)
    return dac_dict, adc_dict


collect_range_data('excelData/ADD_adapter_test.xlsm')

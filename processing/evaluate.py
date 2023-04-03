import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
from sklearn.metrics import precision_recall_fscore_support as score

groundTrueData = pd.read_csv('../groundTrueData/Geovirusdata_reverse_error_check.csv')
#print(groundTrueData[groundTrueData['name'] == 'Rangitoto'])

GeocodedData3 = pd.read_csv('../processing/disambiguatedfas.csv')
GeocodedData3 = GeocodedData3[GeocodedData3['Country_Code'].notnull()]
print(GeocodedData3.shape)

def evaluate(y_test, predicted):
    precision, recall, fscore, support = score(y_test, predicted, average="weighted") # weighted, macro
    print('precision: {}'.format(precision))
    print('recall: {}'.format(recall))
    print('fscore: {}'.format(fscore))
    print('support: {}'.format(support))
    return precision, recall, fscore, support
def desamb_grndtrue(groundTrueData, GeocodedData):
    print('Initial shape :', groundTrueData.shape, GeocodedData.shape)
    GeocodedData['name'] = GeocodedData['input_sne']

    df_groundTrueData = groundTrueData[groundTrueData['country_code'].notnull()]
    df_GeocodedData = GeocodedData[GeocodedData['Country_Code'].notnull()]

    df_groundTrueData['name'] = df_groundTrueData['name'].str.lower()
    df_GeocodedData['name'] = df_GeocodedData['name'].str.lower()

    merged_df = pd.merge(df_groundTrueData, df_GeocodedData, how = 'inner', on=['source', 'name'])
    data_copy = merged_df.copy()

    merged_df['True_country_code'] = merged_df['country_code']
    merged_df['Predicted_country_code'] = merged_df['Country_Code']

    merged_df = merged_df[['source', 'name', 'country_code', 'Output_sne', 'Desamb_Phase', 'input_sne',
                           'True_country_code','Predicted_country_code']]
    print(merged_df)
    merged_df['y_test'] = 1

    merged_df['predicted'] = np.where(merged_df['True_country_code'] == merged_df['Predicted_country_code'] , 1, 0)

#     errors = merged_df.loc[merged_df['country_code'] != merged_df['Country_Code']]

    errors = merged_df[merged_df['True_country_code'] != merged_df['Predicted_country_code']]

    y_test = merged_df['y_test'].tolist()
    predicted = merged_df['predicted'].tolist()

    precision, recall, fscore, support = evaluate(np.array(y_test), np.array(predicted))
    return precision, recall, fscore, support, errors


precision, recall, fscore, support, errors = desamb_grndtrue(groundTrueData, GeocodedData3)
print("### :", len(groundTrueData), len(GeocodedData3))
print("************\n")


###### Check for erros status
errors_by_ph = errors['Desamb_Phase'].value_counts()
print(errors_by_ph)
def plot_phase(df):
    plt.figure(figsize=(15,12))
    df.plot(kind='bar', )
    plt.title('Desambiguation Method', fontsize=15)
    plt.xlabel('Desambiguation phase', fontsize=15)
    plt.xticks(rotation=90, fontsize=15)
    plt.ylabel('Number of desamb SNE', fontsize=15)
    plt.yticks(fontsize=15)
    plt.savefig('../processing/error_by_phase.jpeg')
    plt.show()
    plt.close()


plot_phase(errors_by_ph)


def evaluate_on_defaultgeo(file):
    merged_df =  pd.read_csv(file)

    merged_df['y_test'] = 1

    merged_df['predicted'] = np.where(merged_df['country_code'] == merged_df['deflt_Country_code'] , 1, 0)

#     errors = merged_df.loc[merged_df['country_code'] != merged_df['Country_Code']]

    errors = merged_df[merged_df['country_code'] != merged_df['deflt_Country_code']]

    y_test = merged_df['y_test'].tolist()
    predicted = merged_df['predicted'].tolist()

    precision, recall, fscore, support = evaluate(np.array(y_test), np.array(predicted))
    return precision, recall, fscore, support, errors


precision, recall, fscore, support, errors = evaluate_on_defaultgeo("../processing/defaultgeocoding.csv")

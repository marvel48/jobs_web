import pandas as pd
CSV_FILE = 'results.csv'
BASE = "https://ltclicensing.oregon.gov"
KEEP = ['city', 'beds', 'funding_source', 'status', 'url', 'street',
        'zip', 'facility_type', 'admin_name', 'phone', 'email', 'owner',
        'owner_since'
       ]
MAPPING_COLUMNS = {
    'url':'Individual Facility URL',
                'street':'Street',
                'zip':'Zip',
                'admin_name':'Administrator Name',
                'owner':'Owner',
                'email':'Email',
                'status': 'Status',
                'facility_name':'',
                'phone':'Phone',
                'beds':'Total Licensed Beds',
                'funding_source':'Funding Source(s)',
                'facility_type':'Facility Type',
                'city':'City', 
               }
def get_dataframe():
    ''' return dataframe with processed url and zip '''
    df = pd.read_csv(CSV_FILE)
    df['url'] = df['url'].apply(lambda x: (BASE+x))
    df['zip'] = df['zip'].apply(lambda x: x.split()[-1])
    df = df[KEEP]
    df = df.rename(columns=MAPPING_COLUMNS)
    return df


if __name__=='__main__':
    ''' main '''
    df = get_dataframe()
    df.to_excel('OregeonFacilities.xlsx', encoding='utf-8')



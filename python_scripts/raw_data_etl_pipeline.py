from extract_functions import extract_csv
from load_functions import load_db, load_db_append 

raw_rev_1_data = extract_csv(R'C:\Users\alexs\OneDrive\Documents\Data Engineering\EV_CPO_V1\Raw Data Files\Revenue_source_1.csv')
raw_rev_2_data = extract_csv(R'C:\Users\alexs\OneDrive\Documents\Data Engineering\EV_CPO_V1\Raw Data Files\Revenue_source_2.csv')
raw_rev_3_data = extract_csv(R'C:\Users\alexs\OneDrive\Documents\Data Engineering\EV_CPO_V1\Raw Data Files\Revenue_source_3.csv')

load_db(raw_rev_1_data, 'rev_source_1')
load_db(raw_rev_2_data, 'rev_source_2')
load_db(raw_rev_3_data, 'rev_source_3')

load_db_append('rev_source_1', 'rev_source_1_append')
load_db_append('rev_source_2', 'rev_source_2_append')
load_db_append('rev_source_3', 'rev_source_3_append')
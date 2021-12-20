import pandas as pd
import datetime as dt
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.plotting import plot_period_transactions

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 20)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Görev 1:

# 1. Online Retail II excelindeki 2010-2011 verisini okuyunuz. Oluşturduğunuz dataframe’in kopyasını oluşturunuz.


df = pd.read_excel(r"/Users/cenancanbikmaz/PycharmProjects/DSMLBC-7/HAFTA_3/online_retail_II.xlsx")

df_ = df.copy()

df_.head()

# # 2. Veri setinin betimsel istatistiklerini inceleyiniz.

def check_df(dataframe):
    print("################ Shape ####################")
    print(dataframe.shape)
    print("############### Columns ###################")
    print(dataframe.columns)
    print("############### Types #####################")
    print(dataframe.dtypes)
    print("############### Head ######################")
    print(dataframe.head())
    print("############### Tail ######################")
    print(dataframe.tail())
    print("############### Describe ###################")
    print(dataframe.describe().T)

check_df(df)

# 3. Veri setinde eksik gözlem var mı? Varsa hangi değişkende kaç tane eksik gözlem vardır?

df.isnull().sum()

# Invoice             0
# StockCode           0
# Description      2928
# Quantity            0
# InvoiceDate         0
# Price               0
# Customer ID    107927
# Country             0

# 4. Eksik gözlemleri veri setinden çıkartınız. Çıkarma işleminde ‘inplace=True’ parametresini kullanınız.

df.dropna(inplace=True)

# 5. Eşsiz ürün sayısı kaçtır?

df["Description"].nunique()

# 4459

# 6. Hangi üründen kaçar tane vardır?

df["Description"].value_counts()

# 7. En çok sipariş edilen 5 ürünü çoktan aza doğru sıralayınız.

df['Description'].value_counts().sort_values(ascending=False).head(5)

# WHITE HANGING HEART T-LIGHT HOLDER    3245
# REGENCY CAKESTAND 3 TIER              1872
# STRAWBERRY CERAMIC TRINKET BOX        1536
# ASSORTED COLOUR BIRD ORNAMENT         1376
# HOME BUILDING BLOCK WORD              1229

# 8. Faturalardaki‘C’iptal edilen işlemleri göstermektedir. İptal edilen işlemleri veri setinden çıkartınız.

df = df[~df["Invoice"].str.contains("C", na=False)]

df = df[(df['Quantity'] > 0)]

df = df[(df['Price'] > 0)]

def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

replace_with_thresholds(df, 'Quantity')

replace_with_thresholds(df, 'Price')

# 9. Fatura başına elde edilen toplam kazancı ifade eden ‘TotalPrice’ adında bir değişken oluşturunuz.

df['TotalPrice'] = df['Quantity'] * df['Price']

df.describe().T

# Quantity    407664.00000    11.90652   28.72511     1.00000     2.00000
# Price       407664.00000     3.00562    3.25057     0.00100     1.25000
# Customer ID 407664.00000 15368.59260 1679.76214 12346.00000 13997.00000
# TotalPrice  407664.00000    20.66303   52.13736     0.00100     4.95000
#                     50%         75%         max
# Quantity        5.00000    12.00000   358.50000
# Price           1.95000     3.75000    36.94000
# Customer ID 15321.00000 16812.00000 18287.00000
# TotalPrice     11.90000    19.50000  3925.57500

# Görev 2: RFM metriklerinin hesaplanması

# Recency, Frequency ve Monetary tanımlarını yapınız.

# Müşteri özelinde Recency, Frequency ve Monetary metriklerini groupby, agg ve lambda ile hesaplayınız.

# Hesapladığınız metrikleri rfm isimli bir değişkene atayınız.

# Oluşturduğunuz metriklerin isimlerini recency, frequency ve monetary olarak değiştiriniz.

df['InvoiceDate'].max()

today_date = dt.datetime(2011, 12, 11)

rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda InvoiceDate: (today_date - InvoiceDate.max()).days, 'Invoice': lambda Invoice: Invoice.nunique(), 'TotalPrice': lambda TotalPrice: TotalPrice.sum()})

rfm.head()

rfm.columns = ['recency', 'frequency', 'monetary']

# Görev 3: RFM skorlarının oluşturulması ve tek bir değişkene çevrilmesi

# Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çeviriniz.

# Bu skorları recency_score, frequency_score ve monetary_score olarak kaydediniz.

# Oluşan 2 farklı değişkenin değerini tek bir değişken olarak ifade ediniz ve RFM_SCORE olarak kaydediniz.

rfm['recency_score'] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])

rfm['frequency_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])

rfm['monetary_score'] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm['RFM_SCORE'] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str))

rfm.describe().T

rfm.head()

rfm[rfm['RFM_SCORE'] == '55'].head()

rfm[rfm['RFM_SCORE'] == '11'].head()

# Görev 4: RFM skorlarının segment olarak tanımlanması

# Oluşturulan RFM skorların daha açıklanabilir olması için segment tanımlamaları yapınız.

seg_map = {r'[1-2][1-2]': 'hibernating',
           r'[1-2][3-4]': 'at_Risk',
           r'[1-2]5': 'cant_loose',
           r'3[1-2]': 'about_to_sleep',
           r'33': 'need_attention',
           r'[3-4][4-5]': 'loyal_customers',
           r'41': 'promising',
           r'51': 'new_customers',
           r'[4-5][2-3]': 'potential_loyalists',
           r'5[4-5]': 'champions'}

rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)

rfm.head()

# Görev 5: Önemli bulduğunuz 3 segmenti seçiniz. Bu üç segmenti;

# - Hem aksiyon kararları açısından,

# - Hem de segmentlerin yapısı açısından (ortalama RFM değerleri) yorumlayınız.

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

# segment                     recency       frequency         monetary
#                     mean      count   mean    count  mean      count
#
# about_to_sleep      418.81924   343   1.20117   343  435.42911   343
# at_Risk             517.15876   611   3.07365   611 1089.29237   611
# cant_loose          489.11688    77   9.11688    77 3486.98753    77
# champions           372.11916   663  12.55354   663 6570.38743   663
# hibernating         578.88571  1015   1.12611  1015  363.96283  1015
# loyal_customers     401.28706   742   6.83019   742 2672.96751   742
# need_attention      418.26570   207   2.44928   207 1009.15886   207
# new_customers       373.58000    50   1.00000    50  385.87780    50

rfm[rfm["segment"] == "hibernating"].head()

# Alışveriş yapma sıklığı uzun süren ve uykuda olan müşterilerdir. Bu müşterilerin dikkatini çekebilecek
# pazarlama stratejileri geliştirilmelidir.

rfm[rfm["segment"] == "loyal_customers"].head()

# Bu müşteriler potansiyel sadık müşterilerdir. Bu sebeple bu müşterilere özel kampanyalar hazırlanmalı ve
# haftalık veya günlük alışveriş fiyat bültenleri ve kampayalar ile ilgili bilgiler gönderilmelidir.

rfm[rfm["segment"] == "need_attention"].head()

# Bu müşteriler dikkat edilmesi gereken potansiyel sadık müşteri olma yolunda ilerleyen müşterilerdir.
# Bu müşterilere özel bazı kampanyalar, indirimler düzenlenmeli ve dikkatli çekilmelidir.

new_df = pd.DataFrame()
new_df["new_customer_id_v2"] = rfm[rfm["segment"] == "loyal_customers"].index
new_df.to_excel("new_customers.xlsx")


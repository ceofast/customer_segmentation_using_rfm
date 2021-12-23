# customer_segmentation_using_rfm
# Invoice      : Invoice Number, If this code starts with C, it means that the operation has been cancelled.       
# StockCode    : Stock Code, Unique number for each product. 
# Description  : Description, Product name.
# Quantity     : Quantity, Number of products.
# InvoiceDate  : Invoice date.
# Price        : Invoice price (Sterling).
# Customer ID  : Unique customer number.
# Country      : Country name.

Task 1 :

1. Read the 2010 - 2011 data in the Online Retail II excel. Make a copy of the dataframe you created.
2. Examine the descriptive statistics of the data set.
3. Are there any missing observations in the data set? If yes, how many missing observations in which variable?
4. Remove the missing observations from the data set. Use the 'inplace=True' parameter for subtraction.
5. How many unique items are there?
6. How many of each product are there?
7. Sort the 5 most ordered products from most to least.
8. The 'C' in the invoices shows the canceled transactions. Remove the canceled transactions from the dataset.
9. Create a variable named 'TotalPrice' that represents the total earnings per invoice.

Task 2 : Calculation of RFM metrics.

Make the definitions of Recency, Frequency and Monetary.
Calculate customer specific Recency, Frequency and Monetary metrics with groupby, agg and lambda.
Assign your calculated metrics to a variable named rfm.
Change the names of the metrics you created to recency, frequency and monetary.
Note 1: For the recency value, accept today's date as (2011, 12, 11).
Note 2: After creating the rfm dataframe, filter the dataset to "monetary>0".

Task 3: Generating and converting RFM scores to a single variable

Convert Recency, Frequency and Monetary metrics to scores between 1-5 with the help of qcut.
Record these scores as recency_score, frequency_score and monetary_score.
Express the value of 2 different variables as a single variable and save it as RFM_SCORE.
E.g;
Create the recency_score, frequency_score scores of 5, 2, respectively, in separate variables, with the naming of the RFM_SCORE variable.

CAUTION! We do not include the Monetary score.

Task 4: Defining RFM scores as segments

Make segment definitions so that the generated RFM scores can be explained more clearly.
Convert the scores into segments with the help of the seg_map below. Clue:

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
           
Task 5: It's action time!

Select 3 segments that you find important. These three segments;
- Both in terms of action decisions,
- Interpret both in terms of the structure of the segments (mean RFM values).
Select the customer IDs of the "Loyal Customers" class and get the excel output.

These documentations belong to the "Veri Bilimi Okulu". Do not use in any article and publication without permission.

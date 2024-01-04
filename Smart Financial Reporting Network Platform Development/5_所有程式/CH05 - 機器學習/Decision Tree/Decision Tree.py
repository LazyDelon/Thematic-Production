import os
import numpy as np 
import pandas as pd 


import matplotlib.pyplot as plt 

import warnings

warnings.filterwarnings('ignore')


data = '正3負2.csv'
df = pd.read_csv(data)
df['判斷'] = df['代碼']
df.to_csv('正3負2.csv', index=False, encoding='utf-8-sig')
df


data = '正3負2.csv'
df = pd.read_csv(data, index_col='判斷')
df = df.drop_duplicates(keep='first')
df.to_csv('正3負2.csv', index=False, encoding='utf-8-sig')
df


df['正負樣本'].value_counts()


X = df.drop(['代碼', '股票', 'ROE_5Y.1', 'EPS_5Y.1', '毛利率_5Y.1', '現金殖利率.1', '符合數量', '正負樣本'], axis=1) 

y = df['正負樣本']


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33, random_state = 42)


from sklearn.tree import DecisionTreeClassifier


clf_gini = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=0)

clf_gini.fit(X_train, y_train)

y_pred_gini = clf_gini.predict(X_test)


from sklearn.metrics import accuracy_score

print('Model accuracy score with criterion gini index: {0:0.4f}'. format(accuracy_score(y_test, y_pred_gini)))


y_pred_train_gini = clf_gini.predict(X_train)

y_pred_train_gini


print('Training-set accuracy score: {0:0.4f}'. format(accuracy_score(y_train, y_pred_train_gini)))


print('Training set score: {:.4f}'.format(clf_gini.score(X_train, y_train)))

print('Test set score: {:.4f}'.format(clf_gini.score(X_test, y_test)))


plt.figure(figsize=(12,8))

from sklearn import tree

tree.plot_tree(clf_gini.fit(X_train, y_train), feature_names=X_train.columns)

import graphviz 

Data = tree.export_graphviz(clf_gini, out_file=None, feature_names=X_train.columns)   
Output = graphviz.Source(Data.replace('helvetica', "Microsoft YaHei"), encoding='utf-8')
Output.format = 'png'
Output.render("正3負2") 
Output

df = X_train.merge(y_train, on='判斷')
df


# A類：第一種可能

# 355 rows × 4 columns
ROE_5Y = df[(df['ROE_5Y'] <= 10.035)]
ROE_5Y

# 290 rows × 4 columns
Dividend_Yield = ROE_5Y[(ROE_5Y['現金殖利率'] <= 5.045)]
Dividend_Yield

Dividend_Yield['代碼'] = Dividend_Yield.index
Dividend_Yield.to_csv('Class_A.csv', encoding='utf-8-sig')

A = Dividend_Yield
A


# B類：第二種可能

# 355 rows × 4 columns
ROE_5Y = df[(df['ROE_5Y'] <= 10.035)]
ROE_5Y

# 65 rows × 4 columns
Dividend_Yield = ROE_5Y[(ROE_5Y['現金殖利率'] >= 5.045)]
Dividend_Yield

# 37 rows × 4 columns
Gross_Margin = Dividend_Yield[(Dividend_Yield['毛利率_5Y'] <= 20.335)]
Gross_Margin
len(Gross_Margin)

Gross_Margin['代碼'] = Gross_Margin.index
Gross_Margin.to_csv('Class_B.csv', encoding='utf-8-sig')

B = Gross_Margin
B

# 355 rows × 4 columns
ROE_5Y = df[(df['ROE_5Y'] <= 10.035)]
ROE_5Y

# 65 rows × 4 columns
Dividend_Yield = ROE_5Y[(ROE_5Y['現金殖利率'] >= 5.045)]
Dividend_Yield

# 37 rows × 4 columns
Gross_Margin = Dividend_Yield[(Dividend_Yield['毛利率_5Y'] >= 20.335)]
Gross_Margin
len(Gross_Margin)

Gross_Margin['代碼'] = Gross_Margin.index
Gross_Margin.to_csv('Class_C.csv', encoding='utf-8-sig')

C = Gross_Margin
C

# D類：第四種可能

# 246 rows × 4 columns
ROE_5Y = df[(df['ROE_5Y'] >= 10.035)]
ROE_5Y

# 85 rows × 4 columns
Gross_Margin = ROE_5Y[(ROE_5Y['毛利率_5Y'] <= 19.98)]
Gross_Margin

# 41 rows × 4 columns
Dividend_Yield = Gross_Margin[(Gross_Margin['現金殖利率'] <= 4.905)]
Dividend_Yield
# len(Dividend_Yield)

Dividend_Yield['代碼'] = Dividend_Yield.index
Dividend_Yield.to_csv('Class_D.csv', encoding='utf-8-sig')

D = Dividend_Yield
D


# E類：第五種可能

# 246 rows × 4 columns
ROE_5Y = df[(df['ROE_5Y'] >= 10.035)]
ROE_5Y

# 85 rows × 4 columns
Gross_Margin = ROE_5Y[(ROE_5Y['毛利率_5Y'] <= 19.98)]
Gross_Margin

# 44 rows × 4 columns
Dividend_Yield = Gross_Margin[(Gross_Margin['現金殖利率'] >= 4.905)]
Dividend_Yield
len(Dividend_Yield)

Dividend_Yield['代碼'] = Dividend_Yield.index
Dividend_Yield.to_csv('Class_E.csv', encoding='utf-8-sig')

E = Dividend_Yield
E

# F類：第四種可能

# 246 rows × 4 columns
ROE_5Y = df[(df['ROE_5Y'] >= 10.035)]
ROE_5Y

# 161 rows × 4 columns
Gross_Margin = ROE_5Y[(ROE_5Y['毛利率_5Y'] >= 19.98)]
Gross_Margin

Gross_Margin['代碼'] = Gross_Margin.index
Gross_Margin.to_csv('Class_F.csv', encoding='utf-8-sig')

F = Gross_Margin
F


# 正樣本資料

True_M = pd.concat([C, E, F])
True_M['代碼'] = True_M.index
True_M.to_csv('Possitive Sample Data.csv', encoding='utf-8-sig')
True_M


# 負樣本資料

False_M = pd.concat([A, B, D])
False_M['代碼'] = False_M.index
False_M.to_csv('Negative Sample Data.csv', encoding='utf-8-sig')
False_M


data = '正3負2.csv'
File = pd.read_csv(data)
File['判斷'] = File['代碼']
File.to_csv('正3負2.csv', index=False, encoding='utf-8-sig')
File

data = '正3負2.csv'
File = pd.read_csv(data, index_col='判斷')
File = File.drop_duplicates(keep='first')
File.to_csv('正3負2.csv', index=False, encoding='utf-8-sig')
File

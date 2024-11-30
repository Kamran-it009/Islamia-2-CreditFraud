import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

df = pd.read_csv('fraudTest.csv')


def fraud_transaction():
    d = df["is_fraud"].value_counts().reset_index()
    d.columns = ['is_fraud', 'count']
    # Create the pie chart with updated parameters
    fig = px.pie(d, values="count", names=['No', 'Yes'], hole=0.40, opacity=0.9,
                 labels={"is_fraud": "Fraud", "count": "Number of Samples"})
    fig.update_layout(title=dict(text="Pie Chart of Fraudulent Transactions"))
    fig.update_traces(textposition="outside", textinfo="percent+label")
    fig.show()

def gender_analysis():
    df_fraud = df[df['is_fraud'] == 1]
    plt.figure(figsize=(5, 5))
    sns.set()
    plt.title('Gender Analysis of Fraud Persons')
    sns.countplot(x=df_fraud['gender'], color='tomato')
    plt.xlabel('Gender')
    plt.ylabel('Count')
    plt.show()

def category_analysis():
    df_fraud = df[df['is_fraud'] == 1]
    plt.figure(figsize=(14, 7))
    sns.set()
    plt.suptitle('Category Analysis of Fraud persons')
    sns.countplot(df_fraud['category'], palette='winter')
    plt.xlabel('Number of Trasactions')
    plt.ylabel('Trasaction Category')
    plt.show()

def ammount_distribution():
    df_fraud = df[df['is_fraud'] == 1]
    amounts = df_fraud['amt']
    bins = [0, 100, 500, 1000, 5000]
    labels = ['0-100', '101-500', '501-1000', '1001-5000']
    df_fraud['amount_range'] = pd.cut(amounts, bins=bins, labels=labels)
    plt.figure(figsize=(8, 6))
    sns.set(style="whitegrid")
    sns.countplot(x='amount_range', data=df_fraud, palette='summer')
    plt.title('Amount Distribution Across Different Ranges')
    plt.xlabel('Amount Range')
    plt.ylabel('Frequency')
    plt.xticks()
    plt.show()

gender_analysis()
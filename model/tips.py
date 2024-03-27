## Python Titanic Model, prepared for a titanic.py file

# Import the required libraries for the TitanicModel class
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression

class TipsModel:
    """This class encompasses the total tip model to predict how much a customer will tip based on various factors."""
    
    _instance = None

    def __init__(self):
        self.tips_data = sns.load_dataset('tips')
        self.model = None
        self.features = ['total_bill', 'sex', 'smoker', 'time', 'size']
        self.target = 'tip'
        self.encoder = OneHotEncoder(handle_unknown='ignore')

    def _clean(self):
        self.tips_data['sex'] = self.tips_data['sex'].apply(lambda x: 1 if x == 'Male' else 0)
        self.tips_data['smoker'] = self.tips_data['smoker'].apply(lambda x: 1 if x == 'Yes' else 0)
        self.tips_data['time'] = self.tips_data['time'].apply(lambda x: 1 if x == 'Dinner' else 0)

        # One-hot encode 'day' column
        onehot = self.encoder.fit_transform(self.tips_data[['day']]).toarray()
        cols = ['day_' + str(val) for val in self.encoder.categories_[0]]
        onehot_df = pd.DataFrame(onehot, columns=cols)
        self.tips_data = pd.concat([self.tips_data, onehot_df], axis=1)
        self.features.extend(cols)

        self.tips_data.dropna(inplace=True)

    def _train(self):
        X = self.tips_data[self.features]
        y = self.tips_data[self.target]

        self.model = LinearRegression()
        self.model.fit(X, y)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._clean()
            cls._instance._train()
        return cls._instance

    def predict_tip(self, customer):
        # Clean and prepare customer data for prediction
        customer_df = pd.DataFrame(customer, index=[0])
        
        # Ensure that categorical variables are encoded using the same scheme as in the training data
        customer_df['sex'] = customer_df['sex'].apply(lambda x: 1 if x == 'Male' else 0)
        customer_df['smoker'] = customer_df['smoker'].apply(lambda x: 1 if x == 'Yes' else 0)
        customer_df['time'] = customer_df['time'].apply(lambda x: 1 if x == 'Dinner' else 0)
        
        # One-hot encode 'day' column
        for day in ['Fri', 'Sat', 'Sun', 'Thur']:
            customer_df['day_' + day] = 0  # Initialize all day columns to 0
        if 'day' in customer:
            customer_df['day_' + customer['day'][0]] = 1  # Set the corresponding day column to 1 if present
        
        # Ensure the features are in the same order as in the training data
        customer_df = customer_df.reindex(columns=self.features, fill_value=0)
        
        # Predict the tip amount
        tip_amount = self.model.predict(customer_df)
        return tip_amount[0]


def testTip():
    print("Step 1: Define customer data for prediction:")
    customer_info = {
        'total_bill': [16.99],
        'sex': ['Female'],
        'smoker': ['No'],
        'day': ['Sun'],  # Ensure 'Sun' is passed as a string
        'time': ['Dinner'],
        'size': [2]
    }
    print("\t", customer_info)
    print()

    tipModel = TipsModel.get_instance()
    print("Step 2:", tipModel.get_instance.__doc__)
   
    print("Step 3:", tipModel.predict_tip.__doc__)
    tip_amount = tipModel.predict_tip(customer_info)
    print('\t Predicted tip amount: ${:.2f}'.format(tip_amount))
    print()
    
    
def initTips1():
    """ Initialize the Titanic Model.
    This function is used to load the Titanic Model into memory, and prepare it for prediction.
    """
    TipsModel.get_instance()
    
if __name__ == "__main__":
    print("Begin:", testTip.__doc__)
    testTip()

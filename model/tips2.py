## Python Titanic Model, prepared for a titanic.py file

# Import the required libraries for the TitanicModel class
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np
import seaborn as sns

class TipsModel2:
    """This whole class encompasses the total tip model to determine how much a customer will tip based on other facts
       Utilizes the seaborne CSV dataset of https://github.com/mwaskom/seaborn-data/blob/master/tips.csv
    """
    # This is the instance which stores the entire model, you can use this model many times in prediction, but it's initialized once
    _instance = None
    
    # constructor, used to initialize the whole tips model 
    def __init__(self):
        # Load the seaborn dataset of tips.csv
        self.tips_data = sns.load_dataset('tips')

        # Determine the  model
        self.model = None

        # define ML features and target
        self.features = ['total_bill', 'sex', 'smoker', 'dayThur', 'dayFri', "daySat", "daySun", 'time', 'size']
        self.target = 'tip'
        # Update self.features to match the updated column names, because when it one hot encodes it'll include 
        # Thursday, Friday, Saturday, Sunday as numerical numbers, so if it was on that day it'll be represented as likely a 1
        self.encoder = OneHotEncoder(handle_unknown='ignore')


    # clean the tips dataset, prepare it for training
    def _clean(self):

        # All these options that can be represented binarically with 1's and 0's convert them (basically anything with two options only turn it into an integer)
        self.tips_data['sex'] = self.tips_data['sex'].apply(lambda x: 1 if x == 'male' else 0)
        self.tips_data['smoker'] = self.tips_data['smoker'].apply(lambda x: 1 if x == 'Yes' else 0)
        self.tips_data['time'] = self.tips_data['time'].apply(lambda x: 1 if x == 'Dinner' else 0) 


        # Drop any rows within the day subset 
        self.tips_data.dropna(subset=['day'], inplace=True)

        # Categorical data of day turning into a binary matrix -> transform it into a n numpy array stored in onehot
        onehot = self.encoder.fit_transform(self.tips_data[['day']]).toarray()

        # Here we're gonna create a bunch of different columns with each specific date 
        cols = ['day' + str(val) for val in self.encoder.categories_[0]]

        # Now load the oneshot as a dataframe for pandas
        onehot_df = pd.DataFrame(onehot, columns=cols)
        self.tips_data = pd.concat([self.tips_data, onehot_df], axis=1)

        # Remove the categorical columns for the day
        self.tips_data.drop(['day'], axis=1, inplace=True)

        # Add these columns to the specific features for us to analyze
        self.features.extend(cols)

        # I don't' don't I need this for the tips data
        self.tips_data.dropna(inplace=True)


        

    # train the tips model using linear regression
    def _train(self):
        # split the data into features and target, the dependant 
        x = self.tips_data[self.features]
        y = self.tips_data[self.target]

        # Use LinearRegression for regression tasks, beucase linear regression has a continous outcome of the tip variable
        # Logistic Regression is used in a yes / no example and wouldn't really be relevant here
        self.model = LinearRegression()
        self.model.fit(x, y)

    @classmethod
    def get_instance(cls):
        """ First let's check if the instance exists for the Tips Model.
        The model is used for predicting tip amounts based on customer information.

        Returns:
            Tips model: a singular one time use _instance of the TitanicModel, which contains data and methods for prediction.
        """        
        # check for instance, if it doesn't exist, create it
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._clean()
            cls._instance._train()
        # return the instance, to be used for prediction
        return cls._instance

    def predict_tip(self, customer_info):
        """ Predict the tip amount for a customer based on their information.

        Args:
            customer_info (dict): A dictionary representing customer information. The dictionary should contain the following keys:
                'total_bill': The total bill amount which is just a float
                'sex': The customer's sex ('Male' or 'Female')
                'smoker': Whether the customer is a smoker ('Yes' or 'No')
                'day': The day of the week ('Thur', 'Fri', 'Sat', 'Sun')
                'time': The time of day ('Lunch' or 'Dinner')
                'size': The size of the group which is an integer

        Returns:
        float: predicted tip amount
        """
        # clean the customer data and prepare it for prediction using dataframes from pandas
        customer_df = pd.DataFrame(customer_info, index=[0])


        # Again here we're going to apply binary form on categories that are one or the other
        customer_df['sex'] = customer_df['sex'].apply(lambda x: 1 if x == 'Male' else 0)
        customer_df['smoker'] = customer_df['smoker'].apply(lambda x: 1 if x == 'Yes' else 0)
        customer_df['time'] = customer_df['time'].apply(lambda x: 1 if x == 'Dinner' else 0) 



        # One-hot encode 'day' feature -> Binary matrix x-> dataframe and having the multiple categories of each specific day in a binary matrix
        onehot = self.encoder.transform(customer_df[['day']]).toarray()
        cols = ['day' + str(val) for val in self.encoder.categories_[0]]
        onehot_df = pd.DataFrame(onehot, columns=cols)
        customer_df = pd.concat([customer_df, onehot_df], axis=1)
        customer_df.drop(['day'], axis=1, inplace=True)
        
        # Ensure feature names match those used during training
        customer_df = customer_df[self.features]

        # Predict tip using the trained model
        tip = np.squeeze(self.model.predict(customer_df))
        
        return tip
    
def testTip():
    """ Test the Titanic Model for predicting tip amounts.
    Using the TitanicModel class, we can predict the tip amount for a customer.
    Print output of this test contains method documentation, customer data, and predicted tip amount.
    """
     
    # setup customer data for prediction
    print(" Step 1: Define customer data for prediction:")
    customer_info = {
        'total_bill': [16.99],
        'sex': ['Female'],
        'smoker': ['No'],
        'day': ['Sun'],
        'time': ['Dinner'],
        'size': [2]
    }
    print("\t", customer_info)
    print()

    # get an instance of the cleaned and trained Titanic Model
    tipModel = TipsModel2.get_instance()
    print(" Step 2:", tipModel.get_instance.__doc__)
   
    # print the predicted tip amount
    print(" Step 3:", tipModel.predict_tip.__doc__)
    tip_amount = tipModel.predict_tip(customer_info)
    print('\t Predicted tip amount: ${:.2f}'.format(tip_amount))
    print()
    
    
def initTips2():
    """ Initialize the Titanic Model.
    This function is used to load the Titanic Model into memory, and prepare it for prediction.
    """
    TipsModel2.get_instance()

if __name__ == "__main__":
    print(" Begin:", testTip.__doc__)
    testTip()
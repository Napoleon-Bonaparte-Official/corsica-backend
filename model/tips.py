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

class TipsModel:
    """This whole class encompasses the total tip model to determine how much a customer will tip based on other facts
    """
    # This is the instance which stores the entire model, you can use this model many times in prediction, but it's initialized once
    _instance = None
    
    # constructor, used to initialize the TitanicModel
    def __init__(self):
        self.tips_data = sns.load_dataset('tips')
        # Determine the  model
        self.model = None
        self.dt = None
        # define ML features and target
        self.features = ['total_bill', 'sex', 'smoker', 'day', 'time', 'size']
        self.target = 'tip'

        self.tips_data = sns.load_dataset('tips')

        # Update self.features to match the updated column names
        self.encoder = OneHotEncoder(handle_unknown='ignore')
        # load the titanic dataset




    # clean the tips dataset, prepare it for training
    def _clean(self):
        self.titanic_data['sex'] = self.titanic_data['sex'].apply(lambda x: 1 if x == 'male' else 0)
        self.
        # Categorical data of Day
        onehot = self.encoder.fit_transform(self.tips_data[['day']]).toarray()
        cols = ['day' + str(val) for val in self.encoder.categories_[0]]
        onehot_df = pd.DataFrame(onehot, columns=cols)
        self.titanic_data = pd.concat([self.titanic_data, onehot_df], axis=1)
        self.titanic_data.drop(['day'], axis=1, inplace=True)


        

      # train the tips model using linear regression
    def _train(self):
        # split the data into features and target
        X = self.tips_data[self.features]
        y = self.tips_data[self.target]
        
        # perform train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # initialize and train the model
        self.model = LogisticRegression(iter=1000)
        self.model.fit(X_train, y_train)
        
        # evaluate the model
        y_pred = self.model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        print(f'R-squared score: {r2}')

    @classmethod
    def get_instance(cls):
        """ Gets, and conditionally cleans and builds, the singleton instance of the TitanicModel.
        The model is used for predicting tip amounts based on customer information.

        Returns:
            TitanicModel: the singleton _instance of the TitanicModel, which contains data and methods for prediction.
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
                'total_bill': The total bill amount
                'sex': The customer's sex ('Male' or 'Female')
                'smoker': Whether the customer is a smoker ('Yes' or 'No')
                'day': The day of the week ('Thur', 'Fri', 'Sat', 'Sun')
                'time': The time of day ('Lunch' or 'Dinner')
                'size': The size of the group

        Returns:
           float: predicted tip amount
        """
        # clean the customer data and prepare it for prediction
        customer_df = pd.DataFrame(customer_info, index=[0])
        categorical_cols = ['sex', 'smoker', 'day', 'time']
        customer_df = pd.get_dummies(customer_df, columns=categorical_cols, drop_first=True)
        
        # predict the tip amount
        tip_amount = self.model.predict(customer_df[self.features])
        return tip_amount[0]
    
def testTip():
    """ Test the Titanic Model for predicting tip amounts.
    Using the TitanicModel class, we can predict the tip amount for a customer.
    Print output of this test contains method documentation, customer data, and predicted tip amount.
    """
     
    # setup customer data for prediction
    print(" Step 1: Define customer data for prediction:")
    customer_info = {
        'total_bill': [50],
        'sex': ['Male'],
        'smoker': ['Yes'],
        'day': ['Sat'],
        'time': ['Dinner'],
        'size': [4]
    }
    print("\t", customer_info)
    print()

    # get an instance of the cleaned and trained Titanic Model
    tipModel = TipsModel.get_instance()
    print(" Step 2:", tipModel.get_instance.__doc__)
   
    # print the predicted tip amount
    print(" Step 3:", tipModel.predict_tip.__doc__)
    tip_amount = tipModel.predict_tip(customer_info)
    print('\t Predicted tip amount: ${:.2f}'.format(tip_amount))
    print()
    
if __name__ == "__main__":
    print(" Begin:", testTip.__doc__)
    testTip()
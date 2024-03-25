import json
from IPython.display import display
import seaborn as sns
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd

# Load the Tips dataset
tips_data = sns.load_dataset('tips')
print("Tips Data")

# print(titanic_data.columns) # titanic data set
# display(titanic_data[['survived','pclass', 'sex', 'age', 'sibsp', 'parch', 'class', 'fare', 'embark_town', 'alone']]) # look at selected columns


def clean_data(td):
    # td.drop(['alive', 'who', 'adult_male', 'class', 'embark_town', 'deck'], axis=1, inplace=True)
    #td.dropna(inplace=True) # drop rows with at least one missing value, after dropping unuseful columns

    # Encode categorical variables
    enc = OneHotEncoder(handle_unknown='ignore')
    enc.fit(td[['embarked']])
    onehot = enc.transform(td[['embarked']]).toarray()
    cols = ['embarked_' + val for val in enc.categories_[0]]
    td[cols] = pd.DataFrame(onehot)
    td.drop(['embarked'], axis=1, inplace=True)
    td.dropna(inplace=True) # drop rows with at least one missing value, after preparing the data
    return td, enc

# clean_data(titanic_data)


def prep_analysis(td):
    X = td.drop('tip', axis=1)
    y = td['tip']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Train a decision tree classifier
    dt = DecisionTreeClassifier()
    dt.fit(X_train, y_train)

    # Test the model
    y_pred = dt.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print('DecisionTreeClassifier Accuracy: {:.2%}'.format(accuracy))  

    # Train a logistic regression model
    logreg = LogisticRegression()
    logreg.fit(X_train, y_train)

    # Test the model
    y_pred = logreg.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print('LogisticRegression Accuracy: {:.2%}'.format(accuracy))  
    return logreg
    
def prediction(passenger, td = titanic_data):
    new_passenger = passenger.copy()
    print(new_passenger['sex'])
# Preprocess the new passenger data
    new_passenger['sex'] = new_passenger['sex'].apply(lambda x: 1 if x == 'male' else 0)
    new_passenger['alone'] = new_passenger['alone'].apply(lambda x: 1 if x == True else 0)

    # Encode 'embarked' variable
    onehot = enc.transform(new_passenger[['embarked']]).toarray()
    cols = ['embarked_' + val for val in enc.categories_[0]]
    new_passenger[cols] = pd.DataFrame(onehot, index=new_passenger.index)
    new_passenger.drop(['name'], axis=1, inplace=True)
    new_passenger.drop(['embarked'], axis=1, inplace=True)

    display(new_passenger)

    # Predict the survival probability for the new passenger
    dead_proba, alive_proba = np.squeeze(logreg.predict_proba(new_passenger))

    # Print the survival probability
    print('Death probability: {:.2%}'.format(dead_proba))  
    print('Survival probability: {:.2%}'.format(alive_proba))
    results = {
        "death": 'Death probability: {:.2%}'.format(dead_proba), 
        "survival": 'Survival probability: {:.2%}'.format(alive_proba)
    }
    return results
    
def init_dataset():
    global titanic_data, td, enc, logreg
    titanic_data = sns.load_dataset('tips')
    td = titanic_data
    td, enc = clean_data(titanic_data)
    logreg = prep_analysis(titanic_data)
    return td




# passenger = pd.DataFrame({
#     "name": ["TEST"],
#     "pclass": [1],
#     "sex": ["male"],
#     "age": [12],
#     "sibsp": [100],
#     "parch": [100], 
#     "fare": [100], 
#     "embarked": ["S"], 
#     "alone": ["True"]
# })
# prediction(passenger)
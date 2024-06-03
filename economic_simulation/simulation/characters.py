import joblib
import numpy as np
import pandas as pd

class Character:
    def __init__(self, name, income, savings, debt):
        self.name = name
        self.income = income
        self.savings = savings
        self.debt = debt
        self.happiness = 50  # Initial baseline happiness

        # Load the pre-trained happiness model
        self.model = joblib.load("simulation/happiness_model.pkl")

        # Personality traits
        self.risk_tolerance = np.random.uniform(0, 1)  # 0: risk-averse, 1: risk-seeking
        self.spending_habit = np.random.uniform(0, 1)  # 0: frugal, 1: extravagant

    def update_emotions(self, gdp_growth, inflation_rate, unemployment_rate):
        # Prepare the input features
        features = pd.DataFrame([{
            "gdp_growth": gdp_growth,
            "inflation_rate": inflation_rate,
            "unemployment_rate": unemployment_rate,
            "income": self.income,
            "savings": self.savings,
            "debt": self.debt
        }])
        
        # Predict happiness category using the model
        happiness_category = self.model.predict(features)[0]

        # Map the category to a happiness score
        if happiness_category == 0:
            self.happiness = np.random.randint(0, 30)  # Unhappy
        elif happiness_category == 1:
            self.happiness = np.random.randint(30, 70)  # Neutral
        else:
            self.happiness = np.random.randint(70, 100)  # Happy

    def decide_spending(self, economic_conditions):
        # Decide spending amount based on income, savings, and spending habit
        base_spending = self.income * self.spending_habit
        economic_factor = 1 - economic_conditions['interest_rate'] + economic_conditions['consumer_confidence'] / 100
        spending = base_spending * economic_factor

        if spending > self.savings:
            spending = self.savings  # Cannot spend more than available savings

        self.savings -= spending
        return spending

    def decide_saving(self):
        # Save a portion of income based on risk tolerance
        saving_rate = 0.1 + self.risk_tolerance * 0.2  # Save between 10% and 30% of income
        saving_amount = self.income * saving_rate
        self.savings += saving_amount

    def decide_borrowing(self, economic_conditions):
        # Decide borrowing amount based on debt levels and economic conditions
        if self.debt < self.income * 0.5 and economic_conditions['interest_rate'] < 0.05:
            borrow_amount = self.income * 0.2  # Borrow 20% of income
            self.debt += borrow_amount
            self.savings += borrow_amount
        else:
            borrow_amount = 0

        return borrow_amount

def create_characters(num_characters):
    names = ["Lara", "Han", "Natasha", "Doom", "Jim"]
    return [Character(np.random.choice(names), np.random.randint(30000, 100000), np.random.randint(5000, 20000), np.random.randint(0, 5000)) for _ in range(num_characters)]

import pandas as pd
import numpy as np
from .characters import create_characters, Character

# Placeholder for the global economic data
economic_data = {
    "interest_rate": 0.05,
    "inflation_rate": 0.02,
    "gdp": 1000,
    "total_debt": 5000,
    "tax_rate": 0.20,
    "gov_spending": 0.05,
    "min_wage": 15,
    "consumer_confidence": 75,
}

def simulate_economy(policies, periods=10):
    characters = create_characters(5)
    total_debt = economic_data["total_debt"]
    gdp = economic_data["gdp"]
    inflation_rate = economic_data["inflation_rate"]
    interest_rate = economic_data["interest_rate"]
    tax_rate = economic_data["tax_rate"]
    gov_spending = economic_data["gov_spending"]
    min_wage = economic_data["min_wage"]
    consumer_confidence = economic_data["consumer_confidence"]

    gdp_list = []
    inflation_list = []
    interest_list = []
    unemployment_list = []
    total_debt_list = []
    debt_to_gdp_ratio_list = []
    savings_rate_list = []
    real_wages_list = []
    inflation_adjusted_savings_list = []
    characters_emotions = []
    events = []

    for period in range(periods):
        prev_gdp = gdp
        for policy in policies:
            if policy['type'] == 'interest_rate':
                interest_rate += policy['effect']
            elif policy['type'] == 'fiscal_stimulus':
                gdp += gdp * policy['effect']
                total_debt += policy['effect'] * gdp
            elif policy['type'] == 'quantitative_easing':
                gdp += gdp * policy['effect']
                total_debt += gdp * policy['effect']
                inflation_rate += inflation_rate * 0.1
            elif policy['type'] == 'tax_rate':
                tax_rate = policy['effect']
            elif policy['type'] == 'gov_spending':
                gov_spending = policy['effect']
                gdp += gdp * gov_spending
            elif policy['type'] == 'min_wage':
                min_wage = policy['effect']
            elif policy['type'] == 'consumer_confidence':
                consumer_confidence = policy['effect']

        gdp_growth = gdp - prev_gdp
        inflation_rate = calculate_inflation(gdp, interest_rate)
        unemployment_rate = calculate_unemployment(gdp, inflation_rate)

        economic_conditions = {
            "interest_rate": interest_rate,
            "consumer_confidence": consumer_confidence
        }

        for character in characters:
            character.income += character.income * (interest_rate - inflation_rate) * (consumer_confidence / 100)
            character.decide_saving()
            borrow_amount = character.decide_borrowing(economic_conditions)
            spending = character.decide_spending(economic_conditions)
            gdp += spending  # Aggregate character spending adds to GDP
            character.update_emotions(gdp_growth, inflation_rate, unemployment_rate)

            if borrow_amount > 0:
                events.append({"name": character.name, "description": f"took out a loan of ${borrow_amount:.2f}"})
            events.append({"name": character.name, "description": f"spent ${spending:.2f}"})

        gdp_list.append(gdp)
        inflation_list.append(inflation_rate)
        interest_list.append(interest_rate)
        unemployment_list.append(unemployment_rate)
        total_debt_list.append(total_debt)
        debt_to_gdp_ratio_list.append(total_debt / gdp)
        
        avg_savings_rate = np.mean([character.savings / character.income for character in characters])
        savings_rate_list.append(avg_savings_rate)

        avg_real_wages = np.mean([character.income / (1 + inflation_rate) for character in characters])
        real_wages_list.append(avg_real_wages)

        avg_inflation_adjusted_savings = np.mean([character.savings / (1 + inflation_rate) for character in characters])
        inflation_adjusted_savings_list.append(avg_inflation_adjusted_savings)

        characters_emotions.append([{ 
            "name": character.name, 
            "income": character.income,
            "savings": character.savings,
            "debt": character.debt,
            "happiness": character.happiness 
        } for character in characters])

    character_data = [{'name': character.name, 'income': character.income, 'savings': character.savings, 'debt': character.debt, 'happiness': character.happiness} for character in characters]
    return character_data, gdp_list, inflation_list, interest_list, unemployment_list, total_debt_list, debt_to_gdp_ratio_list, savings_rate_list, real_wages_list, inflation_adjusted_savings_list, characters_emotions, events

def update_economic_data(data):
    global economic_data
    economic_data.update(data)

def run_economic_simulation(policies):
    # Simulate economy over multiple periods
    character_data, gdp_list, inflation_list, interest_list, unemployment_list, total_debt_list, debt_to_gdp_ratio_list, savings_rate_list, real_wages_list, inflation_adjusted_savings_list, characters_emotions, events = simulate_economy(policies)

    # Return the results
    results = {
        "gdp_list": gdp_list,
        "inflation_list": inflation_list,
        "interest_list": interest_list,
        "unemployment_list": unemployment_list,
        "total_debt_list": total_debt_list,
        "debt_to_gdp_ratio_list": debt_to_gdp_ratio_list,
        "savings_rate_list": savings_rate_list,
        "real_wages_list": real_wages_list,
        "inflation_adjusted_savings_list": inflation_adjusted_savings_list,
        "character_data": character_data,
        "characters_emotions": characters_emotions,
        "events": events
    }
    return results

def calculate_inflation(gdp, interest_rate):
    return 0.02 + interest_rate * 0.1

def calculate_unemployment(gdp, inflation_rate):
    return 0.05 - inflation_rate * 0.1

function runSimulation() {
    const interestRate = parseFloat(document.getElementById('interest_rate').value) || 0;
    const fiscalStimulus = parseFloat(document.getElementById('fiscal_stimulus').value) || 0;
    const quantitativeEasing = parseFloat(document.getElementById('quantitative_easing').value) || 0;
    const taxRate = parseFloat(document.getElementById('tax_rate').value) || 0;
    const govSpending = parseFloat(document.getElementById('gov_spending').value) || 0;
    const minWage = parseFloat(document.getElementById('min_wage').value) || 0;
    const consumerConfidence = parseFloat(document.getElementById('consumer_confidence').value) || 0;

    const policies = [
        { type: "interest_rate", effect: interestRate / 100 },
        { type: "fiscal_stimulus", effect: fiscalStimulus / 100 },
        { type: "quantitative_easing", effect: quantitativeEasing / 100 },
        { type: "tax_rate", effect: taxRate / 100 },
        { type: "gov_spending", effect: govSpending / 100 },
        { type: "min_wage", effect: minWage },
        { type: "consumer_confidence", effect: consumerConfidence }
    ];

    fetch('/run_simulation/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ policies: JSON.stringify(policies) })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
            return;
        }
        
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = `
            <h2>Simulation Results</h2>
        `;

        // Display characters and emotions
        displayCharacters(data.characters_emotions);

        // Display real-time events
        displayEvents(data.events);

        // Plot time-series data
        plotTimeSeries(data.gdp_list, 'GDP', 'gdp-chart');
        plotTimeSeries(data.inflation_list, 'Inflation Rate', 'inflation-chart');
        plotTimeSeries(data.interest_list, 'Interest Rate', 'interest-chart');
        plotTimeSeries(data.unemployment_list, 'Unemployment Rate', 'unemployment-chart');
        plotTimeSeries(data.total_debt_list, 'Total Debt', 'total-debt-chart');
        plotTimeSeries(data.debt_to_gdp_ratio_list, 'Debt-to-GDP Ratio', 'debt-to-gdp-chart');
        plotTimeSeries(data.savings_rate_list, 'Savings Rate', 'savings-rate-chart');
        plotTimeSeries(data.real_wages_list, 'Real Wages', 'real-wages-chart');
        plotTimeSeries(data.inflation_adjusted_savings_list, 'Inflation-Adjusted Savings', 'inflation-adjusted-savings-chart');

        const householdData = data.household_data;

        const incomes = householdData.map(h => h.income);
        const savings = householdData.map(h => h.savings);
        const debts = householdData.map(h => h.debt);

        plotHistogram(incomes, 'Household Income Distribution', 'household-income-chart');
        plotHistogram(savings, 'Household Savings Distribution', 'household-savings-chart');
        plotHistogram(debts, 'Household Debt Distribution', 'household-debt-chart');
    })
    .catch(error => console.error('Error:', error));
}

function setScenario(scenario) {
    if (scenario === 'recession') {
        document.getElementById('interest_rate').value = -2;
        document.getElementById('fiscal_stimulus').value = 3;
        document.getElementById('quantitative_easing').value = 5;
        document.getElementById('tax_rate').value = 15;
        document.getElementById('gov_spending').value = 10;
        document.getElementById('min_wage').value = 10;
        document.getElementById('consumer_confidence').value = 40;
    } else if (scenario === 'boom') {
        document.getElementById('interest_rate').value = 1;
        document.getElementById('fiscal_stimulus').value = 0;
        document.getElementById('quantitative_easing').value = 0;
        document.getElementById('tax_rate').value = 20;
        document.getElementById('gov_spending').value = 5;
        document.getElementById('min_wage').value = 15;
        document.getElementById('consumer_confidence').value = 90;
    } else {
        document.getElementById('interest_rate').value = 5;
        document.getElementById('fiscal_stimulus').value = 0;
        document.getElementById('quantitative_easing').value = 0;
        document.getElementById('tax_rate').value = 20;
        document.getElementById('gov_spending').value = 5;
        document.getElementById('min_wage').value = 15;
        document.getElementById('consumer_confidence').value = 75;
    }
    updateAllSliderValues();
}

function updateSliderValue(id) {
    document.getElementById(id + '_value').innerText = document.getElementById(id).value;
}

function updateAllSliderValues() {
    const sliders = ['interest_rate', 'fiscal_stimulus', 'quantitative_easing', 'tax_rate', 'gov_spending', 'min_wage', 'consumer_confidence'];
    sliders.forEach(updateSliderValue);
}

function displayCharacters(characters_emotions) {

    const afterDiv = document.getElementById('after');

    afterDiv.style.display = 'block';

    const charactersDiv = document.getElementById('characters');
    charactersDiv.innerHTML = '';

    const characterNames = ["doom", "jim", "natasha", "lara", "han"];

    characters_emotions.forEach((period, index) => {
        const periodDiv = document.createElement('div');
        periodDiv.innerHTML = `<h3>Period ${index + 1}</h3>`;
        const characterContainer = document.createElement('div');
        characterContainer.className = 'character-container';

        period.forEach((character, charIndex) => {
            const characterDiv = document.createElement('div');
            characterDiv.className = 'character';
            characterDiv.innerHTML = `
                <div class="score ${getHappinessClass(character.happiness)}">${character.happiness}</div>
                <img src="${characterImages[characterNames[charIndex % characterNames.length]]}" alt="${characterNames[charIndex % characterNames.length]}">
                <span class="name">${characterNames[charIndex % characterNames.length]}</span>
                <div class="profile">
                    <h3>${characterNames[charIndex % characterNames.length]}</h3>
                    <p><strong>Income:</strong> $${character.income.toFixed(2)}</p>
                    <p><strong>Savings:</strong> $${character.savings.toFixed(2)}</p>
                    <p><strong>Debt:</strong> $${character.debt.toFixed(2)}</p>
                    <p><strong>Happiness:</strong> ${character.happiness}</p>
                </div>
            `;
            characterDiv.addEventListener('mouseover', () => {
                characterDiv.querySelector('.profile').style.display = 'block';
            });
            characterDiv.addEventListener('mouseout', () => {
                characterDiv.querySelector('.profile').style.display = 'none';
            });
            characterContainer.appendChild(characterDiv);
        });

        periodDiv.appendChild(characterContainer);
        charactersDiv.appendChild(periodDiv);
    });
}

function displayEvents(events) {
    const eventsDiv = document.getElementById('events');
    eventsDiv.innerHTML = '<h2>Real-Time Events</h2>';
    
    events.forEach(event => {
        const eventDiv = document.createElement('div');
        eventDiv.className = 'event';
        eventDiv.innerHTML = `<strong>${event.name}:</strong> ${event.description}`;
        eventsDiv.appendChild(eventDiv);
    });
}

function getHappinessClass(happiness) {
    if (happiness >= 70) return 'happy';
    if (happiness >= 30) return 'neutral';
    return 'sad';
}

function plotTimeSeries(data, title, elementId) {
    const trace = {
        x: Array.from({ length: data.length }, (_, i) => i + 1),
        y: data,
        type: 'scatter',
        name: title,
        mode: 'lines+markers'
    };

    const layout = {
        title: title,
        xaxis: { title: 'Time Period' },
        yaxis: { title: title }
    };

    Plotly.newPlot(elementId, [trace], layout);
}

function plotHistogram(data, title, elementId) {
    const trace = {
        x: data,
        type: 'histogram',
        name: title
    };

    const layout = {
        title: title,
        xaxis: { title: title },
        yaxis: { title: 'Count' }
    };

    Plotly.newPlot(elementId, [trace], layout);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



document.addEventListener('DOMContentLoaded', function() {
    const characters = document.querySelectorAll('.character');

    characters.forEach(character => {
        const happinessText = character.querySelector('p:nth-of-type(4)').innerText;
        const happinessValue = parseInt(happinessText.replace('Happiness: ', ''), 10);
        const happinessBar = document.createElement('div');
        happinessBar.classList.add('happiness-bar');
        happinessBar.style.width = `${happinessValue}%`;

        if (happinessValue >= 60) {
            happinessBar.classList.add('happy');
        } else if (happinessValue >= 40) {
            happinessBar.classList.add('neutral');
        } else {
            happinessBar.classList.add('unhappy');
        }

        character.insertBefore(happinessBar, character.querySelector('img'));
    });
});

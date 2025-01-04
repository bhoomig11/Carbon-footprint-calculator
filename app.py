from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Get form data
    car_kms = float(request.form.get('car_kms', 0))
    fuel_efficiency = float(request.form.get('fuel_efficiency', 0))
    public_transport = float(request.form.get('public_transport', 0))
    electricity_usage = float(request.form.get('electricity_usage', 0))
    gas_usage = float(request.form.get('gas_usage', 0))
    diet = request.form.get('diet', 'vegetarian').lower()

    # Emission factors
    emission_factor_car = 2.3  # kg CO₂ per liter of gasoline
    emission_factor_pt = 0.1  # kg CO₂ per km
    emission_factor_electricity = 0.45  # kg CO₂ per kWh
    emission_factor_gas = 5.3  # kg CO₂ per therm
    diet_emission_factors = {
        "vegetarian": 1.7,  # kg CO₂ per day
        "non-vegetarian": 2.5,  # kg CO₂ per day
        "vegan": 1.5  # kg CO₂ per day
    }

    # Calculate emissions
    car_emissions = (car_kms / 100) * fuel_efficiency * emission_factor_car * 52
    pt_emissions = public_transport * emission_factor_pt * 52
    electricity_emissions = electricity_usage * emission_factor_electricity * 12
    gas_emissions = gas_usage * emission_factor_gas * 12
    food_emissions = diet_emission_factors.get(diet, 2.5) * 365

    total_emissions = car_emissions + pt_emissions + electricity_emissions + gas_emissions + food_emissions

    # Categorize emissions
    if total_emissions < 5000:
        category = "good"  # Green
    elif 5000 <= total_emissions <= 15000:
        category = "normal"  # Blue
    else:
        category = "bad"  # Red

    return render_template('result.html', total_emissions=total_emissions, category=category)

if __name__ == "__main__":
    app.run(debug=True)

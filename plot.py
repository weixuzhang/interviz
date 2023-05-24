import matplotlib.pyplot as plt

data = [
    {"city": "New York", "airportcode": "JFK", "airportname": "John F. Kennedy International Airport", "country": "United States", "countryabbrev": "US"},
    {"city": "London", "airportcode": "LHR", "airportname": "London Heathrow Airport", "country": "United Kingdom", "countryabbrev": "UK"},
    {"city": "Frankfurt", "airportcode": "FRA", "airportname": "Frankfurt Airport", "country": "Germany", "countryabbrev": "DE"}
]

flight_data = [
    {"country": "United States", "flight_count": 10},
    {"country": "United Kingdom", "flight_count": 15},
    {"country": "Germany", "flight_count": 8}
]

countries = [d['country'] for d in flight_data]
flight_counts = [d['flight_count'] for d in flight_data]

plt.bar(countries, flight_counts)
plt.xlabel('Country')
plt.ylabel('Flight Count')
plt.title('Flight Count by Airport Country')
plt.xticks(rotation=45)
plt.show()


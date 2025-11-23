---
name: capacity-management
description: Управление мощностями облачной платформы. Use when planning capacity, forecasting demand, optimizing resource utilization, or preventing capacity constraints.
---

# Capacity Management

## Когда использовать

- Planning capacity для growth
- Demand forecasting
- Resource utilization optimization
- Preventing capacity constraints
- Cost-performance balancing

## Capacity Planning Models

### Growth Forecasting

```python
import pandas as pd
from sklearn.linear_model import LinearRegression

class CapacityForecaster:
    def forecast_demand(self, historical_data, months_ahead=12):
        """Forecast future capacity needs"""

        # Historical usage data
        df = pd.DataFrame(historical_data)
        df['month_num'] = range(len(df))

        # Linear regression model
        model = LinearRegression()
        X = df[['month_num']]
        y = df['usage']
        model.fit(X, y)

        # Forecast
        future_months = range(len(df), len(df) + months_ahead)
        forecast = model.predict([[m] for m in future_months])

        # Add buffer (20% for safety)
        forecast_with_buffer = forecast * 1.2

        return forecast_with_buffer

# Example usage
historical = [
    {'month': '2024-01', 'usage': 1000},  # GB
    {'month': '2024-02', 'usage': 1100},
    {'month': '2024-03', 'usage': 1250},
    # ...
]

forecaster = CapacityForecaster()
future_capacity = forecaster.forecast_demand(historical)
# Result: [1450, 1520, 1590, ...] GB для next 12 months
```

### Utilization Optimization

```yaml
# Target Utilization Levels

Compute:
  target: 70%  # Headroom для spikes
  actions:
    - < 40%: Scale down или right-size
    - > 85%: Scale up или optimize

Storage:
  target: 80%  # Lower headroom needed
  actions:
    - > 90%: Expand capacity

Network:
  target: 60%  # Higher headroom для bursts
  actions:
    - > 75%: Add bandwidth

Database Connections:
  target: 75%
  actions:
    - > 90%: Increase max_connections или add read replicas
```

---

**Все capacity plans сохраняются в Markdown на русском языке.**

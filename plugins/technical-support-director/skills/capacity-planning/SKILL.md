---
name: capacity-planning
description: Workforce capacity planning и resource optimization для команд технической поддержки. Включает staffing models, forecasting, shift planning, utilization optimization. Use when planning headcount, optimizing schedules, or forecasting support needs.
---

# Планирование Мощностей (Capacity Planning)

## Когда Использовать

- Annual или quarterly headcount planning
- Shift schedule optimization
- Seasonal capacity adjustments
- New product launch planning
- Service tier expansion

## Staffing Model Calculation

### Basic Formula

```python
def calculate_required_fte(
    monthly_ticket_volume,
    avg_handling_time_hours,
    target_utilization=0.80,
    availability_factor=0.85,  # PTO, training, meetings
    coverage_model="24x7"  # or "business_hours"
):
    """
    Calculate FTE needed для support team
    """
    # Total work hours needed
    total_hours_needed = monthly_ticket_volume * avg_handling_time_hours

    # Working hours per FTE
    if coverage_model == "business_hours":
        hours_per_fte_month = 160  # 8hrs * 20 days
    else:  # 24x7
        # Need ~4.2 FTE для 24x7 single-person coverage (accounting for shifts)
        hours_per_fte_month = 160 * 0.4  # Effective hours due to shift coverage

    # Effective hours considering availability и utilization
    effective_hours = hours_per_fte_month * availability_factor * target_utilization

    # Required FTE
    required_fte = total_hours_needed / effective_hours

    return math.ceil(required_fte)
```

**Example:**
- Monthly tickets: 3,500
- Avg handling time: 2.5 hours
- Target utilization: 80%
- 24x7 coverage

Result: ~127 FTE

## Ticket Volume Forecasting

### Time Series Forecasting

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def forecast_ticket_volume(historical_monthly_data, periods_ahead=12):
    """
    Forecast ticket volume используя Holt-Winters seasonal method
    """
    model = ExponentialSmoothing(
        historical_monthly_data,
        seasonal_periods=12,
        trend='add',
        seasonal='add'
    )

    fit = model.fit()
    forecast = fit.forecast(periods_ahead)

    return {
        "forecast": forecast,
        "confidence_interval_95": calculate_ci(forecast, historical_monthly_data),
        "seasonal_pattern": fit.seasonal
    }
```

### Seasonality Patterns

```markdown
# Typical Support Seasonality

## High Volume Periods
- **January**: Post-holiday return, new year projects
- **September**: Back-to-school, Q3 end
- **November**: Pre-holiday rush, Black Friday
- **Quarter Ends**: Budget spending, project deadlines

## Low Volume Periods
- **July-August**: Summer holidays
- **December**: Winter holidays
- **Long weekends**: Reduced business activity

## Planning Adjustments
- Scale up 15-20% для high periods
- Allow more PTO during low periods
- Schedule training during valleys
```

## Shift Planning

### 24x7 Coverage Model

```markdown
# Shift Schedule Example (3-shift rotation)

## Shift Distribution
- **Shift 1 (Early)**: 06:00-14:00 (Americas/Europe)
- **Shift 2 (Mid)**: 14:00-22:00 (Americas/Asia)
- **Shift 3 (Night)**: 22:00-06:00 (Asia/Pacific)

## Staffing per Shift
- Shift 1: 40% of team (highest volume)
- Shift 2: 35% of team
- Shift 3: 25% of team

## Rotation Pattern (4-week cycle)
Week 1: Early shift
Week 2: Mid shift
Week 3: Night shift
Week 4: Early shift (+ 2 days off for recovery)
```

### Follow-the-Sun Model

```markdown
# Follow-the-Sun Coverage

## Locations
- **Americas Hub**: 08:00-17:00 EST (40% team)
- **EMEA Hub**: 08:00-17:00 CET (30% team)
- **APAC Hub**: 08:00-17:00 SGT (30% team)

## Handoff Protocol
- 30-minute overlap between regions
- Handoff doc updated real-time
- Warm handoff for critical issues

## Benefits
- No night shifts (better work-life balance)
- Native language support по timezones
- Reduced burnout
```

## Utilization Optimization

### Target Utilization Rates

```python
UTILIZATION_TARGETS = {
    "direct_support": {
        "target": 0.75,  # 75% of time on tickets
        "range": (0.70, 0.80),
        "notes": "Too high = burnout, too low = inefficiency"
    },
    "indirect_work": {
        "target": 0.15,  # 15% on KB, training, meetings
        "activities": ["Knowledge base", "Training", "Meetings", "Process improvement"]
    },
    "buffer": {
        "target": 0.10,  # 10% buffer for spikes
        "purpose": "Flexibility for volume fluctuations"
    }
}
```

### Skill-Based Routing

```markdown
# Tiered Support Model

## Tier 1 (60% of team)
- **Skills**: General platform knowledge
- **Handles**: 70% of tickets (P3, P4, simple P2)
- **Avg Resolution**: 1.5 hours
- **Cost**: $50K/year per FTE

## Tier 2 (30% of team)
- **Skills**: Deep technical, specialized
- **Handles**: 25% of tickets (complex P2, P3, escalations from T1)
- **Avg Resolution**: 4 hours
- **Cost**: $80K/year per FTE

## Tier 3 (10% of team)
- **Skills**: Expert, architecture, engineering
- **Handles**: 5% of tickets (P1, complex architecture, bugs)
- **Avg Resolution**: 8 hours
- **Cost**: $120K/year per FTE

## Optimization
- Train T1 to handle more → Reduce T2/T3 escalations
- Automate common T1 issues → Free capacity
- Knowledge base → Shift left
```

## Capacity Planning для Product Launches

```markdown
# New Product Launch Capacity Plan

## Pre-Launch (4 weeks before)
- [ ] Forecast adoption rate
- [ ] Estimate support impact (tickets/user)
- [ ] Identify knowledge gaps
- [ ] Create training materials
- [ ] Develop runbooks

## Launch (Week 0-2)
- [ ] +30% capacity buffer (temporary contractors)
- [ ] Dedicated product expert on-call
- [ ] Daily triage meetings
- [ ] Fast-track KB article creation

## Stabilization (Week 3-8)
- [ ] Analyze actual volume vs forecast
- [ ] Adjust staffing accordingly
- [ ] Transition contractors if still needed
- [ ] Document lessons learned

## Steady State (Week 9+)
- [ ] Normal staffing levels
- [ ] Continuous improvement
```

## Budget Planning

```python
def calculate_support_budget(team_size, region="US"):
    """
    Annual support team budget calculation
    """
    costs = {
        "salaries": {
            "tier_1": 50_000 * 0.60 * team_size,
            "tier_2": 80_000 * 0.30 * team_size,
            "tier_3": 120_000 * 0.10 * team_size,
        },
        "overhead": {
            "benefits": 0.30,  # 30% of salaries
            "office": 10_000 * team_size,  # Per person
            "equipment": 2_000 * team_size,  # Laptop, monitors
        },
        "tools": {
            "ticketing": 100 * team_size * 12,  # $100/mo per user
            "monitoring": 50 * team_size * 12,
            "collaboration": 30 * team_size * 12,
        },
        "vendor_support": {
            "aws": 15_000 * 12,  # Enterprise support
            "azure": 10_000 * 12,
            "gcp": 10_000 * 12,
        },
        "training": {
            "per_person": 3_000 * team_size,  # Annual training budget
            "certifications": 1_500 * team_size * 0.5,  # Half the team
        }
    }

    total_salaries = sum(costs["salaries"].values())
    total_overhead = total_salaries * costs["overhead"]["benefits"] + costs["overhead"]["office"] + costs["overhead"]["equipment"]
    total_tools = sum(costs["tools"].values())
    total_vendor = sum(costs["vendor_support"].values())
    total_training = sum(costs["training"].values())

    total_budget = total_salaries + total_overhead + total_tools + total_vendor + total_training

    return {
        "total_annual_budget": total_budget,
        "cost_per_fte": total_budget / team_size,
        "breakdown": costs
    }
```

## References
- `models/staffing-calculator.py` - Interactive staffing calculator
- `templates/shift-schedules.xlsx` - Shift planning templates
- `forecasting/ticket-volume-forecast.ipynb` - Jupyter notebook для forecasting

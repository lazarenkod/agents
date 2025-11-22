#!/usr/bin/env python3
"""
SLA Compliance и Service Credit Calculator
"""

def calculate_availability_sla(uptime_minutes, total_minutes):
    """Рассчитать availability percentage"""
    return (uptime_minutes / total_minutes) * 100

def calculate_service_credit(availability, target_sla, monthly_fee):
    """
    Рассчитать service credits за availability breach
    
    Standard credit rates:
    - Enterprise (99.99%): 10% per 0.1% below target
    - Business (99.95%): 5% per 0.1% below target
    - Standard (99.9%): 3% per 0.1% below target
    """
    if availability >= target_sla:
        return 0  # No breach
    
    breach_percentage = target_sla - availability
    breach_units = breach_percentage / 0.1
    
    # Determine credit rate based on SLA tier
    if target_sla >= 99.99:
        credit_rate = 0.10  # Enterprise
    elif target_sla >= 99.95:
        credit_rate = 0.05  # Business
    else:
        credit_rate = 0.03  # Standard
    
    credit = monthly_fee * credit_rate * breach_units
    return min(credit, monthly_fee)  # Cap at 100%

# Example usage
if __name__ == "__main__":
    # Example: Enterprise customer
    monthly_fee = 25000
    target = 99.99
    actual = 99.92
    
    credit = calculate_service_credit(actual, target, monthly_fee)
    print(f"Service Credit: ${credit:,.2f}")
    print(f"% of Monthly Fee: {(credit/monthly_fee)*100:.1f}%")

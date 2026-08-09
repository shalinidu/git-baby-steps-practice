principal = 15847.0
annual_rate = 7.34 / 100
compoundings_per_year = 12
years = 8 + 7/12

amount = principal * (1 + annual_rate / compoundings_per_year) ** (compoundings_per_year * years)
interest = amount - principal

print(f"Principal: ${principal:,.2f}")
print(f"Annual rate: {annual_rate*100:.2f}%")
print(f"Time: {years:.2f} years")
print(f"Compoundings per year: {compoundings_per_year}")
print(f"Final amount: ${amount:,.2f}")
print(f"Total interest: ${interest:,.2f}")

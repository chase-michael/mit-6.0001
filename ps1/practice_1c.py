annual_salary = float(input('Enter annual salary: '))
home_price = 1000000
down_payment = home_price * 0.25
roi = 0.04
semi_annual_raise = 0.07


def salary_for_month(annual_salary, month, semi_annual_raise):
    compound_times = int(month / 6)
    salary_multipliter = (1 + semi_annual_raise) ** compound_times
    return annual_salary * salary_multipliter / 12


def get_amount_saved(annual_salary, rate_of_savings):
    account_balance = 0
    for month in range(1, 37):
        account_balance += account_balance * (roi / 12)
        account_balance += salary_for_month(annual_salary, month, semi_annual_raise) * rate_of_savings
    return account_balance


def main():
    bottom = 0
    top = 1
    steps = 0
    while bottom < top:
        mid = bottom + ((top-bottom) / 2)
        dif = down_payment - get_amount_saved(annual_salary, mid)
        steps += 1
        if abs(dif) < 100:
            print("Best savings rate:", "{:.2f}".format(mid*100), "%\nSteps in bisection search:", steps)
            break
        if dif < 0:
            top = mid
        else:
            bottom = mid
    if bottom == top:
        print("It is not possible to pay the down payment in three years.")

main()

class SavingsAccount:
    balance = 0
    r = 0.04

    def increment(self, monthly_savings: float):
        self.balance += monthly_savings / 12
        self.balance += self.balance * (self.r / 12)


def calculate_down_payment(home_cost: float) -> float:
    down_payment_portion = 0.25
    return home_cost * down_payment_portion


def calc_monthly(annual_salary: float, portion_saved: float) -> float:
    monthly_savings = annual_salary / 12
    return monthly_savings


def months_to_down_payment(amount_needed: float, annual_salary: float, portion_saved: float) -> int:
    savings_account = SavingsAccount()
    month = 0
    monthly_savings = calc_monthly(annual_salary, portion_saved)
    while savings_account.balance < amount_needed:
        savings_account.increment(monthly_savings)
        month += 1
    return month


def main():
    annual_salary = float(input('Enter your annual salary: '))
    portion_saved = float(input('Enter the percent of your salary to save, as a decimal: '))
    total_cost = float(input('Enter the cost of your dream home: '))
    down_payment = calculate_down_payment(home_cost=total_cost)
    print('Number of months:', months_to_down_payment(down_payment, annual_salary, portion_saved))


main()
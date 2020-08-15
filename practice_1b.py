class BankingInfo:
    balance = 0
    r = 0.04
    month = 0

    def __init__(self):
        self.monthly_salary = float(input('Enter your annual salary: ')) / 12
        self.percent_saved = float(input('Enter the percent of your salary to save, as a decimal: '))
        self.semi_annual_raise = float(input('Enter the semi­annual raise, as a decimal: '))

    def update_monthly(self):
        if self.month != 0 and self.month % 6 == 0:
            self.monthly_salary += self.monthly_salary * self.semi_annual_raise
        self.month += 1

    def increment_month(self):
        self.update_monthly()
        self.balance += self.balance * (self.r / 12)
        self.balance += self.monthly_salary * self.percent_saved


class DreamHome:

    def __init__(self):
        home_price = float(input('Enter the cost of your dream home: '))
        self.down_payment = home_price * 0.25


def months_to_down_payment(dream_home: DreamHome, bank_account: BankingInfo) -> int:
    month = 0
    while bank_account.balance < dream_home.down_payment:
        bank_account.increment_month()
        month += 1
    return month


def main():
    bank_account = BankingInfo()  # Opens a savings account and banking portfolio that takes in the user's info
    dream_home = DreamHome()  # Creates a profile on the user's dream home
    # The program calculates the number of months needed to save a down payment
    total_months = months_to_down_payment(dream_home, bank_account)
    print('Number of months:', total_months)


main()

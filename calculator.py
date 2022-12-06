import datetime as dt


class Record:
    DATE_FORMAT = "%d.%m.%Y"

    def __init__(self, amount, comment, date = None):
        self.amount = amount
        self.comment = str(comment)

        if date is None:
            self.date = dt.date.today()
        else:
           self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date() 


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_stats(self, days_amount):
        result = 0
        past_date = dt.date.today() - dt.timedelta(days = days_amount)
        today = dt.date.today()
        
        for record in self.records:
            if past_date < record.date <= today:
                result += record.amount
        return result
    
    def get_today_stats(self):
        return self.get_stats(1)

    def get_week_stats(self):
        return self.get_stats(7)

    def get_remained(self):
        spent = self.get_today_stats()
        res = self.limit - spent
        return res
    

class CashCalculator(Calculator):
    RUB_RATE = 1.0
    USD_RATE = 68.61
    EURO_RATE = 77.75

    def get_today_cash_remained(self, currency):
        remained = self.get_remained()
        if remained == 0:
            return "Денег нет, держись"

        currency_switch = {
            "rub": (self.RUB_RATE, "руб"),
            "usd": (self.USD_RATE, "USD"),
            "eur": (self.EURO_RATE, "Euro")
        }
        currency_str = (f"{round(abs(remained) / currency_switch[currency][0], 2)} {currency_switch[currency][1]}")

        if remained < 0:
            return (f"Денег нет, держись: твой долг - {currency_str}")

        return (f"На сегодня осталось {currency_str}")


class CaloriesCalculator(Calculator):
    
    def get_calories_remained(self):
        remained = self.get_remained()
        if remained > 0:
            return ("Сегодня можно съесть что-нибудь ещё, "
                    f"но с общей калорийностью не более {remained} кКал")
            
        return "Хватит есть!"

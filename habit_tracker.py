from datetime import date, time, datetime, timedelta, timezone
import json
import os
import sys


def get_habits_path():
    """Возвращает путь к файлу habits.json в папке пользователя"""
    if sys.platform == "win32":
        # Windows: C:\Users\Имя\AppData\Roaming\HabitTracker\
        base = os.environ.get('APPDATA', os.path.expanduser('~'))
    else:
        # Linux/Mac: ~/.local/share/HabitTracker/
        base = os.path.expanduser('~/.local/share')
    
    folder = os.path.join(base, 'HabitTracker')
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, 'habits.json')

class HabitTracker:
    def __init__(self):
        self.habits = {}

    def __str__(self):
        habits = ""
        for key, value in self.habits.items():
            habits += (f"{key}: {value} \n")
        return habits
    
    def start(self):
        path = get_habits_path()
        if os.path.exists(path):
            with open(path, "r") as f:
                self.habits = json.load(f)
        print(self)
        self.menu()

    def menu(self):
        print("ТРЕКЕР ПРИВЫЧЕК")
        print("Выберите действие:")
        print("1 - добавить новую привычку")
        print("2 - отметить выполнение")
        print("3 - посмотреть статистику по привычке")
        print("4 - график выполнения привычки за последние 7 дней")
        print("5 - закрыть программу")
        value = input()
        if value == "1":
            self.add()
        elif value == "2":
            self.check()
        elif value == "3":
            self.stats()
        elif value == "4":
            self.graph()
        elif value == "5":
            self.exit()
        else:
            print("Неверная команда! попробуйте еще раз")
            self.menu()

    def add(self):
        habit = input("Введите название привычки: ")
        for key in self.habits.keys():
            if str(key).lower() == habit.lower():
                print("Такая привычка уже есть")
                self.menu()
                return
        habit_dict = {habit: []}
        self.habits.update(habit_dict)
        print("Добавлена новая привычка")
        print(self.habits)
        self.menu()

    def check(self):
        habit = input("Введите название привычки: ")
        for key, value in self.habits.items():
            if str(key).lower() == habit.lower():
                if date.today().isoformat() not in value:
                    value.append(date.today().isoformat())
                    print(f"Вы отметили привычку {key}!")
                else:
                    print("Привычка уже отмечена")
                self.menu()
                return
        print("Такой привычки еще нет")
        self.menu()

    def stats(self):
        habit = input("Введите название привычки: ")
        week_count = 0
        streak_count = 0
        for key, value in self.habits.items():
            if str(key).lower() == habit.lower():
                print(f"Общее количество выполнений: {len(value)}")
                for date in value:
                    if (datetime.fromisoformat(date)).date() > datetime.now().date() - timedelta(days=7):
                        week_count += 1
                    if str(datetime.now().date()) in value:
                        while str(datetime.now().date() - timedelta(days=streak_count)) in value:
                            streak_count += 1
                            print(f"Огонек зажжен. Серия: {streak_count}д.")
                    elif str(datetime.now().date() - timedelta(days=1)) in value:
                        if str(datetime.now().date() - timedelta(days=streak_count+1)) in value:
                            streak_count += 1
                        else:
                            print(f"Огонек НЕ зажжен. Отметьте привычку чтобы продлить серию. Серия: {streak_count}д.")
                    else:
                        print("Серия равна 0. Начните отмечать привычку чтобы зажжечь огонек")
                print(f"Процент выполнения за неделю: {week_count}/7 ({round(week_count/7 * 100)}%)")
                self.menu()
                return
        print("Такой привычки нет")
        self.menu()

    def graph(self):
        habit = input("Введите название привычки: ")
        for key, value in self.habits.items():
            if str(key).lower() == habit.lower():
                count = 0
                week_count = 0
                for date in value:
                    if (datetime.fromisoformat(date)).date() > datetime.now().date() - timedelta(days=7):
                        week_count += 1
                if str(key).lower() == habit.lower():
                    print(f"{key} (за последние 7 дней):")
                    while count < 7:
                        day = datetime.now().date() + timedelta(days=count-6)
                        print(f"{day} {["█" if str(day) in value else "░"]}")
                        count += 1
                    print(f"Итого: {week_count}/7 ({round(week_count/7 * 100)}%)")
                    self.menu()
                    return
        print("Такой привычки нет")
        self.menu()
        

    def exit(self):
        path = get_habits_path()
        with open(path, "w") as f:
           json.dump(self.habits, f)
        f.close()
        exit()
        

my_tracker = HabitTracker()
my_tracker.start()
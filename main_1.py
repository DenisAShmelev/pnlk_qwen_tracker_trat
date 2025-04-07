def main():
    # Ввод данных от пользователя
    try:
        days = int(input("Введите количество дней: "))
        total_expense = float(input("Введите общую сумму трат: "))
        
        if days <= 0 or total_expense < 0:
            print("Количество дней должно быть положительным числом, а сумма трат — неотрицательной.")
            return
        
        # Расчет планируемой траты на каждый день
        daily_expense = total_expense / days
        
        # Вывод таблицы
        print("\nПланируемые траты по дням:")
        print(f"{'День':<10}{'Сумма':<15}")
        print("-" * 25)
        
        for day in range(1, days + 1):
            print(f"{day:<10}{daily_expense:.2f}")
        
        # Вывод общей суммы для проверки
        print("-" * 25)
        print(f"Итого: {total_expense:.2f}")
    
    except ValueError:
        print("Ошибка: Введите корректные числовые значения.")

if __name__ == "__main__":
    main()
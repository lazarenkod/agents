# Получение Информации о Портфеле

Простой скрипт для **чтения данных** о портфеле из TraderNet API без каких-либо операций на бирже

## Быстрый Старт

### 1️⃣ Установка (первый раз)

```bash
# Установить зависимости
pip install requests pandas openpyxl
```

### 2️⃣ Установить API Credentials

```bash
# Получить API Key и Secret из https://tradernet.global/settings → API

export TRADERNET_API_KEY="tr_ваш_api_key"
export TRADERNET_API_SECRET="ваш_secret"
```

### 3️⃣ Запустить скрипт

```bash
# Просто получить информацию о портфеле
python3 get_portfolio.py

# Или в JSON формате
python3 get_portfolio.py --json

# Или сохранить в CSV файл
python3 get_portfolio.py --csv my_portfolio.csv
```

---

## Примеры Использования

### Пример 1: Просмотр портфеля (красивый формат)

```bash
python3 get_portfolio.py
```

**Результат:**
```
====================================================================================================
📊 ИНФОРМАЦИЯ О ПОРТФЕЛЕ
====================================================================================================
Дата/Время:     2024-10-29 12:30:45
Общая стоимость: $341,891.00
Совокупная прибыль: $115,427.07 (+105.67%)
Позиций:        31
====================================================================================================

ПОЗИЦИИ:
----------------------------------------------------------------------------------------------------
Тикер         Кол-во      Цена      Стоимость     Доля      Вход    Прибыль        %
----------------------------------------------------------------------------------------------------
NVDA.US            575 $207.00     $119,025 34.86%  $96.96  +$63,275  +113.50%
PLTR.US            166 $191.26      $31,749  9.30%  $62.40  +$21,390  +206.49%
NBIS.US            170 $123.84      $21,053  6.17%  $40.59  +$14,152  +205.09%
AMD.US              37 $262.13       $9,699  2.84% $157.44   +$3,873   +66.49%
...

====================================================================================================
```

### Пример 2: Получить в JSON формате

```bash
python3 get_portfolio.py --json > portfolio.json
```

**Результат (portfolio.json):**
```json
{
  "timestamp": "2024-10-29T12:30:45.123456",
  "summary": {
    "total_value": 341891.00,
    "total_profit": 115427.07,
    "total_profit_pct": 105.67,
    "positions_count": 31
  },
  "positions": [
    {
      "ticker": "NVDA.US",
      "quantity": 575,
      "entry_price": 96.96,
      "current_price": 207.00,
      "entry_value": 55749.34,
      "current_value": 119025.00,
      "allocation_pct": 34.86,
      "profit": 63275.66,
      "profit_pct": 113.50
    },
    ...
  ]
}
```

### Пример 3: Сохранить в CSV

```bash
python3 get_portfolio.py --csv my_portfolio.csv
```

Файл `my_portfolio.csv`:
```
ticker,quantity,entry_price,current_price,entry_value,current_value,profit,profit_pct,allocation_pct
NVDA.US,575,96.96,207.00,55749.34,119025.00,63275.66,113.50,34.86
PLTR.US,166,62.40,191.26,10358.95,31749.16,21390.21,206.49,9.30
...
```

---

## Опции Командной Строки

| Опция | Описание | Пример |
|-------|---------|--------|
| (нет) | Вывести красивый формат | `python3 get_portfolio.py` |
| `--json` | Вывести в JSON формате | `python3 get_portfolio.py --json` |
| `--csv FILE` | Сохранить в CSV файл | `python3 get_portfolio.py --csv portfolio.csv` |

---

## Примеры для Разных Задач

### 💡 Дневная Проверка Портфеля

```bash
# Просто смотрю статус в удобном формате
python3 get_portfolio.py
```

### 📊 Анализ Портфеля в Python

```bash
# Получаю JSON и анализирую в Python скрипте
python3 get_portfolio.py --json | python3 analyze.py
```

### 💾 Сохранение Истории Портфеля

```bash
# Сохраняю портфель с датой
python3 get_portfolio.py --csv portfolio_$(date +%Y%m%d).csv

# Результат: portfolio_20241029.csv, portfolio_20241030.csv, ...
```

### 📈 Мониторинг в Таблице

```bash
# Сохраняю в CSV для анализа в Excel или Google Sheets
python3 get_portfolio.py --csv my_portfolio.csv

# Затем открываю в Excel и анализирую
```

---

## Интеграция с Другими Скриптами

### Получить портфель в Python скрипте

```python
from tradernet_integration import TraderNetClient, PortfolioAnalyzer, load_credentials_from_env

# Подключиться
api_key, api_secret = load_credentials_from_env()
client = TraderNetClient(api_key, api_secret)

# Получить портфель
analyzer = PortfolioAnalyzer(client)
df, stats = analyzer.analyze_current_portfolio()

# Использовать данные
print(f"Общая стоимость: ${stats['total_value']:,.2f}")
print(f"Прибыль: ${stats['total_profit']:,.2f}")

# Работать с DataFrame
for idx, row in df.head(5).iterrows():
    print(f"{row['ticker']}: {row['quantity']} @ ${row['current_price']}")
```

### Автоматическое Сохранение История

```bash
# Создать директорию для истории
mkdir -p portfolio_history

# Добавить в crontab для дневного снимка (каждый день в 4 PM)
0 16 * * 1-5 python3 /path/to/get_portfolio.py --csv /path/to/portfolio_history/portfolio_$(date +\%Y\%m\%d).csv

# Результат: каждый день будет новый файл portfolio_20241029.csv, portfolio_20241030.csv, ...
```

---

## Что Делает Скрипт

✅ **Делает:**
- Получает текущий портфель из API
- Загружает котировки для всех позиций
- Вычисляет прибыль и убытки
- Показывает распределение по позициям
- Выводит красивый отчет

❌ **НЕ делает:**
- Не отправляет ордеры
- Не продает/покупает акции
- Не делает каких-либо операций на бирже
- Не изменяет портфель

---

## Troubleshooting

### Ошибка: "API Key not found"

```bash
# Проверить что переменные установлены
echo $TRADERNET_API_KEY
echo $TRADERNET_API_SECRET

# Если пусто - установить их
export TRADERNET_API_KEY="tr_..."
export TRADERNET_API_SECRET="..."
```

### Ошибка: "No module named 'pandas'"

```bash
# Установить pandas
pip install pandas
```

### Ошибка: "Connection refused"

```bash
# Проверить интернет
ping tradernet.global

# Проверить что TraderNet доступен
curl https://api.tradernet.global/health
```

---

## Автоматизация (Schedule)

### Каждый День в 4 PM (cron)

```bash
# Редактировать crontab
crontab -e

# Добавить строку
0 16 * * 1-5 python3 /Users/dmitry.lazarenko/Documents/projects/stocks-ai/agents/get_portfolio.py --csv /tmp/portfolio.csv && echo "✓ Portfolio updated at $(date)" >> ~/portfolio_updates.log
```

### Python Scheduler

```python
import schedule
import time
import subprocess

def get_portfolio():
    subprocess.run(["python3", "get_portfolio.py"])

# Запускать каждый день в 4 PM
schedule.every().day.at("16:00").do(get_portfolio)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## Сравнение с Другими Скриптами

| Скрипт | Назначение | Функция |
|--------|-----------|---------|
| **get_portfolio.py** | Просмотр портфеля | ✅ Только читает данные |
| **execute_portfolio_recommendations.py** | Оптимизация портфеля | ⚠️ Выполняет операции на бирже |

**Рекомендация:** Начните с `get_portfolio.py` чтобы понять как работает API, потом переходите к `execute_portfolio_recommendations.py` для автоматизации торговли.

---

## Частые Вопросы

### Q: Скрипт будет делать что-то с моим портфелем?
A: **НЕТ.** Этот скрипт только **читает** информацию. Он не может отправлять ордеры или менять портфель.

### Q: Как часто я могу запускать этот скрипт?
A: Столько раз сколько захотите! Нет ограничений. Можете запускать каждую минуту если нужно.

### Q: Можно ли использовать это для мониторинга портфеля?
A: **ДА!** Отлично подходит для:
- Дневного мониторинга
- Сохранения истории портфеля
- Анализа в Excel
- Интеграции с другими системами

### Q: Что если я хочу добавить операции позже?
A: Используйте `execute_portfolio_recommendations.py` когда будете готовы. Начните с `--dry-run` для проверки.

---

## Следующие Шаги

1. ✅ Запустите `python3 get_portfolio.py` для проверки подключения
2. ✅ Сохраните портфель в CSV для анализа
3. ✅ Создайте schedule для автоматического мониторинга
4. ⏳ Когда будете готовы - используйте `execute_portfolio_recommendations.py`

---

**Дата обновления:** 29 октября 2024
**Версия:** 1.0.0
**Статус:** ✅ ГОТОВО

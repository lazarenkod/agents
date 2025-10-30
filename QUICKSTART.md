# Быстрый Старт: TraderNet Integration

Автоматизируйте управление портфелем за 5 минут

## 5-Минутная Настройка

### 1️⃣ Установить зависимости (1 минута)

```bash
cd /Users/dmitry.lazarenko/Documents/projects/stocks-ai/agents
pip install requests pandas openpyxl
```

### 2️⃣ Получить API Credentials (2 минуты)

1. Перейти в https://tradernet.global → Settings → API
2. Нажать "Create New API Key"
3. Выбрать permissions:
   - ✅ Read Portfolio
   - ✅ Read Orders
   - ✅ Create Orders
   - ✅ Cancel Orders
   - ✅ Get Quotes
4. Нажать "Generate"
5. **Копировать и сохранить:**
   - API Key (начинается с `tr_`)
   - API Secret (длинная строка)

### 3️⃣ Установить Credentials (2 минуты)

```bash
# Установить временно для текущей сессии:
export TRADERNET_API_KEY="tr_ваш_api_key_сюда"
export TRADERNET_API_SECRET="ваш_secret_сюда"

# Проверить что работает:
echo $TRADERNET_API_KEY
```

---

## 🚀 Запуск

### Вариант 1: Тестирование (безопасно)

```bash
python3 execute_portfolio_recommendations.py --dry-run
```

Вывод должен быть:
```
✓ Credentials загружены
✓ Подключение установлено
✓ Анализ завершен

АНАЛИЗ ПОРТФЕЛЯ
================================================================================
Общая стоимость: $341,891.00
Совокупная прибыль: $115,427.07 (+105.67%)
Позиций: 31
================================================================================

TOP 5 ПОЗИЦИЙ:
...
```

### Вариант 2: Реальное выполнение

```bash
# Только критические операции
python3 execute_portfolio_recommendations.py --execute --priority 2

# ВСЕ операции
python3 execute_portfolio_recommendations.py --execute --priority 5
```

---

## 📊 Что будет выполнено?

### Приоритет 1 (КРИТИЧЕСКИЕ - выполнить СРАЗУ)

1. **Триммирование NVDA** (-$47,600)
   - Текущая доля: 34.86% → целевая: 18-20%
   - Продать: ~230-250 акций
   - Получить наличные для диверсификации

2. **Закрытие убыточных позиций** (Tax Loss Harvesting)
   - INTS, NVO, AEVA, ALT, QUBT, SANA, SMCI, UPST
   - Получить: ~$3,858 + налоговые вычеты

3. **Триммирование PLTR** (-$7,650)
   - Текущая доля: 9.30% → целевая: 5%
   - Продать: ~40 акций

### Приоритет 2 (ВЫСОКИЕ - выполнить день 2)

- Триммирование других сильных позиций
- Закрепление больших прибылей

### Приоритет 3+ (СРЕДНИЕ - выполнить неделя 1-2)

- Покупка облигаций (BND, TLT)
- Покупка золота (GLD)
- Диверсификация в другие секторы

---

## 💰 Ожидаемые Результаты

| Метрика | До | После | Улучшение |
|---------|-----|-------|-----------|
| **Концентрация NVDA** | 34.86% | 18-20% | ✓ Норма |
| **Защита портфеля** | 0% облигаций | 15% облигаций | ✓ Хеджирование |
| **Диверсификация** | 80% tech | 50% tech | ✓ Баланс |
| **Макс падение** | -60%+ | -30% | ✓ Управляемый риск |
| **Ожид. доходность** | Хаотичная | 15-20%/год | ✓ Стабильность |

---

## 📋 Примеры Использования

### Пример 1: Дневная проверка

```bash
# Каждый день смотрите рекомендации в режиме dry-run
python3 execute_portfolio_recommendations.py --dry-run
```

### Пример 2: Еженедельная оптимизация

```bash
# Понедельник: критические операции
python3 execute_portfolio_recommendations.py --execute --priority 2

# Среда: добавить защиту
python3 execute_portfolio_recommendations.py --execute --priority 3

# Пятница: завершить оптимизацию
python3 execute_portfolio_recommendations.py --execute --priority 4
```

### Пример 3: Одноразовая оптимизация

```bash
# Выполнить все за раз (если вы уверены)
python3 execute_portfolio_recommendations.py --execute --priority 5
```

---

## 🛑 ВАЖНО: Перед выполнением

- ✅ Проверить в режиме `--dry-run`
- ✅ Убедиться что хватает средств (Free Cash)
- ✅ Проверить рыночные часы (US Market: 9:30-16:00 ET)
- ✅ Иметь резервный план на случай сбоя
- ✅ Начать с Priority 2 (критические), не Priority 5 (все)

---

## 🆘 Если что-то не работает

### Ошибка: "API Key not found"

```bash
# Проверить что переменные установлены
echo $TRADERNET_API_KEY
echo $TRADERNET_API_SECRET

# Если пусто:
export TRADERNET_API_KEY="tr_..."
export TRADERNET_API_SECRET="..."
```

### Ошибка: "Connection failed"

```bash
# Проверить интернет
ping tradernet.global

# Проверить что TraderNet доступен
curl https://api.tradernet.global/health
```

### Ошибка: "Authentication failed"

- Перепроверить что API Key правильный (в TraderNet Settings)
- Может быть нужно создать новый API Key
- Убедиться что permissions выбраны правильно

---

## 📚 Следующие шаги

1. **Изучить детали**: Прочитайте [TRADERNET_SETUP.md](./TRADERNET_SETUP.md)
2. **Мониторить логи**: Проверяйте `trading_log.json` после каждого запуска
3. **Автоматизировать**: Добавьте в cron для автоматического выполнения
4. **Оптимизировать**: Настройте рекомендации под ваши цели

---

## 📞 Поддержка

- 📖 TraderNet Docs: https://tradernet.global/tradernet-api
- 🐍 Python SDK: https://tradernet.global/tradernet-api/python-sdk
- 💬 Support: https://help.tradernet.global

---

**Готовы начать? Выполните эти 3 шага выше и запустите:**

```bash
python3 execute_portfolio_recommendations.py --dry-run
```

Успехов! 🚀

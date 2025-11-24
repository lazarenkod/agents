# Performance Feedback Script: SBI Framework

## Обзор

SBI (Situation-Behavior-Impact) — gold standard для performance feedback, используемый в Google, Amazon, Microsoft, Meta, Netflix. Framework превращает vague feedback ("хорошая работа", "нужно улучшить") в конкретный, actionable, и развивающий feedback.

## SBI Framework: Структура

### S - Situation (Ситуация)

**Определение:** Когда и где произошло? Конкретный контекст.

**Цель:** Установить shared understanding о событии.

**Формат:**

```
"В [время/дата], когда [контекст]..."
"На прошлой неделе во время [событие]..."
"В проекте [название] в момент [момент]..."
```

**Примеры:**

```
✓ GOOD (Specific):
"На вчерашней встрече с Product Team в 15:00..."
"В прошлый четверг, когда мы обсуждали архитектуру системы..."
"Во время sprint planning 15 ноября..."

✗ BAD (Vague):
"Недавно..."
"Обычно ты..."
"Всегда..."
```

### B - Behavior (Поведение)

**Определение:** Что конкретно человек сделал или сказал? Наблюдаемые действия.

**Цель:** Описать факты, не интерпретации.

**Формат:**

```
"Ты [конкретное действие]..."
"Ты сказал: '[прямая цитата]'..."
"Ты [что сделал/не сделал]..."
```

**Критично:** Behavior должен быть observable (другие люди могут подтвердить).

**Примеры:**

```
✓ GOOD (Observable):
"Ты прервал Sarah 3 раза во время ее презентации."
"Ты сказал: 'Это глупая идея' в ответ на proposal."
"Ты не отправил код на review до дедлайна в пятницу."
"Ты выступил с инициативой реструктурировать API."

✗ BAD (Interpretation):
"Ты был неуважителен." (это интерпретация, не behavior)
"Ты не заботишься о качестве." (это judgment)
"У тебя плохой attitude." (слишком vague)
```

### I - Impact (Влияние)

**Определение:** Какое влияние это поведение оказало? На команду, проект, клиента, тебя как менеджера.

**Цель:** Помочь человеку понять "так что?" и "почему это важно?".

**Формат:**

```
"В результате [последствие]..."
"Это привело к [impact]..."
"Из-за этого [что случилось]..."
```

**Типы Impact:**

- **Team impact:** "Команда потеряла доверие к deadline estimates."
- **Project impact:** "Проект delayed на 2 недели."
- **Client impact:** "Клиент был недоволен и escalated."
- **Relationship impact:** "Sarah почувствовала, что ее мнение не ценится."
- **Business impact:** "Мы потеряли $50K revenue из-за bug."
- **Your impact (as manager):** "Я был вынужден объяснять leadership, почему мы не delivered."

**Примеры:**

```
✓ GOOD (Clear Impact):
"В результате, Product Team не получил нужные данные вовремя, и они не смогли сделать decision."
"Это создало напряжение в команде — два человека пришли ко мне с concerns."
"Из-за этого клиент escalated complaint в leadership, и мы потеряли trust."

✗ BAD (No Impact):
"Это плохо."
"Мне не понравилось."
"Так нельзя."
```

## SBI Examples: 20+ реальных сценариев

### Категория 1: Constructive Feedback (Negative)

#### Example 1: Missed Deadline

```
S: "На прошлой неделе, когда мы договорились, что ты завершишь feature [X] к пятнице,"
B: "ты не delivered код и не предупредил меня о задержке заранее."
I: "В результате, Product Team не смог начать QA, и мы сдвинули release на неделю. Это повлияло на доверие Product к нашим estimates."

Follow-up Question:
"Что произошло? Как мы можем prevent это в будущем?"
```

#### Example 2: Poor Code Quality

```
S: "Вчера, когда я reviewed твой PR для проекта [Y],"
B: "я обнаружил 15 issues: нет unit tests, код не соответствует style guide, и есть hardcoded credentials."
I: "Это создало дополнительные 4 часа работы для меня, и мы не можем merge это в production без серьезной rework. Это замедляет всю команду."

Follow-up Question:
"Что мы можем сделать, чтобы код соответствовал standards до review?"
```

#### Example 3: Disrespectful Communication

```
S: "На вчерашней design review встрече в 14:00,"
B: "ты сказал: 'Этот дизайн ужасен, кто это придумал?' и закатил глаза, когда Alex объяснял rationale."
I: "Alex был visibly upset и после встречи пришел ко мне с concerns. Это создало токсичную атмосферу, и команда теперь reluctant делиться идеями."

Follow-up Statement:
"Я ценю твою техническую экспертизу, и мне нужно, чтобы ты выражал disagreement с уважением. Например: 'У меня concerns о этом подходе, вот почему...'"
```

#### Example 4: Not Speaking Up (Underperformance)

```
S: "В прошлом месяце, когда ты застрял на проблеме с database migration,"
B: "ты не сказал мне или команде в течение 2 недель, пока project не was уже at risk."
I: "Мы потеряли 2 недели, которые могли бы потратить на решение проблемы раньше. Теперь проект delayed, и leadership спрашивает, почему."

Follow-up Discussion:
"Я хочу, чтобы ты escalated blockers в течение 24-48 часов. Если ты stuck, это не failure — это нормально. Failure — это молчание."
```

#### Example 5: Lack of Ownership

```
S: "Во время sprint retrospective в прошлую пятницу,"
B: "когда мы обсуждали, почему feature [Z] shipped с bugs, ты сказал: 'QA должны были это поймать', и не взял ответственность за свой код."
I: "Команда почувствовала, что ты blame shifting. Это подрывает trust. Как инженер, ты responsible за качество своего кода, не только QA."

Follow-up Expectation:
"В будущем, когда есть bug, я ожидаю: 'Я мог сделать лучше. Вот как я предотвращу это.' Ownership — это key для Senior level."
```

#### Example 6: Poor Collaboration

```
S: "В проекте [A] на этой неделе,"
B: "ты изменил API contract без уведомления frontend team, и они узнали только когда их build сломался."
I: "Frontend потерял 4 часа на debugging и был вынужден переписать код. Это создало фрустрацию и замедлило их delivery."

Follow-up Action:
"Когда ты меняешь shared dependencies или APIs, ты должен: 1) уведомить affected teams в Slack, 2) update документацию, 3) дать им time adjust before deploying."
```

#### Example 7: Meeting Dominance

```
S: "На сегодняшней team planning встрече,"
B: "ты говорил 70% времени и не дал другим членам команды возможность высказаться. Когда Maria начала говорить, ты ее прервал."
I: "Мы не услышали важные ideas от других. Maria visibly frustrated и disengaged после этого. Нам нужны diverse perspectives для лучших решений."

Follow-up Coaching:
"Я ценю твою passion и экспертизу. В следующий раз, попробуй: 1) говорить max 20% времени, 2) активно приглашать других ('Maria, что ты думаешь?'), 3) ждать 3 секунды после кого-то, прежде чем говорить."
```

#### Example 8: Not Documenting

```
S: "На прошлой неделе, когда ты завершил миграцию database,"
B: "ты не обновил runbook или wiki с изменениями в процессе."
I: "Когда oncall engineer столкнулся с проблемой в выходные, он не знал, как rollback. Это привело к 2-часовому outage."

Follow-up Requirement:
"Для любого production change, я ожидаю обновленную документацию до merge. Это non-negotiable."
```

#### Example 9: Not Preparing for Meetings

```
S: "Сегодня на architecture review meeting,"
B: "ты пришел без подготовленного design doc и improvised презентацию на лету."
I: "Мы потеряли 30 минут, пытаясь понять твой proposal. Meeting был не productive, и нам придется встретиться снова. Это waste времени для 6 человек."

Follow-up Standard:
"Для architecture reviews, я ожидаю design doc отправлен минимум за 48 часов до встречи, чтобы люди могли review."
```

#### Example 10: Passive-Aggressive Behavior

```
S: "Вчера в Slack, когда я попросил тебя помочь junior engineer с PR,"
B: "ты написал: 'Я думал, это не моя работа, но окей' с emoji закатывающего глаза."
I: "Это создало awkward ситуацию. Junior engineer почувствовал себя burden. Mentorship — это part твоей роли как Senior Engineer."

Follow-up Conversation:
"Если у тебя есть concerns о workload или приоритетах, давай обсудим это напрямую. Passive-aggressive комментарии undermine team morale."
```

### Категория 2: Positive Feedback (Reinforcement)

#### Example 11: Excellent Collaboration

```
S: "На этой неделе, когда ты работал с Design team на проекте [X],"
B: "ты организовал early sync meeting, предложил 3 alternative solutions с trade-offs, и incorporated их feedback в финальный design."
I: "Design team был в восторге от collaboration. Product Manager сказал мне, что это лучший cross-functional partnership, который он видел. Проект went smoothly именно благодаря этому."

Reinforcement:
"Это exactly то, что я хочу видеть. Продолжай такой подход в future проектах."
```

#### Example 12: Taking Initiative

```
S: "В прошлом месяце, когда ты заметил, что наш CI pipeline медленный,"
B: "ты не ждал assignment. Ты исследовал проблему, написал proposal, и implemented solution, которое сократило build time с 30 до 8 минут."
I: "Вся команда выиграла — мы экономим 2 часа в день. Leadership заметил это, и я включил это в твой performance review как evidence инициативности."

Reinforcement:
"Это типичный пример ownership и impact. Вот почему я вижу тебя как будущего Staff Engineer."
```

#### Example 13: Great Mentorship

```
S: "За последние 3 месяца, с тех пор как ты began менторить Alex,"
B: "я вижу, что ты проводишь weekly 1-on-1s, делаешь thorough code reviews с educational comments, и pair programming с ним раз в неделю."
I: "Alex значительно вырос — его код качество улучшилось, он более confident, и он недавно delivered first solo feature. Он сказал мне, что ты самый helpful mentor, который у него был."

Reinforcement:
"Это outstanding mentorship. Это именно то, что нам нужно от Senior Engineers. Спасибо за investment в team."
```

#### Example 14: Handling Crisis Well

```
S: "Прошлой ночью, когда произошел production outage в 2 AM,"
B: "ты был oncall и быстро diagnosed issue, communicated в Slack каждые 15 минут с updates, и coordinated с 3 teams для fix. Ты restored service за 45 минут."
I: "Клиенты почти не почувствовали impact. CEO прислал благодарность в eng-all channel. Твоя спокойная и structured подход в кризисе был exceptional."

Reinforcement:
"Это мастер-класс incident response. Я добавлю это в твой promotion packet."
```

#### Example 15: Delivering Under Pressure

```
S: "В последние 2 недели sprint, когда мы были at risk not delivering ключевую feature,"
B: "ты добровольно взял дополнительный work, stayed late (without complaining), и delivered high-quality code в срок."
I: "Мы shipped on time, и клиент был счастлив. Product Manager был impressed твоей dedication. Это спасло quarter OKR."

Reinforcement:
"Я не ожидаю, что ты всегда работаешь extra hours — work-life balance важен. Но в критический момент ты stepped up, и я это ценю."
```

#### Example 16: Giving Constructive Feedback to Peers

```
S: "На прошлой неделе, когда ты reviewed design doc от Maria,"
B: "ты дал detailed, constructive feedback: highlighted strengths, pointed out gaps (with examples), и предложил alternative approach."
I: "Maria сказала мне, что твой feedback был самым полезным, который она получила. Она implemented твои suggestions, и design стал much stronger."

Reinforcement:
"Это great peer leadership. Ты elevating уровень всей команды через thoughtful feedback."
```

#### Example 17: Communication Clarity

```
S: "Вчера на All-Hands, когда ты presented technical project для non-technical audience,"
B: "ты использовал clear analogies, избегал jargon, и визуализировал complex concepts с простыми диаграммами."
I: "Executives понял impact твоей работы. VP Engineering сказал мне: 'Наконец-то я понял, что делает ваша команда!' Это повысило visibility нашей команды."

Reinforcement:
"Это Staff-level communication. Продолжай так презентовать — это важный skill для твоей карьеры."
```

#### Example 18: Improving Process

```
S: "В прошлом квартале, когда ты заметил, что мы часто пропускаем bugs,"
B: "ты создал automated testing framework, написал документацию, и провел training для команды."
I: "Наш bug rate упал на 60%. Мы экономим 10 часов в неделю на manual testing. Другие команды теперь хотят использовать твой framework."

Reinforcement:
"Это системное thinking — ты не просто фиксишь проблемы, ты создаешь solutions, которые scale. Exactly то, что нужно для impact."
```

#### Example 19: Difficult Conversation Handling

```
S: "На этой неделе, когда ты дал critical feedback Alex о его code quality,"
B: "ты был direct, но respectful. Ты использовал конкретные примеры, объяснил impact, и предложил action plan для improvement."
I: "Alex был сначала defensive, но потом сказал мне, что твой feedback был fair и полезным. Он уже implementing твои suggestions."

Reinforcement:
"Сложные разговоры — это leadership. Ты handled это professionally и with care. Это признак зрелости."
```

#### Example 20: Going Beyond Role

```
S: "В последние 6 месяцев,"
B: "ты не только выполняешь свои инженерные задачи, но и активно помогаешь с hiring (interviewed 12 candidates), onboarding (mentored 2 new hires), и представлял команду на конференции."
I: "Твой contributions выходят far beyond code. Ты помог нам hire 3 strong engineers, new hires ramped up быстрее благодаря тебе, и наша team visibility increased в индустрии."

Reinforcement:
"Это level up твоей роли. Ты уже действуешь как Staff Engineer. Давай поговорим о твоей карьере."
```

## Real-Time Feedback vs. Retrospective Feedback

### Real-Time Feedback (Немедленно после события)

**Когда использовать:**
- Поведение critical и нужно изменить немедленно
- Позитивное поведение, которое хочешь reinforced
- Ситуация свежая в памяти

**Как доставить:**

```
Вариант 1: Сразу после meeting/события (в private)
"У тебя минутка? Я хочу дать feedback по meeting, который только что закончился."

Вариант 2: Slack/Email (для minor feedback)
"Quick feedback: На сегодняшней встрече ты отлично handled вопрос от PM о timeline. Твое объяснение было clear и confidence. Keep it up!"

Вариант 3: В конце дня (для constructive feedback)
"В конце дня, давай 10 минут talk о сегодняшней презентации. Хочу дать тебе feedback."
```

**Примеры Real-Time SBI:**

```
Позитивный (сразу после):
S: "Только что на stand-up,"
B: "ты flagged blocker early и предложил конкретное решение."
I: "Это помогло нам save время — мы можем address это сегодня, а не в конце спринта."

Constructive (в течение часа):
S: "На встрече час назад с клиентом,"
B: "ты interrupted клиента 2 раза, когда он объяснял проблему."
I: "Клиент was frustrated и не закончил мысль. Нам нужно reschedule, чтобы услышать полную картину."
```

### Retrospective Feedback (Через время после события)

**Когда использовать:**
- Паттерны behavior (не одна ситуация)
- Performance review cycles
- Когда нужно время собрать примеры

**Как доставить:**

```
Формат: Scheduled 1-on-1

"Я хочу обсудить паттерн, который я наблюдаю за последние несколько недель."

[Используй multiple SBI examples для демонстрации паттерна]
```

**Пример Retrospective SBI (Pattern):**

```
"Я заметил паттерн, который хочу обсудить: deadline management.

Пример 1:
S: 3 недели назад, в проекте [X],
B: ты missed дедлайн на 5 дней без early warning.
I: Product не мог launch вовремя.

Пример 2:
S: 2 недели назад, в проекте [Y],
B: ты снова missed deadline, на этот раз на 3 дня.
I: QA был вынужден work на выходных.

Пример 3:
S: На этой неделе, в проекте [Z],
B: ты told мне в пятницу (deadline day), что не успеешь.
I: Мы сдвинули release, и stakeholders недовольны.

Это паттерн. Давай разберем, что происходит и как мы можем improve."
```

## Constructive vs. Positive Feedback: Когда и как

### Constructive Feedback (Critical)

**Timing:**
- Как можно скорее (в течение 24-48 часов)
- В private setting
- Когда оба спокойны (не в heated moment)

**Tone:**
- Direct, но respectful
- Фокус на behavior, не на человека
- Без emotion или frustration

**Frequency:**
- Когда нужно (не накапливай)
- Но не overwhelming (max 1-2 issues за разговор)

**Template:**

```
"Я хочу дать тебе feedback о [topic]. Это important для твоего growth."

[SBI Framework]

"Я знаю, что ты можешь improve это. Давай discuss, как."

[Action plan]
```

### Positive Feedback (Reinforcement)

**Timing:**
- НЕМЕДЛЕННО (чем быстрее, тем лучше)
- Публично, если человек комфортен с этим
- В private, если sensitive

**Tone:**
- Enthusiastic, genuine
- Конкретный (не generic "good job")
- Focused на impact

**Frequency:**
- ЧАСТО (aim for 3:1 ratio positive:constructive)
- Не ждать formal reviews

**Template:**

```
"Я хочу highlight что-то, что ты сделал отлично."

[SBI Framework]

"Это exactly то, что мы ценим. Спасибо!"

[Optional: "Я добавлю это в твой performance review."]
```

### Соотношение Positive vs. Constructive

```
Best Practice Ratio: 3-5 Positive : 1 Constructive

Почему?
- Люди более open к critical feedback, если они знают, что ты видишь их strengths
- Positive feedback motivates и reinforces хорошее behavior
- Constructive feedback без positive создает demotivation

⚠️ Ловушка: "Compliment Sandwich" (avoid!)
❌ Don't: "Ты отлично работаешь, НО [критика], но в целом хорошо."
✅ Do: Дай positive отдельно. Дай constructive отдельно. Не микшируй.
```

## Written Documentation Format

### Format 1: Email Follow-Up (после устного feedback)

```
Subject: Follow-up: Feedback от [Date]

Привет [Имя],

Я хочу резюмировать feedback, который мы обсудили сегодня в письменном виде для clarity.

**Situation:**
[Когда и где произошло]

**Behavior:**
[Что ты наблюдал]

**Impact:**
[Какое влияние это оказало]

**Action Plan:**
[Что мы договорились сделать]
1. [Action item 1] - Срок: [Date]
2. [Action item 2] - Срок: [Date]

**Support:**
[Что ты предоставишь для помощи]

Давай check in [дата] для review прогресса.

[Твое имя]
```

### Format 2: Performance Review Documentation

```markdown
# Performance Review: [Employee Name]
**Period:** [Date range]
**Reviewer:** [Your name]

---

## Strengths (Positive Feedback)

### 1. [Strength Area]

**Example 1:**
- **Situation:** [Context]
- **Behavior:** [What they did]
- **Impact:** [Result]

**Example 2:**
- **Situation:** [Context]
- **Behavior:** [What they did]
- **Impact:** [Result]

---

## Development Areas (Constructive Feedback)

### 1. [Development Area]

**Example 1:**
- **Situation:** [Context]
- **Behavior:** [What they did]
- **Impact:** [Result]

**Action Plan:**
- [Action item 1]
- [Action item 2]

---

## Overall Rating: [Rating]

**Summary:**
[Overall assessment, balanced positive and constructive]

**Goals for Next Period:**
1. [Goal 1]
2. [Goal 2]
3. [Goal 3]
```

### Format 3: Informal Feedback Log (for yourself)

```markdown
# Feedback Log: [Employee Name]

## [Date]: [Topic]
- **Type:** Positive / Constructive
- **Situation:** [Brief context]
- **Behavior:** [What they did]
- **Impact:** [Result]
- **Given?** Yes / No / Planned for [Date]

---

[Keep running log to track patterns and prepare for reviews]
```

## Follow-Up and Tracking

### Immediate Follow-Up (within 24 hours)

```
Для Constructive Feedback:
1. Отправь email summary с SBI и action plan
2. Schedule follow-up meeting (1-2 weeks out)
3. Offer support/resources
4. Log в HRIS/performance system

Для Positive Feedback:
1. (Optional) Send quick Slack/email reinforcement
2. Log для performance review
3. Share с skip-level manager (if significant)
4. Consider public recognition (team meeting, Slack channel)
```

### Ongoing Tracking (weekly/monthly)

```markdown
# Feedback Tracking Checklist

## Weekly
- [ ] Дал ли я minimum 3 positive feedbacks на команду?
- [ ] Есть ли constructive feedback, который нужно дать?
- [ ] Все critical issues addressed в течение 48 часов?
- [ ] Documented feedback в моем log?

## Monthly
- [ ] Review feedback log для каждого direct report
- [ ] Есть ли паттерны, которые нужно address?
- [ ] Баланс positive vs. constructive (aim 3:1)?
- [ ] Follow-up на past action plans — прогресс?

## Quarterly (Performance Review)
- [ ] Собрал minimum 5-10 SBI examples per person?
- [ ] Баланс strengths и development areas?
- [ ] Clear action plan на следующий квартал?
- [ ] Employee понимает feedback и expectations?
```

## Common Mistakes to Avoid

```
❌ MISTAKE 1: Vague Feedback
"Ты делаешь хорошую работу."
✅ FIX: Дай конкретный SBI example.

❌ MISTAKE 2: Delayed Feedback
Waiting until quarterly review для critical issues.
✅ FIX: Дай feedback в течение 24-48 часов.

❌ MISTAKE 3: Compliment Sandwich
"Ты хорош, НО [критика], но в целом окей."
✅ FIX: Дай positive отдельно, constructive отдельно.

❌ MISTAKE 4: Judgmental Language
"Ты ленивый." / "Ты не заботишься."
✅ FIX: Опиши behavior, не характер: "Ты пропустил 3 дедлайна."

❌ MISTAKE 5: No Follow-Up
Дал feedback и forgot about it.
✅ FIX: Schedule follow-up и track прогресс.

❌ MISTAKE 6: Only Negative
Фокус только на проблемах, игнорируя successes.
✅ FIX: 3:1 ratio positive:constructive.

❌ MISTAKE 7: Generic Praise
"Отличная работа!" (без specifics)
✅ FIX: Дай SBI для positive feedback тоже.

❌ MISTAKE 8: Feedback in Public (for Constructive)
Критикуешь человека перед командой.
✅ FIX: Constructive feedback ВСЕГДА в private.

❌ MISTAKE 9: Not Documenting
Relying на память для performance reviews.
✅ FIX: Log feedback в real-time.

❌ MISTAKE 10: Making It About You
"Я разочарован тобой."
✅ FIX: Фокус на behavior и impact: "Проект delayed на 2 недели."
```

## Advanced: Feedback for Different Personalities

### High Performer (Defensive to Criticism)

```
Approach: Lead с data и impact, не с judgment.

"Ты top performer, и я хочу помочь тебе level up. Вот где я вижу opportunity..."

[SBI с focus на growth, не на problem]

"Это не критика твоего value. Это about unlocking next level."
```

### Struggling Performer (Demoralized)

```
Approach: Balance constructive with recognition, создай hope.

"Я вижу, что ты struggling. Давай разберем конкретные ситуации и найдем, как support тебя."

[SBI с focus на specific behaviors, не на "ты не good enough"]

"Я верю, что ты можешь improve это. Вот plan и поддержка."
```

### New Employee (Needs Direction)

```
Approach: Constructive feedback как learning opportunity.

"Ты новый, и это normal, что есть learning curve. Вот где ты на правильном пути, и где мы хотим adjust..."

[SBI с clear expectations и examples]

"Это не failure — это part процесса. Задавай вопросы."
```

### Senior Employee (Set in Ways)

```
Approach: Peer-to-peer tone, respect experience.

"Я ценю твой опыт. Я хочу share observation и услышать твою perspective."

[SBI с открытостью к dialogue]

"Как ты думаешь об этом? Что я могу не видеть?"
```

## SBI Practice Exercises

**Exercise 1:** Преобразуй vague feedback в SBI

```
Vague: "Ты не team player."
SBI:
S: "На прошлой неделе, во время sprint planning,"
B: "ты отказался помочь Maria с blocked task, сказав 'Это не мой проект.'"
I: "Maria была stuck на 2 дня, и мы missed sprint goal. Team видит, что ты не willing collaborate."
```

**Exercise 2:** Дай positive SBI для этой ситуации

```
Ситуация: Engineer stayed late для fix production bug.
SBI:
S: "Вчера вечером, когда произошел prod incident в 19:00,"
B: "ты stayed до 22:00 для debug и fix, хотя не был oncall."
I: "Мы restored service и prevented customer loss. Это saved компанию $50K. Team ценит твою dedication."
```

---

**Использование:** Этот script — ваш comprehensive guide для performance feedback. SBI framework делает feedback конкретным, fair, и actionable. Практикуйте его на каждой возможности — это станет второй натурой.

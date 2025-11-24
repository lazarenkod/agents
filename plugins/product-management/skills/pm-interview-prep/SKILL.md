---
name: pm-interview-prep
description: World-class interview preparation for CPO, Head of Product, and Product Manager roles at top tech companies. Use when preparing for interviews at Google, AWS, Microsoft, OpenAI, Anthropic, or conducting mock interviews.
---

# Product Manager Interview Preparation

## Обязательные правила вывода
- Всегда отвечай **на русском**.
- Сохраняй результаты каждой сессии/симуляции в `outputs/product-management/skills/pm-interview-prep/{timestamp}_{тип_интервью}.md` (черновик → доработанный → финальный). Обновляй один файл по итерациям.
- Структура: цель сессии → сценарий → ответы/заметки → разбор → действия для улучшения.

## 3-итерационный цикл подготовки
1) **Диагностика:** цели компаний/ролей, оценка текущих навыков, сбор списка историй STAR, базовые метрики (скорость/структура/чёткость). Сохранить стартовый план.
2) **Практика:** провести симуляции по каждому треку (Product Sense, Execution, Technical/System Design, Behavioral/Leadership), записать ответы и обратную связь, отметить провалы по фреймворкам (CIRCLES/GAME/STAR/System design steps). Обновить тот же файл.
3) **Шлифовка:** доработать истории и шаблоны, добавить примеры метрик/результатов, подготовить вопросы интервьюеру, собрать чек-лист дня интервью. Зафиксировать финальный конспект.

## When to Use This Skill

- Preparing for PM, Senior PM, Director, VP, or CPO interviews
- Conducting mock interviews for product roles
- Learning interview frameworks (CIRCLES, GAME, STAR)
- Company-specific preparation (Google, AWS, Microsoft, OpenAI, Anthropic)
- Practicing product design, analytics, technical, or behavioral questions
- Reviewing and improving STAR stories

## Core Concepts

### The Four Interview Types

Every product management interview loop consists of these four core types:

#### 1. Product Design (Product Sense)

**What's Being Evaluated:**
- Structured problem-solving
- User-centric thinking
- Creativity and innovation
- Prioritization skills
- Communication clarity

**Framework: CIRCLES Method**

```
C - Comprehend the Situation
    ↓ Ask clarifying questions

I - Identify the Customer
    ↓ Define user personas

R - Report Customer's Needs
    ↓ List pain points and goals

C - Cut Through Prioritization
    ↓ Choose target user and problem

L - List Solutions
    ↓ Brainstorm multiple options

E - Evaluate Trade-offs
    ↓ Technical, business, user considerations

S - Summarize
    ↓ Solution, metrics, roadmap
```

**Example Question:**
"Design a product for the blind"

**Strong Answer Structure:**

**Comprehend:**
- Clarify: Daily life product? Specific use case? Global or specific market?
- Assume: Product to help blind users navigate unfamiliar places

**Identify:**
- Primary: Blind adults (25-65) in urban areas
- Secondary: Visually impaired, low vision users
- Context: Walking, public transit, shopping

**Report Needs:**
- Navigate safely (avoid obstacles, cross streets)
- Understand surroundings (What's around me? Where am I?)
- Find destinations (Get to specific address)
- Maintain independence (Don't rely on others)

**Cut:**
- Focus on: Safe navigation in unfamiliar places
- Problem: Blind users can't see obstacles or navigate without assistance
- MVP: Real-time obstacle detection and navigation

**List Solutions:**
1. **Haptic belt**: Vibrations indicate obstacle direction
2. **Bone conduction earbuds**: Audio directions without blocking ears
3. **Smart cane**: Sensor-equipped cane with AI guidance
4. **Smartphone app**: Uses camera + LiDAR for detection

**Evaluate:**
- Winner: Smartphone app
  - Pros: No new hardware, accessible, affordable, always improving (software updates)
  - Cons: Requires holding phone, battery life
- Technical: Computer vision (obstacle detection), GPS + maps (navigation), ML (improving over time)
- Business: Freemium (free basic, paid premium with indoor navigation)

**Summarize:**
- Product: "PathVision" - AI-powered navigation app for blind users
- Features: Real-time obstacle detection, voice navigation, landmark identification
- Metrics: DAU, % of walks without incidents, NPS from blind community
- Roadmap: V1 outdoor navigation, V2 indoor (malls, airports), V3 object identification

**Time Allocation:**
- Comprehend: 3 min
- Identify + Report: 5 min
- Cut: 2 min
- List: 8 min
- Evaluate: 12 min
- Summarize: 5 min
- **Total: 35 min**

---

#### 2. Metrics & Analytics (Execution)

**What's Being Evaluated:**
- Data-driven decision making
- Metric selection and definition
- A/B testing knowledge
- Business acumen
- Trade-off evaluation

**Framework: GAME**

```
G - Goals
    ↓ Business and user objectives

A - Actions
    ↓ User behaviors that drive goals

M - Metrics
    ↓ How to measure success

E - Evaluation
    ↓ A/B testing and analysis
```

**Key Metric Types:**

**North Star Metric:**
- Single metric that best captures core value
- Examples:
  - Airbnb: Nights booked
  - Spotify: Time spent listening
  - Slack: Messages sent by teams
  - Netflix: Hours watched per subscriber

**AARRR Pirate Metrics:**
- **Acquisition**: How do users find us? (Signups, installs)
- **Activation**: Do they have a great first experience? (% completing onboarding)
- **Retention**: Do they come back? (D1, D7, D30 retention)
- **Revenue**: How do we monetize? (Conversion rate, ARPU)
- **Referral**: Do they tell others? (Viral coefficient, NPS)

**Example Question:**
"How would you measure success for Instagram Reels?"

**Strong Answer:**

**Goals:**
- Business: Compete with TikTok, increase engagement, retain users
- User: Discover entertaining short videos, express creativity

**Actions:**
- Watch Reels
- Create Reels
- Engage (like, comment, share, save)
- Follow creators
- Use audio/effects

**Metrics:**

**North Star:** Daily time spent watching Reels

**Acquisition:**
- % of Instagram users who discover Reels
- Reels tab impressions
- First Reel watch rate

**Activation:**
- % of users who watch >3 Reels in first session
- % of users who watch Reels again within 7 days

**Engagement:**
- Daily/Monthly Active Reel Watchers
- Reels watched per user per day
- Average watch time per Reel
- Engagement rate (likes, comments, shares per view)

**Creation:**
- % of users who create a Reel
- Reels created per creator per month
- Creation funnel drop-off

**Retention:**
- D1, D7, D30 Reel watcher retention
- % of Instagram DAU using Reels
- Reels vs Feed time split

**Revenue:**
- Ad impressions in Reels
- Ad revenue per 1000 Reels views (RPM)
- Creator monetization (bonuses, gifts)

**Counter-Metrics:**
- Feed engagement (did Reels cannibalize Feed?)
- Stories engagement (did it hurt Stories?)
- Time spent creating content (are we making it too complex?)
- Content quality (moderation removals, reports)

**Evaluation:**

**A/B Test Example:**
"Test: New AI recommendation algorithm"

- **Hypothesis**: Better recommendations increase watch time
- **Metric**: Time spent watching Reels per user per day
- **Segment**: All Reels users
- **Duration**: 2 weeks (need time to learn preferences)
- **Success criteria**: +5% watch time, no decrease in engagement rate
- **Risks**: Cold start problem (new users), filter bubble (less diversity)

**Analysis:**
- Treatment group: 52 min/day watching Reels (+8%)
- Control group: 48 min/day
- Engagement rate: Flat (not worse)
- Decision: Ship to 100%

---

#### 3. Technical (System Design & Architecture)

**What's Being Evaluated:**
- Technical depth
- System design thinking
- Scalability understanding
- API design knowledge
- Trade-off evaluation (CAP theorem, consistency vs availability)

**Framework: System Design Steps**

```
1. Requirements (Functional + Non-functional)
    ↓
2. Estimation (Scale, storage, bandwidth)
    ↓
3. API Design (Endpoints, authentication)
    ↓
4. High-Level Architecture (Components, data flow)
    ↓
5. Deep Dives (Database, caching, scaling)
    ↓
6. Trade-offs (CAP, consistency, cost)
```

**Example Question:**
"Design the backend for Twitter"

**Strong Answer:**

**1. Requirements:**

**Functional:**
- Post tweets (280 chars, images, videos)
- Follow users
- View timeline (tweets from followed users)
- Search tweets
- Like, retweet, reply

**Non-functional:**
- Scale: 500M users, 200M DAU
- Tweets: 400M per day
- Read heavy: 100:1 read:write ratio
- Availability: 99.9% uptime
- Latency: <200ms for timeline load

**2. Estimation:**

**Storage:**
- 400M tweets/day × 1KB avg = 400GB/day = 146TB/year
- With media (images/videos): ×10 = 1.46PB/year

**Bandwidth:**
- Write: 400M tweets/day = 4,630 writes/sec (peak: 20K/sec)
- Read: 100:1 ratio = 460K reads/sec (peak: 2M/sec)

**3. API Design:**

```
POST /api/tweets
{
  "user_id": "U123",
  "text": "Hello world",
  "media_ids": ["M456"]
}

GET /api/timeline?user_id=U123&cursor=xyz&limit=50
Returns: [
  {
    "tweet_id": "T789",
    "user": {...},
    "text": "...",
    "created_at": "...",
    "stats": {"likes": 42, "retweets": 10}
  }
]

POST /api/follow
{
  "follower_id": "U123",
  "followee_id": "U456"
}

GET /api/search?q=keyword&type=latest
```

**4. High-Level Architecture:**

```
                    [Load Balancer]
                           |
        +------------------+------------------+
        |                  |                  |
   [API Servers]   [Timeline Service]   [Tweet Service]
        |                  |                  |
        +------------------+------------------+
                           |
        +------------------+------------------+
        |                  |                  |
[PostgreSQL]          [Redis]           [Kafka]
(tweets, users)    (timelines,      (message queue)
                    hot data)
        |
   [S3/CDN]
(media files)
        |
[Elasticsearch]
(search index)
```

**Components:**

- **API Gateway**: Rate limiting, authentication, routing
- **Tweet Service**: Create/read tweets, validation
- **Timeline Service**: Generate user timelines (fan-out)
- **PostgreSQL**: Users, tweets, follows (sharded by user_id)
- **Redis**: Cached timelines, hot data, trending topics
- **Kafka**: Async processing (fan-out, notifications, analytics)
- **Elasticsearch**: Full-text search on tweets
- **S3 + CDN**: Images, videos, static assets

**5. Deep Dive: Timeline Generation**

**Problem**: User has 10K followers. When they tweet, update 10K timelines?

**Solution: Hybrid Fan-out**

**Fan-out on Write** (for most users):
1. User posts tweet
2. Tweet stored in database
3. Kafka message published
4. Timeline service reads from Kafka
5. For each follower: Insert tweet_id into Redis sorted set (timeline cache)
6. Next time follower opens app: Read from Redis (instant!)

**Fan-out on Read** (for celebrities):
1. Celebrity posts tweet (millions of followers)
2. Don't fan-out (too expensive)
3. Tweet stored in database
4. When follower opens timeline:
   - Get tweets from followed "normal" users (from Redis)
   - Query database for tweets from celebrities they follow
   - Merge and return

**Trade-off:**
- Fan-out on write: Fast reads, slow writes, high storage (timeline for each user)
- Fan-out on read: Slow reads, fast writes, low storage
- Hybrid: Best of both worlds

**6. Trade-offs:**

**CAP Theorem:**
- Consistency: All users see same data at same time
- Availability: System always responds
- Partition tolerance: Works despite network issues

**Twitter's Choice: AP (Availability + Partition Tolerance)**
- Prioritize availability (users can always post/read)
- Accept eventual consistency (new tweet might not appear immediately in all timelines)
- Okay if follower count is slightly off for a few seconds

**Database Sharding:**
- Shard by user_id (all user's data on same shard)
- Allows fast queries for user's tweets
- Challenge: Following users across shards requires cross-shard queries

**Caching Strategy:**
- Cache timelines in Redis (hot data, < 1 hour old)
- Cache user profiles (less frequent changes)
- Cache trending topics (computed periodically)
- TTL: Timelines 10 min, profiles 1 hour

---

#### 4. Behavioral (Leadership & Culture Fit)

**What's Being Evaluated:**
- Past experience and impact
- Leadership and influence
- Problem-solving approach
- Cultural alignment
- Self-awareness and learning

**Framework: STAR Method**

```
S - Situation (Context)
    ↓
T - Task (What needed to be done)
    ↓
A - Action (What YOU did)
    ↓
R - Result (Outcome + Learning)
```

**Time Allocation:**
- Situation: 10% (1 sentence)
- Task: 10% (1 sentence)
- Action: 60% (Most of your answer - what YOU specifically did)
- Result: 20% (Quantified outcome + learning)

**Common Question:**
"Tell me about a time you led a cross-functional team"

**Weak Answer:**
"At my last company, we needed to build a new feature. I worked with engineering and design. It was challenging but we shipped it. The feature was successful."

**Problems:**
- No specific context
- No clear task/goal
- Vague actions ("worked with")
- No quantified results
- No learning

**Strong Answer:**

**Situation:**
"At Spotify, our team's North Star metric (time spent listening) had plateaued for 3 months. Data showed users were spending 10+ minutes per day searching for music but not finding what they wanted."

**Task:**
"As PM, I needed to lead a cross-functional team (4 engineers, 2 designers, 1 data scientist) to improve music discovery and get our North Star metric growing again. Target: Increase time spent listening by 15% in Q2."

**Action:**

*"First, I aligned the team on the problem (not the solution):*
- Ran workshop with team and 5 users showing frustration with search
- Shared data: 40% of searches resulted in user giving up
- Got buy-in: Everyone agreed this was the top priority

*Second, I facilitated ideation with constraints:*
- Engineers: Must work with existing search infrastructure
- Design: Must fit in current app layout
- Data: Must be measurable from day 1

*Third, we prototyped 3 solutions:*
1. Better search autocomplete (engineering-led)
2. AI-powered 'Discover' tab (data science-led)
3. Mood-based playlists (design-led)

*Fourth, I made the call:*
- After user testing all 3, AI Discover had highest engagement
- Had to disagree with engineering lead who wanted autocomplete (less risky)
- Presented data to VP: AI Discover would take 6 weeks but had 3x impact potential
- Got approval and budget for 2 additional ML engineers

*Fifth, I unblocked the team:*
- Negotiated with legal for AI model approval
- Got data access from 3 other teams (required 6 cross-team meetings)
- Ran weekly demos with stakeholders (kept execs informed, prevented surprises)
- Cut scope on edge cases to ship on time (documented for V2)"

**Result:**

"We shipped AI Discover on time (6 weeks). Results after 4 weeks:
- Time spent listening: +22% (beat our 15% goal)
- User satisfaction (NPS): +18 points
- 60% of DAU used Discover daily
- Feature won company 'Innovation of the Quarter' award

**Learning:**
- Leading cross-functional teams requires: Clear goal, respect expertise, make tough calls
- Disagreeing with senior engineers was scary but data made it easier
- Unblocking (legal, data access) is 50% of PM job - plan for it
- Cutting scope is okay if you ship the core value"

**Why This Answer Works:**
- Specific context and metrics
- Clear leadership actions (aligned, facilitated, decided, unblocked)
- Showed influence without authority (negotiated with legal, other teams)
- Quantified results (22%, +18 NPS)
- Demonstrated learning and self-awareness

---

### Company-Specific Frameworks

#### Google: L6-L8 PM Preparation

**Evaluation Criteria (Googleyness):**
- **Cognitive ability**: Structured problem-solving, learning agility
- **Leadership**: Leading without authority, mentorship, team building
- **Googleyness**: Collaboration, humility, comfort with ambiguity
- **Role-related knowledge**: Product expertise, technical depth, user empathy

**Interview Loop (5-6 rounds):**
1. Product Design (45 min): "Improve Google Maps for tourists"
2. Analytical (45 min): "How would you measure success for Gmail?"
3. Technical (45 min): "Design the backend for Google Drive real-time collaboration"
4. Strategy (45 min): "Google wants to enter fintech. What product would you build?"
5. Leadership/Googleyness (45 min): Behavioral questions (STAR method)
6. Hiring Committee Review: No immediate decision, data-driven evaluation

**Key Principles:**

**User-First:**
- Every answer starts with user problem
- Consider 1B+ global users
- Think about accessibility and inclusion

**10x Thinking:**
- Don't just improve 10%, improve 10x
- "What would be possible if we removed all constraints?"
- Moonshot thinking (ambitious long-term vision)

**Data-Driven:**
- Quantify everything
- A/B test methodology
- Metrics for every decision

**Technical Depth:**
- Understand system architecture
- APIs and integrations
- ML/AI capabilities (Google's strength)

**Googleyness:**
- Collaboration over competition
- Humility and learning mindset
- "How might we..." vs "I think..."

**Example Googleyness Question:**
"Tell me about a time you were wrong"

**Strong Answer:**
"At my previous company, I pushed for a feature I was convinced would increase retention. I had user interviews supporting it. My engineering lead had concerns about technical complexity, but I insisted. We built it over 6 weeks. Result: Retention flat, no impact. I was wrong. Learning: (1) I didn't test the hypothesis first (should have built prototype), (2) I dismissed engineering concerns (complexity matters), (3) User interviews aren't enough (need behavioral data). Now I always start with smallest testable hypothesis and deeply respect technical constraints. This failure made me a better PM."

---

#### Amazon: Senior PM to VP Preparation

**Evaluation Criteria (14 Leadership Principles):**

1. **Customer Obsession**: Start with customer, work backwards
2. **Ownership**: Act on behalf of entire company
3. **Invent and Simplify**: Expect innovation from team
4. **Are Right, A Lot**: Strong judgment, seek diverse perspectives
5. **Learn and Be Curious**: Never done learning
6. **Hire and Develop the Best**: Raise performance bar
7. **Insist on the Highest Standards**: High standards for deliverables
8. **Think Big**: Bold direction inspires results
9. **Bias for Action**: Speed matters in business
10. **Frugality**: Accomplish more with less
11. **Earn Trust**: Listen attentively, speak candidly
12. **Dive Deep**: Operate at all levels, stay connected to details
13. **Have Backbone; Disagree and Commit**: Challenge decisions, commit wholly once decided
14. **Deliver Results**: Focus on key inputs, deliver with right quality

**Interview Loop (5-6 rounds):**
- Each interviewer focuses on 2-3 leadership principles
- Deep dive on past product work (PRFAQ, case study)
- Expect 2-3 STAR stories per principle
- Bar Raiser round (independent evaluator)

**Working Backwards (PRFAQ):**

Amazon's product development starts with a Press Release:

```
FOR IMMEDIATE RELEASE

Amazon Announces [Product Name]

SEATTLE, WA - [Date] - Amazon today introduced [Product], a new service that [one sentence value prop].

PROBLEM
Customers today struggle with [specific problem]. [Describe pain points and current solutions' shortcomings.]

SOLUTION
[Product] solves this by [how it works]. Customers can now [key benefits and use cases].

"[Product] is a game-changer for [customer segment]," said [Name], VP of [Division]. "[Vision statement about long-term impact]."

CUSTOMER QUOTE
"Before [Product], I had to [painful process]. Now, [how it's better]," said [Customer Name], [customer type].

HOW IT WORKS
1. [Step 1]
2. [Step 2]
3. [Step 3]

AVAILABILITY
[Product] is available today at [where/how to access] starting at [price].

For more information, visit [URL].

---

FREQUENTLY ASKED QUESTIONS

Q: Why did you build this?
A: [Strategic rationale, market opportunity, customer pain]

Q: How is this different from [competitor]?
A: [Unique value proposition, differentiation]

Q: What about [edge case concern]?
A: [How you'll handle it]

Q: What's the long-term vision?
A: [Roadmap, future expansion]

Q: How do you make money?
A: [Business model, pricing]

Q: What are the risks?
A: [Honest assessment of challenges]
```

**Example Interview Questions:**

**Customer Obsession:**
"Tell me about a time you built something customers didn't initially want but needed"

**Ownership:**
"Tell me about a time you went above and beyond your role to deliver results"

**Disagree and Commit:**
"Tell me about a time you strongly disagreed with a decision but committed fully afterward"

**Dive Deep:**
"Walk me through the most complex technical problem you've solved. What were the details?"

**Tips:**
- Have 2-3 stories per leadership principle (28-42 stories total)
- Use STAR method religiously
- Quantify results (revenue, metrics, efficiency gains)
- Show ownership ("I did" not "we did")
- Be specific (dates, numbers, names)
- Prepare for deep follow-up questions

---

#### Microsoft: Senior PM to Partner PM Preparation

**Evaluation Criteria:**
- **Growth Mindset**: Learn-it-all vs know-it-all mentality
- **Customer Obsession**: Deep empathy for customers
- **Diversity & Inclusion**: Diverse teams drive innovation
- **One Microsoft**: Cross-product collaboration

**Three Core Competencies:**
1. **Create Clarity**: Bring clarity to complex situations
2. **Generate Energy**: Inspire teams and customers
3. **Deliver Success**: Ship products that matter

**Interview Loop (4-5 rounds):**
1. Product Design & Strategy (60 min)
2. Technical & Architecture (60 min)
3. Leadership & Collaboration (60 min)
4. As-Appropriate (AA): Final round with senior leader (if you're doing well)

**Key Themes:**

**Growth Mindset (Satya's Culture):**
- Learn from failures
- Seek feedback
- Adapt to new information
- "What did you learn?" is the most important question

**Customer Empathy:**
- Understand customer context deeply
- B2B/enterprise focus (Microsoft's strength)
- Accessibility and inclusion

**Collaboration:**
- Work across product teams (Office, Azure, Windows, etc.)
- Partner ecosystem (ISVs, consultants)
- Open source and standards

**Example Questions:**

**Growth Mindset:**
"Tell me about a time you had to change your mind based on new data"

"Tell me about a failure and what you learned"

**Customer Obsession:**
"Tell me about how you gather customer insights"

"Describe a time you advocated for a customer against internal pressure"

**Collaboration:**
"Tell me about a time you worked across multiple product teams"

"Tell me about a conflict with a partner and how you resolved it"

**Tips:**
- Emphasize learning and growth in every story
- Show empathy for customers (especially enterprise)
- Think about accessibility (Microsoft is a leader here)
- Demonstrate cross-product thinking (Office + Azure + Teams)
- Understand hybrid cloud, AI Copilot strategy

---

#### OpenAI: PM to Product Lead Preparation

**Mission Alignment:**
"Ensure that artificial general intelligence (AGI) benefits all of humanity"

**Evaluation Criteria:**
- **AI/ML Product Expertise**: Deep understanding of LLMs, safety, capabilities
- **Responsible AI**: Safety, ethics, alignment considerations
- **Developer Focus**: API-first thinking, platform strategy
- **Mission Alignment**: Commitment to beneficial AGI

**Interview Loop (4-5 rounds):**
1. Product Design: AI product design (60 min)
2. Technical: LLM systems, APIs, ML infrastructure (60 min)
3. Strategy: AI market, competitive landscape, safety trade-offs (45 min)
4. Mission & Values: AI safety, ethics, long-term impact (45 min)
5. Cross-functional: Working with researchers and engineers (45 min)

**Required Knowledge:**

**LLM Fundamentals:**
- GPT architecture (transformer, attention, parameters)
- Training process (pre-training, fine-tuning, RLHF)
- Capabilities and limitations
- Prompt engineering
- Context windows and tokens

**Product Portfolio:**
- **ChatGPT**: Consumer product, free/Plus ($20/mo), Enterprise
- **API**: Developers pay per token, rate limits, models (GPT-4, GPT-3.5)
- **Plugins**: Extend ChatGPT with external data/actions
- **GPT Store**: Marketplace for custom GPTs
- **DALL-E**: Image generation

**Safety & Alignment:**
- Red teaming (adversarial testing)
- Constitutional AI principles
- Bias and fairness testing
- Misuse prevention (content policy, usage policy)
- Iterative deployment (gradual release with monitoring)

**Example Questions:**

**Product Design:**
"Design a new product using GPT-4 for education"

**Strong Answer:**
- Identify user: High school students struggling with math
- Problem: One-on-one tutoring is expensive, not scalable
- Solution: AI tutor that adapts to student's level, explains step-by-step
- Safety: Prevent cheating (don't give direct answers), age-appropriate content
- Metrics: Time spent learning, test score improvements, retention

**Responsible AI:**
"A developer is using our API to generate misinformation. What do you do?"

**Strong Answer:**
- Immediate: Suspend account, investigate usage patterns
- Short-term: Improve content policy, add monitoring for misuse
- Long-term: Build safety into model (Constitutional AI), rate of false info generation
- Trade-off: Balance innovation (open API) with safety (prevent misuse)
- Communication: Transparent about why we took action

**Strategy:**
"How would you compete with Google's Gemini?"

**Strong Answer:**
- OpenAI strengths: First mover (ChatGPT brand), API ecosystem, best models
- Google strengths: Distribution (Search, Gmail, YouTube), data, compute
- Strategy: Double down on API/platform, grow developer ecosystem, enterprise focus
- Differentiation: Best-in-class models, reliability, safety
- Partnership: Integrate with Microsoft (Office, Azure)

**Tips:**
- Demonstrate deep AI/ML knowledge (expected for OpenAI)
- Show thoughtfulness about safety and ethics
- Understand developer needs (API is core product)
- Think about long-term AGI implications
- Show passion for AI's potential to help humanity
- Be honest about risks and limitations

---

#### Anthropic: PM to Product Lead Preparation

**Mission:**
"Build reliable, interpretable, and steerable AI systems"

**Core Values:**
- **Safety First**: AI alignment and safety research foundational
- **Long-term Thinking**: Building for beneficial AGI future
- **Scientific Rigor**: Research-driven product development
- **Responsible Scaling**: Careful, iterative deployment
- **Transparency**: Explaining AI behavior and decisions

**Evaluation Criteria:**
- **AI Safety Expertise**: Constitutional AI, alignment, interpretability
- **Research Collaboration**: Working with AI safety researchers
- **Enterprise Focus**: Security, compliance, reliability for enterprises
- **Responsible Product**: Balancing capability with safety

**Interview Loop (4-5 rounds):**
1. Product Design: AI product design with safety considerations (60 min)
2. Technical: LLMs, Constitutional AI, safety techniques (60 min)
3. Research Collaboration: Working with research team (45 min)
4. Strategy: Responsible AI, market positioning, enterprise (45 min)
5. Values Alignment: Safety, reliability, interpretability (45 min)

**Required Knowledge:**

**Claude Product Family:**
- **Claude 3**: Haiku (fast, cheap), Sonnet (balanced), Opus (most capable)
- **Key features**: 200K context window, vision, low hallucination rate
- **Use cases**: Research, coding, writing, analysis, customer support

**Constitutional AI:**
- AI trained with explicit principles (constitution)
- Self-critique and revision process
- Red teaming and adversarial testing
- RLHF from AI feedback (not just human)
- Harmlessness and helpfulness as core objectives

**Differentiation vs OpenAI:**
- **Longer context**: 200K tokens (vs GPT-4's 128K)
- **More reliable**: Lower hallucination rate, more predictable
- **More steerable**: Better instruction following
- **More interpretable**: Explains reasoning better
- **Enterprise-first**: Focus on B2B, compliance, security
- **Research-driven**: Safety research informs product

**Example Questions:**

**Product Design:**
"Design a feature to make Claude more interpretable to users"

**Strong Answer:**
- Problem: Users don't understand why Claude gives certain answers
- User: Enterprise customers (legal, healthcare, finance) need explainability
- Solution: "Show reasoning" feature - Claude explains its thinking step-by-step
- Technical: Prompt Claude to output reasoning chain, show in UI
- Safety: Ensure reasoning is accurate (not post-hoc rationalization)
- Metrics: User trust (survey), feature usage, reduction in "I don't understand" feedback

**Safety & Responsibility:**
"How would you measure Claude's safety over time?"

**Strong Answer:**

**Proactive Metrics:**
- Red team success rate (% of attacks that breach policy)
- Harmful content generation rate (per 10K queries)
- Bias metrics (gender, race, religion across response types)
- Hallucination rate (factual accuracy on benchmarks)

**Reactive Metrics:**
- User reports of harmful content
- Policy violations detected
- Appeals and corrections

**Longitudinal:**
- Track metrics across model versions (Haiku, Sonnet, Opus)
- Compare to competitors (OpenAI, Google)
- External audits (AI safety orgs)

**Trade-off:**
- More capable models might be less safe (need to measure both)
- Goal: Improve both capability AND safety together

**Strategy:**
"An enterprise customer wants to use Claude for high-stakes medical diagnoses. How do you approach this?"

**Strong Answer:**

**Assess Risk:**
- Medical diagnosis is high-stakes (errors harm patients)
- Requires medical expertise (Claude is not a doctor)
- Liability concerns (who's responsible if wrong?)

**Approach:**

**Option 1: Say No**
- Pros: Avoid risk, maintain trust, prevent harm
- Cons: Miss revenue opportunity, customer finds alternative

**Option 2: Say Yes with Guardrails**
- Use case: Clinical decision support (helps doctors, not replaces)
- Requirements: Doctor always makes final decision, Claude shows sources
- Safety: Extensive testing on medical benchmarks, red teaming by doctors
- Legal: Clear terms that Claude is a tool, not medical device
- Monitoring: Track accuracy, user satisfaction, adverse events
- Transparency: Explain limitations clearly to users

**Recommendation: Option 2 with rigorous guardrails**
- Build trust by being responsible
- Learn from real-world usage (improve model)
- Expand to other high-stakes domains (legal, finance)

**Communication:**
- Internal: "We enable high-stakes use cases with safety first"
- Customer: "Claude assists doctors, never replaces clinical judgment"
- Public: "Our responsible scaling policy ensures safety"

**Tips:**
- Show deep understanding of AI safety (Anthropic's differentiator)
- Demonstrate enterprise thinking (compliance, security, reliability)
- Know Constitutional AI methodology (read the paper!)
- Understand research process (PMs work closely with researchers)
- Be thoughtful about high-stakes use cases
- Show long-term thinking (AGI alignment, not just next quarter)

---

## Practice Questions by Type

### Product Design Questions

**Consumer Products:**
1. Design a product for people who want to learn cooking
2. Improve YouTube for creators
3. Design a fitness app for busy professionals
4. Create a product to reduce food waste
5. Design a dating app for introverts
6. Improve Spotify's podcast discovery
7. Design a product for remote team building
8. Create a budgeting app for Gen Z
9. Design a product to help people read more books
10. Improve Instagram's shopping experience

**B2B/Enterprise:**
11. Design a product for small business inventory management
12. Create a tool for remote team collaboration
13. Design a CRM for real estate agents
14. Build a product for restaurant supply chain
15. Design an analytics platform for e-commerce
16. Create a hiring tool for tech recruiters
17. Design a customer support platform for SaaS companies
18. Build a project management tool for construction
19. Design a compliance tool for financial services
20. Create a product for enterprise API management

**Platform/Ecosystem:**
21. Design a developer platform for AI applications
22. Create a marketplace for freelance services
23. Design an app store for smart home devices
24. Build a platform for online education creators
25. Design a payment platform for gig workers

**Emerging Tech:**
26. Design a product using AR for home improvement
27. Create a VR product for virtual events
28. Design an AI product for legal research
29. Build a blockchain product for supply chain
30. Design a product using LLMs for customer support

---

### Metrics & Analytics Questions

**Consumer:**
1. How would you measure success for Instagram Reels?
2. What metrics would you track for Duolingo?
3. How do you measure success for Netflix's recommendation algorithm?
4. What's the North Star metric for Airbnb?
5. How would you measure success for TikTok's creator fund?

**B2B/SaaS:**
6. How would you measure success for Slack's Enterprise Grid?
7. What metrics matter for Salesforce?
8. How do you measure success for AWS Lambda?
9. What's the North Star metric for Stripe?
10. How would you measure Zoom's success?

**Marketplace:**
11. How would you measure success for Uber Eats?
12. What metrics matter for Etsy?
13. How do you measure success for DoorDash's DashPass?
14. What's the North Star metric for Fiverr?

**AI/ML Products:**
15. How would you measure success for ChatGPT?
16. What metrics matter for Claude API?
17. How do you measure success for Midjourney?
18. What's the North Star metric for GitHub Copilot?

**Diagnostic:**
19. Instagram Reels engagement dropped 10% last week. How do you investigate?
20. Slack's paid conversion rate dropped from 15% to 12%. What happened?
21. YouTube watch time is down 5% for the last month. Root cause?
22. Stripe's API error rate increased 2x. How do you diagnose?

---

### Technical Questions

**System Design:**
1. Design Twitter's backend
2. Design Instagram's photo storage system
3. Design Uber's dispatch system
4. Design Google Drive's real-time collaboration
5. Design Netflix's video streaming infrastructure
6. Design Zoom's video conferencing system
7. Design Slack's messaging infrastructure
8. Design Airbnb's booking system
9. Design Stripe's payment processing
10. Design YouTube's recommendation system

**API Design:**
11. Design a REST API for a todo list application
12. Design a GraphQL API for e-commerce
13. Design an API for real-time notifications
14. Design a WebSocket API for multiplayer games
15. Design an API for AI model inference (OpenAI-style)

**ML/AI Systems:**
16. Design a recommendation system for e-commerce
17. Design a fraud detection system for payments
18. Design a search ranking algorithm
19. Design an LLM-powered chatbot backend
20. Design a content moderation system using AI

**Data:**
21. Design a data pipeline for analytics
22. Design a real-time dashboard for operations
23. Design a data warehouse for business intelligence
24. Design an A/B testing platform
25. Design a metrics tracking system

---

### Behavioral Questions

**Leadership:**
1. Tell me about a time you led a cross-functional team
2. Describe a time you influenced a decision without authority
3. Tell me about a time you had to convince stakeholders to change direction
4. Tell me about a time you mentored a junior PM
5. Describe a time you built consensus among disagreeing parties

**Conflict:**
6. Tell me about a time you disagreed with your manager
7. Describe a conflict with an engineer and how you resolved it
8. Tell me about a time you had to say no to a stakeholder
9. Tell me about a time two team members had a conflict
10. Describe a time you had to deliver bad news to leadership

**Failure & Learning:**
11. Tell me about a product that failed. What did you learn?
12. Describe a time you made a wrong decision. What would you do differently?
13. Tell me about a time you missed a deadline
14. Tell me about your biggest professional mistake
15. Describe a time you received critical feedback. How did you respond?

**Innovation:**
16. Tell me about a time you solved a complex problem
17. Describe the most innovative product you've built
18. Tell me about a time you had to make a decision with incomplete information
19. Tell me about a time you took a calculated risk
20. Describe a time you challenged the status quo

**Customer Focus:**
21. Tell me about a time you advocated for the customer against internal pressure
22. Describe how you gather customer insights
23. Tell me about a time customer feedback changed your roadmap
24. Tell me about a time you had to balance user needs with business goals
25. Describe a time you learned something surprising from a customer

**Execution:**
26. Tell me about a time you shipped a product under tight deadlines
27. Describe how you prioritize a backlog
28. Tell me about a time you had to cut scope to ship on time
29. Tell me about a time you over-delivered on a goal
30. Describe a time you managed multiple projects simultaneously

---

## References

See `/references/` folder for detailed guides:
- `frameworks-quicksheet.md` — быстрые шпаргалки CIRCLES/GAME/STAR/System Design
- `company-interview-focus.md` — ожидания топ-компаний (Google/Amazon/Microsoft/Meta/AI)
- `interview-frameworks.md` — детальные описания интервью фреймворков
- `star-stories-template.md` — примеры оформления историй STAR
- `mock-interview-guide.md` — как проводить эффективные моки

## Assets

See `/assets/` folder for practical materials:
- `mock-interview-script.md` — сценарий мок-интервью и чек-листы обратной связи
- `star-story-template.md` — формат для упаковки историй с цифрами
- `interview-day-checklist.md` — подготовка и контрольный список дня интервью
- `interview-prep-roadmap.md` — поэтапный план подготовки (6 недель)

## Подробные плейбуки (3 итерации)
### Итерация 1 — Диагностика (1–2 часа)
- Целевые компании/уровень/роль; требования (PM/Sr/Staff/Lead/CPO).
- Оценка текущих навыков по трекам: Product Sense, Execution/Analytics, Technical/System Design, Behavioral/Leadership.
- Собери 15–20 STAR историй (разные компетенции), целевые метрики/примеры.
- Артефакт: стартовый план подготовки + gap-анализ, список историй/кейсов.
### Итерация 2 — Практика (2–6 часов, циклы)
- Симуляции по трекам (CIRCLES/GAME/STAR/System Design steps); тайминг и запись.
- Фиксация сильных/слабых сторон, пробелов (метрики, структура, trade-offs, коммуникация).
- Обновление историй, добавление цифр/результатов, усиление конкретики.
- Артефакт: обновлённые ответы/заметки, план улучшений, чек-лист фреймворков.
### Итерация 3 — Шлифовка (1–2 часа)
- Финальные правки историй/кейсов; подготовка вопросов интервьюерам.
- Подготовка дня интервью: логистика, энергия, материалы, резервные ответы.
- Контрольный обзор: скорость/структура/ясность, метрики, уверенность.
- Артефакт: финальный конспект, интервью-day checklist, изменения vs прошлой версии.

## Метрики и качество
- Структура ответа (CIRCLES/GAME/STAR/System Design) — держится ли рамка.
- Конкретика: цифры, метрики, trade-offs, влияние на бизнес/пользователей.
- Ясность/сжатость/логичность, управление временем (30–45 мин сессия).
- Поведение: лидерство, сотрудничество, работа с конфликтами и фидбеком.

## Входы (собери до старта)
- Целевые компании/уровень, описание требований/компетенций.
- Истории/кейсы, метрики/цифры, win/learn моменты.
- Доступное время/слоты для практики, партнёры по мокам.

## Выходы (обязательно зафиксировать)
- Обновлённый список историй (STAR) и кейсов с цифрами.
- Разбор симуляций, чек-лист ошибок и план улучшений.
- Финальный день-интервью план, вопросы интервьюерам, TODO с датами.

## Источники данных и инструменты
- Открытые гайды компаний, примеры вопросов, свои резюме/кейсы.
- Claude Agent SDK: Task (генерация вопросов/разбор ответов), Write (логи сессий).
- Шаблоны из assets/references: mock scripts, STAR шаблон, day checklist.

## Red Flags (осторожно)
- Нет цифр/метрик в историях, нет альтернатив/рисков в ответах.
- Ответы без структуры/тайминга; не отвечают на вопрос пользователя/интервьюера.
- Нет вопросов к интервьюеру; нет плана дня интервью/логистики.

---

## Getting Started

**Week 1-2: Learn Frameworks**
1. Study CIRCLES (product design)
2. Study GAME (metrics)
3. Study System Design approach (technical)
4. Study STAR method (behavioral)
5. Write down 20 STAR stories from your experience

**Week 3-4: Practice**
1. Do 20 product design questions (timed, 35 min each)
2. Do 20 analytical questions
3. Do 10 technical questions
4. Do 3 full mock interviews

**Week 5-6: Company-Specific Prep**
1. Deep dive on target company (products, culture, news)
2. Practice company-specific questions
3. Do 2-3 full mock interview loops (4-5 hours)
4. Prepare thoughtful questions for interviewers
5. Final review of your STAR stories

**Ready to Practice?**

Let me know which type of interview you'd like to practice:
- 🎯 Product Design (CIRCLES)
- 📊 Metrics & Analytics (GAME)
- 🔧 Technical (System Design)
- 🗣️ Behavioral (STAR)
- 🏢 Company-specific prep

Or just ask any questions about interview preparation!

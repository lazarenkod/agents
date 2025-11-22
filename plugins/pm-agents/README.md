# PM Agents Plugin

Comprehensive plugin для Project Managers, Delivery Managers и Technical Project Managers с senior-level expertise.

## Overview

Этот плагин предоставляет специализированных AI агентов, skills и commands для управления сложными техническими проектами на уровне senior PM ролей в AWS, Azure, Google Cloud, OpenAI, Claude и Microsoft.

**Key Features:**
- 🎯 3 специализированных агента (PM, DM, TPM)
- 📚 10+ expert-level skills
- ⚙️ 3+ automation commands
- 🌍 Все артефакты на русском языке
- 📊 Production-ready templates и frameworks

## Agents

### 1. Project Manager (`project-manager`)
Senior-level стратегический PM для управления комплексными инициативами.

**Expertise:**
- Strategic planning & execution
- Stakeholder management
- Risk management & mitigation
- OKR/KPI framework design
- Cross-functional coordination
- Budget & resource management
- Cloud platform experience (AWS/Azure/GCP)
- AI/ML product management

**Model:** Sonnet (complex reasoning)

**Use когда:**
- Planning complex multi-team projects
- Quarterly/annual strategic planning
- Executive stakeholder alignment
- Portfolio prioritization
- High-risk initiative management

### 2. Delivery Manager (`delivery-manager`)
Expert в operational excellence и high-velocity delivery.

**Expertise:**
- CI/CD pipeline optimization
- DevOps & SRE collaboration
- Agile/Lean process improvement
- DORA metrics implementation
- Quality & testing strategy
- Team performance optimization
- Incident management
- Scaling delivery organizations

**Model:** Sonnet (process optimization)

**Use когда:**
- Improving delivery velocity
- Implementing CI/CD best practices
- Scaling team operations
- Quality improvement initiatives
- Process optimization

### 3. Technical Project Manager (`technical-project-manager`)
Hybrid technical leader с engineering background.

**Expertise:**
- System architecture & design
- Cloud infrastructure (AWS/Azure/GCP)
- Data engineering & ML platforms
- Technical estimation & planning
- Architecture Decision Records (ADRs)
- DevOps & SRE leadership
- AI/ML technical management
- Security & compliance

**Model:** Sonnet (technical depth)

**Use когда:**
- Infrastructure migrations
- Platform engineering projects
- Technical debt initiatives
- ML/AI infrastructure
- Architecture decisions

## Skills

### Project Management Skills

**strategic-planning**
- Quarterly/annual roadmapping
- OKR framework
- Portfolio prioritization (RICE, WSJF)
- Business case development
- 📄 Template: `strategic-plan-template.md`

**stakeholder-management**
- Power/Interest mapping
- Influence strategies
- Executive communication
- Conflict resolution
- 📄 Templates: stakeholder profiles, communication plans

**risk-management**
- Risk identification & assessment
- Mitigation planning
- RAID logs
- Crisis management
- 📄 Template: `risk-register-template.md`

**okr-framework**
- Goal setting methodology
- OKR cascading
- Progress tracking
- Quarterly planning
- 📄 Templates: OKR templates, tracking sheets

**architecture-decision-records**
- ADR framework
- Decision documentation
- Trade-off analysis
- Technical governance
- 📄 Templates: ADR templates, examples

### Delivery Management Skills

**dora-metrics**
- Deployment frequency
- Lead time for changes
- MTTR optimization
- Change failure rate
- 📄 Dashboards и improvement plans

**incident-management**
- Incident response
- Post-mortem framework
- On-call practices
- Crisis communication
- 📄 Templates: incident reports, post-mortems

### Technical PM Skills

**mlops-practices**
- ML lifecycle management
- Model deployment pipelines
- LLM integration (OpenAI, Claude)
- RAG architecture
- Monitoring & governance
- 📄 Project planning templates

## Commands

### `/project-kickoff`
Comprehensive project initiation workflow.

**Creates:**
- Project charter
- Stakeholder map
- Risk register
- RACI matrix
- Initial project plan
- Communication plan

**Usage:**
```bash
/project-kickoff
# Answer interactive questions
# All documents created in projects/{name}/
```

### `/quarterly-planning`
Quarterly OKR planning и roadmapping.

**Creates:**
- Quarterly OKRs
- Initiative roadmap
- Resource allocation plan
- Dependency map
- Risk assessment
- Success metrics dashboard

**Usage:**
```bash
/quarterly-planning
# Guide through planning process
# Outputs in planning/Q[n]-[year]/
```

### `/status-report`
Generate professional status reports.

**Types:**
- Weekly team updates
- Executive summaries (1-pager)
- Monthly business reviews
- Quarterly reports

**Usage:**
```bash
/status-report
# Select report type
# Answer questions
# Get formatted markdown report
```

## Installation

```bash
# Install plugin
claude-code plugin install pm-agents

# Verify installation
claude-code plugin list
```

## Usage Examples

### Starting a New Project

```bash
# 1. Kickoff project
/project-kickoff
> Project name: AI Platform Migration
> Sponsor: CTO
> Timeline: 6 months
...

# 2. Agent automatically creates all artifacts
# Review: projects/ai-platform-migration/

# 3. Use project-manager agent for ongoing management
```

### Quarterly Planning

```bash
# Use quarterly-planning command
/quarterly-planning
> Quarter: Q2 2024
> Team: Platform Engineering
...

# Agent creates comprehensive plan
# Review: planning/Q2-2024/
```

### Improving Delivery Metrics

```bash
# Activate delivery-manager agent
# Agent uses dora-metrics skill
# Creates baseline и improvement plan
```

## File Structure

```
plugins/pm-agents/
├── README.md
├── agents/
│   ├── project-manager.md
│   ├── delivery-manager.md
│   └── technical-project-manager.md
├── skills/
│   ├── strategic-planning/
│   │   ├── SKILL.md
│   │   └── assets/
│   ├── stakeholder-management/
│   ├── risk-management/
│   ├── okr-framework/
│   ├── dora-metrics/
│   ├── architecture-decision-records/
│   ├── mlops-practices/
│   └── incident-management/
└── commands/
    ├── project-kickoff.md
    ├── quarterly-planning.md
    └── status-report.md
```

## Key Benefits

✅ **Senior-Level Expertise**: Capabilities от PM ролей в FAANG компаниях
✅ **Russian Language**: Все артефакты и templates на русском
✅ **Production-Ready**: Tested frameworks и best practices
✅ **Comprehensive**: Coverage всех PM domains
✅ **Cloud-Native**: AWS, Azure, GCP experience built-in
✅ **AI/ML Focus**: Специализация для AI/ML проектов
✅ **Automation**: Commands для common workflows

## Target Users

- **Senior Project Managers** managing complex technical initiatives
- **Delivery Managers** optimizing team velocity
- **Technical PMs** leading infrastructure projects
- **Engineering Managers** needing PM support
- **Product Managers** working on technical products

## Version

**1.0.0** - Initial release

## Support

For issues or questions:
- Review skill documentation в `skills/*/SKILL.md`
- Check command usage в `commands/*.md`
- Review templates в `skills/*/assets/`

## License

Part of Claude Code Plugins Marketplace

# Claude Desktop Integration Guide

This guide explains how to use agents and skills from this marketplace in Claude Desktop application.

## Overview

**Two products, different architectures:**
- **Claude Code** (CLI) — uses plugins from `marketplace.json`
- **Claude Desktop** — uses MCP servers or Project-level prompts

## Option 1: Direct Prompts (Easiest)

### Steps:

1. **Create a Project in Claude Desktop**
   - Open Claude Desktop → Projects → Create Project
   - Name it (e.g., "Tech Content Creation")

2. **Add Agent as Custom Instructions**
   - Go to Project Settings → Custom Instructions
   - Copy agent content (skip YAML frontmatter):
     ```bash
     # Example: copy tech-content-writer agent
     sed '1,/^---$/d; /^---$/,/^$/d' plugins/tech-content-creator/agents/tech-content-writer.md | pbcopy
     ```
   - Paste into Custom Instructions field

3. **Add Skills as Project Knowledge**
   - In Project Knowledge section, click "Add Content"
   - Upload skill markdown files:
     - `plugins/tech-content-creator/skills/russian-content-creation/SKILL.md`
     - `plugins/tech-content-creator/skills/tech-trends-research/SKILL.md`
     - etc.
   - Upload reference files from `references/` and `assets/` folders

4. **Use in Conversations**
   - Start new chat in the project
   - Claude will use Custom Instructions + Knowledge automatically
   - Example prompt: "Write a technical article about AI trends in Russian"

### Example Workflow:

**For Stock Analysis:**
```bash
# 1. Create "Stock Analysis" Project in Claude Desktop

# 2. Copy equity-analyst agent as Custom Instructions:
cat plugins/stock-analysis/agents/equity-analyst.md

# 3. Add skills as Knowledge:
- plugins/stock-analysis/skills/fundamental-analysis/SKILL.md
- plugins/stock-analysis/skills/technical-analysis/SKILL.md
- plugins/stock-analysis/skills/portfolio-analysis/SKILL.md

# 4. Chat: "Analyze NVDA stock with technical and fundamental analysis"
```

---

## Option 2: MCP Server (Advanced)

Create an MCP server that exposes agents and skills as resources.

### Architecture:

```
Claude Desktop
    ↓ (MCP Protocol)
Agents MCP Server
    ↓
marketplace.json → agents, skills, commands
```

### Implementation:

**1. Create MCP Server:**

```typescript
// mcp-server/src/index.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import fs from 'fs/promises';
import path from 'path';

const server = new Server(
  {
    name: 'agents-marketplace',
    version: '1.0.0',
  },
  {
    capabilities: {
      resources: {},
      prompts: {},
    },
  }
);

// Load marketplace
const marketplace = JSON.parse(
  await fs.readFile('.claude-plugin/marketplace.json', 'utf-8')
);

// Expose agents as resources
server.setRequestHandler('resources/list', async () => {
  const resources = [];

  for (const plugin of marketplace.plugins) {
    for (const agentPath of plugin.agents || []) {
      const fullPath = path.join(plugin.source, agentPath);
      const content = await fs.readFile(fullPath, 'utf-8');

      resources.push({
        uri: `agent://${plugin.name}/${path.basename(agentPath, '.md')}`,
        name: `${plugin.name}/${path.basename(agentPath, '.md')}`,
        mimeType: 'text/markdown',
        description: extractDescription(content),
      });
    }
  }

  return { resources };
});

server.setRequestHandler('resources/read', async (request) => {
  const uri = request.params.uri;
  const match = uri.match(/agent:\/\/(.+?)\/(.+)/);

  if (match) {
    const [, pluginName, agentName] = match;
    const plugin = marketplace.plugins.find(p => p.name === pluginName);
    const agentPath = plugin.agents.find(a => a.includes(agentName));
    const content = await fs.readFile(
      path.join(plugin.source, agentPath),
      'utf-8'
    );

    return {
      contents: [{
        uri,
        mimeType: 'text/markdown',
        text: content,
      }],
    };
  }

  throw new Error('Resource not found');
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

**2. Configure Claude Desktop:**

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "agents-marketplace": {
      "command": "node",
      "args": ["/path/to/agents/mcp-server/dist/index.js"],
      "cwd": "/path/to/agents"
    }
  }
}
```

**3. Restart Claude Desktop**

Agents will appear in the MCP resources panel.

---

## Option 3: Export Individual Agents

Create standalone prompt files for quick copy-paste:

```bash
# Export script
mkdir -p exports/prompts

for agent in plugins/*/agents/*.md; do
  name=$(basename "$agent" .md)
  plugin=$(basename $(dirname $(dirname "$agent")))

  # Remove frontmatter, save as prompt
  sed '1,/^---$/d; /^---$/,/^$/d' "$agent" > "exports/prompts/${plugin}__${name}.md"
done
```

Then drag & drop into Claude Desktop chats as needed.

---

## Recommended Approach

**For most users:** Use **Option 1** (Direct Prompts)
- ✅ Simple, no setup required
- ✅ Works immediately
- ✅ Good for 1-3 agents per project
- ❌ Manual updates needed

**For power users:** Use **Option 2** (MCP Server)
- ✅ Dynamic access to all agents
- ✅ Auto-updates when agents change
- ✅ Can create custom tools/commands
- ❌ Requires technical setup

**For quick tests:** Use **Option 3** (Export)
- ✅ One-off usage
- ✅ Easy sharing
- ❌ No persistence

---

## Example: Tech Content Creation Project

### Setup:

**1. Create Project "Tech Writing"**

**2. Custom Instructions:**
```markdown
# Tech Content Writer

You are a senior technical content writer for high-tech companies...
[Full content of tech-content-writer.md agent]
```

**3. Project Knowledge:**
- Upload `russian-content-creation/SKILL.md`
- Upload `tech-trends-research/SKILL.md`
- Upload `enterprise-storytelling/SKILL.md`
- Upload assets: `habr-format.md`, `vc-ru-format.md`

**4. Usage:**
```
User: "Напиши статью о трендах GenAI для Habr"

Claude: [Uses Custom Instructions + Skills]
[Saves markdown with proper Russian typography]
```

---

## Tips

1. **Combine related agents** — put backend-architect + database-architect in one project
2. **Update Knowledge regularly** — when skills change, re-upload
3. **Use Projects for domains** — separate projects for different expertise areas
4. **Test prompts** — some agents may need slight adjustments for Desktop context
5. **Leverage API** — for automation, use Claude API with agent prompts

---

## Limitations

**Claude Desktop vs Claude Code differences:**
- No automatic command execution (slash commands)
- No file system tools (Read, Write, Edit)
- No background agents (Task tool)
- Knowledge is static (manual updates)

**Workarounds:**
- Use API for file operations
- Chain prompts manually instead of multi-agent workflows
- Keep skills as reference documents

---

## Next Steps

1. ✅ Choose integration option (1, 2, or 3)
2. ✅ Test with one agent first
3. ✅ Add skills incrementally
4. ✅ Measure quality vs Claude Code

For questions, see: https://docs.claude.com/desktop

#!/bin/bash

# Export agents and skills for Claude Desktop Projects
# Usage: ./scripts/export-for-claude-desktop.sh [plugin-name]

set -e

EXPORT_DIR="exports/claude-desktop"
mkdir -p "$EXPORT_DIR"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Exporting agents and skills for Claude Desktop...${NC}"

# Function to remove YAML frontmatter
remove_frontmatter() {
    local file=$1
    # Remove everything from first --- to second --- (inclusive)
    sed '1,/^---$/d; /^---$/,/^$/d' "$file"
}

# Export specific plugin or all
if [ -n "$1" ]; then
    PLUGINS="plugins/$1"
    if [ ! -d "$PLUGINS" ]; then
        echo "Error: Plugin $1 not found"
        exit 1
    fi
else
    PLUGINS="plugins/*"
fi

# Process each plugin
for plugin_dir in $PLUGINS; do
    if [ ! -d "$plugin_dir" ]; then
        continue
    fi

    plugin_name=$(basename "$plugin_dir")
    echo -e "\n${GREEN}Processing: $plugin_name${NC}"

    plugin_export_dir="$EXPORT_DIR/$plugin_name"
    mkdir -p "$plugin_export_dir"

    # Export agents
    if [ -d "$plugin_dir/agents" ]; then
        agents_dir="$plugin_export_dir/agents"
        mkdir -p "$agents_dir"

        for agent in "$plugin_dir"/agents/*.md; do
            if [ -f "$agent" ]; then
                agent_name=$(basename "$agent" .md)
                echo "  📝 Agent: $agent_name"
                remove_frontmatter "$agent" > "$agents_dir/${agent_name}.md"
            fi
        done
    fi

    # Export skills (keep frontmatter for reference)
    if [ -d "$plugin_dir/skills" ]; then
        skills_dir="$plugin_export_dir/skills"
        mkdir -p "$skills_dir"

        for skill in "$plugin_dir"/skills/*/SKILL.md; do
            if [ -f "$skill" ]; then
                skill_name=$(basename "$(dirname "$skill")")
                skill_export="$skills_dir/$skill_name"
                mkdir -p "$skill_export"

                echo "  📚 Skill: $skill_name"

                # Copy SKILL.md
                cp "$skill" "$skill_export/"

                # Copy assets if exist
                if [ -d "$(dirname "$skill")/assets" ]; then
                    cp -r "$(dirname "$skill")/assets" "$skill_export/"
                fi

                # Copy references if exist
                if [ -d "$(dirname "$skill")/references" ]; then
                    cp -r "$(dirname "$skill")/references" "$skill_export/"
                fi
            fi
        done
    fi

    # Create README for the plugin export
    cat > "$plugin_export_dir/README.md" << EOF
# $plugin_name - Claude Desktop Setup

## Quick Start

1. **Create Project in Claude Desktop**
   - Open Claude Desktop → Projects → Create Project
   - Name: "$plugin_name"

2. **Add Custom Instructions**
   - Copy content from one or more agent files in \`agents/\`
   - Paste into Project Settings → Custom Instructions

3. **Add Project Knowledge**
   - Upload skill files from \`skills/*/SKILL.md\`
   - Upload assets and references as needed

## Available Agents

EOF

    # List agents
    if [ -d "$agents_dir" ]; then
        for agent in "$agents_dir"/*.md; do
            if [ -f "$agent" ]; then
                agent_name=$(basename "$agent" .md)
                echo "- **$agent_name** - \`agents/${agent_name}.md\`" >> "$plugin_export_dir/README.md"
            fi
        done
    fi

    echo "" >> "$plugin_export_dir/README.md"
    echo "## Available Skills" >> "$plugin_export_dir/README.md"
    echo "" >> "$plugin_export_dir/README.md"

    # List skills
    if [ -d "$skills_dir" ]; then
        for skill_dir in "$skills_dir"/*; do
            if [ -d "$skill_dir" ]; then
                skill_name=$(basename "$skill_dir")
                echo "- **$skill_name** - \`skills/${skill_name}/SKILL.md\`" >> "$plugin_export_dir/README.md"
            fi
        done
    fi

    cat >> "$plugin_export_dir/README.md" << EOF

## Usage Example

\`\`\`
# In Claude Desktop chat:
User: [Ask questions related to $plugin_name domain]

Claude: [Uses Custom Instructions from agents + Knowledge from skills]
\`\`\`

## Updating

When agents or skills change in the marketplace:
1. Re-run export script: \`./scripts/export-for-claude-desktop.sh $plugin_name\`
2. Update Custom Instructions in Claude Desktop project
3. Re-upload changed skill files

---

Generated from: https://github.com/lazarenkod/agents
EOF

done

echo -e "\n${GREEN}✅ Export complete!${NC}"
echo -e "📁 Location: $EXPORT_DIR/"
echo ""
echo "Next steps:"
echo "1. Open Claude Desktop"
echo "2. Create a new Project"
echo "3. Follow instructions in exported README.md files"

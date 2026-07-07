# 03 - Explore Models & Create the Agent

## 1) [Optional] Explore models with GitHub Copilot Agent Mode

Open **GitHub Copilot Chat** in VS Code and switch to **Agent Mode**. Ask Copilot to recommend a model for your use case:

```text
I'm building a bilingual AI customer assistant for Savanna Bites restaurant in Nairobi. It needs to handle English, Swahili, and Sheng queries about menu items, pricing, and ordering. Which model would you recommend from the Foundry Toolkit?
```

Review the recommendations.

For this workshop we use **gpt-4.1-mini** via custom models — it balances quality, speed, and multilingual capability.

## 2) Create the agent in Agent Builder

<!-- TODO: Add screenshot of the Agent Builder creation flow -->

1. In Foundry Toolkit, go to **Developer Tools** → **+ Build** → **+ Create Agent** → **Open Agent Builder**.
1. Name the agent: `Biashara-Bot`
1. For the **Model** field, select `gpt-4.1-mini` 
1. In the top right, on the **Save to Foundry** button, click the drop down option and select **Save to Local.**

## 3) Quick baseline test

Before adding a system prompt or tools, send a message:

```text
Do you have chapati and beans? How much is it?
```

The agent gives a generic answer because it has no context about the restaurant. The next sections fix this.

Continue to [04-system-prompt.md](04-system-prompt.md).

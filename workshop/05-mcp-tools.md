# 05 - Connect MCP Tools

## 1) Check MCP configuration

Open `.vscode/mcp.json` and confirm the server entry points to:

```json
{
  "servers": {
    "biashara-bot-data-http": {
      "url": "http://127.0.0.1:8000/mcp",
      "type": "http"
    }
  },
  "inputs": []
}

```

In VS Code, navigate to the `.vscode/mcp.json` file and click **Start** above the `biashara-bot-data` server to launch it.

## 2) Enable tools in Agent Builder

1. Scroll to the **Tools** section of the Agent Builder. 
1. Click on the **+** icon, next to tools then select, **MCP Server > Could not find one? Browse more MCP Servers**
1. In the new tab, select **Custom** then navigate to **mcp.json** then select the edit button.
1. A new **mcp.json** file will be opened, paste the following code to your file:

```json
{
  "servers": {
    "biashara-bot-data-http": {
      "url": "http://127.0.0.1:8000/mcp",
      "type": "http"
    }
  },
  "inputs": []
}

```

## 4) Test with grounded queries

Now ask questions that require grounded data:

```text
What do you have for breakfast and how much does it cost?
```

```text
Mnatuma chakula CBD? Delivery ni how much?
```

```text
I want to order lunch for 15 people at my office. What are your catering options?
```

The agent should now return answers grounded in actual menu data and FAQ entries instead of guessing.

Continue to [06-evaluation.md](06-evaluation.md).

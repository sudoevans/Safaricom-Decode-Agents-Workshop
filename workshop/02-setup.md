# 02 - Setup

## 1) Confirm VS Code extensions

Open VS Code and install the following extensions are installed:

- [AI Toolkit](https://aka.ms/AIToolkit) (includes Microsoft Foundry)
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

## 2) Access to models

1. **TODO**
1. Open the **AI Toolkit** extension in the Activity Bar.
1. Go to **My resources > connected resources** in the pop-up select **add custom model**.
1. Add the resources from the resources tab.

## 4) Install Python dependencies

```bash
pip install -r requirements.txt
```

If needed, use `pip3` instead of `pip`.

## 5) Start the MCP server

```bash
python mcp-server/server.py
```

Keep this terminal running.

## 6) Verify data files

```bash
ls mcp-server/data/
```

Expected files:
- `business-faqs.json`
- `product-catalogue.json`

Continue to [03-model-agent.md](03-model-agent.md).

# 02 - Setup

## 1) Confirm VS Code extensions

Open VS Code and ensure the following extensions are installed:

- [Foundry Toolkit](https://aka.ms/AIToolkit)
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

## 2) Access to models

### If you are in an event
1. Head over to the event link: **link will be provided**
1. Follow the instructions to generate your API Key
1. Once you get your Event API keys, follow the next set of instructions below to add your models to Foundry Toolkit

### If you are doing the session at home with access to Microsoft Foundry.

> :pushpin: You need access to a Microsoft Foundry account either through an Azure subscription or an Azure Free Trial

1. Go to [Microsoft Foundry](https://ai.azure.com) and create a new project.
1. In the new project created, deploy a **gpt-4.1-mini** model.
1. In VS Code, navigate to **Foundry Toolkit > My resources > Microsoft Foundry resources > Set Default Project**

### If you want to run models locally with Foundry Local

> :pushpin: Foundry Local lets you run models on your own machine — no cloud account or API key needed.

1. Install Foundry Local following the [getting started guide](https://learn.microsoft.com/ai/foundry-local/get-started).
1. In your terminal, run `foundry local start` to start the local inference server.
1. In VS Code, open the **Foundry Toolkit** extension in the Activity Bar.
1. Go to **My resources > Local Models** — you'll see models available for local inference (e.g. `phi-4`).

## 3) Add models to Foundry Toolkit

### If you are in an event
1. Open the **Foundry Toolkit** extension in the Activity Bar.
1. Go to **My resources > connected resources**, hover on **Models** and click on the **+** sign. Select **Add Custom Model**.
1. **Endpoint URL.** Copy the **gpt-4.1-mini Endpoint** value from the event.link, paste it here, then click enter
1. **Model name.** Copy the **Model** value from the event.link, paste it here, then click enter
1. **Display model name.** Leave default model name as is, then click enter.
1. **API Key.** Copy the **Event API Key** value from the event.link, paste it here, then click enter
1. A pop up will appear on your right with the following title, **Model added successfully. Try the model in the playground.**

### If you are doing the session at home with access to Microsoft Foundry.
1. Open the **Foundry Toolkit** extension in the Activity Bar.
1. Go to **My resources > your Microsoft Foundry project > Models.**
1. In the models drop down, select **gpt-4.1-mini** model.

### If you are using Foundry Local
1. Open the **Foundry Toolkit** extension in the Activity Bar.
1. Go to **My resources > Local Models.**
1. Select a model (e.g. **phi-4**) — it will download if not already cached.
1. The model is ready to use in the playground and in your web app (no API key required).

## 4) Install Python dependencies

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

If needed, use `python3` instead of `python`.

## 5) Start the MCP server

```bash
python mcp-server/server.py
```

You should see output like:

```
Starting Biashara Agent MCP Data Server (HTTP)...
📡 MCP endpoint available at: http://127.0.0.1:8000/mcp
Tools available: search_business_faqs, get_product_catalogue
```

Keep this terminal running.

Continue to [03-model-agent.md](03-model-agent.md).

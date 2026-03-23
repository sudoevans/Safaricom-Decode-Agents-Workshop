# 06 - Evaluate Agent Responses

## 1) Manual evaluation

In the Agent Builder, switch to the **Evaluation** tab.

1. Select **+ Add an Empty Row** four times to create four test rows.
1. Enter the following **User Query** values:

| Row | User Query |
|-----|-----------|
| 1   | What do you have for breakfast and how much does it cost? |
| 2   | Mnatuma chakula CBD? Delivery ni ngapi? |
| 3   | Do you serve sushi? |
| 4   | I want to order lunch for 15 people at my office. What are your catering options? |

1. Select all rows and click **Run Response** (the play button icon).
1. Review each response. Check that:
   - Menu items and prices come from real data (not hallucinated)
   - Swahili queries get Swahili-appropriate responses
   - Items not on the menu are handled honestly
   - Catering constraints (48hr notice) are mentioned

## 2) AI-assisted evaluation

Use built-in evaluators to automatically score agent responses.

1. Create a new evaluation via the **Add Evaluation** button.
1. Select the following evaluators: `relevance`, `coherence`.
1. Select the `gpt-4.1-mini` model for the evaluator.
1. Select **Run Evaluation** → **Run Evaluation Only**.
1. Review the scores for each response.

> **Note:** The first time you run AI-assisted evaluations, the AI Toolkit will download and install required dependencies. This may take a moment.

## 3) Use GitHub Copilot for evaluator recommendations

Open **GitHub Copilot Chat** in Agent Mode and ask:

```text
What evaluators should I use for a bilingual restaurant assistant
that answers menu, pricing, delivery, and catering questions?
```

Copilot can recommend additional evaluators beyond relevance and coherence (e.g., groundedness, fluency) that you can add to future evaluation runs.

Continue to [07-export-code.md](07-export-code.md).

![Anthropic Claude API Key Guide](../docs/anthropic_api_key.png)

## What is the Claude API?

Anthropic's Claude API lets you integrate Claude's AI models (Haiku, Sonnet, Opus) into your own applications, scripts, or automation workflows. It is a separate platform from claude.ai (the web chat): the API is developer-oriented and requires its own billing setup.

---

## Prerequisites

Before you begin, make sure you have:

- A valid email address (or a Google / Microsoft account)
- A phone number for verification (required in some countries)
- A credit or debit card (international Visa or Mastercard recommended)
- At least **$5 USD** to purchase your first prepaid credits (mandatory to use the API)

---

## Step 1: Create Your Account on the Anthropic Console

1. Go to [platform.claude.com](https://platform.claude.com) (previously `console.anthropic.com` — both URLs work)
2. Click **"Sign up"** and register with your email/password or with Google
3. Verify your email address by clicking the link Anthropic sends you
4. Complete your profile:
   - First and last name
   - Organization name (you can use your own name for personal use)
   - Use case (chatbot, code assistant, analysis, etc.)

---

## Step 2: Add Billing Credits

> ⚠️ **Important:** Since 2025, Anthropic requires mandatory prepaid credits before you can generate or use any API Key in production. Without a balance, API calls will fail.

1. In the console, go to the left-side menu and select **Settings → Billing**
2. Click **"Add payment method"** and enter your card details
3. Then select **"Add credits"** and purchase at least **$5 USD**
4. Optionally, configure a monthly spending limit to avoid unexpected charges

The credits you purchase become a prepaid balance that is consumed as you use the API.

---

## Step 3: Create a New API Key

1. In the left-side menu, click **"API keys"** (or go directly to [platform.claude.com/settings/keys](https://platform.claude.com/settings/keys))
2. Click the **"Create Key"** button
3. Assign a descriptive name to your key (e.g., `Dev-Project`, `Production-App`)
4. Select the **Workspace** it will be associated with:
   - For personal projects: use the **Default** workspace
   - For teams: create separate workspaces per environment
5. Click **"Add"** or **"Create"**

---

## Step 4: Copy and Save the Key

> ⚠️ **CRITICAL!** The key is shown **only once**. Once the window is closed, Anthropic only stores a hashed version and you will never be able to see it again.

1. Copy the key immediately — it will have the format `sk-ant-api03-...`
2. Store it in a safe place (password manager, `.env` file, secrets vault)
3. If you lose it, simply revoke the lost key and create a new one

---

## Step 5: Use the API Key in Your Application

### Option A — Environment Variable (Recommended)

**macOS / Linux:**
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."
```

**Windows (CMD):**
```text
setx ANTHROPIC_API_KEY "sk-ant-api03-..."
```

### Option B — Python with the Official SDK

First, install the SDK:
```bash
pip install anthropic
```

Then use it in your code:
```python
import anthropic

client = anthropic.Anthropic()  # Automatically reads ANTHROPIC_API_KEY from the environment

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, how are you?"}]
)
print(message.content[0].text)
```

### Option C — Direct HTTP (cURL)

```bash
curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --data '{
    "model": "claude-sonnet-4-6",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

---

## Tier System and Rate Limits (2026)

Anthropic organizes API access into 4 tiers that upgrade automatically as your cumulative spending increases:

| Tier   | Required Deposit | RPM   | Max Monthly Spend |
|--------|-----------------|-------|-------------------|
| Tier 1 | $5 USD          | 50    | $100              |
| Tier 2 | $40 USD         | 1,000 | $500              |
| Tier 3 | $200 USD        | 2,000 | $1,000            |
| Tier 4 | $400 USD        | 4,000 | $5,000            |

Tier upgrades are **automatic and instant** once you reach the cumulative deposit threshold — no manual approval required.

---

## Key Model Pricing (April 2026)

The API charges by **tokens** (units of processed text), with separate prices for input and output tokens:

| Model             | Context | Input Price (per 1M tokens) | Output Price (per 1M tokens) |
|-------------------|---------|-----------------------------|-----------------------------|
| Claude Opus 4.6   | 200K    | $5.00                       | $25.00                      |
| Claude Sonnet 4.6 | 200K    | $3.00                       | $15.00                      |
| Claude Haiku 4.5  | 200K    | $1.00                       | $5.00                       |

For testing, **Claude Haiku 4.5** is the most cost-effective option. **Claude Sonnet 4.6** is the recommended model for most production applications.

---

## Workspaces: Project Organization

Workspaces allow you to separate environments and control access:

- Each API Key is tied to a specific Workspace and can only access its resources
- You can create separate Workspaces for `dev`, `staging`, and `production`
- Available roles within a Workspace: **User**, **Limited Developer**, **Developer**, and **Admin**

---

## Security Best Practices

- **Never expose the key on the frontend** or in public/private repositories
- **Use environment variables** in development and **secret managers** (AWS Secrets Manager, HashiCorp Vault) in production
- **Create separate keys per environment** to isolate potential security breaches
- **Immediately revoke** any key you suspect has been compromised (from [platform.claude.com/settings/keys](https://platform.claude.com/settings/keys))
- **Set a spending limit** in Billing to avoid surprise invoices
- **Monitor your usage** in the Usage section of the console

---

## Troubleshooting Common Issues

| Problem                  | Probable Cause                        | Solution                                                                  |
|--------------------------|---------------------------------------|---------------------------------------------------------------------------|
| Error 401 (Unauthorized) | Key copied incorrectly or revoked     | Verify the key or generate a new one                                      |
| Error 429 (Rate Limit)   | Tier limit exceeded                   | Reduce request frequency or upgrade your tier                             |
| Card declined            | Card not accepted                     | Try an international Visa/Mastercard or a virtual card                    |
| API Key doesn't work     | No credits in the account             | Add funds in Billing                                                      |
| Key not visible          | Window closed before copying the key  | Not recoverable: revoke it and create a new one                           |
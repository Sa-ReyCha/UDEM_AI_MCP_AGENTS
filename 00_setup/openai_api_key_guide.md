![OpenAI API Key Guide](../docs/openai_api_key.png)

## What is an OpenAI API Key?

An API Key is a unique credential that grants you access to OpenAI's models and services (such as GPT-4, DALL·E, and Whisper) from your own applications, scripts, or automation tools. It is separate from your ChatGPT account: although you can use the same credentials to log in, the developer platform is a distinct environment designed for technical integrations.

---

## Prerequisites

Before you begin, make sure you have:

- A valid email address (or a Google / Microsoft account)
- A mobile phone number for identity verification
- A credit or debit card (international Visa or Mastercard recommended)
- At least **$5 USD** to load credits (free trial credits were discontinued in mid-2025)

> ⚠️ **Important note:** Since mid-2025, new accounts no longer receive automatic trial credits. To use the API you must add a payment method and load a minimum of $5 USD.

---

## Step 1: Create or Sign In to the Platform

1. Open your browser and go to [platform.openai.com](https://platform.openai.com)
2. If you already have an OpenAI / ChatGPT account, click **"Log in"** and enter your credentials
3. If you don't have an account, click **"Sign up"** and register with:
   - Email address and password
   - Google account
   - Microsoft account
4. Confirm your email address by clicking the link that OpenAI sends you

---

## Step 2: Verify Your Phone Number

After creating the account, OpenAI will ask you to verify your phone number:

1. Enter your mobile number with the country code
2. You will receive an SMS with a 6-digit code
3. Enter the code in the portal to activate your developer profile

---

## Step 3: Navigate to the API Keys Section

Once you are inside the Dashboard:

1. In the left-side menu, click **"API keys"**
2. You can also go directly to: [platform.openai.com/settings/organization/api-keys](https://platform.openai.com/settings/organization/api-keys)

---

## Step 4: Create a New Secret Key

1. Click the **"Create new secret key"** button
2. Assign a descriptive name to your key (e.g., `My-Dev-Project` or `Personal-Test`)
3. Select the project it will be associated with (you can use **"Default project"** to get started)
4. Choose the key's permission level:

| Permission Level | Description                              | Recommended Use                        |
|------------------|------------------------------------------|----------------------------------------|
| **All**          | Full access to all endpoints             | Personal projects and prototypes       |
| **Restricted**   | Custom access per endpoint               | Production applications                |
| **Read Only**    | Read-only access to all endpoints        | Monitoring or analytics                |

5. Click **"Create secret key"**

---

## Step 5: Copy and Save the Key

> ⚠️ **CRITICAL!** The key is shown **only once**. After you close the window, OpenAI will not display it again.

1. Click the copy icon to copy the key to your clipboard
2. Store it in a safe place (password manager, private configuration file)
3. Click **"Done"** to close the window

The key will have a format similar to: `sk-proj-...` (a long alphanumeric string)

---

## Step 6: Add Billing Credits

Without credits, your API Key will not work. To add funds:

1. In the left-side menu, go to **Settings → Billing**
2. Click **"Add payment method"**
3. Enter your credit/debit card details:
   - Card number, expiration date, CVC
   - Cardholder name and billing address
4. Once the payment method is saved, click **"Add credits"**
5. The recommended minimum is **$5 USD** for testing and development

Your account will immediately be upgraded to **Tier 1** and you can start using the API.

---

## Step 7: Use the API Key in Your Application

### Option A — Environment Variable (Recommended)

**macOS / Linux:**
```bash
export OPENAI_API_KEY="your_api_key_here"
```

**Windows (CMD):**
```text
setx OPENAI_API_KEY "your_api_key_here"
```

### Option B — Python Code (with SDK)

```python
from openai import OpenAI

client = OpenAI()  # Automatically reads OPENAI_API_KEY from the environment

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello, how are you?"}]
)
print(response.choices[0].message.content)
```

### Option C — HTTP Headers (Bearer Token)

```text
Authorization: Bearer your_api_key_here
Content-Type: application/json
```

> OpenAI SDKs are configured to automatically read the `OPENAI_API_KEY` environment variable.

---

## Managing Your API Keys

You can manage all your keys from the **API Keys** section of the dashboard:

- **Rename** an existing key by clicking the edit icon
- **Delete** keys that are no longer in use or that may be compromised
- **View usage** for each key in the **Usage** section

For teams, each member should have their own individual API Key. Sharing keys violates OpenAI's Terms of Use.

---

## Security Best Practices

Protecting your API Key is essential to avoid unauthorized charges and security breaches:

- **Never expose the key on the frontend** (browsers or mobile apps): requests must always go through your backend
- **Never commit the key to a repository**: not public, not private. Use environment variables instead
- **Use secret managers in production**: AWS Secrets Manager, HashiCorp Vault, Azure Key Vault, etc.
- **Create separate keys per environment** (development, staging, production) to isolate potential breaches
- **Rotate keys periodically**: every 60–90 days is recommended
- **Monitor usage**: enable alerts in the Billing section to detect abnormal consumption
- **Set usage limits** in **Settings → Limits** to avoid unexpected bills

---

## Key Model Pricing (April 2026)

Costs depend on the model you use. The API charges by **tokens** (units of processed text):

| Model          | Usage Type      | Approximate Cost      |
|----------------|-----------------|-----------------------|
| GPT-4o         | Input / Output  | Varies by token count |
| GPT-4o mini    | Input / Output  | More economical       |
| GPT-3.5 Turbo  | Input / Output  | Most economical       |

For test projects, **$5 USD** is usually enough to experiment with hundreds or thousands of calls depending on the chosen model.

---

## Troubleshooting Common Issues

| Problem                  | Possible Cause                        | Solution                                                             |
|--------------------------|---------------------------------------|----------------------------------------------------------------------|
| Card declined            | Card not accepted in your region      | Try an international Visa/Mastercard or a virtual card               |
| API Key doesn't work     | No credits loaded                     | Add funds in Billing                                                 |
| Error 401 (Unauthorized) | Key copied incorrectly or revoked     | Generate a new key and verify it is pasted correctly                 |
| Key not visible          | Lost after closing the window         | Cannot be recovered; create a new key                               |
| Account blocked          | Suspicious activity detected          | Contact support at [help.openai.com](https://help.openai.com)        |
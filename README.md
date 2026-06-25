# Multichannel Ad Campaign Coordinator Skill

This repository contains the **Multichannel Ad Campaign Coordinator Skill** — an autonomous agent skill configuration (`skill.json`), developer SDK client (`campaign_coordinator.py`), and validation script for coordinating paid ad traffic. It is designed to automatically allocate budgets across platforms (Meta, Google, TikTok), generate platform-specific copy variations, and yield integration-ready API payloads.

---

## 🚀 Capabilities

* **Strategic Budget Allocator:** Recommends campaign budgets dynamically based on requested platform strengths and campaign objectives (conversions, lead gen, brand awareness).
* **Format-Specific Copywriting:** Generates optimized hooks and copy variations conforming to distinct character constraints and platform tones (e.g. Google Search Ads vs TikTok Spark Ads).
* **Direct Ad Manager API Integration:** Generates JSON payload schemas structured exactly for third-party REST API creation endpoints (Meta Marketing API / Google Ads API).

---

## 🛠️ Setup & Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configuration:
   Set your API environment variables if executing requests against the live production server (otherwise, client executes in mock mode):
   * **PowerShell**:
     ```powershell
     $env:CAMPAIGN_API_KEY="your_api_key"
     ```
   * **bash**:
     ```bash
     export CAMPAIGN_API_KEY="your_api_key"
     ```

---

## 💻 SDK Usage Reference

```python
from campaign_coordinator import CampaignCoordinatorClient

# Initialize Client (mock mode by default)
client = CampaignCoordinatorClient()

# Recommend budget allocation splits
allocations = client.suggest_allocation(
    total_budget=1000.00,
    channels=["meta", "tiktok"],
    goal="conversions"
)
print(allocations)

# Generate copy variations
creatives = client.generate_ad_copy(
    product_name="Zenith Watch",
    selling_points=["14 days battery", "Heart monitor"],
    channels=["meta"]
)
print(creatives[0]["body_text"])

# Get integration ready JSON API payload
payload = client.build_api_payloads(
    client_id="act_123",
    campaign_name="Zenith_Campaign",
    budget=allocations["meta"],
    channel="meta",
    creative=creatives[0]
)
```

---

## 📜 License
This project is licensed under the MIT License.

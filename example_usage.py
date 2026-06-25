import sys
import json
from campaign_coordinator import CampaignCoordinatorClient

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        
    print("=== Multichannel Ad Campaign Coordinator Example ===")
    
    # Initialize client in mock mode
    client = CampaignCoordinatorClient()
    
    product_name = "Zenith Smart Watch"
    selling_points = [
        "Up to 14 days of battery life",
        "Advanced health metric heart rate monitoring",
        "Rugged, water-resistant design built for outdoor activities"
    ]
    channels = ["meta", "google", "tiktok"]
    
    # 1. Get budget allocation suggestion
    print("\n--- Budget Allocation Suggestions ---")
    allocation = client.suggest_allocation(
        total_budget=5000.00,
        channels=channels,
        goal="conversions"
    )
    for c, amt in allocation.items():
        print(f"  Allocated to {c.upper()}: ${amt:.2f}")

    # 2. Generate ad copywriting variations
    print("\n--- Ad Copywriting Variations ---")
    creatives = client.generate_ad_copy(product_name, selling_points, channels)
    for cr in creatives:
        print(f"\nPlatform: {cr['channel'].upper()} (Format: {cr['format']})")
        print(f"  Headline: {cr['headline']}")
        print(f"  Body: {cr['body_text']}")
        print(f"  CTA: {cr['call_to_action']}")

    # 3. Build integration API payloads
    print("\n--- Generating Integration API Payloads ---")
    for cr in creatives:
        chan = cr['channel']
        budget = allocation[chan]
        payload = client.build_api_payloads(
            client_id="act_129847198",
            campaign_name=f"Zenith_Watch_{chan.upper()}_Conversions",
            budget=budget,
            channel=chan,
            creative=cr
        )
        print(f"\n[{chan.upper()} API Payload]:")
        print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()

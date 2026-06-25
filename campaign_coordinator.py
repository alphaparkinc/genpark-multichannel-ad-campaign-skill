import os
import requests
from typing import List, Dict, Any, Optional

class CampaignCoordinatorError(Exception):
    """Base exception class for Campaign Coordinator Client."""
    pass

class CampaignCoordinatorClient:
    """
    Client for automating multi-channel ad budget allocations, ad copy generation, and API payloads.
    Supports a mock mode for local testing.
    """
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.campaign-coordinator.ai/v1"):
        self.api_key = api_key or os.environ.get("CAMPAIGN_API_KEY")
        self.base_url = base_url.rstrip("/")
        self.mock_mode = self.api_key is None or self.api_key == "mock"
        
        if self.mock_mode:
            print("[CampaignCoordinatorClient] API Key not set. Running in MOCK Mode.")

    def suggest_allocation(self, total_budget: float, channels: List[str], goal: str) -> Dict[str, float]:
        """
        Dynamically split campaign budget between channels based on primary goal.
        """
        if self.mock_mode:
            # Simulated allocation algorithm
            count = len(channels)
            if count == 0:
                return {}
            
            splits = {}
            if goal.lower() == "conversions":
                # Favor Google Search and Meta Ads
                weights = {"google": 0.45, "meta": 0.35, "tiktok": 0.20}
            elif goal.lower() == "brand_awareness":
                # Favor TikTok Ads and Meta Ads
                weights = {"tiktok": 0.50, "meta": 0.30, "google": 0.20}
            else:
                # Equal splits
                weights = {c: 1.0 / count for c in channels}
            
            # Filter and normalize weights for requested channels
            req_weights = {c: weights.get(c.lower(), 1.0/count) for c in channels}
            total_weight = sum(req_weights.values())
            
            for c in channels:
                splits[c] = round((req_weights[c] / total_weight) * total_budget, 2)
            return splits

        # Remote API integration call
        payload = {"total_budget": total_budget, "channels": channels, "goal": goal}
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            resp = requests.post(f"{self.base_url}/campaign/allocate", json=payload, headers=headers, timeout=30)
            return resp.json()["allocations"]
        except Exception as e:
            raise CampaignCoordinatorError(f"API Allocation failed: {e}")

    def generate_ad_copy(self, product_name: str, selling_points: List[str], channels: List[str]) -> List[Dict[str, Any]]:
        """
        Generate platform-optimized ad copy variations.
        """
        if self.mock_mode:
            print(f"[Mock API] Generating ad copy variations for: {product_name}")
            creatives = []
            hook = selling_points[0] if selling_points else "Upgrade your daily routine today!"
            
            for c in channels:
                chan = c.lower()
                if chan == "meta":
                    creatives.append({
                        "channel": "meta",
                        "format": "Feed Image/Carousel",
                        "headline": f"Discover the New {product_name} 🔥",
                        "body_text": f"Struggling with standard options? {hook}.\n\nWhy choose Zenith:\n" + "\n".join([f"✅ {p}" for p in selling_points]) + "\n\nClick below to shop now!",
                        "call_to_action": "SHOP_NOW"
                    })
                elif chan == "google":
                    # Google Ads character limits: Headline 30 chars, Description 90 chars
                    headline = f"Get the {product_name}"[:30]
                    description = f"Experience premium performance. {hook}"[:90]
                    creatives.append({
                        "channel": "google",
                        "format": "Responsive Search Ad",
                        "headline": headline,
                        "body_text": description,
                        "call_to_action": "None"
                    })
                elif chan == "tiktok":
                    creatives.append({
                        "channel": "tiktok",
                        "format": "Spark Video Ad",
                        "headline": f"This changes everything! 🤫 {product_name} test run",
                        "body_text": f"Wait till the end to see the results. {hook}. Get yours link in bio!",
                        "call_to_action": "LEARN_MORE"
                    })
            return creatives

        payload = {"product_name": product_name, "selling_points": selling_points, "channels": channels}
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            resp = requests.post(f"{self.base_url}/campaign/copywriting", json=payload, headers=headers, timeout=30)
            return resp.json()["creatives"]
        except Exception as e:
            raise CampaignCoordinatorError(f"API Copywriting failed: {e}")

    def build_api_payloads(self, client_id: str, campaign_name: str, budget: float, channel: str, creative: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build valid request payloads for third party ad network APIs.
        """
        chan = channel.lower()
        if chan == "meta":
            return {
                "name": campaign_name,
                "objective": "OUTCOMES",
                "status": "PAUSED",
                "daily_budget": int(budget * 100), # in cents
                "creative": {
                    "title": creative.get("headline"),
                    "body": creative.get("body_text"),
                    "call_to_action_type": creative.get("call_to_action", "SHOP_NOW")
                }
            }
        elif chan == "google":
            return {
                "campaign": {
                    "name": campaign_name,
                    "advertising_channel_type": "SEARCH",
                    "status": "PAUSED",
                    "manual_cpc": {},
                    "campaign_budget": budget
                },
                "ad_group_ad": {
                    "ad": {
                        "expanded_text_ad": {
                            "headline_part1": creative.get("headline", "")[:30],
                            "description": creative.get("body_text", "")[:90]
                        }
                    }
                }
            }
        return {"error": f"Payload generator for channel '{channel}' not implemented."}

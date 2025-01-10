import json
import requests

class WebhookSender:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "webhook_url": ("STRING",),
                "property_name": ("STRING",),
                "property_value": ("STRING",),
                "identifier": ("STRING",),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "send_to_webhook"
    CATEGORY = "Custom/Webhook"

    def send_to_webhook(self, webhook_url, property_name, property_value, identifier):
        try:
            print("Sending to webhook")
            input_dict = {property_name: property_value, "identifier": identifier}
            response = requests.post(webhook_url, json=input_dict)
            response.raise_for_status()
            print(response.status_code)
            return (f"Success: {response.status_code}",)
        except requests.exceptions.RequestException as e:
            return (f"Error: {str(e)}",)

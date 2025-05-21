import cv2
import numpy as np

def parse_ticket(ticket_img):
    h, w = ticket_img.shape[:2]

    # Section boundaries (top, bottom) based on % height
    regions = {
        "order":     ticket_img[int(0.0000*h):int(0.0795*h), :],
        "bread":     ticket_img[int(0.0795*h):int(0.1712*h), :],
        "topping1":  ticket_img[int(0.1712*h):int(0.2493*h), :],
        "topping2":  ticket_img[int(0.2493*h):int(0.3301*h), :],
        "topping3":  ticket_img[int(0.3301*h):int(0.4109*h), :],
        "topping4":  ticket_img[int(0.4109*h):int(0.4917*h), :],
        "sauce":     ticket_img[int(0.4917*h):int(0.5726*h), :],
        "pasta":     ticket_img[int(0.5726*h):int(0.6534*h), :],
        "doneness":  ticket_img[int(0.6534*h):int(0.7260*h), :]
    }

    # For debug: save each region to verify visually
    for name, region in regions.items():
        cv2.imwrite(f"debug_{name}.png", region)

    # Placeholder logic — replace with matching functions later
    parsed = {
        "bread": classify_section(regions["bread"], "bread"),
        "toppings": [
            classify_section(regions["topping1"], "topping"),
            classify_section(regions["topping2"], "topping"),
            classify_section(regions["topping3"], "topping"),
            classify_section(regions["topping4"], "topping")
        ],
        "sauce": classify_section(regions["sauce"], "sauce"),
        "pasta": classify_section(regions["pasta"], "pasta"),
        "doneness": estimate_doneness(regions["doneness"])
    }

    # Remove empty toppings
    parsed["toppings"] = [t for t in parsed["toppings"] if t != "none"]

    return parsed


# === Stub Functions ===

def classify_section(img, category):
    """Return placeholder based on visual section."""
    # TODO: Replace with template or on-screen match
    return f"{category}_placeholder"

def estimate_doneness(img):
    """Estimate doneness based on orange bar fill."""
    # TODO: Implement pixel intensity scan
    return "medium"

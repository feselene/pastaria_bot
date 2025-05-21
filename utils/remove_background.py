from rembg import remove
from PIL import Image

def crop_to_content(img: Image.Image) -> Image.Image:
    """Crop to non-transparent pixels in an RGBA image."""
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    bbox = img.getbbox()  # Bounding box of non-zero alpha
    if bbox:
        return img.crop(bbox)
    return img  # Return unchanged if bbox is None

# Paths
input_path = r'C:\Users\ceo\IdeaProjects\pastaria_bot\assets\img_2.png'
output_path = r'C:\Users\ceo\IdeaProjects\pastaria_bot\assets\img_clean.png'

# Remove background
input_image = Image.open(input_path)
output_image = remove(input_image)

# Crop to object bounds
output_cropped = crop_to_content(output_image)

# Save output
output_cropped.save(output_path)
print(f"✅ Saved tightly cropped image to: {output_path}")

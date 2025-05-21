from rembg import remove
from PIL import Image

def remove_background_and_crop(input_path: str, output_path: str) -> None:
    """
    Removes the background from an image and tightly crops it to the content.

    Parameters:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the output cropped image.
    """
    def crop_to_content(img: Image.Image) -> Image.Image:
        """Crop to non-transparent pixels in an RGBA image."""
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        bbox = img.getbbox()
        if bbox:
            return img.crop(bbox)
        return img

    # Load and process
    input_image = Image.open(input_path)
    output_image = remove(input_image)
    output_cropped = crop_to_content(output_image)
    output_cropped.save(output_path)
    print(f"✅ Saved tightly cropped image to: {output_path}")

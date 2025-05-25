from PIL import Image
from rembg import remove


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


def crop(input_path: str, output_path: str,
         xratio1: float = 0.395, yratio1: float = 0.15,
         xratio2: float = 0.595, yratio2: float = 0.9) -> None:
    if not all(0 <= r <= 1 for r in [xratio1, yratio1, xratio2, yratio2]):
        raise ValueError("All ratios must be between 0 and 1.")

    if xratio1 > xratio2 or yratio1 > yratio2:
        raise ValueError("Top-left ratios must be <= bottom-right ratios.")

    # Load image
    image = Image.open(input_path)
    width, height = image.size

    # Convert ratios to pixel coordinates
    left = int(width * xratio1)
    upper = int(height * yratio1)
    right = int(width * xratio2)
    lower = int(height * yratio2)

    # Crop and save
    cropped_image = image.crop((left, upper, right, lower))
    cropped_image.save(output_path)
    print(f"✅ Saved cropped region to: {output_path}")


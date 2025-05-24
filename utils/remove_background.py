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


def crop(input_path: str, output_path: str) -> None:
    """
    Crops a specific rectangular region (e.g., a circle label) from the input image.

    Parameters:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the cropped image.
    """
    # Load image
    image = Image.open(input_path)

    # Define bounding box (left, upper, right, lower)
    # Adjust these values to tightly crop the circle
    box = (115, 10, 175, 65)  # (x1, y1, x2, y2)
    cropped_image = image.crop(box)

    # Save cropped image
    cropped_image.save(output_path)
    print(f"✅ Saved cropped circle region to: {output_path}")

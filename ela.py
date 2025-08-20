import os
import sys
from PIL import Image, ImageChops, ImageEnhance

def convert_to_ela_image(path, quality=90):
    """
    Convert input image to ELA (Error Level Analysis) applied image
    
    Args:
        path (str): Path to the input image
        quality (int): JPEG quality level for resaving (default: 90)
        
    Returns:
        str: Path to the generated ELA image
    Raises:
        ValueError: If image cannot be processed
    """
    try:
        # Validate input quality
        if not 1 <= quality <= 100:
            raise ValueError("Quality must be between 1 and 100")

        # Open and validate original image
        if not os.path.exists(path):
            raise FileNotFoundError(f"Input file not found: {path}")

        with Image.open(path) as original_image:
            original_image = original_image.convert("RGB")

            # Create temp directory if it doesn't exist
            temp_dir = "temp_ela"
            os.makedirs(temp_dir, exist_ok=True)

            # Save resaved image with specified quality
            resaved_path = os.path.join(temp_dir, "resaved_image.jpg")
            original_image.save(resaved_path, "JPEG", quality=quality)

            # Calculate ELA difference
            with Image.open(resaved_path) as resaved_image:
                ela_image = ImageChops.difference(original_image, resaved_image)

                # Calculate scaling factor
                extrema = ela_image.getextrema()
                max_difference = max(pix[1] for pix in extrema) if extrema else 1
                max_difference = max(max_difference, 1)  # Ensure we don't divide by zero
                scale = 350.0 / max_difference

                # Enhance and save ELA image
                ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
                
                output_path = os.path.join(temp_dir, "ela_image.png")
                ela_image.save(output_path)
                
                # Clean up temporary files
                try:
                    os.remove(resaved_path)
                except:
                    pass
                
                return output_path

    except Exception as e:
        raise ValueError(f"ELA processing failed: {str(e)}")

if __name__ == "__main__":
    try:
        if len(sys.argv) < 3:
            print("Usage: python ela.py <image_path> <quality>")
            sys.exit(1)
            
        file_path = sys.argv[1]
        quality = int(sys.argv[2])
        
        output_path = convert_to_ela_image(file_path, quality)
        print(f"ELA image saved to: {output_path}")
        
        # Show the image if running interactively
        with Image.open(output_path) as img:
            img.show()
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
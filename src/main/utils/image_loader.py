import customtkinter
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import io
import os

def load_svg_image(svg_path, size=(20, 20)):
    """
    Loads an SVG image, converts it to PNG in memory, and returns a CTkImage.
    """
    drawing = svg2rlg(svg_path)
    
    # Render the SVG to a PNG in memory
    png_data = io.BytesIO()
    renderPM.drawToFile(drawing, png_data, fmt="PNG")
    png_data.seek(0) # Rewind to the beginning of the BytesIO object

    # Open the PNG data with Pillow
    pil_image = Image.open(png_data)
    
    # Resize the image if a specific size is requested
    if size:
        pil_image = pil_image.resize(size, Image.LANCZOS) # Use LANCZOS for high-quality downsampling

    # Create and return a CustomTkinter image
    return customtkinter.CTkImage(light_image=pil_image, dark_image=pil_image, size=size)
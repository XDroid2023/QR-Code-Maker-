import qrcode
import os
from datetime import datetime

def generate_qr_code(data, filename=None):
    """
    Generate a QR code from the given data and save it to a file.
    
    Args:
        data (str): The data to encode in the QR code
        filename (str, optional): The filename to save the QR code. If None, generates a timestamp-based name.
    
    Returns:
        str: The path to the saved QR code image
    """
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create an image from the QR Code
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Generate filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"qr_code_{timestamp}.png"
    elif not filename.endswith('.png'):
        filename += '.png'
    
    # Save the image
    qr_image.save(filename)
    return filename

def main():
    while True:
        # Get user input
        print("\nQR Code Generator")
        print("-----------------")
        data = input("Enter the text/URL for the QR code (or 'quit' to exit): ")
        
        if data.lower() == 'quit':
            break
        
        filename = input("Enter filename (optional, press Enter for automatic name): ").strip()
        
        # Generate QR code
        filename = generate_qr_code(data, filename if filename else None)
        
        # Get absolute path
        abs_path = os.path.abspath(filename)
        print(f"\nQR code generated successfully!")
        print(f"Saved as: {abs_path}")

if __name__ == "__main__":
    main()

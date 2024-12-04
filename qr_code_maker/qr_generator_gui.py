import customtkinter as ctk
import qrcode
from PIL import Image, ImageTk, ImageDraw
import os
from datetime import datetime
import webbrowser
from tkinter import filedialog
import colorsys
import numpy as np

class QRCodeGenerator(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Rainbow QR Generator")
        self.geometry("900x700")
        self.grid_columnconfigure(0, weight=1)
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Configure colors
        self.tech_blue = "#00a8ff"
        self.neon_blue = "#0984e3"
        self.dark_bg = "#1e272e"
        self.accent_color = "#00d2d3"
        
        # Set window background
        self.configure(fg_color=self.dark_bg)

        # Create main frame
        self.main_frame = ctk.CTkFrame(self, fg_color=self.dark_bg)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Title with tech style
        self.title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.title_frame.grid(row=0, column=0, pady=(0, 20))
        
        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="RAINBOW QR GENERATOR",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=self.tech_blue
        )
        self.title_label.grid(row=0, column=0, pady=(0, 5))
        
        self.subtitle_label = ctk.CTkLabel(
            self.title_frame,
            text="Generate Colorful QR Codes Instantly",
            font=ctk.CTkFont(size=14),
            text_color=self.accent_color
        )
        self.subtitle_label.grid(row=1, column=0)

        # Input frame with glass effect
        self.input_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.dark_bg,
            border_width=2,
            border_color=self.tech_blue
        )
        self.input_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.input_frame.grid_columnconfigure(1, weight=1)

        # Text input
        self.text_label = ctk.CTkLabel(
            self.input_frame,
            text="INPUT DATA:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.accent_color
        )
        self.text_label.grid(row=0, column=0, padx=(20, 10), pady=20)

        self.text_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Enter text or URL to generate QR code",
            width=400,
            height=40,
            border_color=self.tech_blue,
            fg_color="#2d3436"
        )
        self.text_entry.grid(row=0, column=1, padx=10, pady=20, sticky="ew")

        # Style options frame
        self.style_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.dark_bg,
            border_width=2,
            border_color=self.tech_blue
        )
        self.style_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        # Rainbow style selector
        self.style_label = ctk.CTkLabel(
            self.style_frame,
            text="RAINBOW STYLE:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.accent_color
        )
        self.style_label.grid(row=0, column=0, padx=20, pady=10)
        
        self.style_var = ctk.StringVar(value="rainbow")
        self.style_menu = ctk.CTkOptionMenu(
            self.style_frame,
            values=["Rainbow", "Sunset", "Ocean", "Forest"],
            variable=self.style_var,
            font=ctk.CTkFont(size=14),
            fg_color=self.tech_blue,
            button_color=self.neon_blue
        )
        self.style_menu.grid(row=0, column=1, padx=20, pady=10)

        # Generate button with tech style
        self.generate_button = ctk.CTkButton(
            self.style_frame,
            text="GENERATE",
            command=self.generate_qr_code,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color=self.tech_blue,
            hover_color=self.neon_blue
        )
        self.generate_button.grid(row=0, column=2, padx=20, pady=10)

        # QR Code display frame with tech border
        self.display_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.dark_bg,
            border_width=2,
            border_color=self.tech_blue
        )
        self.display_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.main_frame.grid_rowconfigure(3, weight=1)
        self.display_frame.grid_columnconfigure(0, weight=1)
        self.display_frame.grid_rowconfigure(0, weight=1)

        # Initial display label
        self.qr_label = ctk.CTkLabel(
            self.display_frame,
            text="QR CODE PREVIEW",
            font=ctk.CTkFont(size=16),
            text_color=self.accent_color
        )
        self.qr_label.grid(row=0, column=0, padx=20, pady=20)

        # Action buttons frame
        self.action_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.action_frame.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.action_frame.grid_columnconfigure((0, 1), weight=1)

        # Save button with tech style
        self.save_button = ctk.CTkButton(
            self.action_frame,
            text="SAVE QR CODE",
            command=self.save_qr_code,
            state="disabled",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color=self.tech_blue,
            hover_color=self.neon_blue
        )
        self.save_button.grid(row=0, column=0, padx=5, pady=10, sticky="e")

        # Clear button with tech style
        self.clear_button = ctk.CTkButton(
            self.action_frame,
            text="CLEAR",
            command=self.clear_all,
            state="disabled",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="#c0392b",
            hover_color="#e74c3c"
        )
        self.clear_button.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        # Status label with tech style
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=self.accent_color
        )
        self.status_label.grid(row=5, column=0, pady=(0, 10))

        # Store the current QR code image
        self.current_qr = None
        self.photo_image = None
        
    def create_gradient_palette(self, style):
        if style.lower() == "rainbow":
            # Create a rainbow gradient
            colors = []
            for i in range(360):
                rgb = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(i / 360.0, 1.0, 1.0))
                colors.append(rgb)
        elif style.lower() == "sunset":
            # Create a sunset gradient (orange to purple)
            colors = [
                (255, 87, 34),  # Deep Orange
                (244, 67, 54),  # Red
                (233, 30, 99),  # Pink
                (156, 39, 176)  # Purple
            ]
        elif style.lower() == "ocean":
            # Create an ocean gradient (blue tones)
            colors = [
                (0, 176, 255),    # Light Blue
                (0, 145, 234),    # Blue
                (25, 118, 210),   # Dark Blue
                (21, 101, 192)    # Deeper Blue
            ]
        else:  # Forest
            # Create a forest gradient (green tones)
            colors = [
                (76, 175, 80),    # Light Green
                (56, 142, 60),    # Green
                (27, 94, 32),     # Dark Green
                (0, 105, 92)      # Teal
            ]
            
        return colors

    def create_rainbow_qr(self, qr_matrix, style):
        # Get the size of the QR code matrix
        size = len(qr_matrix)
        scale = 10  # Scale factor for the final image
        border = 40  # Border size
        
        # Create a new image with a border
        img_size = size * scale + 2 * border
        img = Image.new('RGB', (img_size, img_size), self.dark_bg)
        draw = ImageDraw.Draw(img)
        
        # Get color palette based on style
        colors = self.create_gradient_palette(style)
        
        # Calculate the number of colors needed
        total_colors = len(colors)
        
        # Draw each module of the QR code
        for r in range(size):
            for c in range(size):
                if qr_matrix[r][c]:
                    # Calculate color index based on position
                    color_index = int(((r + c) / (size * 2)) * total_colors)
                    if color_index >= total_colors:
                        color_index = total_colors - 1
                        
                    # Get color from palette
                    color = colors[color_index]
                    
                    # Calculate position with border
                    x = c * scale + border
                    y = r * scale + border
                    
                    # Draw a filled rectangle
                    draw.rectangle(
                        [x, y, x + scale - 1, y + scale - 1],
                        fill=color
                    )
        
        return img

    def generate_qr_code(self):
        data = self.text_entry.get().strip()
        if not data:
            self.status_label.configure(text="⚠️ Please enter some text or URL", text_color="#e74c3c")
            return

        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Get the QR matrix
        matrix = qr.get_matrix()
        
        # Create rainbow QR code
        style = self.style_var.get()
        self.current_qr = self.create_rainbow_qr(matrix, style)
        
        # Resize for display
        display_size = (300, 300)
        resized_qr = self.current_qr.resize(display_size, Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        self.photo_image = ImageTk.PhotoImage(resized_qr)
        
        # Update display
        self.qr_label.configure(image=self.photo_image, text="")
        
        # Enable buttons
        self.save_button.configure(state="normal")
        self.clear_button.configure(state="normal")
        
        # Update status
        self.status_label.configure(text="✓ Rainbow QR Code generated successfully!", text_color=self.accent_color)

    def save_qr_code(self):
        if self.current_qr:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            initial_file = f"rainbow_qr_{timestamp}.png"
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                initialfile=initial_file,
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            
            if file_path:
                self.current_qr.save(file_path)
                self.status_label.configure(
                    text="✓ Rainbow QR Code saved successfully!",
                    text_color=self.accent_color
                )

    def clear_all(self):
        self.text_entry.delete(0, 'end')
        self.qr_label.configure(image=None, text="QR CODE PREVIEW")
        self.current_qr = None
        self.photo_image = None
        self.save_button.configure(state="disabled")
        self.clear_button.configure(state="disabled")
        self.status_label.configure(text="")

if __name__ == "__main__":
    app = QRCodeGenerator()
    app.mainloop()

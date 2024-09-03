import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from zind import zind

class ZindApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zind Viewer")

        # Initialize Zind
        self.Z = zind("/media/user/WD_BLACK/noah/zind/datasets")

        # Set up frames
        self.house_frame = ttk.Frame(self.root)
        self.house_frame.pack(pady=10)

        self.pano_frame = ttk.Frame(self.root)
        self.pano_frame.pack(pady=10)

        self.layout_frame = ttk.Frame(self.root)
        self.layout_frame.pack(pady=10)

        self.image_frame = ttk.Frame(self.root)
        self.image_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Set up house list
        self.house_label = ttk.Label(self.house_frame, text="Select a House:")
        self.house_label.pack(side=tk.LEFT)

        self.house_combobox = ttk.Combobox(self.house_frame, state="readonly")
        self.house_combobox['values'] = self.Z.house_list
        self.house_combobox.bind("<<ComboboxSelected>>", self.house_selected)
        self.house_combobox.pack(side=tk.LEFT)

        # Set up pano list
        self.pano_label = ttk.Label(self.pano_frame, text="Select a Panorama:")
        self.pano_label.pack(side=tk.LEFT)

        self.pano_combobox = ttk.Combobox(self.pano_frame, state="readonly")
        self.pano_combobox.bind("<<ComboboxSelected>>", self.update_image)
        self.pano_combobox.pack(side=tk.LEFT)

        # Set up layout type list
        self.layout_label = ttk.Label(self.layout_frame, text="Select Layout Type:")
        self.layout_label.pack(side=tk.LEFT)

        self.layout_combobox = ttk.Combobox(self.layout_frame, state="readonly")
        self.layout_combobox['values'] = ["layout_raw", "layout_complete", "layout_visible"]
        self.layout_combobox.current(0)  # Set default to "layout_raw"
        self.layout_combobox.bind("<<ComboboxSelected>>", self.update_image)
        self.layout_combobox.pack(side=tk.LEFT)

        # Image label
        self.img_label = ttk.Label(self.image_frame)
        self.img_label.pack(fill=tk.BOTH, expand=True)

        # Bind window resize event to dynamically resize the image
        self.root.bind("<Configure>", self.on_resize)

        # Variables to hold the current image
        self.current_image = None
        self.img_tk = None

    def house_selected(self, event):
        # Update pano list when house is selected
        selected_house = self.house_combobox.get()
        pano_list = self.Z.get_pano_list(selected_house)
        self.pano_combobox['values'] = pano_list
        self.pano_combobox.current(0)
        self.update_image(None)  # Update image for the initial panorama

    def update_image(self, event):
        # Get selected house, pano, and layout type
        selected_house = self.house_combobox.get()
        selected_pano = self.pano_combobox.get()
        layout_type = self.layout_combobox.get()

        if not selected_house or not selected_pano:
            return  # If no valid selection, do nothing

        # Visualize the image
        img_array = self.Z.visualize(selected_house, selected_pano, layout_type=layout_type)

        # Convert image array to a PIL Image
        self.current_image = Image.fromarray(img_array)

        # Resize the image to fit the current window size
        self.resize_image()

    def resize_image(self):
        if self.current_image is None:
            return

        # Get the size of the image frame
        frame_width = self.image_frame.winfo_width()
        frame_height = self.image_frame.winfo_height()

        # Resize the image to fit the frame
        resized_image = self.current_image.resize((frame_width, frame_height), Image.LANCZOS)
        self.img_tk = ImageTk.PhotoImage(resized_image)

        # Update image label
        self.img_label.config(image=self.img_tk)
        self.img_label.image = self.img_tk

    def on_resize(self, event):
        # Handle window resize event to resize the image
        self.resize_image()

def main():
    root = tk.Tk()
    app = ZindApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
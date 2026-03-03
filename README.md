# Cloudinary AI Upscaler – Blender Add-on

**Quickly upload images from Blender to Cloudinary and get an AI-upscaled version.**

This add-on adds a simple panel in the **Image Editor** that lets you:

<img width="447" height="358" alt="image" src="https://github.com/user-attachments/assets/3961c94c-7e6c-4eba-ab52-1132f992aafe" />



- Enter your Cloudinary credentials once
- Drag & drop (or pick) any image file from your computer
- Upload it to your Cloudinary account
- Automatically apply Cloudinary's AI upscale transformation
- Copy the resulting upscaled URL to clipboard and open it in your browser

## Features

- N-panel tab in the **Image Editor** called **Cloudinary**
- Secure input for Cloud Name, API Key, API Secret (hidden by default)
- **Test Connection** button to verify credentials
- Drag-and-drop file field (or click to browse/pick file)
- One-click **Upscale** button that appears once a file is selected
- Optional button to upscale the **active image** if it has a valid filepath on disk
- Uses Cloudinary transformations: `e_upscale`, `q_auto`, `f_auto`
- Clears clipboard with the final upscaled URL and opens it automatically

## Requirements

- Blender **3.0** or newer
- A **Cloudinary** account (free tier is usually sufficient for testing)
- Internet connection

The add-on automatically installs the `cloudinary` Python package into Blender's embedded Python if it's missing.

## Installation

1. Download this repository as ZIP  
   (Code → Download ZIP – do **not** unzip it)

2. In Blender:  
   **Edit → Preferences → Add-ons → Install…**

3. Select the downloaded `.zip` file → **Install Add-on**

4. Search for **"Cloudinary AI Upscaler"** and enable it

The panel appears in the **Image Editor** sidebar (press **N** to show sidebar → **Cloudinary** tab).

## Setup

<img width="447" height="358" alt="image" src="https://github.com/user-attachments/assets/a724f439-7638-457f-814a-dd015bf98f3c" />

1. Go to your Cloudinary dashboard[](https://cloudinary.com/console)  or set one up https://cloudinary.com/
   Copy your **Cloud name**, **API Key**, and **API Secret**

2. In Blender → Image Editor → N-panel → **Cloudinary** tab:
   - Click the eye/lock icon to show credential fields
   - Paste Cloud Name, API Key, API Secret
   - Click **Test Connection** (globe icon) to verify
   - (Optional) hide credentials again with the eye icon

## Usage

### Drag & Drop (recommended)

1. In the **Cloudinary** panel find the field labeled  
   **Drag & Drop Image Below:**

2. Drag any image file (.png, .jpg, .exr, etc.) from your file explorer into that field  
   (or click the field to open the file picker)

3. Once the path appears, a button shows:  
   **Upscale: yourfilename.png**

4. Click it → the image uploads → AI upscale is applied → URL is copied to clipboard → browser opens the result

### Using the Active Image (limited)

If an image is loaded/visible in the **Image Editor** **and** it has a valid file path on disk (not packed, not a render result without save), a second button appears:

**Upscale yourimagename**

Clicking it works the same way — but only if `img.filepath` points to an existing file.

## Important Notes

- This add-on **requires** the image to exist as a real file on disk.  
  Render results, packed images, or unsaved edits in the Image Editor will **not** work unless you first save them to disk.

- Cloudinary's `e_upscale` effect is used (good for enlarging photos, textures, faces, etc.).  
  No custom size/scale factor is configurable yet — Cloudinary decides the output dimensions.

- Free Cloudinary accounts have usage limits (transformations, bandwidth). Heavy use may require a paid plan.

- Credentials are stored in the scene — **do not share .blend files** with credentials filled in.



Feel free to fork, modify, or use in any project.

Made with frustration and coffee in Zurich.

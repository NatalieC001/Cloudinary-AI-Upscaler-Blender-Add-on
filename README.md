# Cloudinary AI Upscaler – Blender Add-on

Cloudinary_SecureInstaller.py offers a more secure installer -  seprating out the password from scene (so you cant accidentally export your api passwords if you share blender scenes)

<img width="719" height="210" alt="image" src="https://github.com/user-attachments/assets/826afac2-65d2-4a93-98d4-a4a95a970943" />


**Quickly upload images from Blender to Cloudinary and get an AI-upscaled version.**

This add-on adds a simple panel in the **Image Editor** that lets you:

<img width="484" height="331" alt="image" src="https://github.com/user-attachments/assets/dcc03910-60ae-4602-91b6-9064fffef326" />



- Enter your Cloudinary credentials once
- Drag & drop (or pick) any image file from your computer
- Upload it to your Cloudinary account
- Automatically apply Cloudinary's AI upscale transformation
- Copy the resulting upscaled URL to clipboard and open it in your browser

## Features

<img width="277" height="355" alt="image" src="https://github.com/user-attachments/assets/8083bd4d-8995-4826-b9b0-0222ddae77d1" />

- N-panel tab in the **Image Editor** called **Cloudinary**
- Secure input for Cloud Name, API Key, API Secret (hidden by default and kept sepperate as part of blender prefs not scene data)
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

<img width="710" height="201" alt="image" src="https://github.com/user-attachments/assets/09790949-9d27-422c-93ba-77941cf2a086" />

1. load the script into plugins

2. In Blender:  
   Open Plugins
   Copy Install and fill in credentials.
   Go to your Cloudinary dashboard[](https://cloudinary.com/console)  or set one up https://cloudinary.com/
   Copy your **Cloud name**, **API Key**, and **API Secret**
   - Paste Cloud Name, API Key, API Secret into fields

## Setup

<img width="484" height="331" alt="image" src="https://github.com/user-attachments/assets/e09c0b28-c946-47d8-8f47-5dbdca681d97" />


This creates the Cloudinary panel in the Image Viewport.

<img width="615" height="594" alt="image" src="https://github.com/user-attachments/assets/f91b8a5c-ad7e-4f77-8c35-8c25fdcabb0c" />

2. In Blender → Image Editor → N-panel → **Cloudinary** tab:
   - Click **Test Connection** (globe icon) to verify your credentials


## Usage
find the image you want to alter ( This add-on **requires** the image to exist as a real file on disk not imbedded into the project.  
Render results, packed images, or unsaved edits in the Image Editor will **not** work unless you first save them to disk.)

select the size you want the image resized too, its format etc


## Important Notes

- Cloudinary's `e_upscale` effect is used (good for enlarging photos, textures, faces, etc.).  
  No custom size/scale factor is configurable yet — Cloudinary decides the output dimensions.

- Free Cloudinary accounts have usage limits (transformations, bandwidth). Heavy use may require a paid plan.

- Credentials are stored in the scene — **do not share .blend files** with credentials filled in.

- This software is provided as-is. Use this script at your own risk.

Enjoy and hopefully it helps :)

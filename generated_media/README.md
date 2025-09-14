# Generated Media Directory

This directory contains all media files generated using MCP servers in the kamuios project.

## Directory Structure

```
generated_media/
├── images/
│   ├── text-to-image/     # T2I: Flux, Imagen, Dreamina, etc.
│   ├── image-to-image/    # I2I: Edits, transformations, style transfers
│   └── upscaled/          # Upscaled images using AuraSR
├── videos/
│   ├── text-to-video/     # T2V: Veo3, WAN text-to-video
│   ├── image-to-video/    # I2V: Hailuo, Seedance, WAN i2v
│   └── video-to-video/    # V2V: Lipsync, upscaling, modifications
├── audio/
│   ├── text-to-speech/    # TTS: MiniMax Speech models
│   └── voice-design/      # Voice modifications and designs
└── music/
    ├── text-to-music/     # Music generation from text prompts
    └── lyria/             # Google Lyria generated music
```

## Available MCP Servers

### Image Generation (12 servers)
- Flux Schnell, Flux Krea LoRA
- Imagen3, Imagen4 Fast/Ultra
- Dreamina v3.1, Seedream V4
- Qwen Image, WAN v2.2-a14b
- Ideogram Character Base
- Gemini 2.5 Flash Image
- Nano Banana

### Image Editing (8 servers)
- AuraSR (upscaling)
- Flux Kontext LoRA/Max
- Gemini 2.5 Flash Image Edit
- Qwen Image Edit
- Ideogram Character Remix
- Seedream V4 Edit

### Video Generation (10 servers)
- Text-to-Video: Veo3, WAN v2.2-5b
- Image-to-Video: Hailuo-02, Seedance V1, Veo3 Fast, WAN v2.2-a14b
- Video-to-Video: Creatify Lipsync, Luma Ray2, Pixverse, Runway Aleph

### Audio & Music (4 servers)
- Text-to-Speech: MiniMax Speech-02-Turbo
- Text-to-Music: MiniMax Music V1.5, Google Lyria
- Video-to-Audio: ThinkSound

## Usage Notes

- All servers are accessible without additional authentication
- Files are automatically organized by generation type
- Use descriptive filenames with timestamps when saving
- Large files (>100MB) should be compressed if possible

## Examples

```bash
# Save T2I generation
mv generated_image.jpg generated_media/images/text-to-image/

# Save I2V generation  
mv generated_video.mp4 generated_media/videos/image-to-video/

# Save TTS generation
mv generated_speech.mp3 generated_media/audio/text-to-speech/
```

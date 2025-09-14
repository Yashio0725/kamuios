#!/usr/bin/env python3
"""
Kamui Code MCP クライアント
Kamui CodeのMCPサーバー群を使用するためのクライアントスクリプト
"""

import asyncio
import aiohttp
import base64
import json
import os
from typing import Dict, Any, Optional, List
from pathlib import Path

class KamuiMCPClient:
    def __init__(self):
        self.base_url = os.getenv("KAMUI_BASE_URL", "https://kamui-code.ai")
        self.token = os.getenv("KAMUI_TOKEN")
        
        if not self.token:
            raise ValueError("KAMUI_TOKEN環境変数が設定されていません")
    
    async def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Kamui Code APIにリクエストを送信"""
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"API Error {response.status}: {error_text}")
    
    # Text-to-Image 機能
    async def flux_schnell_t2i(self, prompt: str, width: int = 1024, height: int = 1024) -> Dict[str, Any]:
        """Flux Schnell Text-to-Image"""
        data = {
            "prompt": prompt,
            "width": width,
            "height": height,
            "num_inference_steps": 4,
            "guidance_scale": 0.0
        }
        return await self._make_request("/t2i/fal/flux/schnell", data)
    
    async def imagen3_t2i(self, prompt: str, aspect_ratio: str = "1:1") -> Dict[str, Any]:
        """Google Imagen 3 Text-to-Image"""
        data = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "safety_tolerance": "BLOCK_ONLY_HIGH",
            "person_generation": "ALLOW_ADULT"
        }
        return await self._make_request("/t2i/google/imagen", data)
    
    async def dreamina_t2i(self, prompt: str, style: str = "realistic") -> Dict[str, Any]:
        """Bytedance Dreamina v3.1 Text-to-Image"""
        data = {
            "prompt": prompt,
            "style": style,
            "quality": "high"
        }
        return await self._make_request("/t2i/fal/bytedance/dreamina/v3.1/text-to-image", data)
    
    # Image-to-Image 機能
    async def flux_kontext_i2i(self, image_path: str, prompt: str, strength: float = 0.8) -> Dict[str, Any]:
        """Flux Kontext Image-to-Image"""
        image_data = self._encode_image(image_path)
        data = {
            "image_url": f"data:image/jpeg;base64,{image_data}",
            "prompt": prompt,
            "strength": strength,
            "num_inference_steps": 28
        }
        return await self._make_request("/i2i/fal/flux/kontext", data)
    
    async def aura_sr_upscale(self, image_path: str, scale_factor: int = 4) -> Dict[str, Any]:
        """AuraSR Image Upscaling"""
        image_data = self._encode_image(image_path)
        data = {
            "image_url": f"data:image/jpeg;base64,{image_data}",
            "scale_factor": scale_factor
        }
        return await self._make_request("/i2i/fal/aura-sr", data)
    
    async def ideogram_character_remix(self, image_path: str, prompt: str) -> Dict[str, Any]:
        """Ideogram Character Remix"""
        image_data = self._encode_image(image_path)
        data = {
            "image_url": f"data:image/jpeg;base64,{image_data}",
            "prompt": prompt,
            "style_type": "GENERAL"
        }
        return await self._make_request("/i2i/fal/ideogram/character-remix", data)
    
    # Text-to-Video 機能
    async def veo3_fast_t2v(self, prompt: str, duration: int = 5) -> Dict[str, Any]:
        """Veo3 Fast Text-to-Video"""
        data = {
            "prompt": prompt,
            "duration": duration,
            "aspect_ratio": "16:9"
        }
        return await self._make_request("/t2v/fal/veo3/fast", data)
    
    # Video Analysis 機能
    async def gemini_video_analysis(self, video_path: str, prompt: str) -> Dict[str, Any]:
        """Gemini Video Analysis"""
        video_data = self._encode_video(video_path)
        data = {
            "video_url": f"data:video/mp4;base64,{video_data}",
            "prompt": prompt
        }
        return await self._make_request("/video-analysis/google/gemini", data)
    
    # ファイルアップロード機能
    async def upload_file(self, file_path: str) -> Dict[str, Any]:
        """File Upload to FAL"""
        file_data = self._encode_file(file_path)
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext in ['.jpg', '.jpeg', '.png', '.webp']:
            mime_type = f"image/{file_ext[1:]}"
        elif file_ext in ['.mp4', '.mov', '.avi']:
            mime_type = f"video/{file_ext[1:]}"
        else:
            mime_type = "application/octet-stream"
        
        data = {
            "file_data": file_data,
            "mime_type": mime_type,
            "filename": Path(file_path).name
        }
        return await self._make_request("/uploader/fal", data)
    
    def _encode_image(self, image_path: str) -> str:
        """画像をBase64エンコード"""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    
    def _encode_video(self, video_path: str) -> str:
        """動画をBase64エンコード"""
        with open(video_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    
    def _encode_file(self, file_path: str) -> str:
        """ファイルをBase64エンコード"""
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()

# ストーリーボード生成用のヘルパー関数
class StoryboardGenerator:
    def __init__(self, client: KamuiMCPClient):
        self.client = client
    
    async def generate_scene_images(self, scenes_yaml_path: str, output_dir: str = "generated_images"):
        """ストーリーボードシーンから画像を生成"""
        import yaml
        
        # シーンデータを読み込み
        with open(scenes_yaml_path, 'r', encoding='utf-8') as f:
            scenes_data = yaml.safe_load(f)
        
        # 出力ディレクトリを作成
        Path(output_dir).mkdir(exist_ok=True)
        
        results = []
        
        for scene_id, scene_data in scenes_data.get('scenes', {}).items():
            text_content = scene_data.get('text', '')
            script_content = scene_data.get('script', '')
            
            # テキストとスクリプトから画像生成プロンプトを作成
            prompt = f"ストーリーボードシーン: {text_content}\n\nスクリプト: {script_content}"
            
            try:
                # Flux Schnellで画像生成
                result = await self.client.flux_schnell_t2i(
                    prompt=prompt,
                    width=1024,
                    height=576  # 16:9 aspect ratio for storyboard
                )
                
                # 結果を保存
                output_path = f"{output_dir}/scene_{scene_id}.json"
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        'scene_id': scene_id,
                        'prompt': prompt,
                        'result': result
                    }, f, ensure_ascii=False, indent=2)
                
                results.append({
                    'scene_id': scene_id,
                    'status': 'success',
                    'output_path': output_path
                })
                
                print(f"✅ シーン {scene_id} の画像生成完了")
                
            except Exception as e:
                results.append({
                    'scene_id': scene_id,
                    'status': 'error',
                    'error': str(e)
                })
                print(f"❌ シーン {scene_id} の画像生成エラー: {e}")
        
        return results

# CLI インターフェース
async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Kamui Code MCP クライアント")
    parser.add_argument("command", choices=[
        "t2i-flux", "t2i-imagen3", "t2i-dreamina",
        "i2i-kontext", "i2i-upscale", "i2i-remix",
        "t2v-veo3", "video-analysis", "upload",
        "generate-storyboard"
    ])
    parser.add_argument("--prompt", help="生成プロンプト")
    parser.add_argument("--image", help="入力画像パス")
    parser.add_argument("--video", help="入力動画パス")
    parser.add_argument("--file", help="アップロードファイルパス")
    parser.add_argument("--scenes", help="シーンYAMLファイルパス")
    parser.add_argument("--output", help="出力ディレクトリ", default="output")
    
    args = parser.parse_args()
    
    try:
        client = KamuiMCPClient()
        
        if args.command == "t2i-flux":
            result = await client.flux_schnell_t2i(args.prompt)
        elif args.command == "t2i-imagen3":
            result = await client.imagen3_t2i(args.prompt)
        elif args.command == "t2i-dreamina":
            result = await client.dreamina_t2i(args.prompt)
        elif args.command == "i2i-kontext":
            result = await client.flux_kontext_i2i(args.image, args.prompt)
        elif args.command == "i2i-upscale":
            result = await client.aura_sr_upscale(args.image)
        elif args.command == "i2i-remix":
            result = await client.ideogram_character_remix(args.image, args.prompt)
        elif args.command == "t2v-veo3":
            result = await client.veo3_fast_t2v(args.prompt)
        elif args.command == "video-analysis":
            result = await client.gemini_video_analysis(args.video, args.prompt)
        elif args.command == "upload":
            result = await client.upload_file(args.file)
        elif args.command == "generate-storyboard":
            generator = StoryboardGenerator(client)
            result = await generator.generate_scene_images(args.scenes, args.output)
        
        # 結果を出力
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"エラー: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(asyncio.run(main()))

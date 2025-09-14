#!/usr/bin/env python3
"""
Kamui Code 簡単クライアント（同期版）
標準ライブラリのrequestsを使用してaiohttp依存を回避
"""

import requests
import base64
import json
import os
from pathlib import Path

class KamuiSimpleClient:
    def __init__(self):
        self.base_url = os.getenv("KAMUI_BASE_URL", "https://kamui-code.ai")
        self.token = os.getenv("KAMUI_TOKEN")
        
        if not self.token:
            raise ValueError("KAMUI_TOKEN環境変数が設定されていません")
    
    def _make_request(self, endpoint, data):
        """Kamui Code APIにリクエストを送信（同期版）"""
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=60)
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"API Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"リクエストエラー: {e}")
    
    def imagen3_t2i(self, prompt, aspect_ratio="1:1"):
        """Google Imagen 3 Text-to-Image（同期版）"""
        data = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "safety_tolerance": "BLOCK_ONLY_HIGH",
            "person_generation": "ALLOW_ADULT"
        }
        return self._make_request("/t2i/google/imagen", data)
    
    def flux_schnell_t2i(self, prompt, width=1024, height=1024):
        """Flux Schnell Text-to-Image（同期版）"""
        data = {
            "prompt": prompt,
            "width": width,
            "height": height,
            "num_inference_steps": 4,
            "guidance_scale": 0.0
        }
        return self._make_request("/t2i/fal/flux/schnell", data)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Kamui Code 簡単クライアント")
    parser.add_argument("command", choices=["imagen3", "flux"])
    parser.add_argument("--prompt", required=True, help="生成プロンプト")
    parser.add_argument("--aspect-ratio", default="1:1", help="アスペクト比（imagen3のみ）")
    
    args = parser.parse_args()
    
    try:
        client = KamuiSimpleClient()
        
        print(f"🎨 {args.command}で画像生成中...")
        print(f"プロンプト: {args.prompt}")
        
        if args.command == "imagen3":
            result = client.imagen3_t2i(args.prompt, args.aspect_ratio)
        elif args.command == "flux":
            result = client.flux_schnell_t2i(args.prompt)
        
        print("✅ 生成完了！")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

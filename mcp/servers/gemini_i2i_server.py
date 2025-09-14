#!/usr/bin/env python3
"""
Gemini Flash Image-to-Image MCPサーバー
Google Gemini Flash APIを使用したimage-to-image変換サーバー
"""

import asyncio
import base64
import json
import os
from typing import Any, Dict, List, Optional
import aiohttp
from mcp.server import Server
from mcp.types import Resource, Tool, TextContent, ImageContent

# 環境変数からAPIキーを取得
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

class GeminiI2IServer:
    def __init__(self):
        self.server = Server("gemini-flash-i2i")
        self.setup_handlers()
    
    def setup_handlers(self):
        """MCPサーバーのハンドラーを設定"""
        
        @self.server.list_resources()
        async def list_resources() -> List[Resource]:
            """利用可能なリソースを返す"""
            return [
                Resource(
                    uri="gemini://i2i/transform",
                    name="Image Transform",
                    description="画像を別のスタイルや形式に変換",
                    mimeType="application/json"
                ),
                Resource(
                    uri="gemini://i2i/enhance", 
                    name="Image Enhancement",
                    description="画像の品質向上・高解像度化",
                    mimeType="application/json"
                ),
                Resource(
                    uri="gemini://i2i/storyboard",
                    name="Storyboard Generation", 
                    description="ストーリーボード用画像生成",
                    mimeType="application/json"
                )
            ]
        
        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """リソースの詳細情報を返す"""
            if uri == "gemini://i2i/transform":
                return json.dumps({
                    "description": "画像変換API",
                    "parameters": {
                        "sourceImage": "Base64エンコードされた入力画像",
                        "prompt": "変換指示のプロンプト", 
                        "style": "出力画像のスタイル"
                    }
                })
            elif uri == "gemini://i2i/enhance":
                return json.dumps({
                    "description": "画像強化API",
                    "parameters": {
                        "sourceImage": "Base64エンコードされた入力画像",
                        "enhanceType": "強化の種類",
                        "factor": "強化の倍率"
                    }
                })
            elif uri == "gemini://i2i/storyboard":
                return json.dumps({
                    "description": "ストーリーボード生成API",
                    "parameters": {
                        "referenceImage": "参考画像（Base64）",
                        "sceneDescription": "シーンの説明",
                        "mood": "シーンの雰囲気"
                    }
                })
            else:
                raise ValueError(f"Unknown resource: {uri}")
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """利用可能なツールを返す"""
            return [
                Tool(
                    name="transform_image",
                    description="Gemini Flash APIを使用して画像を変換",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "image_data": {"type": "string", "description": "Base64エンコードされた画像データ"},
                            "prompt": {"type": "string", "description": "変換指示のプロンプト"},
                            "style": {"type": "string", "description": "出力スタイル"}
                        },
                        "required": ["image_data", "prompt"]
                    }
                ),
                Tool(
                    name="generate_storyboard_image",
                    description="ストーリーボード用の画像を生成",
                    inputSchema={
                        "type": "object", 
                        "properties": {
                            "scene_description": {"type": "string", "description": "シーンの説明"},
                            "reference_image": {"type": "string", "description": "参考画像（Base64、オプション）"},
                            "style": {"type": "string", "description": "画像スタイル"}
                        },
                        "required": ["scene_description"]
                    }
                ),
                Tool(
                    name="enhance_image",
                    description="画像の品質を向上させる",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "image_data": {"type": "string", "description": "Base64エンコードされた画像データ"},
                            "enhance_type": {"type": "string", "description": "強化の種類"},
                            "factor": {"type": "number", "description": "強化の倍率"}
                        },
                        "required": ["image_data", "enhance_type"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """ツールを実行"""
            if not GEMINI_API_KEY:
                return [TextContent(type="text", text="エラー: GEMINI_API_KEYが設定されていません")]
            
            try:
                if name == "transform_image":
                    result = await self.transform_image(
                        arguments["image_data"],
                        arguments["prompt"], 
                        arguments.get("style", "realistic")
                    )
                elif name == "generate_storyboard_image":
                    result = await self.generate_storyboard_image(
                        arguments["scene_description"],
                        arguments.get("reference_image"),
                        arguments.get("style", "sketch")
                    )
                elif name == "enhance_image":
                    result = await self.enhance_image(
                        arguments["image_data"],
                        arguments["enhance_type"],
                        arguments.get("factor", 2)
                    )
                else:
                    return [TextContent(type="text", text=f"未知のツール: {name}")]
                
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
                
            except Exception as e:
                return [TextContent(type="text", text=f"エラー: {str(e)}")]
    
    async def transform_image(self, image_data: str, prompt: str, style: str) -> Dict[str, Any]:
        """画像変換を実行"""
        payload = {
            "contents": [{
                "parts": [
                    {"text": f"以下の画像を{style}スタイルで変換してください。指示: {prompt}"},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_data
                        }
                    }
                ]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1024
            }
        }
        
        return await self.call_gemini_api(payload)
    
    async def generate_storyboard_image(self, scene_description: str, reference_image: Optional[str], style: str) -> Dict[str, Any]:
        """ストーリーボード画像生成を実行"""
        parts = [{"text": f"以下のシーン描写に基づいて{style}スタイルのストーリーボード画像を生成してください: {scene_description}"}]
        
        if reference_image:
            parts.append({
                "inline_data": {
                    "mime_type": "image/jpeg", 
                    "data": reference_image
                }
            })
        
        payload = {
            "contents": [{"parts": parts}],
            "generationConfig": {
                "temperature": 0.8,
                "maxOutputTokens": 1024
            }
        }
        
        return await self.call_gemini_api(payload)
    
    async def enhance_image(self, image_data: str, enhance_type: str, factor: float) -> Dict[str, Any]:
        """画像強化を実行"""
        enhancement_prompts = {
            "upscale": f"{factor}倍に高解像度化",
            "denoise": "ノイズを除去して鮮明に",
            "sharpen": "シャープネスを向上",
            "colorize": "色彩を豊かに"
        }
        
        prompt = enhancement_prompts.get(enhance_type, "画像を改善")
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": f"以下の画像を{prompt}してください"},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_data
                        }
                    }
                ]
            }],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 1024
            }
        }
        
        return await self.call_gemini_api(payload)
    
    async def call_gemini_api(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Gemini APIを呼び出し"""
        url = f"{GEMINI_BASE_URL}/models/gemini-2.0-flash-exp:generateContent"
        headers = {
            "x-goog-api-key": GEMINI_API_KEY,
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "data": result,
                        "message": "画像処理が完了しました"
                    }
                else:
                    error_text = await response.text()
                    return {
                        "success": False,
                        "error": f"API呼び出しエラー: {response.status}",
                        "details": error_text
                    }
    
    async def run(self):
        """サーバーを起動"""
        from mcp.server.stdio import stdio_server
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(read_stream, write_stream, self.server.create_initialization_options())

async def main():
    """メイン関数"""
    server = GeminiI2IServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())

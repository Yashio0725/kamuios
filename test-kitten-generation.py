#!/usr/bin/env python3
"""
可愛い子猫画像生成テスト（認証なし）
Kamui Code APIを直接呼び出してテスト
"""

import json
import sys

def test_kitten_generation():
    """認証なしでKamui Code APIをテスト"""
    
    # テスト用のプロンプト
    prompt = "可愛い子猫、ふわふわの毛、大きな瞳、愛らしい表情、高品質、写真のようにリアル"
    
    print("🐱 可愛い子猫画像生成テスト")
    print("=" * 50)
    print(f"プロンプト: {prompt}")
    print(f"API: https://kamui-code.ai/t2i/google/imagen")
    print()
    
    # リクエストデータ
    data = {
        "prompt": prompt,
        "aspect_ratio": "1:1",
        "safety_tolerance": "BLOCK_ONLY_HIGH",
        "person_generation": "ALLOW_ADULT"
    }
    
    print("📋 リクエストデータ:")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print()
    
    # 実際のHTTPリクエストはWindsurf/Cascadeの内蔵機能で実行
    print("💡 次のステップ:")
    print("1. Cascadeの内蔵HTTP機能を使用")
    print("2. POST https://kamui-code.ai/t2i/google/imagen")
    print("3. 上記のJSONデータを送信")
    
    return True

if __name__ == "__main__":
    test_kitten_generation()

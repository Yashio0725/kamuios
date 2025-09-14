#!/usr/bin/env python3
"""
可愛い子猫画像生成スクリプト
requestsライブラリを使用（最も実用的な方法）
"""

import json
import os
import sys

def generate_kitten_with_requests():
    """requestsを使って子猫画像を生成"""
    try:
        import requests
    except ImportError:
        print("❌ requestsライブラリが必要です")
        print("インストール方法:")
        print("  pip3 install --user requests")
        print("または:")
        print("  sudo apt install python3-requests")
        return False
    
    # 環境変数チェック
    token = os.getenv("KAMUI_TOKEN")
    if not token:
        print("❌ KAMUI_TOKENが設定されていません")
        print("設定方法:")
        print('  export KAMUI_TOKEN="your-token-here"')
        return False
    
    # API設定
    base_url = "https://kamui-code.ai"
    endpoint = "/t2i/google/imagen"
    url = f"{base_url}{endpoint}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 可愛い子猫のプロンプト
    data = {
        "prompt": "可愛い子猫、ふわふわの毛、大きな瞳、愛らしい表情、高品質、写真のようにリアル",
        "aspect_ratio": "1:1",
        "safety_tolerance": "BLOCK_ONLY_HIGH",
        "person_generation": "ALLOW_ADULT"
    }
    
    print("🐱 可愛い子猫の画像を生成中...")
    print(f"API: {url}")
    print(f"プロンプト: {data['prompt']}")
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 生成成功！")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return True
        else:
            print(f"❌ API エラー: {response.status_code}")
            print(f"レスポンス: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ タイムアウト: APIの応答が遅すぎます")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ リクエストエラー: {e}")
        return False

def generate_kitten_with_urllib():
    """標準ライブラリ（urllib）を使って子猫画像を生成（複雑版）"""
    import urllib.request
    import urllib.parse
    
    # 環境変数チェック
    token = os.getenv("KAMUI_TOKEN")
    if not token:
        print("❌ KAMUI_TOKENが設定されていません")
        return False
    
    # API設定
    base_url = "https://kamui-code.ai"
    endpoint = "/t2i/google/imagen"
    url = f"{base_url}{endpoint}"
    
    # データ準備
    data = {
        "prompt": "可愛い子猫、ふわふわの毛、大きな瞳、愛らしい表情、高品質、写真のようにリアル",
        "aspect_ratio": "1:1",
        "safety_tolerance": "BLOCK_ONLY_HIGH",
        "person_generation": "ALLOW_ADULT"
    }
    
    # JSONエンコード
    json_data = json.dumps(data).encode('utf-8')
    
    # リクエスト作成
    req = urllib.request.Request(
        url,
        data=json_data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method='POST'
    )
    
    print("🐱 可愛い子猫の画像を生成中（標準ライブラリ版）...")
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            if response.status == 200:
                result = json.loads(response.read().decode('utf-8'))
                print("✅ 生成成功！")
                print(json.dumps(result, ensure_ascii=False, indent=2))
                return True
            else:
                print(f"❌ API エラー: {response.status}")
                return False
                
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def main():
    print("🎨 Kamui Code Imagen3 子猫画像生成")
    print("=" * 50)
    
    # まずrequests版を試す
    print("\n📦 Method 1: requests ライブラリ使用（推奨）")
    if generate_kitten_with_requests():
        return 0
    
    # requestsが使えない場合は標準ライブラリ版
    print("\n📚 Method 2: 標準ライブラリ使用（フォールバック）")
    if generate_kitten_with_urllib():
        return 0
    
    print("\n❌ 両方の方法で失敗しました")
    return 1

if __name__ == "__main__":
    exit(main())

# Gemini Flash i2i MCPサーバー セットアップガイド

このガイドでは、Gemini Flash Image-to-Image MCPサーバーをセットアップして、Cascadeから直接i2i機能を使用する方法を説明します。

## 🚀 クイックスタート

### 1. 必要な依存関係のインストール

```bash
cd ~/kamuios
pip3 install --user aiohttp mcp
```

### 2. Gemini API キーの設定

```bash
# 環境変数を設定
export GEMINI_API_KEY="your-gemini-api-key-here"

# 永続化する場合は ~/.bashrc に追加
echo 'export GEMINI_API_KEY="your-gemini-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### 3. MCPサーバーの実行権限設定

```bash
chmod +x mcp/servers/gemini_i2i_server.py
```

## 📋 設定ファイル

### 作成されたファイル

- `mcp/mcp-gemini-i2i.json` - Gemini i2i MCP設定
- `mcp/config.json` - 更新されたメインMCP設定
- `mcp/servers/gemini_i2i_server.py` - MCPサーバー実装

### WindsurfでのMCP設定

Windsurfの設定ファイル（通常は `~/.config/windsurf/settings.json`）に以下を追加：

```json
{
  "mcp.servers": {
    "gemini-flash-i2i": {
      "command": "python3",
      "args": ["/home/yn090/kamuios/mcp/servers/gemini_i2i_server.py"],
      "env": {
        "GEMINI_API_KEY": "${GEMINI_API_KEY}"
      }
    }
  }
}
```

## 🎯 利用可能な機能

### 1. Image Transform（画像変換）

**機能**: 画像を別のスタイルや形式に変換

**使用例**:
```
transform_image({
  "image_data": "base64-encoded-image",
  "prompt": "この画像をアニメ風に変換してください",
  "style": "anime"
})
```

### 2. Storyboard Generation（ストーリーボード生成）

**機能**: シーン描写からストーリーボード画像を生成

**使用例**:
```
generate_storyboard_image({
  "scene_description": "暗闇の中から巨大なモンスターがゆっくりと姿を現す",
  "style": "sketch"
})
```

### 3. Image Enhancement（画像強化）

**機能**: 画像の品質向上・高解像度化

**使用例**:
```
enhance_image({
  "image_data": "base64-encoded-image", 
  "enhance_type": "upscale",
  "factor": 2
})
```

## 🔧 Cascadeからの使用方法

### MCPリソースの確認

```
list_resources("gemini-flash-i2i")
```

### リソースの詳細取得

```
read_resource("gemini-flash-i2i", "gemini://i2i/transform")
```

### ツールの実行

Cascadeから直接ツールを呼び出すことができます：

1. **画像変換**: `transform_image`
2. **ストーリーボード生成**: `generate_storyboard_image`
3. **画像強化**: `enhance_image`

## 🎨 ストーリーボードビューアーとの連携

### シーン画像の自動生成

`data/storyboard-scenes.yaml`のシーン描写を使用して、自動的にストーリーボード画像を生成できます：

```bash
# シーンデータから画像生成スクリプト（今後実装予定）
python3 scripts/generate-storyboard-images.py
```

### 既存画像の変換

ストーリーボードビューアーの既存画像を別のスタイルに変換：

1. 元画像をBase64エンコード
2. `transform_image`ツールで変換
3. 生成された画像をストーリーボードに適用

## 📊 サポートされる画像形式

### 入力形式
- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)

### 出力形式
- JPEG (.jpg)
- PNG (.png)

## 🎭 スタイルオプション

### 画像変換スタイル
- `realistic` - リアルスティック
- `anime` - アニメ風
- `sketch` - スケッチ風
- `oil-painting` - 油絵風
- `watercolor` - 水彩画風

### 強化タイプ
- `upscale` - 高解像度化
- `denoise` - ノイズ除去
- `sharpen` - シャープネス向上
- `colorize` - 色彩強化

## ⚠️ 注意事項

### API制限
- Gemini APIの利用制限に注意
- 大きな画像ファイルは処理時間が長くなる可能性
- API キーは安全に管理してください

### トラブルシューティング

#### MCPサーバーが起動しない場合
1. Python依存関係を確認: `pip3 list | grep -E "(aiohttp|mcp)"`
2. API キーが設定されているか確認: `echo $GEMINI_API_KEY`
3. ファイルの実行権限を確認: `ls -la mcp/servers/gemini_i2i_server.py`

#### API呼び出しエラーの場合
1. API キーの有効性を確認
2. Gemini APIの利用制限を確認
3. ネットワーク接続を確認

## 🔄 今後の拡張予定

- **バッチ処理**: 複数画像の一括変換
- **カスタムスタイル**: ユーザー定義スタイルの追加
- **自動化スクリプト**: ストーリーボードの自動画像生成
- **キャッシュ機能**: 生成済み画像のキャッシュ

## 📞 サポート

問題が発生した場合は、以下を確認してください：

1. `~/kamuios/docs/storyboard-management.md` - ストーリーボード管理
2. `~/kamuios/mcp/` - MCP設定ファイル
3. ログファイル（実行時に出力される）

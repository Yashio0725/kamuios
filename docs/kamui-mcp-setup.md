# Kamui Code MCP サーバー セットアップガイド

このガイドでは、Kamui CodeのMCPサーバー群をセットアップして、Cascadeから直接AI機能を使用する方法を説明します。

## 🚀 クイックスタート

### 1. 環境セットアップ

```bash
cd ~/kamuios

# 依存関係のインストールとセットアップ
make kamui-setup
```

### 2. Kamui Token の設定

```bash
# 環境変数を設定（セッション用）
export KAMUI_TOKEN="your-kamui-token-here"

# 永続化する場合は ~/.bashrc に追加
echo 'export KAMUI_TOKEN="your-kamui-token-here"' >> ~/.bashrc
source ~/.bashrc
```

### 3. 動作テスト

```bash
# Text-to-Image生成テスト
make kamui-t2i PROMPT="美しい日本の風景"

# ストーリーボード画像自動生成テスト
make kamui-storyboard
```

## 📋 利用可能なMCPサーバー

### 🎨 Text-to-Image (t2i) サーバー

| サーバー名 | 説明 | 特徴 |
|-----------|------|------|
| `flux-schnell` | Flux-1 Schnell (Fast) | 高速生成、4ステップ |
| `imagen3` | Google Imagen 3 | 高品質、多様なアスペクト比 |
| `dreamina-v31` | Bytedance Dreamina v3.1 | リアルスティック |
| `imagen4-fast` | Imagen4 Fast | 速度重視 |
| `imagen4-ultra` | Imagen4 Ultra | 最高品質 |
| `qwen-image` | Qwen-Image | 中国語対応 |
| `wan-v2-2-a14b` | WAN v2.2-a14b | アニメスタイル |

### 🖼️ Image-to-Image (i2i) サーバー

| サーバー名 | 説明 | 用途 |
|-----------|------|------|
| `aura-sr` | AuraSR Upscaling | 画像高解像度化 |
| `flux-kontext` | Flux Kontext LoRA | スタイル変換 |
| `flux-kontext-max` | Flux Kontext Max | 高品質変換 |
| `ideogram-character-remix` | Character Remix | キャラクター変換 |
| `qwen-image-edit` | Qwen Image Edit | AI画像編集 |

### 🎬 Text-to-Video (t2v) サーバー

| サーバー名 | 説明 | 特徴 |
|-----------|------|------|
| `veo3-fast` | Veo3 Fast | 高速動画生成 |
| `wan-v2-2-5b-fast` | WAN v2.2-5b Fast | アニメ動画 |

### 🎥 Video Analysis サーバー

| サーバー名 | 説明 | 機能 |
|-----------|------|------|
| `video-analysis-gemini` | Gemini Video Analysis | 動画内容解析 |

## 🛠️ 使用方法

### Makefileコマンド

#### Text-to-Image生成
```bash
make kamui-t2i PROMPT="生成したい画像の説明"
```

**例:**
```bash
make kamui-t2i PROMPT="夕日に照らされた桜並木、アニメスタイル"
make kamui-t2i PROMPT="未来都市の夜景、サイバーパンク"
```

#### Image-to-Image変換
```bash
make kamui-i2i IMAGE="path/to/image.jpg" PROMPT="変換指示"
```

**例:**
```bash
make kamui-i2i IMAGE="input.jpg" PROMPT="この写真をアニメ風に変換"
make kamui-i2i IMAGE="sketch.png" PROMPT="このスケッチを油絵風に"
```

#### ストーリーボード画像自動生成
```bash
make kamui-storyboard
```

### Pythonスクリプト直接実行

#### 基本的な使用例

```bash
# Flux Schnell Text-to-Image
python3 scripts/kamui-mcp-client.py t2i-flux --prompt "美しい風景"

# Google Imagen 3 Text-to-Image  
python3 scripts/kamui-mcp-client.py t2i-imagen3 --prompt "未来の都市"

# Flux Kontext Image-to-Image
python3 scripts/kamui-mcp-client.py i2i-kontext --image input.jpg --prompt "アニメスタイルに変換"

# AuraSR 画像アップスケール
python3 scripts/kamui-mcp-client.py i2i-upscale --image low_res.jpg

# Veo3 Text-to-Video
python3 scripts/kamui-mcp-client.py t2v-veo3 --prompt "猫が遊んでいる様子"

# ファイルアップロード
python3 scripts/kamui-mcp-client.py upload --file image.jpg
```

## 🎭 ストーリーボードビューアーとの連携

### 自動画像生成ワークフロー

1. **シーンデータ編集**
   ```bash
   make edit-scenes
   ```

2. **画像自動生成**
   ```bash
   make kamui-storyboard
   ```

3. **ストーリーボード更新**
   ```bash
   make build-storyboard
   ```

### 生成された画像の活用

生成された画像は `generated_storyboard_images/` フォルダに保存されます：

```
generated_storyboard_images/
├── scene_1.json          # シーン1の生成結果
├── scene_2.json          # シーン2の生成結果
└── ...
```

各JSONファイルには以下の情報が含まれます：
- `scene_id`: シーンID
- `prompt`: 使用されたプロンプト
- `result`: API応答結果（画像URLなど）

## 🔧 WindsurfでのMCP設定

### 設定ファイルの場所

Windsurfの設定ファイル（`~/.config/windsurf/settings.json`）に以下を追加：

```json
{
  "mcp.servers": {
    "kamui-t2i-flux": {
      "command": "python3",
      "args": ["/home/yn090/kamuios/scripts/kamui-mcp-client.py", "t2i-flux"],
      "env": {
        "KAMUI_TOKEN": "${KAMUI_TOKEN}"
      }
    },
    "kamui-i2i-kontext": {
      "command": "python3", 
      "args": ["/home/yn090/kamuios/scripts/kamui-mcp-client.py", "i2i-kontext"],
      "env": {
        "KAMUI_TOKEN": "${KAMUI_TOKEN}"
      }
    }
  }
}
```

### Cascadeからの使用

Cascadeから直接MCPサーバーを呼び出すことができます：

```
# リソース一覧取得
list_resources("kamui-t2i-flux")

# ツール実行
call_tool("kamui-t2i-flux", "generate_image", {
  "prompt": "美しい風景画",
  "width": 1024,
  "height": 1024
})
```

## 📊 サポートされる形式

### 入力画像形式
- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)

### 出力形式
- 画像: JPEG, PNG
- 動画: MP4
- JSON: API応答データ

## 🎨 プロンプト作成のコツ

### Text-to-Image
```
良い例:
- "夕日に照らされた桜並木、アニメスタイル、高品質"
- "未来都市の夜景、ネオンライト、サイバーパンク、4K"

避けるべき:
- "きれいな絵"（曖昧すぎる）
- "写真"（具体性不足）
```

### Image-to-Image
```
良い例:
- "この写真をジブリ映画のようなアニメスタイルに変換"
- "スケッチを油絵風の絵画に変換、暖かい色調で"

避けるべき:
- "変換して"（指示が不明確）
- "良くして"（目標が不明）
```

## ⚠️ 注意事項とトラブルシューティング

### API制限
- Kamui Code APIの利用制限に注意
- 大きなファイルは処理時間が長くなる可能性
- トークンは安全に管理してください

### よくある問題

#### 1. "KAMUI_TOKEN環境変数が設定されていません"
```bash
export KAMUI_TOKEN="your-token-here"
```

#### 2. "ModuleNotFoundError: No module named 'aiohttp'"
```bash
make kamui-setup
```

#### 3. "Permission denied"
```bash
chmod +x scripts/kamui-mcp-client.py
```

#### 4. API呼び出しエラー
- トークンの有効性を確認
- ネットワーク接続を確認
- API利用制限を確認

## 🔄 今後の拡張予定

- **バッチ処理**: 複数画像の一括処理
- **カスタムプリセット**: よく使うプロンプトの保存
- **品質設定**: 生成品質の詳細調整
- **進捗表示**: 長時間処理の進捗確認
- **結果管理**: 生成結果の整理・検索機能

## 📞 サポート

問題が発生した場合は、以下を確認してください：

1. **環境設定**: `echo $KAMUI_TOKEN`
2. **依存関係**: `pip3 list | grep -E "(aiohttp|pyyaml)"`
3. **ファイル権限**: `ls -la scripts/kamui-mcp-client.py`
4. **ログ確認**: スクリプト実行時の出力メッセージ

## 📚 関連ドキュメント

- [ストーリーボード管理](./storyboard-management.md)
- [MCP設定](./mcp-setup.md)
- [Kamui Code API仕様](https://api.kamui.code/docs)

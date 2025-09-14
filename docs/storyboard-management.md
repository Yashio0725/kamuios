# ストーリーボードビューアー管理システム

このシステムを使用すると、ストーリーボードのTEXTとSCRIPT部分を外部ファイルで管理し、自動でstoryboard-viewer.yamlに反映できます。

## 🚀 クイックスタート

**シーンの内容を変更したい場合：**

1. **編集開始**
   ```bash
   cd ~/kamuios
   make edit-scenes
   ```

2. **内容を変更** - YAMLファイルでシーンのtextやscriptを編集

3. **反映実行**
   ```bash
   make build-storyboard
   ```

4. **確認** - localhost:1313のストーリーボードビューアーで確認

**これだけです！** 🎉

## ファイル構成

```
kamuios/
├── data/
│   ├── storyboard-scenes.yaml          # シーンデータ（編集対象）
│   └── saas/
│       └── storyboard-viewer.yaml      # ストーリーボードビューアー（自動生成）
├── scripts/
│   └── build-storyboard-simple.py      # ビルドスクリプト
├── Makefile                            # 便利コマンド
└── docs/
    └── storyboard-management.md        # このファイル
```

## 使用方法

### 1. シーンデータの編集

```bash
# シーンデータファイルを編集
make edit-scenes
```

または直接ファイルを編集：
```bash
nano data/storyboard-scenes.yaml
```

### 2. ストーリーボードビューアーに反映

```bash
# シーンデータをYAMLに反映
make build-storyboard
```

## シーンデータファイルの形式

`data/storyboard-scenes.yaml`の構造：

```yaml
scenes:
  - id: 1
    cut: "001"
    time: "3秒"
    text: |
      映像の描写内容（HTMLタグ使用可）
      複数行にわたって記述可能
    script: |
      音響効果の内容（HTMLタグ使用可）
      BGM、SE、環境音などを記述
```

### フィールド説明

- **id**: シーン番号（1-10）
- **cut**: カット番号（"001", "002"など）
- **time**: 表示時間
- **text**: 映像の描写（カメラワーク、キャラクターの動きなど）
- **script**: 音響効果（BGM、SE、環境音など）

## 📝 具体的な編集例

### シーン1のテキストを変更する場合

```yaml
scenes:
  - id: 1
    cut: "001"
    time: "3秒"
    text: |
      新しい映像の描写をここに記述<br>
      カメラワークや演出の詳細<br>
      キャラクターの動きなど
    script: |
      BGM: 新しい音楽の指定<br>
      SE: 効果音の詳細<br>
      環境音: 背景音の設定
```

### 複数シーンを一度に変更

YAMLファイルなので、複数のシーンを同時に編集できます。インデントに注意して編集してください。

## 編集のワークフロー

1. `data/storyboard-scenes.yaml`を編集
2. `make build-storyboard`でYAMLに反映
3. ストーリーボードビューアーで確認

## 注意事項

- HTMLタグ（`<br>`など）をそのまま使用可能
- YAMLの`|`記法で複数行テキストを記述可能
- 見開きビューと縦並びビューの両方に自動反映されます
- バックアップを取ってから編集することを推奨

## トラブルシューティング

### エラーが発生した場合

1. YAMLファイルの構文をチェック（インデントに注意）
2. 必要なファイルが存在するか確認
3. Pythonが正しくインストールされているか確認
4. PyYAMLライブラリがインストールされているか確認

### 手動での復元

万が一問題が発生した場合は、gitで前の状態に戻せます：

```bash
git checkout HEAD -- data/saas/storyboard-viewer.yaml
```

## ❓ よくある質問（FAQ）

### Q: シーンを追加・削除したい場合は？

A: 現在は10シーン固定です。シーン数を変更する場合は、storyboard-viewer.yamlのテンプレート部分も修正が必要です。

### Q: 画像や動画ファイルを変更したい場合は？

A: 画像・動画ファイルの変更は、storyboard-viewer.yaml内の`data-sketch-src`や`data-live-src`属性を直接編集してください。

### Q: エディタが開かない場合は？

A: 以下のコマンドで直接編集できます：
```bash
nano ~/kamuios/data/storyboard-scenes.yaml
```

### Q: 変更が反映されない場合は？

A: 以下を確認してください：
1. `make build-storyboard`を実行したか
2. YAMLの構文エラーがないか
3. ブラウザでページを再読み込みしたか

### Q: バックアップを取りたい場合は？

A: 以下のコマンドでバックアップできます：
```bash
cp data/storyboard-scenes.yaml data/storyboard-scenes.yaml.backup
```

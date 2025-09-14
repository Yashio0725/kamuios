# ストーリーボードビューアー管理用Makefile

.PHONY: build-storyboard edit-scenes help kamui-setup kamui-t2i kamui-i2i kamui-storyboard

# デフォルトターゲット
help:
	@echo "🎬 ストーリーボードビューアー管理コマンド"
	@echo ""
	@echo "📝 ストーリーボード編集:"
	@echo "  make build-storyboard  - シーンデータをstoryboard-viewer.yamlに反映"
	@echo "  make edit-scenes       - シーンデータファイルを編集用に開く"
	@echo ""
	@echo "🤖 Kamui MCP サーバー:"
	@echo "  make kamui-setup       - Kamui MCP環境をセットアップ"
	@echo "  make kamui-t2i         - Text-to-Image生成（プロンプト指定）"
	@echo "  make kamui-i2i         - Image-to-Image変換（画像・プロンプト指定）"
	@echo "  make kamui-storyboard  - ストーリーボード画像自動生成"
	@echo ""
	@echo "  make help             - このヘルプを表示"

# シーンデータをYAMLに反映
build-storyboard:
	@echo "🎭 ストーリーボードをビルド中..."
	python3 scripts/build-storyboard-simple.py

# シーンデータファイルを編集
edit-scenes:
	@echo "📝 シーンデータファイルを開きます..."
	@echo "ファイル: data/storyboard-scenes.yaml"
	@if command -v code >/dev/null 2>&1; then \
		code data/storyboard-scenes.yaml; \
	elif command -v nano >/dev/null 2>&1; then \
		nano data/storyboard-scenes.yaml; \
	else \
		echo "エディタが見つかりません。手動でファイルを編集してください。"; \
	fi

# Kamui MCP環境セットアップ
kamui-setup:
	@echo "🤖 Kamui MCP環境をセットアップ中..."
	@echo "必要な依存関係をインストール..."
	pip3 install --user aiohttp pyyaml
	@echo "実行権限を設定..."
	chmod +x scripts/kamui-mcp-client.py
	@echo "✅ セットアップ完了！"
	@echo ""
	@echo "📋 次のステップ:"
	@echo "1. KAMUI_TOKENを設定: export KAMUI_TOKEN='your-token'"
	@echo "2. テスト実行: make kamui-t2i PROMPT='美しい風景'"

# Text-to-Image生成
kamui-t2i:
	@if [ -z "$(PROMPT)" ]; then \
		echo "❌ PROMPTを指定してください: make kamui-t2i PROMPT='生成したい画像の説明'"; \
		exit 1; \
	fi
	@echo "🎨 Text-to-Image生成中..."
	@echo "プロンプト: $(PROMPT)"
	python3 scripts/kamui-mcp-client.py t2i-flux --prompt "$(PROMPT)" --output generated_images

# Image-to-Image変換
kamui-i2i:
	@if [ -z "$(IMAGE)" ] || [ -z "$(PROMPT)" ]; then \
		echo "❌ IMAGEとPROMPTを指定してください:"; \
		echo "   make kamui-i2i IMAGE='path/to/image.jpg' PROMPT='変換指示'"; \
		exit 1; \
	fi
	@echo "🖼️ Image-to-Image変換中..."
	@echo "入力画像: $(IMAGE)"
	@echo "プロンプト: $(PROMPT)"
	python3 scripts/kamui-mcp-client.py i2i-kontext --image "$(IMAGE)" --prompt "$(PROMPT)" --output generated_images

# ストーリーボード画像自動生成
kamui-storyboard:
	@echo "📚 ストーリーボード画像を自動生成中..."
	@if [ ! -f "data/storyboard-scenes.yaml" ]; then \
		echo "❌ data/storyboard-scenes.yamlが見つかりません"; \
		exit 1; \
	fi
	python3 scripts/kamui-mcp-client.py generate-storyboard --scenes data/storyboard-scenes.yaml --output generated_storyboard_images
	@echo "✅ 生成完了！generated_storyboard_images/ フォルダを確認してください"

# kamuiosプロジェクト開発ワークフローガイド

## 🔄 推奨開発フロー

### 1. MCPツールで要件定義書作成
```bash
# MCPツール実行（Claude Code / Cursor等で）
mcp19_create_requirement
```

### 2. 要件定義書プレビュー確認
```bash
# ブラウザで開く
open requirements-preview.html
```
- YAMLファイルを選択: `data/saas/requirements-*.yaml`
- マーメイド図付きで内容確認
- タブ切り替えで全セクション検証

### 3. 企画書詳細化（オプション）
- 要件定義書をベースにMarkdown企画書作成
- ビジネス分析・KPI・リスク分析を追加
- `docs/*-proposal.md` として保存

### 4. 実装フェーズ
- 要件定義書の技術スタック・アーキテクチャ図を参照
- ガントチャートに従って開発進行
- AIに具体的な実装指示

## 📁 ファイル構成

```
kamuios/
├── data/saas/
│   └── requirements-*.yaml          # 要件定義書（構造化データ）
├── docs/
│   ├── *-proposal.md               # 企画書（詳細分析）
│   └── requirements-creation-guide.md
├── requirements-preview.html       # プレビューツール
└── mermaid-test*.html              # テスト用ファイル
```

## 🎯 このワークフローの特徴

- **構造化データ先行**: YAMLの体系的な構造が基盤
- **MCPツール活用**: AI支援で効率的な要件定義
- **即座にプレビュー**: Hugoサーバー不要で確認可能
- **マーメイド図対応**: アーキテクチャ・ガント・フローチャート表示
- **段階的詳細化**: YAML→プレビュー→企画書→実装

## 🔧 使用ツール

- **MCP**: `mcp19_create_requirement` - 要件定義書生成
- **プレビュー**: `requirements-preview.html` - ブラウザ確認
- **マーメイド**: 図表の視覚化
- **YAML**: 構造化データ管理

---

このワークフローにより、アイデアから実装まで体系的かつ効率的に進められます。

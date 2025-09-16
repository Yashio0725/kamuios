# Kamuios AI従業員システム使用ガイド

## 概要

Kamuiosプロジェクトでは、特定の役割を持つAI「従業員」を定義し、専門的なタスクを効率的に実行できます。各従業員はYAMLファイルで定義され、役割、責任、具体的な作業手順が記載されています。

## 従業員システムの構造

### ファイル構成
```
data/saas/
├── employees_requirements-docs-agent.yaml  # エミリー（要件定義執筆担当）
├── employees_designer-agent.yaml           # サラ（デザイナー）
├── employees_hiring-agent.yaml             # トム（採用担当）
└── employees_private-saas-developer.yaml   # ケンジ（プライベートSaaS開発）
```

### チームダッシュボード
- `data/saas/prompts-repo.yaml`でチーム状況を可視化
- 各従業員のタスク進捗をリアルタイム表示

## エミリー（要件定義執筆担当）の使用例

### 1. 基本情報
- **名前**: エミリー
- **役割**: 要件定義執筆担当（KAMUI OS / KAMUI CODE）
- **専門分野**: 要件定義書の作成・編集・導線調整
- **YAMLファイル**: `employees_requirements-docs-agent.yaml`

### 2. 使用手順

#### Step 1: YAMLファイルの準備
```bash
# エミリーのYAMLファイルを開く
code data/saas/employees_requirements-docs-agent.yaml
```

#### Step 2: 依頼内容の更新
YAMLファイル内の「依頼テンプレート」セクションを実際のタスクに合わせて編集：

```yaml
## 依頼テンプレート（本件の要望）
- ECサイト要件定義書を作成してください。
  - `id: requirements-ecommerce`、カテゴリは「要件定義・開発」
  - 機能要件（商品管理/カート/決済/在庫/顧客管理）を含むこと
  - 非機能要件（セキュリティ/パフォーマンス/可用性）を明記
  - UIフロー（Mermaid図）と実装計画を含むこと
```

#### Step 3: AIへの指示
1. 更新したYAMLファイル全体をコピー
2. Claude/ChatGPTなどのAIツールに貼り付け
3. 「この従業員の指示に従って作業してください」と依頼

#### Step 4: 作業実行
AIが以下の手順で自動実行：
1. `data/saas/requirements-ecommerce.yaml`ファイル作成
2. 画像を`static/images/`に配置
3. カード一覧への追加（`themes/kamui-docs/layouts/index.html`）
4. TOCへの登録（`themes/kamui-docs/static/js/main.js`）
5. 動作確認（`hugo server -D`で`#requirements-ecommerce`をテスト）

#### Step 5: タスク完了の更新
```yaml
employee:
  name: エミリー
  role: 要件定義執筆
  tasks:
    - title: ECサイト要件定義書 執筆
      status: done  # doing → done に変更
```

### 3. エミリーの作業範囲

#### 得意な作業
- 新規要件定義書の作成
- 既存要件書の編集・更新
- カード導線の調整
- TOC構造の最適化
- Hugo テンプレートとの連携

#### 作業成果物
- 構造化されたYAML要件定義書
- カード形式の概要表示
- 詳細な機能・非機能要件
- Mermaid図によるフロー表現
- 実装計画とガントチャート

### 4. 実際の使用例

#### 既存の作業実績
エミリーが作成済みの要件定義書：
- `requirements-neko-cafe.yaml` - ネコカフェシステム
- `requirements-kamui-os.yaml` - KAMUI OS基盤
- `requirements-document.yaml` - KAMUI CODE

#### 現在のタスク状況
```yaml
tasks:
  - title: KAMUI OS 要件定義書 執筆
    status: doing
  - title: KAMUI OS NPM 要件定義書 執筆  
    status: doing
  - title: SNSマーケダッシュボード 要件定義書 執筆
    status: doing
```

## 他の従業員との連携

### サラ（デザイナー）
- UI/UXデザイン
- コンポーネント設計
- レスポンシブ最適化

### トム（採用担当）
- 新しいAI従業員の追加
- YAMLファイルの作成
- チーム構成の管理

### ケンジ（プライベートSaaS開発）
- セキュリティ機能
- 認証システム
- プライベート機能開発

## ベストプラクティス

### 1. 事前準備
- YAMLファイルの依頼テンプレートを必ず更新
- 具体的で明確な指示を記載
- 成果物の形式を明確に指定

### 2. 作業中
- AIに全体のYAMLファイルを渡す
- 段階的な確認を行う
- エラーが発生した場合は手順を見直す

### 3. 作業後
- 成果物の動作確認
- タスクステータスの更新
- チームダッシュボードでの進捗確認

## トラブルシューティング

### よくある問題
1. **YAML文法エラー**: バッククォートやコロンを含む場合は値をダブルクォートで囲む
2. **目次の重複**: `main.js`の並べ替え時に重複除外済み。新規子追加時はIDの重複に注意
3. **直リンクで本文が開かない**: `requirementsDocCard-<sectionId>`と`requirementsDocBody-<sectionId>`のID整合を確認

### デバッグ手順
1. `hugo server -D`でローカル確認
2. ブラウザ開発者ツールでエラーチェック
3. YAMLファイルの構文確認
4. パスの整合性確認

## まとめ

Kamuios AI従業員システムは、専門的なタスクを効率的に実行するための強力なツールです。エミリーを例にした要件定義書作成は、システムの典型的な使用例です。適切な準備と手順に従うことで、高品質な成果物を短時間で作成できます。

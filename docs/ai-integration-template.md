# AI統合テンプレート

MCPで要件定義書を生成した後、以下のプロンプトでAIに統合を依頼してください。

## 統合依頼プロンプト

```
上記で生成された要件定義書を、kamuiosプロジェクトの標準形式に変換して統合してください。

### 統合手順:
1. 生成された要件定義書の内容を解析
2. 以下のYAML構造に変換:
   - id: requirements-{プロジェクト名}
   - category: 2 (要件定義・開発)
   - 標準的なtabs構造
   - overview_cards, functional_requirements, non_functional_requirements
   - user_personas, mermaid図, gantt図
3. data/saas/requirements-{プロジェクト名}.yaml として保存
4. 必要に応じてナビゲーション更新の案内

### 参考ファイル:
- data/saas/requirements-document.yaml (構造の参考)
- docs/requirements-creation-guide.md (詳細仕様)

プロジェクト名: {ここにプロジェクト名を入力}
```

## 使用例

### ステップ1: MCP実行
Claude CodeまたはCursorで要件定義書MCPを実行

### ステップ2: 統合依頼
```
上記で生成されたネコカフェ予約システムの要件定義書を、kamuiosプロジェクトの標準形式に変換して統合してください。

プロジェクト名: neko-cafe

参考ファイル:
- data/saas/requirements-document.yaml
- docs/requirements-creation-guide.md
```

### ステップ3: 確認
```
hugo server -D
http://localhost:1313/#requirements-neko-cafe
```

## AIが実行すべき具体的作業

1. **YAML変換**
   - MCPの出力をプロジェクト標準形式に変換
   - 必須フィールドの補完
   - 日本語対応の確認

2. **ファイル保存**
   - `data/saas/requirements-{プロジェクト名}.yaml` に保存
   - 適切なエンコーディング（UTF-8）で保存

3. **ナビゲーション更新**
   - `themes/kamui-docs/layouts/index.html` の requirements-document ブロックにカード追加
   - または更新手順の案内

4. **表示確認**
   - Hugo サーバーでの表示確認
   - リンクとナビゲーションの動作確認

## 期待される結果

- 美しく構造化された要件定義書がプロジェクトに統合される
- 既存のフレームワークで完全に表示される
- ナビゲーションから直接アクセス可能
- 他の要件定義書と一貫したデザイン・構造

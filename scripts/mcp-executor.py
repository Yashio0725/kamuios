#!/usr/bin/env python3
"""
プロジェクト内MCP実行環境
外部MCPサーバーを直接呼び出してプロジェクトに統合
"""

import json
import yaml
import os
import sys
from pathlib import Path
import subprocess
import tempfile

class ProjectMCPExecutor:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.mcp_dir = self.project_root / "mcp"
        
    def execute_requirements_mcp(self, prompt: str, project_name: str):
        """要件定義書MCPを実行してプロジェクトに統合"""
        
        # 1. 外部MCPサーバーまたはローカルMCPを実行
        requirements_data = self._call_mcp_server(prompt)
        
        # 2. プロジェクト形式に変換
        yaml_content = self._convert_to_project_format(requirements_data, project_name)
        
        # 3. ファイル保存
        self._save_requirements_file(yaml_content, project_name)
        
        # 4. 統合完了の案内
        self._show_integration_guide(project_name)
    
    def _call_mcp_server(self, prompt: str) -> dict:
        """MCPサーバーを呼び出し（実装方法は複数選択可能）"""
        
        # 方法A: 外部HTTPサーバーを呼び出し
        # return self._call_http_mcp(prompt)
        
        # 方法B: ローカルMCPスクリプトを実行
        # return self._call_local_mcp(prompt)
        
        # 方法C: Claude Code/Cursor経由の手動入力
        return self._manual_input_workflow(prompt)
    
    def _manual_input_workflow(self, prompt: str) -> dict:
        """手動入力ワークフロー（Claude Code実行結果を入力）"""
        print(f"\n📋 要件定義書生成ワークフロー")
        print(f"プロンプト: {prompt}")
        print(f"\n以下の手順で進めてください：")
        print(f"1. Claude CodeまたはCursorで要件定義書MCPを実行")
        print(f"2. 生成された要件定義書をJSON形式でコピー")
        print(f"3. 下記に貼り付けてEnterを押してください")
        print(f"\n要件定義書JSON（複数行可、空行で終了）:")
        
        lines = []
        while True:
            try:
                line = input()
                if line.strip() == "":
                    break
                lines.append(line)
            except EOFError:
                break
        
        json_text = "\n".join(lines)
        
        try:
            return json.loads(json_text)
        except json.JSONDecodeError as e:
            print(f"❌ JSON形式が正しくありません: {e}")
            return self._create_default_structure(prompt)
    
    def _create_default_structure(self, prompt: str) -> dict:
        """デフォルト構造を作成（MCPが利用できない場合）"""
        return {
            "title": f"{prompt} 要件定義書",
            "overview": f"{prompt}に関するシステムの要件定義書",
            "functional_requirements": [
                {"name": "基本機能", "description": "システムの基本機能", "priority": "必須"}
            ],
            "non_functional_requirements": [
                {"category": "パフォーマンス", "requirements": ["レスポンスタイム3秒以内"]}
            ],
            "user_personas": [
                {"name": "ユーザー", "role": "利用者", "goals": ["システム利用"], "pain_points": ["課題"], "needs": ["ニーズ"]}
            ]
        }
    
    def _convert_to_project_format(self, data: dict, project_name: str) -> str:
        """プロジェクト形式のYAMLに変換"""
        project_yaml = [{
            "id": f"requirements-{project_name}",
            "category": 2,
            "category_name": "要件定義・開発", 
            "title": data.get("title", f"{project_name} 要件定義書"),
            "content": data.get("overview", ""),
            "image": f"/images/requirements_{project_name}_card.png",
            
            "tabs": [
                {"id": "overview", "label": "概要", "icon": "📋", "active": True},
                {"id": "users", "label": "ユーザー分析", "icon": "👥"},
                {"id": "requirements", "label": "要件定義", "icon": "📝"},
                {"id": "architecture", "label": "アーキテクチャ", "icon": "🏗️"},
                {"id": "implementation", "label": "実装", "icon": "💻"},
                {"id": "operations", "label": "運用", "icon": "⚙️"}
            ],
            
            "header_info": {
                "version": "1.0",
                "date": "2025年9月",
                "status": "ドラフト"
            },
            
            "overview_cards": [
                {
                    "title": "プロジェクト概要",
                    "icon": "📋",
                    "content": data.get("overview", "")
                },
                {
                    "title": "主要機能", 
                    "icon": "⚡",
                    "content": "\n".join([f"- {req.get('name', '')}" for req in data.get("functional_requirements", [])])
                }
            ],
            
            "functional_requirements": [
                {
                    "id": f"FR-{i+1:03d}",
                    "name": req.get("name", ""),
                    "description": req.get("description", ""),
                    "priority": req.get("priority", "推奨")
                }
                for i, req in enumerate(data.get("functional_requirements", []))
            ],
            
            "non_functional_requirements": data.get("non_functional_requirements", []),
            "user_personas": data.get("user_personas", []),
            
            "mermaid": """
graph TD
    A[フロントエンド] --> B[APIサーバー]
    B --> C[データベース]
    
    style A fill:#3B82F6,stroke:#fff,stroke-width:2px,color:#fff
    style B fill:#10B981,stroke:#fff,stroke-width:2px,color:#fff
    style C fill:#F59E0B,stroke:#fff,stroke-width:2px,color:#fff
""",
            
            "gantt": """
gantt
    title 開発スケジュール
    dateFormat YYYY-MM-DD
    section フェーズ1
    要件定義 :done, req, 2025-01-01, 14d
    基本設計 :active, design, after req, 21d
    section フェーズ2
    実装 :impl, after design, 60d
    テスト :test, after impl, 21d
"""
        }]
        
        return yaml.dump(project_yaml, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    def _save_requirements_file(self, yaml_content: str, project_name: str):
        """要件定義書ファイルを保存"""
        file_path = self.project_root / "data" / "saas" / f"requirements-{project_name}.yaml"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        
        print(f"\n✅ 要件定義書を保存しました: {file_path}")
    
    def _show_integration_guide(self, project_name: str):
        """統合完了後の案内"""
        print(f"\n📋 統合完了！次の手順で確認してください：")
        print(f"")
        print(f"1. ナビゲーション更新（手動）:")
        print(f"   themes/kamui-docs/layouts/index.html の requirements-document ブロックに")
        print(f"   {project_name} のカードを追加")
        print(f"")
        print(f"2. 表示確認:")
        print(f"   hugo server -D")
        print(f"   http://localhost:1313/#requirements-{project_name}")
        print(f"")
        print(f"3. 画像追加（オプション）:")
        print(f"   static/images/requirements_{project_name}_card.png を配置")

def main():
    if len(sys.argv) < 3:
        print("使用方法: python mcp-executor.py <prompt> <project-name>")
        print("例: python mcp-executor.py 'ネコカフェ予約システム' 'neko-cafe'")
        sys.exit(1)
    
    prompt = sys.argv[1]
    project_name = sys.argv[2]
    
    executor = ProjectMCPExecutor()
    executor.execute_requirements_mcp(prompt, project_name)

if __name__ == "__main__":
    main()

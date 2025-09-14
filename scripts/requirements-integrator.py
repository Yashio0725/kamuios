#!/usr/bin/env python3
"""
要件定義書統合スクリプト
外部MCPから生成された要件定義書をkamuiosプロジェクト形式に変換・統合
"""

import json
import yaml
import os
import sys
from pathlib import Path
from typing import Dict, Any, List
import asyncio
import aiohttp

class RequirementsIntegrator:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.data_dir = self.project_root / "data" / "saas"
        self.images_dir = self.project_root / "static" / "images"
        
    async def call_external_mcp(self, prompt: str) -> Dict[str, Any]:
        """外部MCPサーバーを呼び出して要件定義書を生成"""
        # mcp-requirement.jsonから設定を読み込み
        mcp_config_path = self.project_root / "mcp" / "mcp-requirement.json"
        with open(mcp_config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        requirement_server = config["mcpServers"]["requirement"]
        url = requirement_server["url"]
        
        # 外部MCPに要件定義書生成を依頼
        data = {
            "prompt": prompt,
            "format": "structured",
            "language": "ja"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"MCP Error {response.status}: {await response.text()}")
    
    def convert_to_project_yaml(self, external_data: Dict[str, Any], project_name: str) -> str:
        """外部MCPの出力をプロジェクトのYAML形式に変換"""
        
        # プロジェクトのYAML構造に変換
        project_yaml = {
            "id": f"requirements-{project_name}",
            "category": 2,
            "category_name": "要件定義・開発",
            "title": external_data.get("title", f"{project_name} 要件定義書"),
            "content": external_data.get("overview", ""),
            "image": f"/images/requirements_{project_name}_card.png",
            
            # タブナビゲーション
            "tabs": [
                {"id": "overview", "label": "概要", "icon": "📋", "active": True},
                {"id": "users", "label": "ユーザー分析", "icon": "👥"},
                {"id": "requirements", "label": "要件定義", "icon": "📝"},
                {"id": "architecture", "label": "アーキテクチャ", "icon": "🏗️"},
                {"id": "implementation", "label": "実装", "icon": "💻"},
                {"id": "operations", "label": "運用", "icon": "⚙️"}
            ],
            
            # ヘッダー情報
            "header_info": {
                "version": "1.0",
                "date": "2025年9月",
                "status": "ドラフト"
            },
            
            # 概要カード
            "overview_cards": self._convert_overview_cards(external_data),
            
            # 機能要件
            "functional_requirements": self._convert_functional_requirements(external_data),
            
            # 非機能要件
            "non_functional_requirements": self._convert_non_functional_requirements(external_data),
            
            # 技術スタック
            "tech_stack": self._convert_tech_stack(external_data),
            
            # ユーザーペルソナ
            "user_personas": self._convert_user_personas(external_data),
            
            # アーキテクチャ図（Mermaid）
            "mermaid": self._generate_mermaid_diagram(external_data),
            
            # ガントチャート
            "gantt": self._generate_gantt_chart(external_data)
        }
        
        # YAML形式で出力（リスト形式）
        return yaml.dump([project_yaml], default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    def _convert_overview_cards(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """概要カードを変換"""
        return [
            {
                "title": "プロジェクト概要",
                "icon": "📋",
                "content": data.get("overview", "")
            },
            {
                "title": "対象領域",
                "icon": "🎯", 
                "content": "\n".join([f"- **{area}**: {desc}" for area, desc in data.get("target_areas", {}).items()])
            },
            {
                "title": "主要機能",
                "icon": "⚡",
                "content": "\n".join([f"- {feature}" for feature in data.get("key_features", [])])
            }
        ]
    
    def _convert_functional_requirements(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """機能要件を変換"""
        requirements = []
        for i, req in enumerate(data.get("functional_requirements", []), 1):
            requirements.append({
                "id": f"FR-{i:03d}",
                "name": req.get("name", ""),
                "description": req.get("description", ""),
                "priority": req.get("priority", "推奨")
            })
        return requirements
    
    def _convert_non_functional_requirements(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """非機能要件を変換"""
        return data.get("non_functional_requirements", [
            {
                "category": "パフォーマンス",
                "requirements": ["レスポンスタイム3秒以内", "同時接続100ユーザー対応"]
            },
            {
                "category": "可用性", 
                "requirements": ["99.5%以上のアップタイム", "計画メンテナンス月1回以内"]
            },
            {
                "category": "セキュリティ",
                "requirements": ["HTTPS通信必須", "認証機能実装"]
            }
        ])
    
    def _convert_tech_stack(self, data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """技術スタックを変換"""
        return data.get("tech_stack", {
            "frontend": [
                {"name": "React", "version": "18.x", "purpose": "UIフレームワーク"},
                {"name": "TypeScript", "version": "5.x", "purpose": "型安全な開発"}
            ],
            "backend": [
                {"name": "Node.js", "version": "20.x", "purpose": "サーバーランタイム"},
                {"name": "Express", "version": "4.x", "purpose": "Webフレームワーク"}
            ]
        })
    
    def _convert_user_personas(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """ユーザーペルソナを変換"""
        return data.get("user_personas", [])
    
    def _generate_mermaid_diagram(self, data: Dict[str, Any]) -> str:
        """Mermaidアーキテクチャ図を生成"""
        return data.get("mermaid", """
graph TD
    A[フロントエンド] --> B[APIゲートウェイ]
    B --> C[ビジネスロジック]
    C --> D[データベース]
    
    style A fill:#3B82F6,stroke:#fff,stroke-width:2px,color:#fff
    style B fill:#10B981,stroke:#fff,stroke-width:2px,color:#fff
    style C fill:#8B5CF6,stroke:#fff,stroke-width:2px,color:#fff
    style D fill:#F59E0B,stroke:#fff,stroke-width:2px,color:#fff
""")
    
    def _generate_gantt_chart(self, data: Dict[str, Any]) -> str:
        """ガントチャートを生成"""
        return data.get("gantt", """
gantt
    title プロジェクト開発スケジュール
    dateFormat YYYY-MM-DD
    section フェーズ1
    要件定義 :done, req, 2025-01-01, 14d
    基本設計 :active, design, after req, 21d
    section フェーズ2
    実装 :impl, after design, 60d
    テスト :test, after impl, 21d
    section フェーズ3
    デプロイ :deploy, after test, 7d
""")
    
    def save_requirements_file(self, yaml_content: str, project_name: str):
        """要件定義書YAMLファイルを保存"""
        file_path = self.data_dir / f"requirements-{project_name}.yaml"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        
        print(f"要件定義書を保存しました: {file_path}")
    
    def update_navigation(self, project_name: str, title: str):
        """ナビゲーションを更新（index.htmlにカードを追加）"""
        # この部分は手動で行うか、HTMLパーサーを使用して自動化
        print(f"手動でナビゲーションを更新してください:")
        print(f"- themes/kamui-docs/layouts/index.html の requirements-document ブロックに {project_name} のカードを追加")
        print(f"- タイトル: {title}")
    
    async def generate_and_integrate(self, prompt: str, project_name: str):
        """要件定義書生成から統合までの完全なワークフロー"""
        try:
            print(f"外部MCPに要件定義書生成を依頼中...")
            external_data = await self.call_external_mcp(prompt)
            
            print(f"プロジェクト形式に変換中...")
            yaml_content = self.convert_to_project_yaml(external_data, project_name)
            
            print(f"ファイルを保存中...")
            self.save_requirements_file(yaml_content, project_name)
            
            print(f"ナビゲーション更新の案内...")
            self.update_navigation(project_name, external_data.get("title", f"{project_name} 要件定義書"))
            
            print(f"\n✅ 要件定義書の統合が完了しました!")
            print(f"確認方法: hugo server -D で起動後、#requirements-{project_name} にアクセス")
            
        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")

async def main():
    if len(sys.argv) < 3:
        print("使用方法: python requirements-integrator.py <prompt> <project-name>")
        print("例: python requirements-integrator.py 'ネコカフェの予約システム' 'neko-cafe'")
        sys.exit(1)
    
    prompt = sys.argv[1]
    project_name = sys.argv[2]
    
    integrator = RequirementsIntegrator()
    await integrator.generate_and_integrate(prompt, project_name)

if __name__ == "__main__":
    asyncio.run(main())

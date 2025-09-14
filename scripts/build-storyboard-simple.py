#!/usr/bin/env python3
"""
ストーリーボードビューアー自動ビルドスクリプト
シーンデータ(YAML)をstoryboard-viewer.yamlに反映
"""

import yaml
import re
import os
from pathlib import Path

def main():
    print("🎬 ストーリーボードビルダー開始...")
    
    # ファイルパス設定
    script_dir = Path(__file__).parent
    scenes_file = script_dir.parent / "data" / "storyboard-scenes.yaml"
    yaml_file = script_dir.parent / "data" / "saas" / "storyboard-viewer.yaml"
    
    try:
        # シーンデータを読み込み
        with open(scenes_file, 'r', encoding='utf-8') as f:
            scenes_data = yaml.safe_load(f)
        
        scenes = scenes_data['scenes']
        print(f"📝 {len(scenes)}個のシーンを読み込みました")
        
        # YAMLファイルを読み込み
        with open(yaml_file, 'r', encoding='utf-8') as f:
            yaml_content = f.read()
        
        # 各シーンを処理
        for scene in scenes:
            scene_id = scene['id']
            cut_num = scene['cut']
            # 改行文字を適切に処理（YAMLの複数行テキストから不要な改行を除去）
            text_content = scene['text'].strip().replace('\n', '')
            script_content = scene['script'].strip().replace('\n', '')
            
            print(f"🎭 シーン{scene_id} (CUT {cut_num})を処理中...")
            
            # パターン1: 見開きビュー用の置換
            pattern1 = rf'(<div class="cell timecell">{cut_num}</div>.*?</figure>\s*</div>\s*)<div class="cell text">.*?</div>\s*<div class="cell script">.*?</div>'
            replacement1 = rf'\1<div class="cell text">{text_content}</div>\n                <div class="cell script">{script_content}</div>'
            
            yaml_content = re.sub(pattern1, replacement1, yaml_content, flags=re.DOTALL)
        
        # 更新されたYAMLファイルを保存
        with open(yaml_file, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        
        print("✅ ストーリーボードビューアーが正常に更新されました！")
        print(f"📄 更新ファイル: {yaml_file}")
        
    except FileNotFoundError as e:
        print(f"❌ ファイルが見つかりません: {e}")
    except yaml.YAMLError as e:
        print(f"❌ YAMLファイルの読み込みエラー: {e}")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")

if __name__ == "__main__":
    main()

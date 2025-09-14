#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// ファイルパス設定
const SCENES_FILE = path.join(__dirname, '../data/storyboard-scenes.json');
const TEMPLATE_FILE = path.join(__dirname, '../data/saas/storyboard-viewer.yaml');
const OUTPUT_FILE = path.join(__dirname, '../data/saas/storyboard-viewer.yaml');

console.log('🎬 ストーリーボードビルダー開始...');

try {
  // シーンデータを読み込み
  const scenesData = JSON.parse(fs.readFileSync(SCENES_FILE, 'utf8'));
  console.log(`📝 ${scenesData.scenes.length}個のシーンを読み込みました`);

  // 現在のYAMLファイルを読み込み
  let yamlContent = fs.readFileSync(TEMPLATE_FILE, 'utf8');

  // 各シーンのデータを置換
  scenesData.scenes.forEach((scene, index) => {
    const sceneNum = scene.id.toString().padStart(3, '0');
    
    console.log(`🎭 シーン${scene.id}を処理中...`);

    // 見開きビュー用の置換（左ページ：1-5、右ページ：6-10）
    const spreadViewPattern = new RegExp(
      `(<div class="cell timecell">${sceneNum}</div>\\s*<div class="cell">\\s*<figure class="frame">.*?</figure>\\s*</div>\\s*)<div class="cell text">.*?</div>\\s*<div class="cell script">.*?</div>`,
      'gs'
    );

    const spreadReplacement = `$1<div class="cell text">${scene.text}</div>
                <div class="cell script">${scene.script}</div>`;

    yamlContent = yamlContent.replace(spreadViewPattern, spreadReplacement);

    // 縦並びビュー用の置換
    const verticalViewPattern = new RegExp(
      `(<div class="cell timecell">${sceneNum}</div>\\s*<div class="cell">\\s*<figure class="frame">.*?</figure>\\s*</div>\\s*)<div class="cell text">.*?</div>\\s*<div class="cell script">.*?</div>`,
      'gs'
    );

    const verticalReplacement = `$1<div class="cell text">${scene.text}</div>
                <div class="cell script">${scene.script}</div>`;

    yamlContent = yamlContent.replace(verticalViewPattern, verticalReplacement);
  });

  // 更新されたYAMLファイルを保存
  fs.writeFileSync(OUTPUT_FILE, yamlContent, 'utf8');
  
  console.log('✅ ストーリーボードビューアーが正常に更新されました！');
  console.log(`📄 出力ファイル: ${OUTPUT_FILE}`);

} catch (error) {
  console.error('❌ エラーが発生しました:', error.message);
  process.exit(1);
}

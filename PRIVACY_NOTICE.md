# プライバシーとセキュリティに関する注意事項

## 重要な注意

このプロジェクトでは、開発過程でAIとの対話ログや開発ログが生成される場合があります。
これらのファイルには個人情報や開発の詳細が含まれる可能性があるため、**絶対にGitHubに公開しないでください**。

## 除外されるファイル

以下のファイルは`.gitignore`により自動的に除外されます：

### 開発ログ関連
- `development_log.txt`
- `log_helper.py`
- `chat_log.txt`
- `conversation_log.txt`
- `ai_chat_*.txt`
- `ai_conversation_*.txt`
- `*.chat`
- `*.conversation`
- `*_log.txt`
- `*_chat.txt`
- `dev_notes.txt`
- `development_notes.txt`

### AI対話関連
- `*ai_interaction*`
- `*chat_history*`
- `*conversation_history*`

## 開発者への推奨事項

1. **ローカル開発時の注意**
   - 個人的なメモやログファイルは上記の命名規則に従ってください
   - 機密情報を含むファイルは必ず`.gitignore`に追加してください

2. **コミット前の確認**
   ```bash
   git status
   ```
   を実行して、意図しないファイルが含まれていないか確認してください

3. **既にコミットしてしまった場合**
   ```bash
   git rm --cached filename
   git commit -m "Remove sensitive file"
   ```

## ゲーム固有の除外ファイル

以下のゲーム関連ファイルも除外されます：
- `*.save` - セーブファイル
- `config.ini` - 設定ファイル
- `highscores.dat` - ハイスコアデータ
- `rankings.json` - ランキングデータ（個人情報含む可能性）

## 質問がある場合

プライバシーやセキュリティに関して不明な点がある場合は、
コミットする前に必ず確認してください。

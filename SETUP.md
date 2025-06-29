# セットアップガイド

## 必要な環境

- Python 3.7以上
- pip (Pythonパッケージマネージャー)

## インストール手順

### 1. 依存関係のインストール

```bash
# Windowsの場合
pip install pygame numpy scipy

# macOS/Linuxの場合
pip3 install pygame numpy scipy

# または requirements.txt を使用
pip install -r requirements.txt
```

### 2. ゲームの実行

```bash
python main.py
```

**初回起動時の自動セットアップ**:
- 音声ファイルが存在しない場合、自動的に生成されます
- プログレスバー付きの生成画面が表示されます
- 生成完了後、Enterキーでゲームを開始できます

### 3. 手動での音声ファイル生成（オプション）

事前に音声ファイルを生成したい場合：

```bash
python generate_audio_files.py
```

## ゲーム仕様

### 画面構成
- 解像度: 1280x720 (修正済み)
- ゲームエリア: 左2/3 (853x720)
- UIエリア: 右1/3 (427x720)

### 操作方法
- **移動**: 矢印キー または WASD
- **射撃**: スペースキー
- **爆弾**: Xキー (NEW!)
- **メニュー**: ESC
- **決定**: Enter
- **ランキング表示**: R (メニュー画面で)

### ゲームシステム

#### 自機仕様
- ライフ: 3つ
- 被弾時: ライフ-1、中央にリスポーン
- 無敵時間: 3秒間（半透明点滅）
- 爆弾: ライフごとに2個使用可能（計6個）
- 被弾時に爆弾数が回復

#### スコアシステム
- 敵撃破: +100点
- スコアアイテム: +10点 (NEW!)
- ハイスコア: 上位10位まで記録
- ニックネーム登録可能

#### 敵の種類と強さ (NEW!)
**弱い敵 (薄赤色)**
- 弾幕密度: 低
- 移動速度: 速い
- アイテムドロップ: 1-2個

**通常敵 (赤色)**
- 弾幕密度: 中
- 移動速度: 普通
- アイテムドロップ: 2-4個

**強い敵 (暗赤色・黄枠)**
- 弾幕密度: 高
- 移動速度: 遅い
- アイテムドロップ: 4-7個
- 時間経過で出現率上昇

#### 弾幕パターン
1. **RadialEnemy**: 放射状弾幕
2. **CircularEnemy**: 円状波動弾幕
3. **SpiralEnemy**: 螺旋状弾幕

#### 視覚効果
- 敵撃破時の爆発エフェクト
- パーティクル効果
- スコアアイテムの点滅効果
- 大規模な爆弾爆発エフェクト

#### 音響効果 (NEW!)
- **SF風BGM**（各画面に対応、WAVファイル）
  - メニュー: アンビエント宇宙テーマ（60秒ループ）
  - ゲーム: アクション戦闘テーマ（120秒ループ）
  - ゲームオーバー: ドラマチックテーマ（20秒）
  - ランキング: 勝利テーマ（30秒ループ）
- **効果音**（WAVファイル、高品質44.1kHz）
  - 射撃音: レーザーパルス効果
  - 爆発音: 敵撃破時の爆発
  - 爆弾音: 大規模爆発（2秒間）
  - アイテム収集音: 上昇チャイム
  - プレイヤー被弾音: アラート音
  - 敵出現音: ワープイン効果
  - メニュー操作音: UI確認・移動音

#### 爆弾システム (NEW!)
- 広範囲の敵と弾を一掃する爆発攻撃
- ライフ1つにつき2個使用可能
- 被弾時に爆弾数が回復
- 爆発範囲内の全ての敵と弾を破壊

## 修正内容

### v2.0の新機能
- 画面サイズを1280x720に変更（見切れ問題解決）
- 弾のサイズを1.5倍に拡大
- UI文字を日本語化
- 爆弾システム追加
- 敵の強さ段階システム（3段階）
- スコア加算アイテムシステム
- 時間経過による難易度調整
- SF風BGMと効果音システム

## トラブルシューティング

### よくある問題

1. **初回起動時に音声生成が失敗する**
   - 必要なパッケージを確認：
   ```bash
   pip install numpy scipy
   ```
   - 権限の問題がある場合、assetsディレクトリを手動作成：
   ```bash
   mkdir -p assets/audio/bgm assets/audio/sfx
   ```

2. **音声生成画面で進行が止まる**
   - Ctrl+Cで中断し、手動で音声ファイルを生成：
   ```bash
   python generate_audio_files.py
   ```
   - その後ゲームを再起動

3. **pygameが見つからない**
   ```bash
   pip install pygame
   ```

2. **画面が表示されない**
   - WSL環境の場合、X11転送の設定が必要です
   - Windows環境での直接実行を推奨します

3. **音が出ない**
   - pygame.mixerの初期化に失敗している可能性があります
   - オーディオドライバーを確認してください
   - BGMが再生されない場合、numpyがインストールされているか確認：
   ```bash
   pip install numpy
   ```

4. **日本語が文字化けする (NEW!)**
   - システムに日本語フォントがインストールされていない可能性があります
   - 以下の対処法を試してください：

   **Windows:**
   - MS Gothic、Meiryo、Yu Gothicなどが自動的に使用されます
   - 通常は問題ありません

   **macOS:**
   - Hiragino Sans、Hiragino Kaku Gothic ProNが使用されます
   - 通常は問題ありません

   **Linux:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install fonts-noto-cjk
   sudo apt-get install fonts-takao-gothic
   
   # CentOS/RHEL
   sudo yum install google-noto-cjk-fonts
   ```

5. **音声ファイル生成に失敗する**
   - 必要なパッケージをインストール：
   ```bash
   pip install numpy scipy
   ```
   - 権限の問題がある場合：
   ```bash
   # Windowsの場合、管理者として実行
   # Linux/macOSの場合
   sudo python generate_audio_files.py
   ```

6. **音声ファイルが見つからない**
   - assets/audioディレクトリが存在するか確認
   - 音声ファイル生成を再実行：
   ```bash
   python generate_audio_files.py
   ```

7. **フォントテスト**
   日本語フォントが正しく動作するかテストできます：
   ```bash
   python test_font.py
   ```

8. **音声テスト**
   音響システムが正しく動作するかテストできます：
   ```bash
   python test_audio.py
   ```

## ファイル構成

```
QGamen_DanmakuShooting/
├── main.py              # メインエントリーポイント
├── src/                 # ソースコード
│   ├── game.py         # ゲームメインクラス
│   ├── player.py       # プレイヤー関連（爆弾追加）
│   ├── enemy.py        # 敵関連（強さ段階追加）
│   ├── bullet.py       # 弾丸管理
│   ├── ui.py           # ユーザーインターフェース（日本語化）
│   ├── effects.py      # 視覚効果
│   ├── items.py        # アイテムシステム（NEW!）
│   ├── ranking.py      # ランキングシステム
│   ├── font_manager.py # 日本語フォント管理
│   └── audio_manager.py # BGM・効果音管理（NEW!）
├── rankings.json       # ハイスコア記録（自動生成）
└── test_game.py        # テストスクリプト
```

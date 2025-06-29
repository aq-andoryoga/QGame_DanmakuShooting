# セットアップガイド

## 必要な環境

- Python 3.7以上
- pip (Pythonパッケージマネージャー)

## インストール手順

### 1. 依存関係のインストール

```bash
# Windowsの場合
pip install pygame numpy

# macOS/Linuxの場合
pip3 install pygame numpy

# または requirements.txt を使用
pip install -r requirements.txt
```

### 2. ゲームの実行

```bash
python main.py
```

または

```bash
python3 main.py
```

## ゲーム仕様

### 画面構成
- 解像度: 1920x1080
- ゲームエリア: 左2/3 (1280x1080)
- UIエリア: 右1/3 (640x1080)

### 操作方法
- **移動**: 矢印キー または WASD
- **射撃**: スペースキー
- **メニュー**: ESC
- **決定**: Enter
- **ランキング表示**: R (メニュー画面で)

### ゲームシステム

#### 自機仕様
- ライフ: 3つ
- 被弾時: ライフ-1、中央にリスポーン
- 無敵時間: 3秒間（半透明点滅）

#### スコアシステム
- 敵撃破: +100点
- ハイスコア: 上位10位まで記録
- ニックネーム登録可能

#### 敵の種類
1. **RadialEnemy** (赤): 放射状弾幕
2. **CircularEnemy** (薄赤): 円状波動弾幕
3. **SpiralEnemy** (紫): 螺旋状弾幕

#### 視覚効果
- 敵撃破時の爆発エフェクト
- パーティクル効果

## トラブルシューティング

### pygameが見つからない場合
```bash
pip install pygame
```

### 画面が表示されない場合
- WSL環境の場合、X11転送の設定が必要
- Windows環境で直接実行することを推奨

### 音が出ない場合
- pygame.mixerの初期化に失敗している可能性
- オーディオドライバーの確認

## ファイル構成

```
QGamen_DanmakuShooting/
├── main.py              # メインエントリーポイント
├── src/                 # ソースコード
│   ├── game.py         # ゲームメインクラス
│   ├── player.py       # プレイヤー関連
│   ├── enemy.py        # 敵関連
│   ├── bullet.py       # 弾丸管理
│   ├── ui.py           # ユーザーインターフェース
│   ├── effects.py      # 視覚効果
│   └── ranking.py      # ランキングシステム
├── rankings.json       # ハイスコア記録（自動生成）
└── test_game.py        # テストスクリプト
```

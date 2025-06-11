# AWS Icons Memory Game

Pygameを使用した神経衰弱（メモリーマッチング）ゲームです。AWSのアイコンを使ってカードマッチングを楽しめます。

## ゲーム概要

このゲームは、裏返されたカードの中から同じAWSアイコンのペアを見つけるメモリーゲームです。
難易度に応じて、カードの枚数が変わります。

## 特徴

- 3つの難易度レベル（かんたん、ふつう、むずかしい）
- AWSサービスのアイコンを使用したカード
- 日本語対応インターフェース
- シンプルで直感的な操作性

## 難易度設定

- **かんたん (4×4)**: 16枚のカード、8ペア
- **ふつう (6×6)**: 36枚のカード、18ペア
- **むずかしい (8×8)**: 64枚のカード、32ペア

## ゲームの操作方法

### メニュー画面
- ボタンにマウスを合わせると色が変わる（ホバーエフェクト）
- クリックで難易度を選択

### ゲーム画面
- カードをクリックすると裏返る
- 「メニューに戻る」ボタンをクリックするとメニューに戻る

### ゲームクリア画面
- Rキー: 同じ難易度でリスタート
- Mキー: メニューに戻る

## 必要環境

- Python 3.6以上
- Pygame

## インストール方法

1. リポジトリをクローン
```
git clone https://github.com/yourusername/aws-icons-memory-game.git
cd aws-icons-memory-game
```

2. 必要なパッケージをインストール
```
pip install pygame
```

3. AWSアイコンのダウンロード
   - [AWS Architecture Icons](https://aws.amazon.com/jp/architecture/icons/)からアイコンパッケージをダウンロード
   - ダウンロードしたZIPファイルを解凍
   - プロジェクトのルートディレクトリに「awsicon」フォルダを作成
   - 解凍したフォルダから「Asset-Package/Architecture-Service-Icons/Arch_*/32」内のPNGファイルを「awsicon」フォルダにコピー

4. ゲームを実行
```
python memory_game.py
```

## フォルダ構成

- `memory_game.py` - メインゲームコード
- `awsicon/` - AWSアイコン画像ファイル（[AWS Architecture Icons](https://aws.amazon.com/jp/architecture/icons/)からダウンロードしたアイコンパッケージを使用）

## 技術的特徴

- Pygameを使用したグラフィカルインターフェース
- macOS向け日本語フォント対応
- イベント駆動型のゲームループ
- オブジェクト指向設計

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 作者

[あなたの名前]

---

*注: AWSアイコンはAmazon Web Servicesの商標であり、このゲームは非公式です。*

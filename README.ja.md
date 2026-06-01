<div align="center">

# leader-skills

**AIがあなたのビッグテックのリーダーとなり、あなたを成長へと導く**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](plugin.json)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-%E2%9C%93-orange.svg)](https://claude.ai/code)
[![VS Code Copilot](https://img.shields.io/badge/VS%20Code%20Copilot-%E2%9C%93-007ACC.svg)](https://code.visualstudio.com)
[![Cursor](https://img.shields.io/badge/Cursor-%E2%9C%93-6366f1.svg)](https://cursor.sh)
[![Kiro](https://img.shields.io/badge/Kiro-%E2%9C%93-22c55e.svg)](https://kiro.dev)
[![CodeBuddy](https://img.shields.io/badge/CodeBuddy-%E2%9C%93-red.svg)](#)

[中文](README.md) · [English](README.en.md) · **日本語**

![Leader Skills Logo](leaderskills.png)

<br>

> *あなたはビッグテックに入社する必要はない。*  
> *ビッグテックの経験が、あなたのところにやってくる。*

</div>

---

## 目次

- [概要](#概要)
- [クイックスタート](#クイックスタート)
- [シーンとコマンド](#シーンとコマンド)
- [会社カルチャー](#会社カルチャー)
- [プレッシャーレベル（L0–L5）](#プレッシャーレベルl0l5)
- [自分だけのリーダーを作る](#自分だけのリーダーを作る)
- [Anti-PUA 保証](#anti-pua-保証)
- [プラットフォーム統合](#プラットフォーム統合)
- [プロジェクト構成](#プロジェクト構成)

---

## 概要

多くの AI アシスタントはあなたの「作業」を手伝います。leader-skills はあなたの「思考」を鍛えます。

AI は ByteDance、Alibaba、Tencent といった企業の P9/P10 レベルのマネージャーを演じます。
厳しい質問を投げかけ、最も弱い論点を指摘し、答えを簡単には与えません。

```
プッシュの方向:  AI（リーダーとして）──→  あなた（ユーザー）
```

> [!NOTE]
> これはほとんどの AI ツールとは**真逆**のアプローチです。成長には摩擦が必要です。

---

## クイックスタート

### 前提条件

- Claude Code（メイン）、VS Code + Copilot、Cursor、または Kiro

### Claude Code

```bash
# Step 1: リーダーモードを有効化（デフォルト：Alibaba カルチャー）
/leader

# Step 2: プランをリーダーにレビューしてもらう
/review

# Step 3: 1on1 コーチングセッションを開始
/1on1

# KPI のブレークダウン
/kpi

# 会社カルチャーを切り替え
/flavor bytedance

# 無効化
/leader:off
```

### VS Code + GitHub Copilot

```bash
# Option 1: プロジェクトディレクトリにコピー
cp vscode/copilot-instructions.md .vscode/copilot-instructions.md

# Option 2: instructions ファイルを使用（より細かい制御）
cp vscode/instructions/leader.instructions.md .github/instructions/leader.instructions.md
```

> [!TIP]
> コピー後、Copilot チャットで `/leader` と入力するだけで有効になります。その他の設定は不要です。

---

## シーンとコマンド

| コマンド | シーン | 説明 |
|:--------|:------|:------------|
| `/leader` | 汎用プッシュ | リーダーモードを有効化、適切なシーンに自動ルーティング |
| `/review` | プラン・コードレビュー | P9/P10 基準：最も弱い点を見つけ、論理の一貫性を要求 |
| `/1on1` | パフォーマンス面談 | 成果レビュー → キャリア相談 → アクションアイテム |
| `/kpi` | KPI シーズン | 目標交渉、OKR ブレークダウン、上司への働きかけ |
| `/qbr` | 四半期レビュー | 5-Why 根本原因分析 → 説明責任 → コミットメント |
| `/alignment` | 調整セッション | 部門横断の交渉準備とコーチング |
| `/offboard` | 退職面談 | 引き留め交渉、オファー分析、円満退職 |
| `/flavor` | カルチャー切替 | 企業文化の DNA を変更 |
| `/create-leader` | リーダー作成 | 実際の上司を AI に抽出 |
| `/leader:off` | 無効化 | リーダーモードを終了 |

---

## 会社カルチャー

`/flavor <名前>` で切り替え：

| カルチャー | コマンド | 主な特徴 |
|:-------|:--------|:------------|
| 🟠 Alibaba | `/flavor alibaba` | 方向性の一致、クロージャー、「底层逻辑」、グレースケール展開 |
| 🟡 ByteDance | `/flavor bytedance` | データファースト、Context、A/B テスト、10x |
| 🔵 Tencent | `/flavor tencent` | ユーザー価値、プロダクト感覚、シンプルさ |
| 🔴 Huawei | `/flavor huawei` | プロセス厳守、自己批判、悪魔の代弁者 |
| 🟢 Meituan | `/flavor meituan` | 現場実行力、ユーザーファースト、妥協なき追求 |
| ⬛ Xiaomi | `/flavor xiaomi` | ファン文化、スピード、徹底した磨き込み |
| 🟣 Pinduoduo | `/flavor pinduoduo` | ハッスル文化、効率性、コスト規律 |
| ⚡ スタートアップ | `/flavor startup` | PMF ファースト、オールイン、ファウンダーモード |

---

## プレッシャーレベル（L0–L5）

リーダーは提出回数と改善度に応じて自動的にエスカレーションします：

| レベル | トリガー | 動作 |
|:------|:--------|:---------|
| L0 | 1回目の提出 | 信頼構築フェーズ — オープンな質問、関係作り |
| L1 | 2回目、改善なし | 軽い不満 — 未解決の問題を具体的に指摘 |
| L2 | 3回目、改善なし | 公的なプレッシャー — 「チーム全体が待っている」 |
| L3 | 4回目、改善なし | KPI 連動 — 「これがあなたの評価に影響している」 |
| L4 | 5回目、改善なし | 組織的プレッシャー — HR 関与の示唆 |
| L5 | 6回目以降 | 退職トーク — 深刻だが、**必ず改善の道筋を含む** |

> [!TIP]
> `stressed`、`I give up`、`I can't do this` といったキーワードは自動的にプレッシャーレベルを下げ、サポートモードに切り替わります。

---

## 自分だけのリーダーを作る

### 方法 1 — 会話形式（推奨）

```
/create-leader
```

AI が 3 つの質問をし、カスタムリーダーペルソナを生成します。ツールは不要です。

### 方法 2 — ツールチェーン（実際の資料がある場合）

```bash
# Step 1: Feishu チャットエクスポートを解析
python tools/feishu_parser.py ./team_chat.json 老王

# Step 2: メールアーカイブを解析
python tools/email_parser.py ./inbox.mbox 王総 wang@company.com

# Step 3: リーダーファイルを構築
python tools/leader_builder.py \
  --name "王総" \
  --materials ./inbox_parsed.json \
  --flavor alibaba

# Step 4: 出力を検証
python tools/skill_writer.py validate custom_boss

# Step 5: バージョン管理
python tools/version_manager.py custom_boss snapshot minor "話し方を修正"
```

リーダーペルソナは 3 つのファイルで構成されます：

```
leaders/{name}/
├── meta.json       ← 識別情報（名前、レベル、強度、カルチャー）
├── persona.md      ← 性格、プレッシャースタイル、口癖
└── work.md         ← 会議スタイル、レビュースタイル、意思決定
```

2 つのビルトイン例：
- `example_ali_p10/` — 老汪（Alibaba P10、体系的、ENTJ）
- `example_byte_p9/` — 老沈（ByteDance P9、データファースト、Context 重視）

---

## Anti-PUA 保証

> [!IMPORTANT]
> いかなる設定でも上書きできない 3 つの絶対的なレッドライン：
>
> 1. **人格攻撃の禁止** — 批判するのは仕事であって、人ではない
> 2. **L5 は必ず出口を示す** — 最大のプレッシャーには常に実行可能な改善の方向性を伴う
> 3. **現実の問題を優先** — 実際の職場でのハラスメントや法的問題に対しては、AI は即座にキャラクターを解除し、真剣なアドバイスを提供する

---

## プラットフォーム統合

### Claude Code

`SKILL.md` を Claude Code の skills ディレクトリ（またはプロジェクトルート）にコピーしてください。

### VS Code + GitHub Copilot

```bash
# Option 1: プロジェクトレベルの設定
cp vscode/copilot-instructions.md .vscode/copilot-instructions.md

# Option 2: 指示ファイル（より細かい制御）
cp vscode/instructions/leader.instructions.md .github/instructions/leader.instructions.md
```

### Cursor

```bash
cp cursor/rules/leader.mdc .cursor/rules/leader.mdc
```

### Kiro

```bash
cp kiro/steering/leader.md .kiro/steering/leader.md
```

---

## プロジェクト構成

<details>
<summary>クリックして全体構成を表示</summary>

```
leader-skills/
├── SKILL.md                  ← Claude Code メインエントリ
├── ARCHITECTURE.md           ← 詳細設計ドキュメント
├── plugin.json               ← プラグインメタデータ
│
├── skills/                   ← 8 つのサブスキル
│   ├── leader/               ← 有効化＋ルーティング
│   ├── review/               ← コード・プランレビュー
│   ├── oneonone/             ← 1on1 セッション
│   ├── kpi_season/           ← KPI ブレークダウン
│   ├── qbr/                  ← 四半期レビュー
│   ├── alignment/            ← 目標調整
│   ├── offboard/             ← 退職面談
│   └── create_leader/        ← リーダー作成
│
├── flavors/                  ← 8 つの企業文化 DNA パック
│   └── {alibaba,bytedance,tencent,huawei,meituan,xiaomi,pinduoduo,startup}.md
│
├── leaders/                  ← リーダーペルソナファイル
│   ├── _template/            ← スターターテンプレート
│   ├── example_ali_p10/      ← 老汪（Alibaba P10）
│   └── example_byte_p9/      ← 老沈（ByteDance P9）
│
├── scenarios/                ← トリガーとエスカレーションロジック
│   ├── triggers.md
│   └── escalation.md
│
├── commands/                 ← コマンド別指示ファイル
│
├── references/               ← 動作仕様とルール
│   ├── display-protocol.md
│   ├── push-methodology.md
│   ├── leader-builder.md
│   ├── persona-protocol.md
│   └── anti-pua-guard.md
│
├── prompts/                  ← コアプロンプトテンプレート
│   ├── intake.md
│   ├── leader_analyzer.md
│   ├── leader_builder.md
│   ├── push_generator.md
│   └── correction_handler.md
│
├── tools/                    ← Python ユーティリティ
│   ├── leader_builder.py
│   ├── feishu_parser.py
│   ├── email_parser.py
│   ├── version_manager.py
│   └── skill_writer.py
│
├── hooks/                    ← セッションライフサイクルフック
│   ├── hooks.json
│   ├── session_restore.sh
│   ├── frustration_trigger.sh
│   ├── action_item_tracker.sh
│   └── sanitize-session.sh
│
├── vscode/                   ← VS Code + Copilot 統合
├── cursor/                   ← Cursor 統合
├── kiro/                     ← Kiro 統合
└── docs/                     ← ドキュメント
    ├── PRD.md
    └── EXAMPLES.md
```

</details>

詳細アーキテクチャ: [ARCHITECTURE.md](ARCHITECTURE.md) · 使用例: [docs/EXAMPLES.md](docs/EXAMPLES.md) · 中文: [README.md](README.md) · English: [README.en.md](README.en.md)

---

## 関連プロジェクト

- [https://github.com/tanweai/pua](https://github.com/tanweai/pua) — 企業文化ボキャブラリの参考
- https://github.com/titanwings/colleague-skill — 同僚ペルソナフォーマットの参考

---

<div align="center">

*v1.0.0 · MIT License · [GitHub](https://github.com/leader-skills/leader-skills)*

</div>

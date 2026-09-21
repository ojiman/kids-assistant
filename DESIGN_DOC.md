# Design Doc: Kids Assistant — AI Agent Engineering 学習プロジェクト

- **ステータス**: Active
- **最終更新**: 2026-09-21
- **オーナー**: Norio

---

## 1. Project Mission

本プロジェクトの目的は、AI Agentを一度実装できるようになることではない。

**AI Agentの原理・実装・評価・運用を理解し、プロダクト要件に応じて適切なAgent Architectureを設計・実装・評価できる能力を獲得すること**を目的とする。

### 1.1 到達したい状態

未知のプロダクト要件に対して、以下を判断できること。

```text
Requirement
    │
    ▼
LLMが必要か？
    │
    ├── No ──→ Traditional Software
    │
    ▼ Yes
処理フローは固定か？
    │
    ├── Yes ─→ Workflow + LLM
    │
    ▼ No
LLMによる動的な判断・ツール選択が必要か？
    │
    ├── No ──→ Workflow
    │
    ▼ Yes
Agent
```

Agentを採用する場合も、システム全体をAgent化するのではなく、委譲する範囲を限定して設計できることを重視する。

```text
Deterministic Workflow
        │
        ▼
Agentic Decision
        │
        ▼
Policy / Guardrail
        │
        ▼
Human Approval
        │
        ▼
Deterministic Execution
```

### 1.2 第二の目的

小学4年生の子供が、学習や日常の疑問を安心して相談できるアシスタントを実際に使える状態にすること。

**重要**: 1.2は1.1を達成した結果として得られる副産物と位置づける。1.2を急ぐために1.1を犠牲にしてはならない。
ただし逆も真で、実際に使われないものを作り続けることは、設計判断の検証機会を失うことを意味する。

---

## 2. Learning Philosophy

以下の順序で学習する。

```text
Build
  ↓
Understand
  ↓
Evaluate
  ↓
Abstract
  ↓
Rebuild with Framework
  ↓
Design for Production
```

最初からAgent frameworkを利用しない。まずLLM APIを直接利用して、conversation state / agent loop / tool execution / context management / guardrails / evaluation を自分で実装する。

その後、Claude Agent SDK、OpenAI Agents SDK、LangGraph等を利用し、自作実装と比較する。
目的はframework APIを暗記することではなく、次を説明できるようになることである。

> 「このframeworkは、自分が実装したどの責務を抽象化しているのか」

### 2.1 学習モードの原則

AIコーディングエージェント（Claude Code / Codex）を **教師・レビュアー** として使い、**代筆者** としては使わない。

**エージェントに依頼してよいこと**

- 概念の説明、設計判断の選択肢提示とPros/Cons整理
- 自分が書いたコードのレビュー、バグの指摘、改善提案
- エラーメッセージの解読、デバッグの伴走
- 公式ドキュメントの該当箇所の案内
- 質問に答える形での、部分的なコード例の提示（**写経して理解する前提**）

**エージェントに依頼してはいけないこと**

- 「この機能を実装して」と丸投げし、生成物をそのまま採用すること
- 理解していないコードをコミットすること

### 2.2 自分で書く範囲と、委譲してよい範囲

プロジェクトの規模が大きくなるにつれ、すべてを手書きすることは学習効率を下げる。境界を以下に定める。

| 区分 | 対象 |
|---|---|
| **必ず自分で書く** | エージェントループ、ツール実行、ツール実行ゲート、ガードレール、コンテキスト管理、評価ロジック |
| **委譲してよい** | UI（HTML/CSS）、ログの整形、テストの雛形、定型的な配線コード、ドキュメントの清書 |

委譲した場合も、そのコードが何をしているかは説明できる状態を保つ。

### 2.3 自己チェック

コミット前に必ず自問する。

> **このコードの各行が何をしているか、他人に説明できるか？**

説明できない行が1行でもあれば、コミットせずに理解するまで質問する。

---

## 3. Competency Model

AI Agent Engineering能力を以下の8領域に分けて習得する。各マイルストーンはこのいずれかに対応する。

### C1. LLM Fundamentals
Messages / Responses API、system / user / assistant message、token / context window、structured output、tool calling、model selection、latency / cost

### C2. Agent Fundamentals
agent loop、reasoning → action → observation、tool selection、termination condition、state、workflow vs agent、deterministic / non-deterministic boundary

### C3. Context Engineering
conversation history、context window management、summarization、retrieval、short-term / long-term memory、context pollution

### C4. Tool Engineering
tool schema、tool registry、input validation、error handling、timeout、retry、idempotency、permissions、side effects

### C5. Safety & Control
input guardrail、output guardrail、prompt injection、tool execution gate、least privilege、human-in-the-loop、policy enforcement

### C6. Evaluation
deterministic test、model-based evaluation、task success rate、tool selection accuracy、trajectory evaluation、regression testing、evaluation dataset、synthetic user simulation

### C7. Production Engineering
logging、tracing、observability、cost monitoring、latency、failure recovery、session management、security

### C8. Agent Architecture
要件を分析し、Traditional software / LLM call / Workflow + LLM / Single Agent / Agent embedded in Workflow / Multi-Agent から適切な方式を選択できること。

**Multi-Agentは最後に学習し、必要性が明確な場合のみ採用する。**

---

## 4. Project Strategy

Kids Assistantを単なる完成品としてではなく、**Agent Engineering Laboratory** として扱う。
子供向けアシスタントという一貫したユースケースを維持しながら、アーキテクチャを段階的に進化させる。

```text
Simple LLM App
     ↓
Tool-using LLM
     ↓
Agent
     ↓
Controlled Agent
     ↓
Evaluated Agent
     ↓
Observable Agent
     ↓
Production-oriented Agent
     ↓
Framework-based Agent
```

各段階で以下を必須とする。

1. 自分で実装する
2. 動作を観察する
3. DESIGN_DOCに設計判断を書く
4. `docs/learnings/` に理解した内容を自分の言葉で書く

---

## 5. ユーザーとユースケース

### 5.1 想定ユーザー

- **主ユーザー**: 小学4年生（9-10歳）。英語環境の学校に通っており、中学受験準備中。
- **副ユーザー（監督者）**: 親（開発者本人）。会話ログを確認できる必要がある。

### 5.2 想定ユースケース

| # | ユースケース | 必要な機能 |
|---|---|---|
| U1 | 「〜ってどういう意味？」という言葉・概念の質問 | LLM応答のみ |
| U2 | 算数の問題の解き方を聞く | LLM応答 + 計算ツール |
| U3 | 「なんで空は青いの？」のような素朴な疑問 | LLM応答のみ |
| U4 | 英単語の意味・使い方を聞く | LLM応答 + 辞書ツール |
| U5 | 親が「今日何を聞いたか」を確認する | ログ + 週次ダイジェスト |

### 5.3 明示的に対応しないユースケース

- 宿題の答えをそのまま出力すること（考え方を教える方針とする）
- 自由なWeb検索（安全性の担保が困難なため、初期スコープ外）
- 画像の生成・解析

### 5.4 ユーザーテストの方針

実ユーザー（子供）による継続利用のハードルが高いため、**ペルソナシミュレータ**で代替する。

小学4年生のペルソナをLLMに演じさせ、アシスタントと対話させてUX上の問題を検出する。
これは synthetic user simulation としてAgent評価で実際に用いられる手法であり、M8の評価データセット生成にそのまま流用する。

**既知のバイアス（記録しておくこと）**

- 生成される質問は「大人が想像した小学4年生」であり、実際の子供の質問はより断片的・非文法的・脈絡がない
- 合成ユーザーでは「使うのをやめた」という離脱シグナルが得られない
- シミュレータとアシスタントに同一モデルを使うと自己評価バイアスが入る。**別モデルを使用すること**

---

## 6. 技術選定

### 6.1 抽象度のレイヤー

| レイヤー | 内容 | 代表例 |
|---|---|---|
| L1: 生のAPI | 1回のリクエスト/レスポンス。ループは自作 | Anthropic Messages API, OpenAI Responses API |
| L2: ハーネス/SDK | エージェントループ、ツール実行、コンテキスト管理を提供 | Claude Agent SDK, OpenAI Agents SDK, LangGraph |
| L3: マネージド実行環境 | 上記に加えセッション管理・サンドボックス・復旧をホスト側が担う | OpenAI Agents API |

### 6.2 用語の定義

- **ハーネス（harness）**: 生のLLM APIを「自律的に動くエージェント」に仕上げるための制御機構一式。ツールレジストリ、エージェントループ、コンテキスト管理、メモリ、ガードレール、可観測性などを含む。
- **ガードレール（guardrail）**: ハーネスの構成要素の一つ。危険な操作・不適切な内容を検出し、ブロックまたは確認を求める仕組み。

### 6.3 決定：Phase 1 では L1（生のAPI）を採用する

**採用**: Anthropic Messages API + Tool Use（Python）

**理由**:

- 第一目的（仕組みの理解）に対し、L2/L3はエージェントループを隠蔽してしまい、学習効果が大きく損なわれる
- L1で自作することで、L2/L3が何を肩代わりしているのかを後から理解できるようになる
- 普段Claude Codeを使っているため、Anthropicのエコシステムで一貫させた方が質問→検証のループがスムーズ

**ただしL2は最終的にGoalに含める。** M11でframeworkによる再実装を行い、自作実装と責務の対応を比較する。

### 6.4 言語

**採用**: Python（エージェント関連の情報量、公式SDKの第一級サポート）

開発者はServer-side Kotlin（Spring Boot）に習熟している。Phase 2以降でKotlinによる再実装は理解度の検証として有効な選択肢となる。

### 6.5 依存ライブラリの方針

最小限に留める。`anthropic`、`python-dotenv`、M4以降で`fastapi`。
エージェントフレームワーク系ライブラリはPhase 1では **意図的に使用しない**（M11で解禁）。

---

## 7. アーキテクチャ

### 7.1 現在の構成（M3完了時点）

```text
[ユーザー（子供）]
        │
        ▼
[インターフェース層]  ← CLI（M4でWeb UIへ）
        │
        ▼
┌───────────────────────────────────────┐
│  自作ハーネス層                          │
│                                        │
│  ┌──────────────────────────────┐     │
│  │ 入力ガードレール                │     │
│  │ - LLMによる適切性判定           │     │
│  └──────────────────────────────┘     │
│              │                         │
│              ▼                         │
│  ┌──────────────────────────────┐     │
│  │ エージェントループ              │     │
│  │ 1. 履歴 + 入力を API に送信     │     │
│  │ 2. tool_use があればツール実行   │     │
│  │ 3. 結果を履歴に追加して 1へ戻る  │     │
│  │ 4. tool_use がなければ終了       │     │
│  └──────────────────────────────┘     │
│         │            │                 │
│         ▼            ▼                 │
│  ┌───────────┐  ┌──────────────┐     │
│  │ツールレジストリ│  │コンテキスト管理│     │
│  │- 計算       │  │- 履歴保持     │     │
│  │- （拡張可）  │  │- 巻き戻し     │     │
│  └───────────┘  └──────────────┘     │
│              │                         │
│              ▼                         │
│  ┌──────────────────────────────┐     │
│  │ 出力ガードレール                │     │
│  │ - LLMによる適切性判定           │     │
│  └──────────────────────────────┘     │
│              │                         │
│              ▼                         │
│  ┌──────────────────────────────┐     │
│  │ ロギング（親の確認用）           │     │
│  └──────────────────────────────┘     │
└───────────────────────────────────────┘
        │
        ▼
[Anthropic Messages API]
```

### 7.2 目標構成（M10時点の想定）

M6でツール実行ゲート、M7でメモリ層、M9でトレース層が加わる。
各マイルストーン完了時にこの図を更新すること。図の更新自体が理解の確認になる。

### 7.3 ディレクトリ構成（案）

```text
kids-assistant/
├── AGENTS.md              # AIコーディングエージェント向け指示
├── CLAUDE.md              # AGENTS.md へのポインタのみ
├── DESIGN_DOC.md          # 本ドキュメント
├── README.md
├── .env.example
├── requirements.txt
├── src/
│   ├── main.py            # エントリポイント
│   ├── harness/           # loop.py / context.py / logger.py / tracer.py
│   ├── tools/             # registry.py / calculator.py / dictionary.py
│   └── guardrails/        # input.py / output.py / tool_gate.py
├── evals/                 # 評価データセットと評価スクリプト
├── logs/                  # 会話ログ（.gitignore対象）
└── tests/
```

**注意**: 最初から全部作らない。マイルストーンに沿って段階的に育てる（M3時点では `main.py` 1ファイル）。

---

## 8. マイルストーン

各マイルストーンは「動くものができる」単位で区切る。完了時に **何を学んだかを自分の言葉で** `docs/learnings/` に書き残す。

### M0: 素のAPI呼び出し ✅

**ゴール**: Anthropic Messages APIを叩いて応答を得る。1往復のみ。
**学習**: リクエスト/レスポンスの構造、システムプロンプトの効果。 → C1

---

### M1: 会話履歴の保持 ✅

**ゴール**: 複数ターンの会話が成立する。
**学習**: LLM APIはステートレスであり履歴は毎回送る必要がある。トークン数の増加を実測。 → C1, C3

---

### M2: Tool Use & Agent Loop ✅

**ゴール**: 計算ツールを1つ定義し、エージェントループを自作する。
**学習**: ツール定義（JSON Schema）、`stop_reason: tool_use` の検出、ツール実行 → `tool_result` → 再度API、というループ。**このループがハーネスの中核である。** → C2, C4

---

### M3: Guardrails ✅

**ゴール**: 入力・出力の両方に安全機構を入れる。
**学習**: システムプロンプトによる制御だけでは不十分な理由。決定論的チェックとLLMチェックの使い分け。ブロック時のmessages巻き戻し。 → C5

---

### M4: Application Boundary

**ゴール**: ローカルWeb UI（FastAPI + 素のHTML/JS）を実装し、UI / application / agent harness / tools の責務を分離する。

**学習ポイント**
- 「AgentはApplicationそのものではなく、Application Architectureの一部である」ことを理解する
- CLIでは暗黙だったセッション境界・状態管理が、Web化により顕在化する

**完了条件**
- ブラウザから会話でき、ログが記録される
- **小学4年生ペルソナのシミュレータで利用し、UXのフィードバックを得て反映する**（5.4の方針に従う。シミュレータはアシスタント本体と別モデルを使う）

→ C2, C7

---

### M5: Multiple Tools & Tool Engineering

**ゴール**: 複数のツールを実装する（辞書、クイズ生成、ローカル知識検索など）。

**学習ポイント**: tool selection、schema design、input validation、tool error、retry、timeout
**完了条件**: モデルが状況に応じて適切なツールを選択し、ツールが失敗しても会話が破綻しない。

→ C4

---

### M6: Tool Execution Gate

**ゴール**: LLMが要求したツールを直接実行しない構造にする。

```text
LLM → Tool Request → Policy Gate → allow / deny / human approval → Tool
```

**学習ポイント**: ツールのrisk level、最小権限、human-in-the-loopが必要になる条件
**完了条件**: risk levelの高いツールが承認なしに実行されない。

→ C5

---

### M7: Context Engineering & Memory

**ゴール**: 長い会話を扱えるようにする。

**学習ポイント**: context window管理、summarization、retrieval、short-term / long-term memory の違い
**完了条件**: 「履歴を全部LLMに渡す」がなぜスケールしないのかを実測で示し、対策を実装する。

→ C3

---

### M8: Agent Evaluation

**ゴール**: Agent専用の評価環境を構築する。

```text
Test Case → Agent → Trajectory → Evaluator
```

**評価軸**: 最終回答の品質 / 正しいツールを選択したか / 不要なツールを使っていないか / unsafe actionを実行していないか / タスクを完了できたか / token・latency・cost

**学習ポイント**
- Agentの評価が通常のunit testより難しい理由（非決定的、経路が複数、正解が一意でない）
- **評価データセットはM4のペルソナシミュレータから生成する。** 想像で書いたテストケースではなく、実際の対話ログを起点とする

**完了条件**: `evals/` に評価データセットと評価スクリプトが存在し、変更時にリグレッションを検出できる。

→ C6

---

### M9: Observability

**ゴール**: Agentの実行をトレースとして確認できるようにする。

```text
Request
 ├─ LLM call
 ├─ Tool call
 ├─ LLM call
 └─ Response
```

各ステップについて input/output、latency、token、cost、error を追跡する。

**完了条件**: 1リクエストの内部で何が起きたかを、ログを読まずに構造として確認できる。

→ C7

---

### M10: Production Failure Modes

**ゴール**: 意図的に障害を発生させ、Agentの異常系の振る舞いを学ぶ。

**対象**: Tool timeout / malformed arguments / API failure / rate limit / 無限エージェントループ / context overflow

**学習ポイント**: 正常系しか見ていないAgentがいかに脆いか。どこにリトライ・打ち切り・フォールバックを置くべきか。
**完了条件**: 上記すべてについて、落ちずに適切に縮退する。

→ C7

---

### M11: Framework Comparison

**ゴール**: 自作したAgentを既存frameworkで再実装する（Claude Agent SDK / OpenAI Agents SDK / LangGraph から1つ以上）。

**比較項目**

| 項目 | 自作 | Framework |
|---|---|---|
| Agent loop | | |
| Tool management | | |
| State | | |
| Guardrails | | |
| Tracing | | |
| Evaluation | | |
| Human approval | | |

**学習ポイント**: frameworkの優劣を決めることが目的ではない。**どの責務をframeworkへ委譲するか判断できるようになること**が目的。

→ C8

---

### M12: Workflow vs Agent

**ゴール**: 親向けの週次ダイジェスト機能（U5）を実装する。ただし **これをAgentとして実装しない。**

会話ログを読み、その週に子供が何を聞いたかを要約して親に提示する。処理は「ログを読む → 要約する → 整形する → 出力する」の固定列であり、動的なツール選択もループも不要。Workflow + LLM で実装する。

**学習ポイント**
- 同じプロダクトの中で、Agentにすべき部分とすべきでない部分を判断する
- 同機能をAgentとして実装することも可能だが、遅く・高く・非決定的で・テストが難しい。その対比を記述する
- **M12まで到達して初めて「Agentを使わない」判断に意味が出る**

**完了条件**: ダイジェストが動作し、`docs/learnings/m12.md` に「なぜこれをAgentにしなかったか」を説明できている。

→ C8

**安全上の注意**: ダイジェストは会話ログ（`logs/`、gitignore対象）を入力とする。出力先も必ずgitignore対象とすること。

---

## 9. Non-Goals

### 9.1 恒久的にスコープ外

- 高可用性、大規模トラフィック、分散アーキテクチャ
- 家族以外への提供、公開サービス化
- fine-tuning、GPU、モデル訓練
- 作り込んだフロントエンド
- 完成を急ぐこと

### 9.2 Phase 1 ではスコープ外（最終的にはGoal）

| 項目 | 解禁マイルストーン |
|---|---|
| Evaluation | M8 |
| Observability | M9 |
| Production設計（障害耐性） | M10 |
| Agent Framework | M11 |
| Multi-Agent | 必要性が明確になった場合のみ |

---

## 10. 安全設計

### 10.1 必須要件

| ID | 要件 | 実装マイルストーン |
|---|---|---|
| S1 | 全会話をログに記録し、親が後から確認できる | M3 |
| S2 | 不適切な話題への応答を拒否する | M3 |
| S3 | ツールの権限は必要最小限とする（ファイル操作・シェル実行は実装しない） | M2 |
| S4 | APIキーをコードにハードコードしない（.env管理、.gitignore） | M0 |
| S5 | 会話ログをリポジトリにコミットしない | M3 |
| S6 | risk levelの高いツールは承認なしに実行しない | M6 |

### 10.2 設計原則

- **最小権限**: ツールは「安全に完結するもの」のみ。外部への書き込み、コマンド実行は一切実装しない。
- **多層防御**: システムプロンプトのみに依存せず、コード側のチェックも併用する。
- **可観測性**: 何が起きたか後から追えることを、機能追加より優先する。

---

## 11. 決定済み事項

### Q1: インターフェース形態 ✅
ローカルWeb UI（M4で実装）。FastAPI + 素のHTML/JS。React/Vue等は使わない。

### Q2: 実行環境・ホスティング ✅
ローカルPCのみ。クラウド・家庭内サーバーは不要。子供の会話ログを外部に出さない方針と一致。

### Q3: 子供のアクセス端末 ✅
家族共有デバイス。LINE Bot等の外部公開は不要。家庭内LAN内で完結。

### Q4: 使用モデル
アシスタント本体は `claude-haiku-4-5`（コスト効率）。
ガードレール・評価・ペルソナシミュレータには **本体と異なるモデル** を使う（自己評価バイアスの回避）。

---

## 12. 開発ツールの扱い（Claude Code / Codex 両対応）

仕様と指示を **ツール非依存の形で外部化** し、どちらのツールからでも同じ文脈で開発できるようにする。

- `AGENTS.md` を **唯一の情報源（Single Source of Truth）** とする
- `CLAUDE.md` は `AGENTS.md` を参照するだけの薄いポインタとする
- 本 `DESIGN_DOC.md` をリポジトリに含め、`AGENTS.md` から参照させる

**トークン消費の最適化**

- `AGENTS.md` は簡潔に保つ。詳細は本ドキュメントに置き、必要時のみ読ませる
- 1セッション = 1マイルストーン を目安に区切る
- 「実装して」ではなく「レビューして」「なぜこうなるか説明して」という使い方が、結果的にトークン効率も良い

---

## 13. Definition of Done

本プロジェクトは「Kids Assistantが完成した」時点ではなく、以下を満たした時点で完了とする。

### 13.1 Implementation

- [x] Raw LLM APIからAgent loopを実装できる
- [ ] 複数ツールを安全に実行できる
- [ ] Context / memoryを設計できる
- [ ] Tool Execution Gateを実装できる
- [ ] Evaluationを構築できる
- [ ] Agent executionをtraceできる
- [ ] 既存Agent frameworkで同等システムを実装できる
- [ ] 同一プロダクト内でWorkflowとAgentを使い分けられる

### 13.2 Understanding

ホワイトボードまたは自分のコードを指しながら説明できる。

- [ ] LLM applicationとAgentの違い
- [ ] WorkflowとAgentの違い、使い分けの基準
- [ ] Agent loopとは何か
- [ ] Harnessとは何か、何を構成要素とするか
- [ ] Context EngineeringとMemoryの違い
- [ ] Agentの評価が通常のunit testより難しい理由
- [ ] Human-in-the-loopが必要になる条件
- [ ] Agent frameworkが肩代わりしている責務

### 13.3 Architecture

未知のプロダクト要件について、

- [ ] Agentを使うべきか判断できる
- [ ] Agentに委譲する範囲を決められる
- [ ] deterministic codeとの境界を設計できる
- [ ] Tool permissionを設計できる
- [ ] failure modeを列挙できる
- [ ] evaluation strategyを設計できる

### 13.4 Product

- [ ] 子供が実際に使える状態になっている
- [ ] 親が会話ログと週次ダイジェストを確認できる

---

## 14. Ultimate Success Criterion

本プロジェクトの成功は、

> 「Agentを作ったことがある」

ではなく、

> **「要件を見て、Agentを使うべきか、どこまでAgentに任せるべきかを判断し、そのアーキテクチャを設計・実装・評価できる」**

状態になることである。

# Daily AI Open Source (Skill Project)

这是一个 **全 Python 实现** 的 skill 项目，用于自动生成“每日 AI 日报（含自动配图）”。

## 项目目标
每日聚合并输出：
- GitHub 热门 AI 开源项目
- Hugging Face Blog 最新动态
- arXiv cs.AI 最新论文
- 由图片生成大模型自动生成的配图

最终生成结构化 Markdown 日报，可直接发布。

## 核心能力
- **可插拔图片大模型**：支持 `openai` 与 `custom` 两种 provider。
- **用户自定义模型**：通过 `--image-model` 指定模型名。
- **用户自定义端点**：通过 `--image-api-base` + `--image-endpoint` 对接私有部署或第三方兼容接口。
- **自动落盘图片**：日报中的配图会下载/保存到本地，并直接以 Markdown 图片语法嵌入。

## 项目结构

```text
.
├── SKILL.md
├── pyproject.toml
├── src/
│   └── daily_ai_skill/
│       ├── __init__.py
│       ├── cli.py
│       ├── generator.py
│       ├── image_generation.py
│       ├── models.py
│       └── sources.py
├── templates/
│   └── daily_report.md.j2
├── reports/
└── tests/
    └── test_generator.py
```

## 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## 生成日报

### 1) 仅生成文字日报

```bash
daily-ai-report --output reports/daily_ai_report.md
```

### 2) 接入 OpenAI 图片模型自动配图

```bash
export OPENAI_API_KEY=your_key
daily-ai-report \
  --image-provider openai \
  --image-model gpt-image-1 \
  --max-images 6 \
  --output reports/daily_with_images.md
```

### 3) 接入用户自定义模型/服务（OpenAI 兼容接口）

```bash
export CUSTOM_IMAGE_KEY=your_key
daily-ai-report \
  --image-provider custom \
  --image-model your-model-name \
  --image-api-base https://your-image-gateway.example.com \
  --image-endpoint /v1/images/generations \
  --image-api-key-env CUSTOM_IMAGE_KEY \
  --output reports/daily_custom_images.md
=======
### Daily Report Delivery Channels
- Supports multi-channel daily report delivery.
- Configure channels during skill installation.
- Supported channels: **Feishu**, **iMessage**, **OpenClaw**.

### Skill Installation Channel Configuration
Use a channel list in your install configuration:

```yaml
report_delivery:
  enabled: true
  channels:
    - feishu
    - imessage
    - openclaw
```

You can enable one or multiple channels based on your environment.

### Sample Entry (2026-03-23)
- Date: 2026-03-23
  - Project: OpenVision-Lite
  - Stars: 12,345
  - Description: Lightweight multimodal model for vision-language tasks.
  - Link: https://github.com/example/openvision-lite

### Trusted AI Information Sources

#### Research & Papers
- [arXiv](https://arxiv.org) - Open-access archive for scholarly articles in AI/ML
- [Papers With Code](https://paperswithcode.com) - ML papers with code, datasets, and benchmarks
- [Hugging Face](https://huggingface.co) - Open-source AI models, datasets, and demos
- [Semantic Scholar](https://www.semanticscholar.org) - AI-powered research literature search

#### Labs & Research Blogs
- [OpenAI Blog](https://openai.com/blog) - Research and announcements from OpenAI
- [Google DeepMind](https://deepmind.google/research) - DeepMind research publications
- [Meta AI](https://ai.meta.com/blog) - Meta AI research blog
- [Anthropic Research](https://www.anthropic.com/research) - Anthropic AI safety research
- [Microsoft Research AI](https://www.microsoft.com/en-us/research/research-area/artificial-intelligence/) - Microsoft AI research

#### News & Media
- [The Verge - AI](https://www.theverge.com/ai-artificial-intelligence) - AI coverage from The Verge
- [TechCrunch - AI](https://techcrunch.com/category/artificial-intelligence/) - AI startup and industry news
- [VentureBeat - AI](https://venturebeat.com/ai/) - Enterprise AI news and analysis
- [MIT Technology Review - AI](https://www.technologyreview.com/topic/artificial-intelligence/) - In-depth AI reporting

#### Newsletters & Aggregators
- [Import AI](https://importai.net) - Weekly AI newsletter by Jack Clark
- [The Rundown AI](https://www.therundown.ai) - Daily AI news digest
- [Ben's Bites](https://bensbites.co) - Daily AI product and research roundup
- [TLDR AI](https://tldr.tech/ai) - Concise daily AI newsletter

#### Community
- [r/MachineLearning](https://www.reddit.com/r/MachineLearning/) - Reddit ML community
- [Hacker News](https://news.ycombinator.com) - Tech community with strong AI discussion
- [GitHub Trending](https://github.com/trending) - Trending open source projects

### How to Contribute
1. Fork this repository.
2. Add a new entry in the latest daily section following the format.
3. Submit a pull request with a clear summary.

---

## 中文

### 说明
本仓库用于记录来自 **GitHub**、**Hugging Face** 和 **Papers with Code** 的 **每日热门 AI 开源项目**，以结构化的方式快速呈现当天值得关注的项目。

### 分类
- LLM（大语言模型）
- Computer Vision（计算机视觉）
- NLP（自然语言处理）
- MLOps
- AI Agents（智能体）
- Multimodal（多模态）

### 每日更新格式

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
```

## 测试

```bash
pytest
```

## 后续建议（可选）
- 增加 LLM 文本摘要层（对聚合内容做 3~5 条中文摘要）。
- 增加去重与评分机制（关键词、来源权重、热度）。
- 接入定时任务（GitHub Actions / cron）实现每日自动提交。

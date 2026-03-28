# Daily AI Report Skill

## Purpose
生成“每日 AI 日报”，聚合：
1. GitHub 热门 AI 开源项目
2. Hugging Face Blog 最新动态
3. arXiv cs.AI 最新论文
4. 通过图片大模型生成的配图

## Input
- `date`（可选，`YYYY-MM-DD`）
- `output`（可选，默认 `reports/daily_ai_report.md`）
- `image_provider`（可选：`none` / `openai` / `custom`）
- `image_model`（可选，自定义模型名）
- `image_api_base` + `image_endpoint`（可选，自定义图片模型网关）

## Workflow
1. 运行 Python CLI 抓取 GitHub + RSS 数据。
2. 聚合并生成结构化 `DailyReport`。
3. 使用图片大模型按条目生成配图并保存到本地。
4. 基于 Jinja2 模板渲染 Markdown，并直接嵌入图片链接。

## Run
```bash
daily-ai-report --output reports/daily_ai_report.md
```

```bash
export OPENAI_API_KEY=your_key
daily-ai-report --image-provider openai --image-model gpt-image-1 --output reports/with_images.md
```

```bash
export CUSTOM_IMAGE_KEY=your_key
daily-ai-report --image-provider custom --image-model your-model --image-api-base https://your-gateway --image-endpoint /v1/images/generations --image-api-key-env CUSTOM_IMAGE_KEY
```

## Notes
- 图片服务默认为 OpenAI 风格响应（`data[].b64_json` 或 `data[].url`）。
- 若使用私有模型，请确保返回兼容字段。

---
name: gen-image
description: 使用 ModelScope API 生成 AI 图像
argument-hint: <prompt> [model] [loras] [output] [filename] [width] [height] [count] [batch]
allowed-tools:
  - Bash
  - Read
  - Write
---

# /gen-image 命令

此命令用于通过 ModelScope API 生成 AI 图像。

## 执行流程

1. **验证配置**：检查 ModelScope API Token 是否已配置
2. **解析参数**：获取用户提供的 prompt 和可选参数
3. **调用 API**：使用 modelscope-api skill 中的知识调用 ModelScope API
4. **处理结果**：将生成的图像保存到指定目录
5. **报告状态**：向用户报告生成结果

## 参数处理

### 必需参数
- `prompt`: 图像生成提示词，描述想要生成的图像内容

### 可选参数
- `model`: ModelScope 模型 ID，默认使用 "Tongyi-MAI/Z-Image-Turbo"
- `loras`: LoRA 配置
  - 单个 LoRA: `"loras": "<lora-repo-id>"`
  - 多个 LoRA: `"loras": {"<lora-repo-id1>": 0.6, "<lora-repo-id2>": 0.4}`
  - 最多 6 个 LoRA，权重系数总和必须为 1.0
- `output`: 输出目录路径，默认 "./generated-images/"
- `filename`: 输出文件名（不含扩展名），默认使用时间戳
- `width`: 图像宽度，默认 1024
- `height`: 图像高度，默认 1024
- `count`: 生成图像数量，默认 1
- `batch`: 批量生成，每行一个 prompt

## 配置检查

执行前必须验证：
1. API Token 是否已配置（检查 `.claude/modelscope-image-gen.local.md`）
2. 如果未配置，提示用户运行 `/modelscope-config` 命令

## 调用图像生成脚本

使用以下命令执行图像生成：

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/modelscope-api/scripts/image-gen.py" \
  --prompt "<prompt>" \
  --model "<model>" \
  --output "<output>" \
  --width <width> \
  --height <height> \
  --count <count> \
  --timeout <timeout>
```

## 批量生成

如果提供 `batch` 参数：
1. 将 batch 内容按行分割
2. 为每个 prompt 生成图像
3. 使用统一的命名规则（如 `image_001.png`, `image_002.png`）

## 输出处理

1. **创建输出目录**：如果不存在则创建
2. **保存图像**：将生成的图像保存为 PNG 格式
3. **返回信息**：向用户报告保存路径和图像数量

## 错误处理

| 错误类型 | 处理方式 |
|---------|---------|
| API Token 未配置 | 提示运行 `/modelscope-config` |
| API 请求失败 | 显示详细错误信息，建议检查 Token 和网络 |
| 超时 | 提示增加超时时间配置 |
| 保存失败 | 检查目录权限 |

## 使用示例

### 基本用法
```
/gen-image "A golden cat"
```

### 指定模型和尺寸
```
/gen-image "A sunset over mountains" model="Tongyi-MAI/Z-Image-Turbo" width=1920 height=1080
```

### 批量生成
```
/gen-image batch="A golden cat
A sunset over mountains
A futuristic cityscape"
```

### 使用 LoRA
```
/gen-image "A beautiful landscape" loras="your-lora-repo-id"
```

## 注意事项

1. 异步轮询时间可能需要 10-60 秒，请耐心等待
2. 生成的图像会自动保存到本地
3. 确保 Python 环境已安装 `requests` 和 `pillow` 依赖

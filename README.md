# ModelScope Image Generation

ModelScope 图像生成插件 - 通过自然语言对话生成 AI 图像。

## 功能特性

- **对话式图像生成**：通过自然语言描述生成图像
- **命令接口**：提供 `/gen-image` 和 `/modelscope-config` 命令
- **智能代理**：自动识别图像生成请求
- **ModelScope API 集成**：支持多种模型和 LoRA 配置
- **批量生成**：支持批量生成多张图像

## 安装

### 前置要求

- Python 3.8+
- ModelScope API Token

### 安装步骤

1. 克隆或下载此插件到本地
2. 安装依赖：
   ```bash
   pip install requests pillow
   ```
3. 配置 API Token：
   ```bash
   /modelscope-config
   ```
4. 开始使用：
   ```bash
   /gen-image "A golden cat"
   ```

## 使用方法

### 命令

#### `/gen-image`

生成图像。

**参数：**
- `prompt` (必需): 图像生成提示词
- `model` (可选): 模型 ID，默认 "Tongyi-MAI/Z-Image-Turbo"
- `loras` (可选): LoRA 配置
- `output` (可选): 输出目录，默认 "./generated-images/"
- `filename` (可选): 输出文件名，默认自动生成
- `width` (可选): 图像宽度，默认 1024
- `height` (可选): 图像高度，默认 1024
- `count` (可选): 生成数量，默认 1
- `batch` (可选): 批量 prompt（换行分隔）

**示例：**
```
/gen-image "A golden cat"
/gen-image "A sunset over mountains" width=1920 height=1080 count=3
```

#### `/modelscope-config`

配置 ModelScope API。

**参数：**
- `api-key`: ModelScope API Token
- `default-model`: 默认模型
- `default-output`: 默认输出目录
- `timeout`: 轮询超时时间（秒）

**示例：**
```
/modelscope-config api-key="your-token"
```

### 自然语言使用

您也可以直接与对话，插件会自动识别图像生成请求：

- "生成一只金色的猫"
- "画一个日落时的山脉"
- "创建一张科幻风格的太空图片"

## 配置文件

插件配置保存在 `.claude/modelscope-image-gen.local.md`：

```yaml
---
api_key: "your-modelscope-token"
default_model: "Tongyi-MAI/Z-Image-Turbo"
default_output_dir: "./generated-images"
poll_timeout: 300
default_width: 1024
default_height: 1024
default_count: 1
---
```

## 支持的模型

- Tongyi-MAI/Z-Image-Turbo (默认)
- 以及其他 ModelScope 支持的图像生成模型

## 故障排除

### API Token 错误

确保您的 ModelScope API Token 有效：
1. 访问 [ModelScope](https://modelscope.cn/)
2. 获取您的 API Token
3. 运行 `/modelscope-config api-key="your-token"`

### 图像保存失败

检查输出目录权限，确保有写入权限。

### 超时错误

增加超时时间：
```
/modelscope-config timeout=600
```

## 许可证

MIT License

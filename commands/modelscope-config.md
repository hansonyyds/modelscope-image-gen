---
name: modelscope-config
description: 配置 ModelScope API 设置
argument-hint: [api-key] [default-model] [default-output] [timeout]
allowed-tools:
  - Read
  - Write
---

# /modelscope-config 命令

此命令用于配置 ModelScope API 的各项设置。

## 执行流程

1. **检查配置目录**：检查 `~/.modelscope-image-gen/` 目录是否存在
2. **创建目录（如需要）**：自动创建配置目录及父目录
3. **读取/更新配置**：根据用户提供的参数更新配置
4. **保存配置**：将新配置写入 `~/.modelscope-image-gen/modelscope-image-gen.local.md`
5. **验证配置**：确认 API Token 有效性

## 配置文件结构

配置文件位于：`~/.modelscope-image-gen/modelscope-image-gen.local.md`

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

**多项目共享**: 此配置文件为全局配置，所有使用此插件的项目将共享同一配置。

## 参数说明

### api-key
ModelScope API Token，必需。

获取方式：
1. 访问 [ModelScope](https://modelscope.cn/)
2. 登录账户
3. 进入个人中心获取 API Token

### default-model
默认使用的模型 ID，可选。

默认值：`"Tongyi-MAI/Z-Image-Turbo"`

其他可用模型请参考 ModelScope 文档。

### default-output
默认图像输出目录，可选。

默认值：`"./generated-images/"`

### timeout
异步任务轮询超时时间（秒），可选。

默认值：`300`

建议范围：60-600 秒

## 交互式配置

如果用户只运行 `/modelscope-config` 而不提供参数，则进入交互式配置模式：

1. **检查现有配置**：显示当前配置状态
2. **引导输入 Token**：提示用户输入 API Token
3. **设置默认值**：询问是否使用默认模型和输出目录
4. **保存配置**：将配置写入文件

## 从旧版本迁移

如果您之前在项目根目录有 `modelscope-image-gen.local.md` 配置文件：

1. 复制旧配置到全局目录：
   ```bash
   mkdir -p ~/.modelscope-image-gen
   cp /path/to/your/project/modelscope-image-gen.local.md ~/.modelscope-image-gen/
   ```

2. 验证配置：
   ```bash
   /gen-image "test"
   ```

3. 删除旧的配置文件（可选）：
   ```bash
   rm /path/to/your/project/modelscope-image-gen.local.md
   ```

## 配置文件路径

配置文件保存在用户主目录下的固定位置：
```
~/.modelscope-image-gen/modelscope-image-gen.local.md
```

首次配置时，目录会自动创建。

## 错误处理

| 错误类型 | 处理方式 |
|---------|---------|
| 配置文件不存在 | 创建新配置文件 |
| Token 无效 | 提示重新输入 |

## 使用示例

### 设置 API Token
```
/modelscope-config api-key="your-token-here"
```

### 设置完整配置
```
/modelscope-config api-key="your-token" default-model="Tongyi-MAI/Z-Image-Turbo" default-output="./images/" timeout=600
```

### 交互式配置
```
/modelscope-config
```

## 验证配置

配置完成后，可以运行：
```
/gen-image "test"
```

来验证配置是否正确。

## 安全提示

1. **不要提交配置文件**：`.local.md` 文件已在 `.gitignore` 中
2. **保护 Token 安全**：不要与他人分享您的 API Token
3. **定期更新**：建议定期更换 API Token

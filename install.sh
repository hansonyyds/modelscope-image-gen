#!/bin/bash
# ModelScope Image Generation Plugin 安装脚本

set -e

PLUGIN_NAME="modelscope-image-gen"
PLUGIN_SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_TARGET="$HOME/.claude/plugins/$PLUGIN_NAME"

echo "=========================================="
echo "  ModelScope Image Generation Plugin 安装"
echo "=========================================="
echo ""

# 检查插件源目录
if [ ! -f "$PLUGIN_SOURCE/.claude-plugin/plugin.json" ]; then
    echo "错误: 插件目录无效"
    echo "请从插件根目录运行此脚本"
    exit 1
fi

# 创建插件目录
echo "📁 创建插件目录..."
mkdir -p "$HOME/.claude/plugins"

# 复制插件
echo "📦 复制插件文件..."
if [ -d "$PLUGIN_TARGET" ]; then
    echo "⚠️  插件目录已存在，正在备份..."
    mv "$PLUGIN_TARGET" "$PLUGIN_TARGET.backup.$(date +%s)"
fi

cp -r "$PLUGIN_SOURCE" "$PLUGIN_TARGET"
echo "✅ 插件已安装到: $PLUGIN_TARGET"

# 安装 Python 依赖
echo ""
echo "📥 安装 Python 依赖..."
pip install requests pillow --quiet --disable-pip-version-check
echo "✅ Python 依赖已安装"

# 创建示例配置文件
CONFIG_FILE="$HOME/.claude/$PLUGIN_NAME.local.md"
if [ ! -f "$CONFIG_FILE" ]; then
    echo ""
    echo "📝 创建配置文件模板..."
    cp "$PLUGIN_TARGET/.claude/$PLUGIN_NAME.local.md.example" "$CONFIG_FILE"
    echo "✅ 配置文件已创建: $CONFIG_FILE"
    echo ""
    echo "⚠️  请编辑配置文件并填入您的 ModelScope API Token"
    echo "   文件位置: $CONFIG_FILE"
else
    echo ""
    echo "ℹ️  配置文件已存在: $CONFIG_FILE"
fi

echo ""
echo "=========================================="
echo "  安装完成！"
echo "=========================================="
echo ""
echo "📋 后续步骤:"
echo "   1. 编辑配置文件并填入 API Token:"
echo "      $CONFIG_FILE"
echo ""
echo "   2. 重启 Claude Code"
echo ""
echo "   3. 测试插件:"
echo "      /gen-image \"A golden cat\""
echo ""
echo "=========================================="

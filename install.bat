@echo off
REM ModelScope Image Generation Plugin 安装脚本 (Windows)

setlocal enabledelayedexpansion

set PLUGIN_NAME=modelscope-image-gen
set PLUGIN_SOURCE=%~dp0
set PLUGIN_TARGET=%USERPROFILE%\.claude\plugins\%PLUGIN_NAME%

echo ==========================================
echo   ModelScope Image Generation Plugin 安装
echo ==========================================
echo.

REM 检查插件源目录
if not exist "%PLUGIN_SOURCE%\.claude-plugin\plugin.json" (
    echo 错误: 插件目录无效
    echo 请从插件根目录运行此脚本
    pause
    exit /b 1
)

REM 创建插件目录
echo 📁 创建插件目录...
if not exist "%USERPROFILE%\.claude\plugins" mkdir "%USERPROFILE%\.claude\plugins"

REM 复制插件
echo 📦 复制插件文件...
if exist "%PLUGIN_TARGET%" (
    echo ⚠️  插件目录已存在，正在备份...
    set BACKUP=%PLUGIN_TARGET%.backup.%time:~0,2%%time:~3,2%%time:~6,2%
    set BACKUP=%BACKUP: =0%
    move "%PLUGIN_TARGET%" "!BACKUP!" >nul
)

xcopy "%PLUGIN_SOURCE%" "%PLUGIN_TARGET%" /E /I /Y >nul
echo ✅ 插件已安装到: %PLUGIN_TARGET%

REM 安装 Python 依赖
echo.
echo 📥 安装 Python 依赖...
pip install requests pillow --quiet --disable-pip-version-check
if %errorlevel% equ 0 (
    echo ✅ Python 依赖已安装
) else (
    echo ⚠️  Python 依赖安装失败，请手动运行: pip install requests pillow
)

REM 创建示例配置文件
set CONFIG_FILE=%USERPROFILE%\.claude\%PLUGIN_NAME%.local.md
if not exist "%CONFIG_FILE%" (
    echo.
    echo 📝 创建配置文件模板...
    copy "%PLUGIN_TARGET%\.claude\%PLUGIN_NAME%.local.md.example" "%CONFIG_FILE%" >nul
    echo ✅ 配置文件已创建: %CONFIG_FILE%
    echo.
    echo ⚠️  请编辑配置文件并填入您的 ModelScope API Token
    echo    文件位置: %CONFIG_FILE%
) else (
    echo.
    echo ℹ️  配置文件已存在: %CONFIG_FILE%
)

echo.
echo ==========================================
echo   安装完成！
echo ==========================================
echo.
echo 📋 后续步骤:
echo    1. 编辑配置文件并填入 API Token:
echo       %CONFIG_FILE%
echo.
echo    2. 重启 Claude Code
echo.
echo    3. 测试插件:
echo       /gen-image "A golden cat"
echo.
echo ==========================================
pause

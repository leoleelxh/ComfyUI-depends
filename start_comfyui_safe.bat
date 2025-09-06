@echo off
echo ========================================
echo   ComfyUI 安全启动脚本
echo   自动设置环境变量避免插件导入问题
echo ========================================

echo 正在设置环境变量...
set USE_TF=0
set USE_TORCH=1
echo ✅ USE_TF=0 (禁用TensorFlow后端)
echo ✅ USE_TORCH=1 (启用PyTorch后端)

echo.
echo 正在切换到ComfyUI目录...
cd /d "K:\aiapps\comfyui-conda\ComfyUI"

echo 正在激活conda环境...
call conda activate comfy

echo.
echo 🚀 启动ComfyUI...
echo 如果插件导入正常，说明环境变量设置成功
echo.
python main.py --auto-launch

echo.
echo ComfyUI已退出
pause

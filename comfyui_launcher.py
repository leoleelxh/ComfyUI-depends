#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ComfyUI 智能启动器
根据需要的功能自动配置后端
"""

import os
import sys
import argparse
from pathlib import Path

def setup_backend_for_feature(feature):
    """根据功能需求设置后端"""
    
    # 定义不同功能的后端需求
    feature_requirements = {
        'layerstyle': {
            'tensorflow': False,  # LayerStyle主要使用PyTorch
            'torch': True,
            'description': 'LayerStyle插件 - 推荐PyTorch后端'
        },
        'text_generation': {
            'tensorflow': True,   # 某些文本生成模型可能需要TensorFlow
            'torch': True,
            'description': '文本生成 - 支持双后端'
        },
        'image_processing': {
            'tensorflow': False,
            'torch': True,
            'description': '图像处理 - PyTorch后端'
        },
        'nlp_tasks': {
            'tensorflow': True,
            'torch': True,
            'description': 'NLP任务 - 支持双后端'
        },
        'default': {
            'tensorflow': False,
            'torch': True,
            'description': '默认配置 - PyTorch后端'
        }
    }
    
    config = feature_requirements.get(feature, feature_requirements['default'])
    
    print(f"🎯 配置功能: {config['description']}")
    
    if config['tensorflow'] and config['torch']:
        # 支持双后端，优先PyTorch
        os.environ['USE_TF'] = '0'
        os.environ['USE_TORCH'] = '1'
        print("🔧 设置: PyTorch优先（双后端支持）")
    elif config['torch']:
        # 仅PyTorch
        os.environ['USE_TF'] = '0'
        os.environ['USE_TORCH'] = '1'
        print("🔧 设置: 仅PyTorch后端")
    elif config['tensorflow']:
        # 仅TensorFlow
        os.environ['USE_TF'] = '1'
        os.environ['USE_TORCH'] = '0'
        print("🔧 设置: 仅TensorFlow后端")
    
    return config

def check_tensorflow_health():
    """检查TensorFlow健康状态"""
    try:
        import tensorflow as tf
        version = tf.__version__
        print(f"✅ TensorFlow {version} 可用")
        
        # 测试基本操作
        tf.constant([1, 2, 3])
        print("✅ TensorFlow 基本功能正常")
        return True
        
    except Exception as e:
        print(f"❌ TensorFlow 问题: {e}")
        return False

def install_tensorflow_if_needed():
    """如果需要且未安装，则安装TensorFlow"""
    try:
        import tensorflow
        return True
    except ImportError:
        print("📦 TensorFlow 未安装，正在安装...")
        import subprocess
        
        try:
            # 安装稳定版本
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', 
                'tensorflow==2.15.0'
            ])
            print("✅ TensorFlow 安装成功")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ TensorFlow 安装失败: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='ComfyUI 智能启动器')
    parser.add_argument('--feature', '-f', 
                       choices=['layerstyle', 'text_generation', 'image_processing', 'nlp_tasks'],
                       default='layerstyle',
                       help='指定主要使用的功能')
    parser.add_argument('--install-tf', action='store_true',
                       help='如果需要，自动安装TensorFlow')
    parser.add_argument('--check-only', action='store_true',
                       help='仅检查环境，不启动ComfyUI')
    
    args = parser.parse_args()
    
    print("=== ComfyUI 智能启动器 ===")
    
    # 设置后端
    config = setup_backend_for_feature(args.feature)
    
    # 如果需要TensorFlow，检查并安装
    if config.get('tensorflow', False):
        if args.install_tf:
            install_tensorflow_if_needed()
        
        tf_healthy = check_tensorflow_health()
        if not tf_healthy:
            print("⚠️ TensorFlow有问题，切换到PyTorch模式")
            os.environ['USE_TF'] = '0'
            os.environ['USE_TORCH'] = '1'
    
    # 测试transformers
    print("\n🧪 测试 transformers...")
    try:
        from transformers import pipeline
        print("✅ transformers 导入成功")
    except Exception as e:
        print(f"❌ transformers 导入失败: {e}")
        return 1
    
    if args.check_only:
        print("\n✅ 环境检查完成")
        return 0
    
    # 启动ComfyUI
    print("\n🚀 启动 ComfyUI...")
    
    # 假设ComfyUI在上级目录
    comfyui_path = Path(__file__).parent.parent / "ComfyUI" / "main.py"
    
    if comfyui_path.exists():
        os.chdir(comfyui_path.parent)
        os.system(f"python {comfyui_path}")
    else:
        print(f"❌ 找不到ComfyUI: {comfyui_path}")
        print("请手动启动ComfyUI")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 
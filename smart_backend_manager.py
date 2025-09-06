#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能后端管理器
根据需要动态选择 TensorFlow 或 PyTorch 后端
"""

import os
import sys
import warnings

class BackendManager:
    """管理 transformers 的后端选择"""
    
    def __init__(self):
        self.tensorflow_available = False
        self.torch_available = False
        self._check_backends()
    
    def _check_backends(self):
        """检查可用的后端"""
        # 检查 PyTorch
        try:
            import torch
            self.torch_available = True
            print(f"✅ PyTorch 可用: {torch.__version__}")
        except ImportError:
            print("❌ PyTorch 不可用")
        
        # 检查 TensorFlow
        try:
            import tensorflow as tf
            # 测试基本功能
            _ = tf.__version__
            self.tensorflow_available = True
            print(f"✅ TensorFlow 可用: {tf.__version__}")
        except (ImportError, AttributeError) as e:
            print(f"❌ TensorFlow 不可用: {e}")
    
    def use_pytorch_only(self):
        """强制只使用 PyTorch 后端"""
        os.environ['USE_TF'] = '0'
        os.environ['USE_TORCH'] = '1'
        print("🔧 设置为仅使用 PyTorch 后端")
    
    def use_tensorflow_only(self):
        """强制只使用 TensorFlow 后端"""
        if not self.tensorflow_available:
            raise RuntimeError("TensorFlow 不可用，无法设置为 TensorFlow 后端")
        
        os.environ['USE_TF'] = '1'
        os.environ['USE_TORCH'] = '0'
        print("🔧 设置为仅使用 TensorFlow 后端")
    
    def use_auto_backend(self):
        """自动选择最佳后端"""
        if self.torch_available and self.tensorflow_available:
            # 两个都可用，优先使用 PyTorch（更稳定）
            os.environ['USE_TF'] = '0'
            os.environ['USE_TORCH'] = '1'
            print("🔧 自动选择: PyTorch 后端（推荐）")
        elif self.torch_available:
            os.environ['USE_TF'] = '0'
            os.environ['USE_TORCH'] = '1'
            print("🔧 自动选择: PyTorch 后端（仅可用选项）")
        elif self.tensorflow_available:
            os.environ['USE_TF'] = '1'
            os.environ['USE_TORCH'] = '0'
            print("🔧 自动选择: TensorFlow 后端（仅可用选项）")
        else:
            raise RuntimeError("没有可用的后端！请安装 PyTorch 或 TensorFlow")
    
    def test_transformers(self):
        """测试 transformers 导入"""
        try:
            from transformers import pipeline
            print("✅ transformers pipeline 导入成功")
            
            # 尝试创建一个简单的 pipeline
            classifier = pipeline("sentiment-analysis", 
                                model="distilbert-base-uncased-finetuned-sst-2-english")
            result = classifier("I love this!")
            print(f"✅ pipeline 测试成功: {result}")
            return True
            
        except Exception as e:
            print(f"❌ transformers 测试失败: {e}")
            return False

def main():
    """主函数"""
    print("=== 智能后端管理器 ===")
    
    manager = BackendManager()
    
    print(f"\n后端状态:")
    print(f"  PyTorch: {'✅' if manager.torch_available else '❌'}")
    print(f"  TensorFlow: {'✅' if manager.tensorflow_available else '❌'}")
    
    # 根据命令行参数选择策略
    if len(sys.argv) > 1:
        strategy = sys.argv[1].lower()
        
        if strategy == 'pytorch':
            manager.use_pytorch_only()
        elif strategy == 'tensorflow':
            manager.use_tensorflow_only()
        elif strategy == 'auto':
            manager.use_auto_backend()
        else:
            print(f"未知策略: {strategy}")
            print("可用策略: pytorch, tensorflow, auto")
            return
    else:
        # 默认使用自动选择
        manager.use_auto_backend()
    
    print(f"\n当前环境变量:")
    print(f"  USE_TF: {os.environ.get('USE_TF', '未设置')}")
    print(f"  USE_TORCH: {os.environ.get('USE_TORCH', '未设置')}")
    
    print(f"\n测试 transformers...")
    success = manager.test_transformers()
    
    if success:
        print("\n🎉 后端配置成功！")
    else:
        print("\n❌ 后端配置失败，请检查安装")

if __name__ == "__main__":
    main() 
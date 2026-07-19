# Qwen3-ASR 语音识别整合包（便携版）

## 简介

基于通义千问 Qwen3-ASR 开源语音识别模型的 Windows 一键运行整合包。**内嵌 Python、所有依赖和完整模型**，复制到目标电脑双击即可使用，无需安装任何环境。

## 包内容组成（总计约 13GB）

### 模型文件（~12.3GB）

| 模型 | 大小 | 说明 |
|------|------|------|
| Qwen3-ASR-1.7B | ~8.5GB | 大模型，识别精度更高 |
| Qwen3-ASR-0.6B | ~2GB | 小模型，识别速度更快 |
| Qwen3-ForcedAligner-0.6B | ~1.8GB | 时间戳对齐模型，用于生成 SRT 字幕 |

### 内嵌 Python 运行环境（~5GB）

| 内容 | 大小 | 说明 |
|------|------|------|
| Python 3.12.8 嵌入式 | ~10MB | Python 解释器和标准库 |
| site-packages | ~1GB | 第三方库的元数据和缓存 |

### 依赖包明细（~4GB）

| 包名 | 大小 | 用途 |
|------|------|------|
| PyTorch 2.5.1+cu121 | ~2.5GB | 深度学习推理框架，支持 CUDA 12.1 GPU 加速 |
| torchvision 0.20.1+cu121 | ~6MB | PyTorch 视觉扩展 |
| transformers 4.57.6 | ~12MB | HuggingFace 模型加载和推理框架 |
| qwen-asr 0.0.6 | ~141KB | Qwen3-ASR 官方推理包 |
| gradio 6.17.3 | ~32MB | Web 界面框架 |
| gradio-client 2.5.0 | ~59KB | Gradio 客户端 |
| accelerate 1.12.0 | ~380KB | HuggingFace 加速推理工具 |
| huggingface_hub 0.36.2 | ~765KB | HuggingFace 模型下载和管理 |
| scipy 1.18.0 | ~36MB | 科学计算库 |
| scikit-learn 1.9.0 | ~8MB | 机器学习库 |
| numpy 2.4.4 | ~12MB | 数值计算基础库 |
| librosa 0.11.0 | ~260KB | 音频处理库 |
| soundfile 0.14.0 | ~1MB | 音频文件读写 |
| av 18.0.0 | ~27MB | 音视频编解码 |
| numba 0.66.0 | ~2.8MB | JIT 编译加速 |
| llvmlite 0.48.0 | ~41MB | LLVM 编译器绑定 |
| pandas 3.0.3 | ~9.8MB | 数据处理 |
| orjson 3.11.9 | ~127KB | 高速 JSON 序列化 |
| fastapi 0.139.0 | ~130KB | Web API 框架 |
| uvicorn 0.50.2 | ~72KB | ASGI 服务器 |
| tokenizers 0.22.2 | ~2.7MB | 高速分词器 |
| nagisa 0.2.11 | ~21MB | 日语分词 |
| soynlp 0.0.493 | ~416KB | 韩语自然语言处理 |
| DyNet38 2.2 | ~1.3MB | 动态神经网络库 |
| 其他依赖 | ~500MB | flask、pydantic、starlette、httpx 等

## 系统要求

| 项目 | 要求 |
|------|------|
| 操作系统 | Windows 10/11 (64-bit) |
| 显卡 | NVIDIA GTX 1060 及以上 |
| 显存 | 6GB 及以上 |
| 硬盘空间 | 至少 15GB 可用 |
| 驱动 | 已安装 NVIDIA 显卡驱动 |

**无需安装 Python、CUDA Toolkit、pip 或其他任何依赖。**

## 快速开始

1. 将整个 `Qwen3-ASR-Portable` 文件夹复制到目标电脑
2. 双击 `启动.bat`
3. 浏览器自动打开 Web 界面（如未打开，手动访问 http://localhost:7860）

## 使用方法

1. **上传音频**：点击左侧音频上传区域，支持 WAV、MP3、FLAC、OGG、M4A 等常见格式
2. **选择模型**：
   - `Qwen3-ASR-1.7B` — 大模型，识别精度更高（推荐）
   - `Qwen3-ASR-0.6B` — 小模型，识别速度更快
3. **选择语言**：默认自动检测，也可手动指定 Chinese、English 等
4. **启用时间戳**：勾选后可生成 SRT 字幕文件
5. **点击"开始识别"**：等待处理完成
6. **下载结果**：识别完成后可下载 TXT 文本文件或 SRT 字幕文件

生成的文件保存在 `outputs` 文件夹中。

## 文件结构

```
Qwen3-ASR-Portable/
├── python/                          # 内嵌 Python 3.12 + 所有依赖
│   ├── python.exe                   # Python 解释器
│   └── Lib/site-packages/           # 已安装的依赖包
├── models/
│   ├── Qwen3-ASR-0.6B/              # 小模型 (约2GB)
│   ├── Qwen3-ASR-1.7B/              # 大模型 (约8.5GB)
│   └── Qwen3-ForcedAligner-0.6B/    # 时间戳对齐模型 (约1.8GB)
├── outputs/                         # 识别结果输出目录
├── engine.py                        # ASR 推理引擎
├── srt_generator.py                 # SRT 字幕生成器
├── webui.py                         # Web 界面主程序
├── config.yaml                      # 配置文件
├── 启动.bat                         # 启动脚本
└── README.md                        # 本说明文件
```

## 支持的语言

中文、英文、粤语、阿拉伯语、德语、法语、西班牙语、葡萄牙语、印尼语、意大利语、韩语、俄语、泰语、越南语、日语、土耳其语、Hindi、马来语、荷兰语、瑞典语、丹麦语、芬兰语、波兰语、捷克语、菲律宾语、波斯语、希腊语、匈牙利语、马其顿语、罗马尼亚语，以及 22 种中国方言。

## 模型对比

| 模型 | 参数量 | 特点 | 适用场景 |
|------|--------|------|----------|
| Qwen3-ASR-1.7B | 17亿 | 精度高，效果好 | 对识别质量要求高 |
| Qwen3-ASR-0.6B | 6亿 | 速度快，资源省 | 快速处理、资源有限 |

## 常见问题

**Q: 启动后浏览器没有自动打开？**
手动在浏览器中访问 http://localhost:7860

**Q: 识别速度很慢？**
首次使用会加载模型到显存，需要等待几十秒。后续识别会快很多。如果显存不足，切换到 0.6B 小模型。

**Q: 支持哪些音频格式？**
支持 WAV、MP3、FLAC、OGG、M4A、AAC、WMA 等常见音频格式。

**Q: SRT 字幕的断句不理想？**
字幕断句基于原文标点和语音停顿。如果识别文本本身缺少标点，断句效果会受影响。

**Q: 识别结果有错误？**
可尝试切换到 1.7B 大模型以获得更高精度。专业术语识别受限于模型训练数据。

**Q: 目标电脑需要联网吗？**
不需要。所有模型和依赖都已内置，完全离线运行。

**Q: 可以删除 python 文件夹吗？**
不可以。python 文件夹包含运行所需的 Python 环境和所有依赖包，删除后无法运行。

## 技术信息

- 基于 [Qwen3-ASR](https://github.com/Web 界面基于 Gradio 构建
- 模型来源：ModelScope / HuggingFace
- 内嵌 Python：3.12.8 (embeddable package)
- PyTorch：2.5.1+cu121
- 许可证：Apache-2.0

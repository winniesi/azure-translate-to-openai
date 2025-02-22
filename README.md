# Azure Translator OpenAI Compatible API

这个项目提供了一个与 OpenAI API 兼容的接口，专门用于处理文本翻译需求。解决了在使用 OpenAI 兼容客户端（如 Cherry Studio）进行翻译时可能遇到的问题，即有时翻译内容会被误识别为 prompt 指令而非待翻译文本。

## 主要功能

- 提供与 OpenAI API 兼容的接口
- 使用 Azure Translator 服务进行可靠的文本翻译
- 支持所有 Azure Translator 支持的语言对
- 特别适合与 Cherry Studio 等工具配合使用
- 目前仅支持将中文翻译成英文

## 配置说明

1. 在项目根目录创建 `.env` 文件
2. 添加以下必要的环境变量：

```
OPENAI_API_KEY=your_openai_api_key
AZURE_TRANSLATOR_KEY=your_azure_translator_key
AZURE_TRANSLATOR_ENDPOINT=your_azure_translator_endpoint
AZURE_TRANSLATOR_LOCATION=your_azure_translator_location
```

## 使用方法

1. 在支持 OpenAI API 的客户端中，将 API 地址修改为本服务的地址
2. 使用 `OPENAI_API_KEY` 作为认证密钥
3. 发送翻译请求时，使用标准的 OpenAI chat completions 格式

## 一键部署

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fwinniesi%2Fazure-translate-to-openai&env=OPENAI_API_KEY,AZURE_TRANSLATOR_KEY,AZURE_TRANSLATOR_ENDPOINT,AZURE_TRANSLATOR_LOCATION)

部署时需要配置环境变量。
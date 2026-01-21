# RunAnywhere SDK Documentation Index

Production-ready toolkit to run AI locally on mobile devices.

## Overview

RunAnywhere SDKs enable you to run large language models (LLMs), speech-to-text, and text-to-speech directly on mobile devices without cloud dependencies.

**Detailed Documentation is located in:**
- `docs/swift/` - Swift SDK (iOS/macOS)
- `docs/kotlin/` - Kotlin SDK (Android)
- `docs/react-native/` - React Native SDK
- `docs/flutter/` - Flutter SDK

Each folder contains:
- `Documentation.md` - Complete API reference
- `ARCHITECTURE.md` - Architecture and design patterns

## Quick Reference

### SDK Installation

| Platform | Package | Install |
|----------|---------|---------|
| Swift | `runanywhere-swift` | Swift Package Manager |
| Kotlin | `io.github.sanchitmonga22:runanywhere-sdk-android` | Gradle |
| React Native | `@runanywhere/core`, `@runanywhere/llamacpp` | npm |
| Flutter | `runanywhere`, `runanywhere_llamacpp` | pub.dev |

### Common Pattern (All Platforms)

1. **Initialize** the SDK
2. **Register** the LlamaCPP backend
3. **Download** a model (with progress)
4. **Load** the model into memory
5. **Chat/Generate** text

### Supported Models

| Model | Size | RAM Required | Best For |
|-------|------|--------------|----------|
| SmolLM2 360M | ~400MB | 500MB | Fast responses |
| Qwen 2.5 0.5B | ~500MB | 600MB | Multilingual |
| Llama 3.2 1B | ~1GB | 1.2GB | General purpose |
| Mistral 7B Q4 | ~4GB | 5GB | High quality |

### Feature Matrix

| Feature | iOS | Android | React Native | Flutter |
|---------|-----|---------|--------------|---------|
| LLM Text Generation | ✅ | ✅ | ✅ | ✅ |
| Streaming | ✅ | ✅ | ✅ | ✅ |
| Speech-to-Text | ✅ | ✅ | ✅ | ✅ |
| Text-to-Speech | ✅ | ✅ | ✅ | ✅ |
| Voice Pipeline | ✅ | ✅ | ✅ | ✅ |
| Model Download | ✅ | ✅ | ✅ | ✅ |

### Minimum Requirements

| Platform | Minimum | Recommended |
|----------|---------|-------------|
| iOS | 17.0+ | 17.0+ |
| macOS | 14.0+ | 14.0+ |
| Android | API 24 (7.0) | API 28+ |
| React Native | 0.74+ | 0.76+ |
| Flutter | 3.10+ | 3.24+ |

**Memory:** 2GB minimum, 4GB+ recommended

## Resources

- **GitHub**: https://github.com/RunanywhereAI/runanywhere-sdks
- **Website**: https://www.runanywhere.ai
- **Email**: founders@runanywhere.ai

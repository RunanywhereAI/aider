# RunAnywhere SDK Documentation

Production-ready toolkit to run AI locally on mobile devices.

## Overview

RunAnywhere SDKs enable you to run large language models (LLMs), speech-to-text, and text-to-speech directly on mobile devices without cloud dependencies.

## SDK Installation

### Swift (iOS/macOS)

Add via Swift Package Manager:
```
https://github.com/RunanywhereAI/runanywhere-sdks
```

### Kotlin (Android)

Add to `build.gradle`:
```gradle
dependencies {
    implementation("com.runanywhere.sdk:runanywhere-kotlin:0.1.4")
    implementation("com.runanywhere.sdk:runanywhere-core-llamacpp:0.1.4")
}
```

### React Native

```bash
npm install @runanywhere/core @runanywhere/llamacpp
```

### Flutter

Add to `pubspec.yaml`:
```yaml
dependencies:
  runanywhere: ^0.15.11
  runanywhere_llamacpp: ^0.15.11
```

## Quick Start

All SDKs follow the same pattern:

1. **Initialize** the SDK
2. **Register** the LlamaCPP backend
3. **Download** a model
4. **Load** the model
5. **Chat/Generate** text

### Swift Example

```swift
import RunAnywhere
import RunAnywhereLlamaCpp

// Initialize
LlamaCPP.register()
try await RunAnywhere.initialize()

// Download and load
try await RunAnywhere.downloadModel("smollm2-360m")
try await RunAnywhere.loadModel("smollm2-360m")

// Generate
let response = try await RunAnywhere.chat("Hello!")
print(response)
```

### Kotlin Example

```kotlin
import com.runanywhere.sdk.public.RunAnywhere
import com.runanywhere.sdk.public.extensions.*

// Initialize
LlamaCPP.register()
RunAnywhere.initialize(environment = SDKEnvironment.DEVELOPMENT)

// Download and load
RunAnywhere.downloadModel("smollm2-360m").collect { println("${it.progress * 100}%") }
RunAnywhere.loadLLMModel("smollm2-360m")

// Generate
val response = RunAnywhere.chat("Hello!")
println(response)
```

### React Native Example

```typescript
import { RunAnywhere, SDKEnvironment } from '@runanywhere/core';
import { LlamaCPP } from '@runanywhere/llamacpp';

// Initialize
await RunAnywhere.initialize({ environment: SDKEnvironment.Development });
LlamaCPP.register();

// Download and load
await RunAnywhere.downloadModel('smollm2-360m');
await RunAnywhere.loadModel('smollm2-360m');

// Generate
const response = await RunAnywhere.chat('Hello!');
console.log(response);
```

### Flutter Example

```dart
import 'package:runanywhere/runanywhere.dart';
import 'package:runanywhere_llamacpp/runanywhere_llamacpp.dart';

// Initialize
await RunAnywhere.initialize();
await LlamaCpp.register();

// Download and load
await RunAnywhere.downloadModel('smollm2-360m');
await RunAnywhere.loadModel('smollm2-360m');

// Generate
final response = await RunAnywhere.chat('Hello!');
print(response);
```

## Supported Models

### LLM Models (GGUF format)

| Model         | Size    | RAM Required | Best For          |
|---------------|---------|--------------|-------------------|
| SmolLM2 360M  | ~400MB  | 500MB        | Fast responses    |
| Qwen 2.5 0.5B | ~500MB  | 600MB        | Multilingual      |
| Llama 3.2 1B  | ~1GB    | 1.2GB        | General purpose   |
| Mistral 7B Q4 | ~4GB    | 5GB          | High quality      |

### Speech-to-Text (Whisper)

| Model        | Size    | Languages    |
|--------------|---------|--------------|
| Whisper Tiny | ~75MB   | English      |
| Whisper Base | ~150MB  | Multilingual |

### Text-to-Speech (Piper)

| Voice                 | Size   | Language     |
|-----------------------|--------|--------------|
| Piper US English      | ~65MB  | English (US) |
| Piper British English | ~65MB  | English (UK) |

## Features

### Text Generation

```swift
// Simple chat
let response = try await RunAnywhere.chat("What is AI?")

// With system prompt
let response = try await RunAnywhere.chat(
    "What is AI?",
    systemPrompt: "You are a helpful teacher"
)
```

### Streaming

```swift
// Swift streaming
for try await chunk in RunAnywhere.streamChat("Tell me a story") {
    print(chunk, terminator: "")
}
```

```kotlin
// Kotlin streaming
RunAnywhere.streamChat("Tell me a story").collect { chunk ->
    print(chunk)
}
```

```typescript
// React Native streaming
await RunAnywhere.streamChat('Tell me a story', (chunk) => {
    process.stdout.write(chunk);
});
```

```dart
// Flutter streaming
await for (final chunk in RunAnywhere.streamChat('Tell me a story')) {
    stdout.write(chunk);
}
```

### Speech-to-Text

```swift
// Swift
let text = try await RunAnywhere.transcribe(audioData)
```

```kotlin
// Kotlin
val text = RunAnywhere.transcribe(audioData)
```

### Text-to-Speech

```swift
// Swift
let audioData = try await RunAnywhere.synthesize("Hello world")
```

```kotlin
// Kotlin
val audioData = RunAnywhere.synthesize("Hello world")
```

### Voice Assistant Pipeline

Combines STT → LLM → TTS for voice interactions:

```swift
// Swift voice assistant
let pipeline = VoiceAssistantPipeline()
pipeline.onResponse = { text, audio in
    // Handle response
}
try await pipeline.process(audioInput)
```

## Best Practices

1. **Initialize Early**: Initialize RunAnywhere when your app starts
2. **Show Progress**: Always show download progress to users
3. **Handle Errors**: Wrap all async calls in try/catch
4. **Memory Management**: Unload models when not needed
5. **Background Loading**: Load models in background threads
6. **Model Selection**: Start with smaller models for faster responses

## Error Handling

```swift
do {
    try await RunAnywhere.loadModel("smollm2-360m")
} catch RunAnywhereError.modelNotFound {
    // Model hasn't been downloaded
} catch RunAnywhereError.insufficientMemory {
    // Not enough RAM for this model
} catch {
    // Other errors
}
```

## Platform Requirements

| Platform     | Minimum      | Recommended | Notes                    |
|--------------|--------------|-------------|--------------------------|
| iOS          | 17.0+        | 17.0+       | iPhone XS or newer       |
| macOS        | 14.0+        | 14.0+       | Apple Silicon preferred  |
| Android      | API 24 (7.0) | API 28+     | 4GB+ RAM recommended     |
| React Native | 0.74+        | 0.76+       | New Architecture ready   |
| Flutter      | 3.10+        | 3.24+       | Dart 3.0+                |

## Resources

- **GitHub**: https://github.com/RunanywhereAI/runanywhere-sdks
- **Website**: https://www.runanywhere.ai
- **Discord**: Join our community
- **Email**: founders@runanywhere.ai

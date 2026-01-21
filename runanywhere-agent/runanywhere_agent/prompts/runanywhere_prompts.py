"""
Custom system prompts for RunAnywhere SDK development.

These prompts are optimized for building mobile apps with on-device AI
using the RunAnywhere SDKs.
"""

import importlib.resources
from pathlib import Path

# ============================================================================
# MAIN SYSTEM PROMPT
# ============================================================================

RUNANYWHERE_SYSTEM_PROMPT = """Act as an expert mobile/cross-platform developer specializing in on-device AI applications using RunAnywhere SDKs.

You are an expert in these 4 RunAnywhere SDKs for running AI locally on mobile devices:

1. **Swift SDK** (iOS/macOS)
   - Package: `runanywhere-swift`
   - Install: Swift Package Manager from https://github.com/RunanywhereAI/runanywhere-sdks

2. **Kotlin SDK** (Android)
   - Package: `com.runanywhere.sdk:runanywhere-kotlin`
   - Install: Gradle dependency

3. **React Native SDK**
   - Packages: `@runanywhere/core`, `@runanywhere/llamacpp`
   - Install: npm install

4. **Flutter SDK**
   - Packages: `runanywhere`, `runanywhere_llamacpp`
   - Install: pub.dev dependencies

Always use best practices when coding with RunAnywhere SDKs:
- Initialize RunAnywhere before any operations
- Register the LlamaCPP backend before loading models
- Download models before loading them (handle progress)
- Use async/await patterns appropriately for each platform
- Handle errors gracefully with try/catch blocks
- Clean up resources when done

{sdk_documentation}

{final_reminders}
"""

# ============================================================================
# SDK DOCUMENTATION
# ============================================================================

SDK_DOCUMENTATION = """
## RunAnywhere SDK Quick Reference

### Common Patterns (All Platforms)

1. **Initialize** → 2. **Register Backend** → 3. **Download Model** → 4. **Load Model** → 5. **Generate/Chat**

### Supported Models

| Model         | Size    | RAM Required | Use Case          |
|---------------|---------|--------------|-------------------|
| SmolLM2 360M  | ~400MB  | 500MB        | Fast, lightweight |
| Qwen 2.5 0.5B | ~500MB  | 600MB        | Multilingual      |
| Llama 3.2 1B  | ~1GB    | 1.2GB        | Balanced          |
| Mistral 7B Q4 | ~4GB    | 5GB          | High quality      |

### Swift SDK (iOS/macOS)

```swift
import RunAnywhere
import RunAnywhereLlamaCpp

// 1. Initialize
LlamaCPP.register()
try await RunAnywhere.initialize()

// 2. Download and load model
try await RunAnywhere.downloadModel("smollm2-360m")
try await RunAnywhere.loadModel("smollm2-360m")

// 3. Generate
let response = try await RunAnywhere.chat("What is the capital of France?")
print(response) // "Paris is the capital of France."

// Streaming example
for try await chunk in RunAnywhere.streamChat("Tell me a story") {
    print(chunk, terminator: "")
}
```

**Install via Swift Package Manager:**
```
https://github.com/RunanywhereAI/runanywhere-sdks
```

### Kotlin SDK (Android)

```kotlin
import com.runanywhere.sdk.public.RunAnywhere
import com.runanywhere.sdk.public.extensions.*

// 1. Initialize
LlamaCPP.register()
RunAnywhere.initialize(environment = SDKEnvironment.DEVELOPMENT)

// 2. Download model with progress
RunAnywhere.downloadModel("smollm2-360m").collect { progress ->
    println("Download: ${progress.progress * 100}%")
}

// 3. Load and generate
RunAnywhere.loadLLMModel("smollm2-360m")
val response = RunAnywhere.chat("What is the capital of France?")
println(response) // "Paris is the capital of France."

// Streaming example
RunAnywhere.streamChat("Tell me a story").collect { chunk ->
    print(chunk)
}
```

**Install via Gradle:**
```gradle
dependencies {
    implementation("com.runanywhere.sdk:runanywhere-kotlin:0.1.4")
    implementation("com.runanywhere.sdk:runanywhere-core-llamacpp:0.1.4")
}
```

### React Native SDK

```typescript
import { RunAnywhere, SDKEnvironment } from '@runanywhere/core';
import { LlamaCPP } from '@runanywhere/llamacpp';

// 1. Initialize
await RunAnywhere.initialize({ environment: SDKEnvironment.Development });
LlamaCPP.register();

// 2. Download and load model
await RunAnywhere.downloadModel('smollm2-360m', (progress) => {
    console.log(`Download: ${progress * 100}%`);
});
await RunAnywhere.loadModel('smollm2-360m');

// 3. Generate
const response = await RunAnywhere.chat('What is the capital of France?');
console.log(response); // "Paris is the capital of France."

// Streaming example
await RunAnywhere.streamChat('Tell me a story', (chunk) => {
    process.stdout.write(chunk);
});
```

**Install via npm:**
```bash
npm install @runanywhere/core @runanywhere/llamacpp
```

### Flutter SDK

```dart
import 'package:runanywhere/runanywhere.dart';
import 'package:runanywhere_llamacpp/runanywhere_llamacpp.dart';

// 1. Initialize
await RunAnywhere.initialize();
await LlamaCpp.register();

// 2. Download and load model
await RunAnywhere.downloadModel('smollm2-360m', onProgress: (progress) {
    print('Download: ${progress * 100}%');
});
await RunAnywhere.loadModel('smollm2-360m');

// 3. Generate
final response = await RunAnywhere.chat('What is the capital of France?');
print(response); // "Paris is the capital of France."

// Streaming example
await for (final chunk in RunAnywhere.streamChat('Tell me a story')) {
    stdout.write(chunk);
}
```

**Install via pub.dev:**
```yaml
dependencies:
  runanywhere: ^0.15.11
  runanywhere_llamacpp: ^0.15.11
```

### Feature Support Matrix

| Feature                   | iOS | Android | React Native | Flutter |
|---------------------------|-----|---------|--------------|---------|
| LLM Text Generation       | ✅  | ✅      | ✅           | ✅      |
| Streaming                 | ✅  | ✅      | ✅           | ✅      |
| Speech-to-Text            | ✅  | ✅      | ✅           | ✅      |
| Text-to-Speech            | ✅  | ✅      | ✅           | ✅      |
| Voice Assistant Pipeline  | ✅  | ✅      | ✅           | ✅      |
| Model Download + Progress | ✅  | ✅      | ✅           | ✅      |
| Structured Output (JSON)  | ✅  | ✅      | 🔜          | 🔜     |
| Apple Foundation Models   | ✅  | —       | —            | —       |

### Minimum Requirements

| Platform     | Minimum      | Recommended |
|--------------|--------------|-------------|
| iOS          | 17.0+        | 17.0+       |
| macOS        | 14.0+        | 14.0+       |
| Android      | API 24 (7.0) | API 28+     |
| React Native | 0.74+        | 0.76+       |
| Flutter      | 3.10+        | 3.24+       |

**Memory:** 2GB minimum, 4GB+ recommended for larger models
"""


def get_sdk_documentation() -> str:
    """
    Get the full SDK documentation for injection into prompts.
    
    Loads documentation from all SDK docs files (Swift, Kotlin, React Native, Flutter).
    
    Returns:
        SDK documentation string.
    """
    docs_parts = []
    
    # Try to load from resources/docs folder
    try:
        resources_path = Path(__file__).parent.parent / "resources"
        docs_path = resources_path / "docs"
        
        if docs_path.exists():
            # Load all SDK documentation files
            sdk_folders = ["swift", "kotlin", "react-native", "flutter"]
            
            for sdk in sdk_folders:
                sdk_path = docs_path / sdk
                if sdk_path.exists():
                    # Load Documentation.md
                    doc_file = sdk_path / "Documentation.md"
                    if doc_file.exists():
                        content = doc_file.read_text(encoding="utf-8")
                        docs_parts.append(f"\n\n{'='*80}\n{sdk.upper()} SDK DOCUMENTATION\n{'='*80}\n\n{content}")
                    
                    # Load ARCHITECTURE.md
                    arch_file = sdk_path / "ARCHITECTURE.md"
                    if arch_file.exists():
                        content = arch_file.read_text(encoding="utf-8")
                        docs_parts.append(f"\n\n{'='*80}\n{sdk.upper()} SDK ARCHITECTURE\n{'='*80}\n\n{content}")
            
            if docs_parts:
                return "\n".join(docs_parts)
        
        # Fall back to main sdk-documentation.md
        main_docs = resources_path / "sdk-documentation.md"
        if main_docs.exists():
            return main_docs.read_text(encoding="utf-8")
            
    except Exception:
        pass
    
    # Fall back to embedded documentation
    return SDK_DOCUMENTATION


def get_system_prompt() -> str:
    """
    Get the complete system prompt with SDK documentation.
    
    Returns:
        Complete system prompt string.
    """
    docs = get_sdk_documentation()
    return RUNANYWHERE_SYSTEM_PROMPT.replace("{sdk_documentation}", docs)


# ============================================================================
# ADDITIONAL PROMPTS
# ============================================================================

RUNANYWHERE_EXAMPLE_MESSAGES = [
    {
        "role": "user",
        "content": "Create a simple iOS app that runs a local LLM",
    },
    {
        "role": "assistant", 
        "content": """I'll create a simple iOS app using the RunAnywhere Swift SDK. Here's the implementation:

ContentView.swift
```swift
import SwiftUI
import RunAnywhere
import RunAnywhereLlamaCpp

struct ContentView: View {
    @State private var prompt = ""
    @State private var response = ""
    @State private var isLoading = false
    @State private var isModelReady = false
    
    var body: some View {
        VStack(spacing: 20) {
            Text("RunAnywhere Demo")
                .font(.title)
            
            if !isModelReady {
                Button("Load Model") {
                    Task { await loadModel() }
                }
                .disabled(isLoading)
            } else {
                TextField("Enter prompt", text: $prompt)
                    .textFieldStyle(.roundedBorder)
                
                Button("Generate") {
                    Task { await generate() }
                }
                .disabled(isLoading || prompt.isEmpty)
                
                if isLoading {
                    ProgressView()
                }
                
                ScrollView {
                    Text(response)
                }
            }
        }
        .padding()
    }
    
    func loadModel() async {
        isLoading = true
        defer { isLoading = false }
        
        do {
            LlamaCPP.register()
            try await RunAnywhere.initialize()
            try await RunAnywhere.downloadModel("smollm2-360m")
            try await RunAnywhere.loadModel("smollm2-360m")
            isModelReady = true
        } catch {
            response = "Error: \\(error.localizedDescription)"
        }
    }
    
    func generate() async {
        isLoading = true
        defer { isLoading = false }
        
        do {
            response = try await RunAnywhere.chat(prompt)
        } catch {
            response = "Error: \\(error.localizedDescription)"
        }
    }
}
```

This creates a minimal iOS app that:
1. Initializes RunAnywhere with the LlamaCPP backend
2. Downloads and loads the SmolLM2 360M model
3. Lets users enter prompts and see AI responses

To use this, add the RunAnywhere SDK via Swift Package Manager using the URL: https://github.com/RunanywhereAI/runanywhere-sdks""",
    },
]

RUNANYWHERE_SYSTEM_REMINDER = """Remember:
- Always initialize RunAnywhere and register LlamaCPP before using other features
- Handle async operations properly for each platform
- Show download progress to users when downloading models
- Handle errors gracefully with try/catch
- Clean up resources when the app closes or component unmounts

{final_reminders}
"""

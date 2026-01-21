"""
Monkey-patching module to inject RunAnywhere SDK prompts into aider.

This module modifies aider's prompt classes at runtime to include
RunAnywhere SDK-specific documentation and examples.
"""

from .runanywhere_prompts import (
    RUNANYWHERE_EXAMPLE_MESSAGES,
    RUNANYWHERE_SYSTEM_PROMPT,
    RUNANYWHERE_SYSTEM_REMINDER,
    get_sdk_documentation,
)


def patch_aider_prompts() -> None:
    """
    Patch aider's prompt classes to include RunAnywhere SDK context.
    
    This function modifies the system prompts and example messages
    in aider's coder classes to focus on RunAnywhere SDK development.
    """
    try:
        # Import aider's prompt modules
        from aider.coders import (
            editblock_prompts,
            wholefile_prompts,
            base_prompts,
        )
        from aider.coders.editblock_fenced_prompts import EditBlockFencedPrompts
        from aider.coders.udiff_prompts import UnifiedDiffPrompts
        
        sdk_docs = get_sdk_documentation()
        
        # Create the enhanced system prompt
        runanywhere_prefix = f"""You are an expert mobile/cross-platform developer specializing in RunAnywhere SDKs for on-device AI.

Focus on helping users build apps with these SDKs:
- Swift SDK (iOS/macOS): runanywhere-swift
- Kotlin SDK (Android): runanywhere-kotlin
- React Native SDK: @runanywhere/core, @runanywhere/llamacpp
- Flutter SDK: runanywhere, runanywhere_llamacpp

Key patterns to follow:
1. Always initialize RunAnywhere before use
2. Register LlamaCPP backend before loading models
3. Download models before loading them
4. Use async/await patterns appropriately
5. Handle errors gracefully

{sdk_docs}

---

"""
        
        # Patch EditBlockPrompts (the main diff-based editing format)
        original_editblock_system = editblock_prompts.EditBlockPrompts.main_system
        editblock_prompts.EditBlockPrompts.main_system = runanywhere_prefix + original_editblock_system
        
        # Patch WholeFilePrompts
        original_wholefile_system = wholefile_prompts.WholeFilePrompts.main_system
        wholefile_prompts.WholeFilePrompts.main_system = runanywhere_prefix + original_wholefile_system
        
        # Patch EditBlockFencedPrompts
        try:
            original_fenced_system = EditBlockFencedPrompts.main_system
            EditBlockFencedPrompts.main_system = runanywhere_prefix + original_fenced_system
        except Exception:
            pass
        
        # Patch UnifiedDiffPrompts
        try:
            original_udiff_system = UnifiedDiffPrompts.main_system
            UnifiedDiffPrompts.main_system = runanywhere_prefix + original_udiff_system
        except Exception:
            pass
        
        # Add example messages if they exist
        try:
            # Add RunAnywhere examples to the end of existing examples
            if hasattr(editblock_prompts.EditBlockPrompts, 'example_messages'):
                editblock_prompts.EditBlockPrompts.example_messages.extend(RUNANYWHERE_EXAMPLE_MESSAGES)
        except Exception:
            pass
        
        print("✓ RunAnywhere SDK prompts loaded")
        
    except ImportError as e:
        print(f"Warning: Could not patch aider prompts: {e}")
    except Exception as e:
        print(f"Warning: Error patching prompts: {e}")


def patch_help_system() -> None:
    """
    Patch aider's help system to include RunAnywhere SDK documentation.
    
    This modifies the HelpPrompts class to focus on RunAnywhere SDK help.
    """
    try:
        from aider.coders.help_prompts import HelpPrompts
        
        HelpPrompts.main_system = """You are an expert on building mobile apps with RunAnywhere SDKs.
Answer the user's questions about how to use RunAnywhere SDKs to build apps with on-device AI.

RunAnywhere provides SDKs for:
- Swift (iOS/macOS)
- Kotlin (Android)
- React Native
- Flutter

Use the provided RunAnywhere SDK documentation to answer questions.

Include links to relevant RunAnywhere resources:
- https://github.com/RunanywhereAI/runanywhere-sdks
- https://www.runanywhere.ai

If you don't know the answer, suggest checking the GitHub repository or contacting founders@runanywhere.ai.

Be helpful but concise.

Keep this info about the user's system in mind:
{platform}
"""
        
        HelpPrompts.repo_content_prefix = """Here are summaries of some files in the project.
These may help you understand how RunAnywhere SDKs are being used.
"""
        
        print("✓ RunAnywhere help system loaded")
        
    except ImportError as e:
        print(f"Warning: Could not patch help system: {e}")
    except Exception as e:
        print(f"Warning: Error patching help system: {e}")


def patch_commit_prompts() -> None:
    """
    Patch aider's commit message prompts to include RunAnywhere context.
    """
    try:
        from aider import prompts
        
        original_commit_system = prompts.commit_system
        
        # Add RunAnywhere context to commit messages
        prompts.commit_system = original_commit_system + """

When the changes involve RunAnywhere SDK code, use appropriate prefixes:
- feat(swift): for Swift SDK changes
- feat(kotlin): for Kotlin SDK changes  
- feat(react-native): for React Native SDK changes
- feat(flutter): for Flutter SDK changes
- feat(ai): for AI/ML related changes
"""
        
    except ImportError:
        pass
    except Exception:
        pass


def apply_all_patches() -> None:
    """Apply all RunAnywhere-specific patches to aider."""
    patch_aider_prompts()
    patch_help_system()
    patch_commit_prompts()

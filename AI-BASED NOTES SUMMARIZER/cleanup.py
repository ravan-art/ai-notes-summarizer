"""
Cleanup Script - Remove Unnecessary Files
"""
import os

# Files to remove (documentation and test files)
files_to_remove = [
    'ACCURACY_IMPROVEMENTS.txt',
    'ACCURACY_OPTIMIZATION.txt',
    'ALL_FEATURES_FIXED.txt',
    'app_missing_part.py',
    'ARCHITECTURE.txt',
    'BEFORE_AFTER_COMPARISON.txt',
    'BUILD_ERROR_FIXED.txt',
    'CHANGES_SUMMARY.txt',
    'CHAT_FEATURE_README.md',
    'CHAT_UI_PREVIEW.txt',
    'check_install.py',
    'COMPLETE_DEBUG_GUIDE.txt',
    'DARK_THEME.txt',
    'DEBUG_AND_FIX.bat',
    'DEBUG_COMPLETE.txt',
    'debug_project.py',
    'debug_system.py',
    'DEPLOYMENT_CHECKLIST.txt',
    'EXAMPLE_QUESTIONS.txt',
    'FINAL_DEBUG_SUMMARY.txt',
    'FINAL_IMPLEMENTATION.txt',
    'FINAL_SUMMARY.txt',
    'FIX_NOT_FOUND_ERROR.txt',
    'FIX_YOUTUBE_MODULE.bat',
    'FIXED_AND_WORKING.txt',
    'HOW_TO_GET_ACCURATE_ANSWERS.txt',
    'IMPLEMENTATION_SUMMARY.txt',
    'INSTALL.txt',
    'INTELLIGENCE_COMPARISON.txt',
    'INTELLIGENT_CHATBOT_GUIDE.txt',
    'INTELLIGENT_CHATBOT_SUMMARY.txt',
    'MAXIMUM_ACCURACY_GUIDE.txt',
    'MODULE_ERROR_FIX.txt',
    'QUICK_REFERENCE.txt',
    'quick_start.py',
    'README_CHAT_FEATURE.txt',
    'README_INTELLIGENT_AI.txt',
    'README_START_HERE.txt',
    'run_app.py',
    'RUN_SERVER.bat',
    'SETUP_CHAT_FEATURE.bat',
    'SETUP_INTELLIGENT_CHATBOT.bat',
    'SIMPLIFIED.txt',
    'START_HERE.txt',
    'start.py',
    'SUMMARIZATION_VERIFICATION.txt',
    'test_features.py',
    'test_qa_system.py',
    'test_routes.py',
    'test_summarization.py',
    'test_youtube.py',
    'test_yt_fixed.py',
    'UI_UX_IMPROVEMENTS.txt',
    'update_database.py',
    'verify.py',
    'YOUTUBE_ERROR_FIXED.txt'
]

print("Cleaning up unnecessary files...")
print("="*60)

removed = 0
not_found = 0

for file in files_to_remove:
    if os.path.exists(file):
        try:
            os.remove(file)
            print(f"Removed: {file}")
            removed += 1
        except Exception as e:
            print(f"Error removing {file}: {e}")
    else:
        not_found += 1

print("="*60)
print(f"Cleanup complete!")
print(f"Removed: {removed} files")
print(f"Not found: {not_found} files")
print("\nKeeping essential files:")
print("  - app.py (main application)")
print("  - models.py (database models)")
print("  - requirements.txt (dependencies)")
print("  - README.md (documentation)")
print("  - .env.example (config template)")
print("  - utils/ (utility modules)")
print("  - templates/ (HTML templates)")
print("  - static/ (CSS, JS, assets)")

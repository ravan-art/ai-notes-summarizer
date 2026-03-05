import os
import sys

def check_installation():
    print("\n🔍 Installation Check (SmartStudyHub)\n" + "="*40)
    
    # 1. Check Python Packages
    print("1. Checking Python Libraries:")
    
    # Check Pillow
    try:
        from PIL import Image
        print("   ✅ Pillow (Image Library) is installed.")
    except ImportError:
        print("   ❌ Pillow is NOT installed.")
        print("      Run: pip install Pillow")

    # Check Pytesseract
    try:
        import pytesseract
        print("   ✅ pytesseract is installed.")
    except ImportError:
        print("   ❌ pytesseract is NOT installed.")
        print("      Run: pip install pytesseract")

    print("-" * 40)

    # 2. Check Tesseract-OCR Software
    print("2. Checking Tesseract-OCR Software:")
    
    # Common default path for Windows
    tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    if os.path.exists(tesseract_path):
        print(f"   ✅ Tesseract.exe found at: {tesseract_path}")
        
        # Try to run it
        try:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            version = pytesseract.get_tesseract_version()
            print(f"   ✅ Tesseract Version: {version}")
            print("\n🎉 Sab kuch sahi se install ho gaya hai! Aap app run kar sakte hain.")
        except Exception as e:
            print(f"   ⚠️ Tesseract found but gave an error: {e}")
    else:
        print("   ❌ Tesseract.exe NOT FOUND at default location.")
        print(f"      Expected: {tesseract_path}")
        print("\n   Agar aapne install nahi kiya hai, to yahan se karein:")
        print("   👉 https://github.com/UB-Mannheim/tesseract/wiki")
        print("   (Install karte waqt path change mat karna)")

    print("="*40 + "\n")

if __name__ == "__main__":
    check_installation()
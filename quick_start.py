#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Start Guide สำหรับการใช้งาน OpenCV Homography Matcher
กับภาพของคุณเอง
"""

import os
import shutil
from pathlib import Path


def setup_user_workspace():
    """
    ตั้งค่าพื้นที่ทำงานสำหรับผู้ใช้
    """
    print("🚀 OpenCV Homography Matcher - Quick Start Setup")
    print("=" * 60)

    # สร้างโฟลเดอร์สำหรับภาพของผู้ใช้
    user_dirs = [
        "my_images/eye_level",    # ภาพระดับตา
        "my_images/top_down",     # ภาพแผนที่/โดรน
        "my_results",             # ผลลัพธ์
    ]

    for dir_path in user_dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"📁 สร้างโฟลเดอร์: {dir_path}")

    # สร้างไฟล์ตัวอย่างการใช้งาน
    create_usage_examples()

    print("\n✅ ตั้งค่าเสร็จสิ้น!")
    print("\n📋 วิธีการใช้งาน:")
    print("1. วางภาพ Eye-Level ในโฟลเดอร์ my_images/eye_level/")
    print("2. วางภาพ Top-Down ในโฟลเดอร์ my_images/top_down/")
    print("3. รันคำสั่ง: python quick_start.py")


def create_usage_examples():
    """
    สร้างไฟล์ตัวอย่างการใช้งาน
    """

    # สร้างไฟล์ batch script สำหรับ Windows
    batch_content = """@echo off
echo OpenCV Homography Matcher - Quick Start
echo ========================================

REM ตรวจสอบว่ามีภาพในโฟลเดอร์หรือไม่
if not exist "my_images\\eye_level\\*.jpg" if not exist "my_images\\eye_level\\*.png" (
    echo ❌ ไม่พบภาพ Eye-Level ในโฟลเดอร์ my_images/eye_level/
    echo กรุณาวางภาพในโฟลเดอร์ดังกล่าวก่อน
    pause
    exit /b
)

if not exist "my_images\\top_down\\*.jpg" if not exist "my_images\\top_down\\*.png" (
    echo ❌ ไม่พบภาพ Top-Down ในโฟลเดอร์ my_images/top_down/
    echo กรุณาวางภาพในโฟลเดอร์ดังกล่าวก่อน
    pause
    exit /b
)

echo 🔍 กำลังค้นหาภาพ...
for %%f in (my_images\\eye_level\\*.jpg my_images\\eye_level\\*.png) do set "EYE_LEVEL=%%f"
for %%f in (my_images\\top_down\\*.jpg my_images\\top_down\\*.png) do set "TOP_DOWN=%%f"

echo 📷 Eye-Level: %EYE_LEVEL%
echo 🗺️ Top-Down: %TOP_DOWN%

echo.
echo 🚀 เริ่มการเปรียบเทียบ...
C:/Python313/python.exe cli.py --eye "%EYE_LEVEL%" --top "%TOP_DOWN%" --benchmark --output my_results

echo.
echo ✅ เสร็จสิ้น! ดูผลลัพธ์ในโฟลเดอร์ my_results/
pause
"""

    with open("run_my_images.bat", "w", encoding="utf-8") as f:
        f.write(batch_content)

    # สร้างไฟล์ Python script
    py_content = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import glob
from pathlib import Path
import subprocess

def find_user_images():
    \"\"\"หาภาพในโฟลเดอร์ของผู้ใช้\"\"\"

    eye_level_patterns = ['my_images/eye_level/*.jpg', 'my_images/eye_level/*.png', 'my_images/eye_level/*.jpeg']
    top_down_patterns = ['my_images/top_down/*.jpg', 'my_images/top_down/*.png', 'my_images/top_down/*.jpeg']

    eye_level_images = []
    top_down_images = []

    for pattern in eye_level_patterns:
        eye_level_images.extend(glob.glob(pattern))

    for pattern in top_down_patterns:
        top_down_images.extend(glob.glob(pattern))

    return eye_level_images, top_down_images

def main():
    print("🔍 OpenCV Homography Matcher - รันกับภาพของคุณ")
    print("=" * 60)

    # หาภาพ
    eye_images, top_images = find_user_images()

    if not eye_images:
        print("❌ ไม่พบภาพ Eye-Level ในโฟลเดอร์ my_images/eye_level/")
        print("กรุณาวางภาพในโฟลเดอร์ดังกล่าวก่อน")
        return

    if not top_images:
        print("❌ ไม่พบภาพ Top-Down ในโฟลเดอร์ my_images/top_down/")
        print("กรุณาวางภาพในโฟลเดอร์ดังกล่าวก่อน")
        return

    print(f"📷 พบภาพ Eye-Level: {len(eye_images)} ไฟล์")
    print(f"🗺️ พบภาพ Top-Down: {len(top_images)} ไฟล์")

    # ทดสอบภาพแต่ละคู่
    for i, eye_img in enumerate(eye_images):
        for j, top_img in enumerate(top_images):
            print(f"\\n🔍 ทดสอบคู่ที่ {i+1}-{j+1}")
            print(f"   Eye-Level: {os.path.basename(eye_img)}")
            print(f"   Top-Down:  {os.path.basename(top_img)}")

            output_dir = f"my_results/pair_{i+1}_{j+1}"

            try:
                # รัน CLI
                cmd = [
                    "C:/Python313/python.exe", "cli.py",
                    "--eye", eye_img,
                    "--top", top_img,
                    "--benchmark",
                    "--output", output_dir
                ]

                result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

                if result.returncode == 0:
                    print("   ✅ สำเร็จ")
                else:
                    print("   ❌ ล้มเหลว")

            except Exception as e:
                print(f"   ❌ ข้อผิดพลาด: {e}")

    print(f"\\n🎉 เสร็จสิ้น! ดูผลลัพธ์ในโฟลเดอร์ my_results/")

if __name__ == "__main__":
    main()
"""

    with open("run_my_images.py", "w", encoding="utf-8") as f:
        f.write(py_content)

    # สร้างไฟล์ README สำหรับผู้ใช้
    readme_content = """# วิธีการใช้งานกับภาพของคุณเอง

## 📋 ขั้นตอนการใช้งาน

### 1. เตรียมภาพ
- วางภาพ **Eye-Level** (มุมมองระดับตา) ในโฟลเดอร์ `my_images/eye_level/`
- วางภาพ **Top-Down** (มุมมองจากด้านบน/แผนที่) ในโฟลเดอร์ `my_images/top_down/`

### 2. รันการเปรียบเทียบ

**วิธีที่ 1: ใช้ Batch Script (Windows)**
```bash
run_my_images.bat
```

**วิธีที่ 2: ใช้ Python Script**
```bash
python run_my_images.py
```

**วิธีที่ 3: ใช้ CLI โดยตรง**
```bash
python cli.py --eye my_images/eye_level/your_photo.jpg --top my_images/top_down/map.jpg --benchmark
```

### 3. ดูผลลัพธ์
ผลลัพธ์จะถูกบันทึกในโฟลเดอร์ `my_results/`

## 📸 ประเภทภาพที่รองรับ
- JPG, JPEG, PNG
- ขนาดภาพแนะนำ: 500x500 ถึง 2000x2000 pixels
- ความละเอียดสูงเกินไปอาจทำให้ช้า

## 💡 เทคนิคการถ่ายภาพที่ดี

### ภาพ Eye-Level
- ถ่ายจากระดับสายตาคน
- มีวัตถุหรืออาคารที่โดดเด่น
- หลีกเลี่ยงการเบลอหรือสั่นไหว
- ควรมีรายละเอียดที่ชัดเจน

### ภาพ Top-Down
- ถ่ายจากโดรนหรือใช้แผนที่
- ครอบคลุมพื้นที่เดียวกับภาพ Eye-Level
- มีโครงสร้างหรือสิ่งปลูกสร้างที่เห็นได้ชัด
- หลีกเลี่ยงเงาหรือแสงสะท้อนมาก

## 🎯 ผลลัพธ์ที่คาดหวัง

### Confidence Score
- **0.7-1.0**: ยอดเยี่ยม - ผลลัพธ์เชื่อถือได้สูง
- **0.5-0.7**: ดี - ใช้งานได้
- **0.3-0.5**: ปานกลาง - ควรตรวจสอบ
- **< 0.3**: ต่ำ - ไม่แนะนำให้ใช้

### ไฟล์ผลลัพธ์
- `matches_visualization.jpg` - การแสดงผลการจับคู่
- `comparison.jpg` - การเปรียบเทียบภาพที่แปลงแล้ว
- `transformed_eye_level.jpg` - ภาพที่ถูกแปลง

## ❓ แก้ไขปัญหา

### ไม่พบ matches เพียงพอ
- ลองเปลี่ยน feature detector
- ตรวจสอบว่าภาพมีวัตถุร่วมกันหรือไม่
- ปรับปรุงคุณภาพภาพ

### ผลลัพธ์ไม่แม่นยำ
- ใช้ภาพที่มีรายละเอียดมากขึ้น
- ตรวจสอบการจัดตำแหน่งของภาพ
- ลองใช้ detector อื่น

## 📞 ความช่วยเหลือ
หากมีปัญหา กรุณาตรวจสอบ:
1. ไฟล์ภาพสามารถเปิดได้
2. ภาพทั้งสองมีพื้นที่ที่เหมือนกัน
3. คุณภาพภาพไม่เบลอเกินไป
"""

    with open("my_images/README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    print("📝 สร้างไฟล์ตัวอย่างการใช้งาน:")
    print("   • run_my_images.bat (Windows batch script)")
    print("   • run_my_images.py (Python script)")
    print("   • my_images/README.md (คู่มือการใช้งาน)")


def main():
    setup_user_workspace()


if __name__ == "__main__":
    main()

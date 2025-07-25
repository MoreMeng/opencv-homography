#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import glob
from pathlib import Path
import subprocess

def find_user_images():
    """หาภาพในโฟลเดอร์ของผู้ใช้"""

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
            print(f"\n🔍 ทดสอบคู่ที่ {i+1}-{j+1}")
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

    print(f"\n🎉 เสร็จสิ้น! ดูผลลัพธ์ในโฟลเดอร์ my_results/")

if __name__ == "__main__":
    main()

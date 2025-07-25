#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ตัวอย่างการใช้งาน HomographyMatcher แบบง่าย
สำหรับทดสอบเปรียบเทียบภาพ Eye-Level กับ Top-Down
"""

import cv2
import numpy as np
import os
from homography_matcher import HomographyMatcher


def create_sample_images():
    """
    สร้างภาพตัวอย่างสำหรับทดสอบ
    """
    print("🎨 กำลังสร้างภาพตัวอย่างสำหรับทดสอบ...")

    # สร้างโฟลเดอร์สำหรับภาพตัวอย่าง
    os.makedirs("sample_images", exist_ok=True)

    # สร้างภาพ Top-Down (มุมมองจากด้านบน)
    top_down = np.ones((600, 800, 3), dtype=np.uint8) * 50

    # วาดอาคารหรือวัตถุต่างๆ ในมุมมอง top-down
    # อาคาร 1 (สี่เหลี่ยม)
    cv2.rectangle(top_down, (100, 100), (300, 250), (100, 150, 200), -1)
    cv2.rectangle(top_down, (100, 100), (300, 250), (255, 255, 255), 2)

    # อาคาร 2
    cv2.rectangle(top_down, (450, 150), (650, 300), (150, 200, 100), -1)
    cv2.rectangle(top_down, (450, 150), (650, 300), (255, 255, 255), 2)

    # ถนน
    cv2.rectangle(top_down, (0, 350), (800, 400), (80, 80, 80), -1)
    # เส้นถนน
    for x in range(50, 800, 100):
        cv2.line(top_down, (x, 375), (x + 50, 375), (255, 255, 255), 2)

    # ลานจอดรถ
    cv2.rectangle(top_down, (120, 450), (280, 550), (120, 120, 120), -1)
    # เส้นจอดรถ
    for y in range(460, 540, 20):
        cv2.line(top_down, (130, y), (270, y), (255, 255, 255), 1)

    # ต้นไม้ (วงกลม)
    cv2.circle(top_down, (350, 400), 20, (50, 150, 50), -1)
    cv2.circle(top_down, (500, 450), 25, (50, 150, 50), -1)
    cv2.circle(top_down, (200, 320), 15, (50, 150, 50), -1)

    # เพิ่ม features ที่โดดเด่น
    # สถานี (วงกลมใหญ่)
    cv2.circle(top_down, (400, 250), 40, (200, 200, 50), -1)
    cv2.circle(top_down, (400, 250), 40, (255, 255, 255), 3)
    cv2.putText(top_down, "STATION", (360, 255), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imwrite("sample_images/top_down_view.jpg", top_down)

    # สร้างภาพ Eye-Level (มุมมองจากระดับตา)
    # จำลองการมองจากระดับตาคน โดยใช้ perspective transformation
    eye_level = np.ones((400, 600, 3), dtype=np.uint8) * 80

    # วาดท้องฟ้า
    cv2.rectangle(eye_level, (0, 0), (600, 150), (180, 180, 120), -1)

    # วาดอาคารที่มองเห็นจากระดับตา
    # อาคาร 1 (เปลี่ยนเป็นรูปทรงที่มองเห็นจากข้าง)
    points1 = np.array([[50, 150], [150, 120], [150, 350], [50, 380]], np.int32)
    cv2.fillPoly(eye_level, [points1], (100, 150, 200))
    cv2.polylines(eye_level, [points1], True, (255, 255, 255), 2)

    # อาคาร 2
    points2 = np.array([[200, 140], [300, 110], [300, 340], [200, 370]], np.int32)
    cv2.fillPoly(eye_level, [points2], (150, 200, 100))
    cv2.polylines(eye_level, [points2], True, (255, 255, 255), 2)

    # ถนน (มุมมองจากระดับตา)
    road_points = np.array([[0, 350], [600, 320], [600, 400], [0, 400]], np.int32)
    cv2.fillPoly(eye_level, [road_points], (80, 80, 80))

    # เส้นถนน (perspective)
    for i in range(5):
        x1 = i * 100
        x2 = 600
        y1 = 360
        y2 = 340 + i * 5
        cv2.line(eye_level, (x1, y1), (x2, y2), (255, 255, 255), 2)

    # สถานี (ในมุมมอง eye-level)
    station_points = np.array([[350, 130], [450, 110], [450, 300], [350, 320]], np.int32)
    cv2.fillPoly(eye_level, [station_points], (200, 200, 50))
    cv2.polylines(eye_level, [station_points], True, (255, 255, 255), 3)
    cv2.putText(eye_level, "STATION", (360, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # ต้นไม้ (มุมมอง eye-level)
    # ต้น 1
    cv2.line(eye_level, (480, 300), (480, 350), (139, 69, 19), 5)
    cv2.circle(eye_level, (480, 300), 20, (50, 150, 50), -1)

    # ต้น 2
    cv2.line(eye_level, (120, 320), (120, 370), (139, 69, 19), 4)
    cv2.circle(eye_level, (120, 320), 15, (50, 150, 50), -1)

    # เพิ่มรายละเอียดเพื่อให้มี features มากขึ้น
    # หน้าต่างอาคาร
    for i in range(2):
        for j in range(8):
            cv2.rectangle(eye_level, (70 + j*10, 170 + i*30), (75 + j*10, 190 + i*30), (255, 255, 0), -1)
            cv2.rectangle(eye_level, (220 + j*10, 160 + i*30), (225 + j*10, 180 + i*30), (255, 255, 0), -1)

    cv2.imwrite("sample_images/eye_level_view.jpg", eye_level)

    print("✅ สร้างภาพตัวอย่างเสร็จแล้ว:")
    print("   📁 sample_images/top_down_view.jpg")
    print("   📁 sample_images/eye_level_view.jpg")


def run_basic_comparison():
    """
    รันการเปรียบเทียบแบบพื้นฐาน
    """
    print("\n" + "="*60)
    print("🚀 เริ่มการเปรียบเทียบภาพด้วย SIFT + Homography")
    print("="*60)

    # สร้าง matcher
    matcher = HomographyMatcher(feature_detector='SIFT', min_match_count=8)

    # เปรียบเทียบภาพ
    results = matcher.compare_images(
        "sample_images/eye_level_view.jpg",
        "sample_images/top_down_view.jpg",
        "output/sift_results"
    )

    return results


def run_multiple_detectors():
    """
    ทดสอบการใช้ feature detectors หลายประเภท
    """
    print("\n" + "="*60)
    print("🔬 ทดสอบ Feature Detectors หลายประเภท")
    print("="*60)

    detectors = ['SIFT', 'ORB', 'AKAZE']
    all_results = {}

    for detector in detectors:
        print(f"\n🔍 ทดสอบด้วย {detector}...")
        try:
            matcher = HomographyMatcher(feature_detector=detector, min_match_count=8)
            results = matcher.compare_images(
                "sample_images/eye_level_view.jpg",
                "sample_images/top_down_view.jpg",
                f"output/{detector.lower()}_results"
            )
            all_results[detector] = results
        except Exception as e:
            print(f"❌ ข้อผิดพลาดกับ {detector}: {str(e)}")
            all_results[detector] = None

    # แสดงการเปรียบเทียบผลลัพธ์
    print("\n" + "="*60)
    print("📊 เปรียบเทียบผลลัพธ์จาก Feature Detectors ต่างๆ")
    print("="*60)
    print(f"{'Detector':<10} {'Keypoints1':<12} {'Keypoints2':<12} {'Matches':<10} {'Success':<10} {'Score':<10}")
    print("-" * 70)

    for detector, results in all_results.items():
        if results:
            success = "✅ Yes" if results['homography_found'] else "❌ No"
            score = f"{results['confidence_score']:.2f}" if results['homography_found'] else "0.00"
            print(f"{detector:<10} {results['eye_level_keypoints']:<12} {results['top_down_keypoints']:<12} "
                  f"{results['total_matches']:<10} {success:<10} {score:<10}")
        else:
            print(f"{detector:<10} {'Error':<12} {'Error':<12} {'Error':<10} {'❌ No':<10} {'0.00':<10}")


def main():
    """ฟังก์ชันหลักสำหรับการทดสอบ"""

    print("🎯 OpenCV Homography Matcher - ตัวอย่างการใช้งาน")
    print("="*60)

    # สร้างภาพตัวอย่าง
    create_sample_images()

    # รันการเปรียบเทียบแบบพื้นฐาน
    basic_results = run_basic_comparison()

    # ทดสอบ detectors หลายประเภท
    run_multiple_detectors()

    print("\n" + "="*60)
    print("🎉 การทดสอบเสร็จสมบูรณ์!")
    print("="*60)
    print("📁 ผลลัพธ์ถูกบันทึกในโฟลเดอร์:")
    print("   - output/sift_results/")
    print("   - output/orb_results/")
    print("   - output/akaze_results/")
    print("\n💡 คำแนะนำ:")
    print("   - ดูไฟล์ matches_visualization.jpg เพื่อดูการจับคู่ features")
    print("   - ดูไฟล์ comparison.jpg เพื่อเปรียบเทียบการ transform")
    print("   - ลองใช้ภาพจริงของคุณเองแทนภาพตัวอย่าง")


if __name__ == "__main__":
    main()

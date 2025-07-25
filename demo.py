#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
การสาธิตการใช้งาน OpenCV Homography Matcher แบบง่าย
สำหรับผู้เริ่มต้น
"""

import cv2
import numpy as np
from homography_matcher import HomographyMatcher
import os


def simple_demo():
    """
    การสาธิตแบบง่าย ๆ
    """
    print("🎯 OpenCV Homography Matcher - การสาธิตแบบง่าย")
    print("=" * 60)
    print("โปรแกรมนี้จะเปรียบเทียบภาพ Eye-Level กับ Top-Down")
    print("เพื่อหาจุดที่ตรงกันและแปลงภาพจากมุมมองหนึ่งไปอีกมุมมองหนึ่ง")
    print("=" * 60)

    # ตรวจสอบว่ามีภาพตัวอย่างหรือไม่
    sample_paths = [
        ("sample_images/eye_level_view.jpg", "sample_images/top_down_view.jpg", "ภาพจำลองพื้นฐาน"),
        ("real_examples/campus_street_view.jpg", "real_examples/campus_map.jpg", "ภาพมหาวิทยาลัย"),
        ("real_examples/mall_interior.jpg", "real_examples/mall_map.jpg", "ภาพห้างสรรพสินค้า")
    ]

    available_samples = []
    for eye_path, top_path, description in sample_paths:
        if os.path.exists(eye_path) and os.path.exists(top_path):
            available_samples.append((eye_path, top_path, description))

    if not available_samples:
        print("❌ ไม่พบภาพตัวอย่าง กรุณารันคำสั่งต่อไปนี้ก่อน:")
        print("   python example_usage.py")
        print("   python create_realistic_examples.py")
        return

    print("📷 ภาพตัวอย่างที่พร้อมใช้งาน:")
    for i, (_, _, description) in enumerate(available_samples, 1):
        print(f"   {i}. {description}")

    print("\n🚀 เริ่มการทดสอบแบบอัตโนมัติ...")

    results_summary = []

    for i, (eye_path, top_path, description) in enumerate(available_samples, 1):
        print(f"\n📍 ทดสอบ {i}: {description}")
        print("-" * 40)

        # ทดสอบกับ detectors ต่าง ๆ
        detectors = ['SIFT', 'ORB', 'AKAZE']
        best_result = None
        best_detector = None
        best_score = 0

        for detector in detectors:
            try:
                print(f"   🔍 ทดสอบด้วย {detector}...", end="")

                matcher = HomographyMatcher(
                    feature_detector=detector,
                    min_match_count=5  # ลดค่าเพื่อให้ทำงานได้ง่ายขึ้น
                )

                output_dir = f"demo_results/test_{i}_{detector.lower()}"
                result = matcher.compare_images(eye_path, top_path, output_dir)

                if result['homography_found'] and result['confidence_score'] > best_score:
                    best_result = result
                    best_detector = detector
                    best_score = result['confidence_score']

                if result['homography_found']:
                    print(f" ✅ Score: {result['confidence_score']:.2f}")
                else:
                    print(f" ❌ Matches: {result['total_matches']}")

            except Exception as e:
                print(f" ❌ Error")

        # สรุปผลลัพธ์ของแต่ละการทดสอบ
        if best_result:
            print(f"   🏆 ผลลัพธ์ที่ดีที่สุด: {best_detector} (Score: {best_score:.2f})")
            results_summary.append({
                'test': description,
                'detector': best_detector,
                'score': best_score,
                'matches': best_result['total_matches'],
                'success': True
            })
        else:
            print(f"   ❌ ไม่สามารถหาความสัมพันธ์ได้")
            results_summary.append({
                'test': description,
                'detector': 'None',
                'score': 0,
                'matches': 0,
                'success': False
            })

    # แสดงสรุปผลรวม
    print("\n" + "=" * 60)
    print("📊 สรุปผลการทดสอบทั้งหมด")
    print("=" * 60)
    print(f"{'ภาพทดสอบ':<20} {'Detector':<8} {'Score':<8} {'Matches':<8} {'ผลลัพธ์'}")
    print("-" * 60)

    success_count = 0
    for result in results_summary:
        status = "✅ สำเร็จ" if result['success'] else "❌ ล้มเหลว"
        if result['success']:
            success_count += 1

        print(f"{result['test']:<20} {result['detector']:<8} {result['score']:<8.2f} "
              f"{result['matches']:<8} {status}")

    print("-" * 60)
    print(f"อัตราความสำเร็จ: {success_count}/{len(results_summary)} "
          f"({success_count/len(results_summary)*100:.1f}%)")

    # คำแนะนำ
    print("\n💡 คำแนะนำการใช้งาน:")
    print("1. ผลลัพธ์ถูกบันทึกในโฟลเดอร์ demo_results/")
    print("2. ดูไฟล์ matches_visualization.jpg เพื่อดูการจับคู่ features")
    print("3. ดูไฟล์ comparison.jpg เพื่อเปรียบเทียบการ transform")
    print("4. Score ≥ 0.5 ถือว่าใช้งานได้")
    print("5. Score ≥ 0.7 ถือว่าเชื่อถือได้สูง")

    print("\n📚 ข้อมูลเพิ่มเติม:")
    print("• SIFT: แม่นยำที่สุด แต่ช้า")
    print("• ORB: เร็วที่สุด แต่อาจไม่แม่นยำ")
    print("• AKAZE: สมดุลระหว่างความเร็วและความแม่นยำ")

    print("\n🎮 การใช้งานต่อไป:")
    print("python cli.py --eye your_eye_level.jpg --top your_top_down.jpg")
    print("python cli.py --benchmark  # ทดสอบทุก detectors")


def explain_theory():
    """
    อธิบายทฤษฎีเบื้องหลัง
    """
    print("\n" + "=" * 60)
    print("📖 ทฤษฎีเบื้องหลัง OpenCV Homography Matching")
    print("=" * 60)

    print("\n🔍 1. Feature Detection (การหา Features)")
    print("   • ค้นหาจุดที่มีลักษณะเด่นในภาพ (corners, edges, blobs)")
    print("   • แต่ละจุดจะมี descriptor ที่อธิบายลักษณะของจุดนั้น")
    print("   • SIFT, ORB, AKAZE เป็น algorithms ที่ใช้หา features")

    print("\n🔗 2. Feature Matching (การจับคู่ Features)")
    print("   • เปรียบเทียบ descriptors ระหว่างสองภาพ")
    print("   • หาจุดที่มีลักษณะคล้ายกันที่สุด")
    print("   • กรอง matches ที่ไม่ดีออกด้วย Lowe's ratio test")

    print("\n📐 3. Homography Estimation")
    print("   • ใช้ matches ที่ได้มาคำนวณ transformation matrix")
    print("   • Homography เป็น matrix 3x3 ที่อธิบายการแปลงระหว่างภาพ")
    print("   • ใช้ RANSAC เพื่อกรอง outliers")

    print("\n🎯 4. การประยุกต์ใช้งาน")
    print("   • เปรียบเทียบภาพจากมุมมองต่างกัน")
    print("   • ตรวจจับวัตถุในภาพ")
    print("   • สร้าง panorama")
    print("   • Augmented Reality")
    print("   • การนำทางด้วยภาพ")


if __name__ == "__main__":
    simple_demo()
    explain_theory()

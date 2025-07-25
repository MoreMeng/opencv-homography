#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
การทดสอบขั้นสูงสำหรับ HomographyMatcher
ทดสอบกับภาพจริงและสถานการณ์ต่างๆ
"""

import cv2
import numpy as np
import os
import time
from homography_matcher import HomographyMatcher


def create_realistic_test_images():
    """
    สร้างภาพทดสอบที่เหมือนจริงมากขึ้น
    """
    print("🎨 สร้างภาพทดสอบแบบเหมือนจริง...")

    os.makedirs("test_images", exist_ok=True)

    # ภาพแผนที่ (Top-Down) ที่ซับซ้อนขึ้น
    map_img = np.ones((800, 1000, 3), dtype=np.uint8) * 240  # พื้นหลังสีอ่อน

    # วาดถนนใหญ่
    cv2.rectangle(map_img, (0, 350), (1000, 450), (160, 160, 160), -1)  # ถนนหลัก
    cv2.rectangle(map_img, (450, 0), (550, 800), (160, 160, 160), -1)  # ถนนตัด

    # เส้นกลางถนน
    for x in range(50, 1000, 100):
        cv2.rectangle(map_img, (x, 390), (x+40, 410), (255, 255, 255), -1)
    for y in range(50, 800, 100):
        cv2.rectangle(map_img, (490, y), (510, y+40), (255, 255, 255), -1)

    # อาคารต่างๆ
    buildings = [
        ((100, 100), (250, 300), (180, 140, 100)),  # อาคารสีน้ำตาล
        ((300, 150), (400, 320), (120, 150, 180)),  # อาคารสีม่วง
        ((600, 100), (780, 280), (100, 180, 120)),  # อาคารสีเขียว
        ((150, 500), (320, 700), (200, 120, 100)),  # อาคารสีส้ม
        ((600, 500), (750, 750), (150, 150, 200)),  # อาคารสีฟ้า
    ]

    for (x1, y1), (x2, y2), color in buildings:
        cv2.rectangle(map_img, (x1, y1), (x2, y2), color, -1)
        cv2.rectangle(map_img, (x1, y1), (x2, y2), (0, 0, 0), 2)

        # เพิ่มหน้าต่าง
        for i in range(3):
            for j in range(5):
                wx = x1 + 20 + j * 30
                wy = y1 + 30 + i * 40
                if wx < x2-10 and wy < y2-10:
                    cv2.rectangle(map_img, (wx, wy), (wx+15, wy+20), (255, 255, 0), -1)
                    cv2.rectangle(map_img, (wx, wy), (wx+15, wy+20), (0, 0, 0), 1)

    # ลานจอดรถ
    cv2.rectangle(map_img, (820, 300), (980, 500), (200, 200, 200), -1)
    for i in range(8):
        cv2.line(map_img, (830, 320 + i*20), (970, 320 + i*20), (255, 255, 255), 1)

    # สวนสาธารณะ
    cv2.circle(map_img, (200, 600), 80, (100, 200, 100), -1)  # สวน
    # ต้นไม้ในสวน
    for i in range(5):
        for j in range(5):
            x = 160 + i * 20
            y = 560 + j * 20
            if (x-200)**2 + (y-600)**2 < 60**2:
                cv2.circle(map_img, (x, y), 8, (50, 150, 50), -1)

    # สะพาน
    cv2.rectangle(map_img, (440, 340), (560, 460), (139, 69, 19), -1)
    cv2.rectangle(map_img, (440, 340), (560, 460), (255, 255, 255), 3)

    # ป้ายและสัญลักษณ์
    cv2.circle(map_img, (500, 200), 30, (255, 0, 0), -1)  # จุดสำคัญ
    cv2.circle(map_img, (500, 200), 30, (255, 255, 255), 3)
    cv2.putText(map_img, "LANDMARK", (450, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    cv2.imwrite("test_images/detailed_map.jpg", map_img)

    # สร้างภาพ Street View ที่สอดคล้องกัน
    street_img = np.ones((600, 800, 3), dtype=np.uint8) * 200  # ท้องฟ้า

    # ท้องฟ้าและเมฆ
    cv2.rectangle(street_img, (0, 0), (800, 200), (220, 220, 180), -1)
    cv2.ellipse(street_img, (200, 150), (80, 30), 0, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(street_img, (600, 100), (60, 25), 0, 0, 360, (255, 255, 255), -1)

    # อาคารในมุมมอง street view (perspective)
    # อาคารซ้าย
    left_building = np.array([[0, 200], [150, 180], [150, 550], [0, 600]], np.int32)
    cv2.fillPoly(street_img, [left_building], (180, 140, 100))
    cv2.polylines(street_img, [left_building], True, (0, 0, 0), 2)

    # หน้าต่างอาคารซ้าย
    for i in range(3):
        for j in range(8):
            wx = 20 + j * 15
            wy = 220 + i * 50
            cv2.rectangle(street_img, (wx, wy), (wx+10, wy+20), (255, 255, 0), -1)
            cv2.rectangle(street_img, (wx, wy), (wx+10, wy+20), (0, 0, 0), 1)

    # อาคารขวา
    right_building = np.array([[650, 180], [800, 200], [800, 600], [650, 550]], np.int32)
    cv2.fillPoly(street_img, [right_building], (120, 150, 180))
    cv2.polylines(street_img, [right_building], True, (0, 0, 0), 2)

    # หน้าต่างอาคารขวา
    for i in range(3):
        for j in range(6):
            wx = 670 + j * 18
            wy = 220 + i * 50
            cv2.rectangle(street_img, (wx, wy), (wx+12, wy+20), (255, 255, 0), -1)
            cv2.rectangle(street_img, (wx, wy), (wx+12, wy+20), (0, 0, 0), 1)

    # อาคารกลาง (ที่สำคัญ - landmark)
    center_building = np.array([[300, 160], [500, 150], [500, 500], [300, 520]], np.int32)
    cv2.fillPoly(street_img, [center_building], (100, 180, 120))
    cv2.polylines(street_img, [center_building], True, (0, 0, 0), 3)

    # สัญลักษณ์พิเศษบนอาคารกลาง
    cv2.circle(street_img, (400, 200), 25, (255, 0, 0), -1)
    cv2.circle(street_img, (400, 200), 25, (255, 255, 255), 3)
    cv2.putText(street_img, "LANDMARK", (340, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # ถนน (perspective view)
    road_pts = np.array([[0, 500], [800, 450], [800, 600], [0, 600]], np.int32)
    cv2.fillPoly(street_img, [road_pts], (120, 120, 120))

    # เส้นถนน
    cv2.line(street_img, (0, 525), (800, 490), (255, 255, 255), 3)
    cv2.line(street_img, (0, 575), (800, 530), (255, 255, 255), 3)

    # เส้นกลางถนน (เส้นประ)
    for i in range(8):
        x1 = i * 100
        x2 = (i + 1) * 100 - 20
        y1 = 550 - i * 5
        y2 = 550 - (i + 1) * 5 + 1
        cv2.line(street_img, (x1, y1), (x2, y2), (255, 255, 0), 2)

    # ไฟจราจร
    cv2.rectangle(street_img, (180, 300), (200, 500), (100, 100, 100), -1)
    cv2.circle(street_img, (190, 320), 8, (255, 0, 0), -1)
    cv2.circle(street_img, (190, 340), 8, (255, 255, 0), -1)
    cv2.circle(street_img, (190, 360), 8, (0, 255, 0), -1)

    # ต้นไม้
    cv2.line(street_img, (250, 450), (250, 500), (139, 69, 19), 8)
    cv2.circle(street_img, (250, 450), 25, (50, 150, 50), -1)

    cv2.line(street_img, (550, 420), (550, 480), (139, 69, 19), 6)
    cv2.circle(street_img, (550, 420), 20, (50, 150, 50), -1)

    cv2.imwrite("test_images/street_view.jpg", street_img)

    print("✅ สร้างภาพทดสอบเสร็จแล้ว:")
    print("   📁 test_images/detailed_map.jpg")
    print("   📁 test_images/street_view.jpg")


def benchmark_detectors():
    """
    วัดประสิทธิภาพของ feature detectors ต่างๆ
    """
    print("\n" + "="*60)
    print("⏱️  การทดสอบประสิทธิภาพ Feature Detectors")
    print("="*60)

    detectors = ['SIFT', 'ORB', 'AKAZE']
    results = {}

    for detector in detectors:
        print(f"\n🔍 ทดสอบ {detector}...")

        start_time = time.time()
        try:
            matcher = HomographyMatcher(feature_detector=detector, min_match_count=15)
            result = matcher.compare_images(
                "test_images/street_view.jpg",
                "test_images/detailed_map.jpg",
                f"test_output/{detector.lower()}_benchmark"
            )
            end_time = time.time()

            result['processing_time'] = end_time - start_time
            results[detector] = result

            print(f"   ⏱️  เวลาในการประมวลผล: {result['processing_time']:.2f} วินาที")

        except Exception as e:
            print(f"   ❌ ข้อผิดพลาด: {str(e)}")
            results[detector] = None

    # แสดงผลสรุป
    print("\n" + "="*80)
    print("📊 สรุปผลการทดสอบประสิทธิภาพ")
    print("="*80)
    print(f"{'Detector':<10} {'Time(s)':<10} {'KP1':<8} {'KP2':<8} {'Matches':<10} {'Success':<10} {'Score':<8}")
    print("-" * 80)

    for detector, result in results.items():
        if result:
            success = "✅ Yes" if result['homography_found'] else "❌ No"
            score = f"{result['confidence_score']:.2f}" if result['homography_found'] else "0.00"
            print(f"{detector:<10} {result['processing_time']:<10.2f} {result['eye_level_keypoints']:<8} "
                  f"{result['top_down_keypoints']:<8} {result['total_matches']:<10} {success:<10} {score:<8}")
        else:
            print(f"{detector:<10} {'Error':<10} {'---':<8} {'---':<8} {'---':<10} {'❌ No':<10} {'0.00':<8}")

    return results


def test_with_transformations():
    """
    ทดสอบกับภาพที่มีการ transform ต่างๆ
    """
    print("\n" + "="*60)
    print("🔄 ทดสอบกับการ Transform ต่างๆ")
    print("="*60)

    # โหลดภาพต้นฉบับ
    base_img = cv2.imread("test_images/street_view.jpg")
    if base_img is None:
        print("❌ ไม่พบภาพต้นฉบับ")
        return

    os.makedirs("test_images/transforms", exist_ok=True)

    transformations = {
        'rotated': {'angle': 15, 'description': 'หมุน 15 องศา'},
        'scaled': {'scale': 0.8, 'description': 'ย่อขนาด 80%'},
        'perspective': {'points': 'custom', 'description': 'เปลี่ยน perspective'},
        'noisy': {'noise': True, 'description': 'เพิ่ม noise'},
        'bright': {'brightness': 50, 'description': 'เพิ่มความสว่าง'}
    }

    h, w = base_img.shape[:2]

    for transform_name, params in transformations.items():
        print(f"\n🔧 สร้างภาพ {params['description']}...")

        if transform_name == 'rotated':
            # หมุนภาพ
            center = (w//2, h//2)
            rotation_matrix = cv2.getRotationMatrix2D(center, params['angle'], 1.0)
            transformed = cv2.warpAffine(base_img, rotation_matrix, (w, h))

        elif transform_name == 'scaled':
            # ย่อขนาด
            new_w, new_h = int(w * params['scale']), int(h * params['scale'])
            scaled = cv2.resize(base_img, (new_w, new_h))
            transformed = np.zeros_like(base_img)
            offset_x, offset_y = (w - new_w) // 2, (h - new_h) // 2
            transformed[offset_y:offset_y+new_h, offset_x:offset_x+new_w] = scaled

        elif transform_name == 'perspective':
            # เปลี่ยน perspective
            src_pts = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
            dst_pts = np.float32([[50, 30], [w-30, 50], [w-80, h-30], [80, h-50]])
            perspective_matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
            transformed = cv2.warpPerspective(base_img, perspective_matrix, (w, h))

        elif transform_name == 'noisy':
            # เพิ่ม noise
            noise = np.random.normal(0, 25, base_img.shape).astype(np.uint8)
            transformed = cv2.add(base_img, noise)

        elif transform_name == 'bright':
            # เพิ่มความสว่าง
            transformed = cv2.convertScaleAbs(base_img, alpha=1.0, beta=params['brightness'])

        # บันทึกภาพ
        transform_path = f"test_images/transforms/{transform_name}_street.jpg"
        cv2.imwrite(transform_path, transformed)

        # ทดสอบการจับคู่
        try:
            matcher = HomographyMatcher(feature_detector='SIFT', min_match_count=10)
            result = matcher.compare_images(
                transform_path,
                "test_images/detailed_map.jpg",
                f"test_output/transform_{transform_name}"
            )

            if result['homography_found']:
                print(f"   ✅ สำเร็จ! Score: {result['confidence_score']:.2f}")
            else:
                print(f"   ❌ ล้มเหลว (Matches: {result['total_matches']})")

        except Exception as e:
            print(f"   ❌ ข้อผิดพลาด: {str(e)}")


def main():
    """ฟังก์ชันหลักสำหรับการทดสอบขั้นสูง"""

    print("🧪 OpenCV Homography Matcher - การทดสอบขั้นสูง")
    print("="*60)

    # สร้างภาพทดสอบ
    create_realistic_test_images()

    # ทดสอบประสิทธิภาพ
    benchmark_results = benchmark_detectors()

    # ทดสอบกับการ transform
    test_with_transformations()

    print("\n" + "="*60)
    print("🎉 การทดสอบขั้นสูงเสร็จสมบูรณ์!")
    print("="*60)
    print("📁 ผลลัพธ์การทดสอบ:")
    print("   - test_output/sift_benchmark/")
    print("   - test_output/orb_benchmark/")
    print("   - test_output/akaze_benchmark/")
    print("   - test_output/transform_*/")
    print("\n💡 ข้อสังเกต:")
    print("   - SIFT มักให้ผลลัพธ์ที่แม่นยำที่สุด")
    print("   - ORB เร็วที่สุดแต่อาจมีความแม่นยำต่ำ")
    print("   - AKAZE เป็นตัวเลือกที่สมดุลระหว่างความเร็วและความแม่นยำ")


if __name__ == "__main__":
    main()

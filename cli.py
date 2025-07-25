#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command Line Interface สำหรับ OpenCV Homography Matcher
ใช้งานง่าย สำหรับเปรียบเทียบภาพ Eye-Level กับ Top-Down
"""

import argparse
import sys
import os
from homography_matcher import HomographyMatcher


def main():
    """ฟังก์ชันหลักสำหรับ CLI"""

    # สร้าง argument parser
    parser = argparse.ArgumentParser(
        description='🔍 OpenCV Homography Matcher - เปรียบเทียบภาพ Eye-Level กับ Top-Down',
        epilog='ตัวอย่างการใช้งาน:\n'
               '  python cli.py --eye eye_level.jpg --top top_down.jpg\n'
               '  python cli.py --eye street.jpg --top map.jpg --detector ORB --output results',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # พารามิเตอร์หลัก
    parser.add_argument('--eye', '--eye-level',
                       dest='eye_level',
                       required=True,
                       help='📷 ไฟล์ภาพ Eye-Level (มุมมองระดับตา)')

    parser.add_argument('--top', '--top-down',
                       dest='top_down',
                       required=True,
                       help='🗺️  ไฟล์ภาพ Top-Down (มุมมองจากด้านบน)')

    # พารามิเตอร์เสริม
    parser.add_argument('--detector',
                       choices=['SIFT', 'ORB', 'AKAZE'],
                       default='SIFT',
                       help='🔎 Feature detector ที่ใช้ (default: SIFT)')

    parser.add_argument('--min-matches',
                       type=int,
                       default=10,
                       help='🔢 จำนวนการจับคู่ขั้นต่ำ (default: 10)')

    parser.add_argument('--output', '-o',
                       default='results',
                       help='📁 โฟลเดอร์สำหรับบันทึกผลลัพธ์ (default: results)')

    parser.add_argument('--verbose', '-v',
                       action='store_true',
                       help='📝 แสดงข้อมูลรายละเอียดเพิ่มเติม')

    parser.add_argument('--benchmark',
                       action='store_true',
                       help='⏱️  ทดสอบประสิทธิภาพของ detectors ทั้งหมด')

    # Parse arguments
    args = parser.parse_args()

    # ตรวจสอบไฟล์ input
    if not os.path.exists(args.eye_level):
        print(f"❌ ไม่พบไฟล์ภาพ Eye-Level: {args.eye_level}")
        return 1

    if not os.path.exists(args.top_down):
        print(f"❌ ไม่พบไฟล์ภาพ Top-Down: {args.top_down}")
        return 1

    # แสดงข้อมูลการตั้งค่า
    print("🔍 OpenCV Homography Matcher")
    print("=" * 50)
    print(f"📷 Eye-Level Image: {args.eye_level}")
    print(f"🗺️  Top-Down Image: {args.top_down}")
    print(f"🔎 Feature Detector: {args.detector}")
    print(f"🔢 Min Matches: {args.min_matches}")
    print(f"📁 Output Directory: {args.output}")
    print("=" * 50)

    try:
        if args.benchmark:
            # ทดสอบทุก detectors
            print("⏱️  กำลังทดสอบประสิทธิภาพของ detectors ทั้งหมด...\n")

            detectors = ['SIFT', 'ORB', 'AKAZE']
            results = {}

            for detector in detectors:
                print(f"🔍 ทดสอบ {detector}...")

                try:
                    matcher = HomographyMatcher(
                        feature_detector=detector,
                        min_match_count=args.min_matches
                    )

                    result = matcher.compare_images(
                        args.eye_level,
                        args.top_down,
                        f"{args.output}/{detector.lower()}_results"
                    )

                    results[detector] = result

                    if result['homography_found']:
                        print(f"   ✅ สำเร็จ! Score: {result['confidence_score']:.2f}")
                    else:
                        print(f"   ❌ ล้มเหลว (Matches: {result['total_matches']})")

                except Exception as e:
                    print(f"   ❌ ข้อผิดพลาด: {str(e)}")
                    results[detector] = None

                print()

            # สรุปผลการทดสอบ
            print("📊 สรุปผลการทดสอบ")
            print("-" * 60)
            print(f"{'Detector':<10} {'Keypoints':<15} {'Matches':<10} {'Success':<10} {'Score':<8}")
            print("-" * 60)

            for detector, result in results.items():
                if result:
                    kp_info = f"{result['eye_level_keypoints']}/{result['top_down_keypoints']}"
                    success = "✅ Yes" if result['homography_found'] else "❌ No"
                    score = f"{result['confidence_score']:.2f}" if result['homography_found'] else "0.00"
                    print(f"{detector:<10} {kp_info:<15} {result['total_matches']:<10} {success:<10} {score:<8}")
                else:
                    print(f"{detector:<10} {'Error':<15} {'Error':<10} {'❌ No':<10} {'0.00':<8}")

        else:
            # ใช้ detector ที่ระบุ
            print(f"🚀 เริ่มการเปรียบเทียบด้วย {args.detector}...\n")

            matcher = HomographyMatcher(
                feature_detector=args.detector,
                min_match_count=args.min_matches
            )

            result = matcher.compare_images(
                args.eye_level,
                args.top_down,
                args.output
            )

            # แสดงผลสรุป
            print("\n" + "=" * 50)
            print("📋 สรุปผลการเปรียบเทียบ")
            print("=" * 50)
            print(f"🔎 Feature Detector: {args.detector}")
            print(f"📊 Eye-Level Keypoints: {result['eye_level_keypoints']}")
            print(f"📊 Top-Down Keypoints: {result['top_down_keypoints']}")
            print(f"🔗 Total Matches: {result['total_matches']}")

            if result['homography_found']:
                print(f"✅ Inlier Matches: {result['inlier_matches']}")
                print(f"🎯 Confidence Score: {result['confidence_score']:.2f}")
                print("\n🎉 การเปรียบเทียบสำเร็จ!")
                print(f"📁 ผลลัพธ์ถูกบันทึกใน: {args.output}")

                # แนะนำการตีความผล
                if result['confidence_score'] >= 0.7:
                    print("💚 ความเชื่อถือได้: สูงมาก - ผลลัพธ์น่าเชื่อถือ")
                elif result['confidence_score'] >= 0.5:
                    print("💛 ความเชื่อถือได้: ปานกลาง - ควรตรวจสอบผลลัพธ์")
                elif result['confidence_score'] >= 0.3:
                    print("🧡 ความเชื่อถือได้: ต่ำ - ผลลัพธ์อาจไม่แม่นยำ")
                else:
                    print("❤️ ความเชื่อถือได้: ต่ำมาก - ไม่แนะนำให้ใช้ผลลัพธ์")

            else:
                print("\n❌ ไม่พบความสัมพันธ์ที่เชื่อถือได้ระหว่างภาพทั้งสอง")
                print("💡 คำแนะนำ:")
                print("   - ลองเปลี่ยน feature detector (--detector ORB หรือ AKAZE)")
                print("   - ลดจำนวน min matches (--min-matches 5)")
                print("   - ตรวจสอบว่าภาพทั้งสองมีวัตถุหรือพื้นที่ที่ตรงกันหรือไม่")

        print(f"\n📂 ไฟล์ผลลัพธ์:")
        print(f"   • matches_visualization.jpg - การแสดงผลการจับคู่ features")
        print(f"   • comparison.jpg - การเปรียบเทียบภาพที่ถูก transform")
        print(f"   • transformed_eye_level.jpg - ภาพ eye-level ที่ถูก transform")

        return 0

    except KeyboardInterrupt:
        print("\n⏹️  การทำงานถูกยกเลิกโดยผู้ใช้")
        return 1

    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {str(e)}")

        if args.verbose:
            import traceback
            print("\n🔍 รายละเอียดข้อผิดพลาด:")
            traceback.print_exc()

        return 1


if __name__ == "__main__":
    exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenCV Homography Matcher
เปรียบเทียบภาพ Eye-Level กับ Top-Down โดยใช้ Feature Matching + Homography

Author: Your Name
Date: 2025-07-25
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
from typing import Tuple, Optional


class HomographyMatcher:
    """
    คลาสสำหรับเปรียบเทียบภาพด้วย Feature Matching และ Homography Transformation
    """

    def __init__(self, feature_detector='SIFT', min_match_count=10):
        """
        Initialize the HomographyMatcher

        Args:
            feature_detector (str): ประเภทของ feature detector ('SIFT', 'ORB', 'AKAZE')
            min_match_count (int): จำนวนการจับคู่ขั้นต่ำที่ต้องการ
        """
        self.min_match_count = min_match_count
        self.feature_detector = feature_detector

        # สร้าง feature detector และ matcher
        if feature_detector == 'SIFT':
            self.detector = cv2.SIFT_create()
            # FLANN matcher สำหรับ SIFT
            FLANN_INDEX_KDTREE = 1
            index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
            search_params = dict(checks=50)
            self.matcher = cv2.FlannBasedMatcher(index_params, search_params)
        elif feature_detector == 'ORB':
            self.detector = cv2.ORB_create()
            # BFMatcher สำหรับ ORB
            self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        elif feature_detector == 'AKAZE':
            self.detector = cv2.AKAZE_create()
            self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        else:
            raise ValueError(f"Unsupported feature detector: {feature_detector}")

    def load_and_preprocess_image(self, image_path: str) -> np.ndarray:
        """
        โหลดและปรับแต่งภาพ

        Args:
            image_path (str): path ของภาพ

        Returns:
            np.ndarray: ภาพที่ปรับแต่งแล้ว
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"ไม่พบไฟล์ภาพ: {image_path}")

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"ไม่สามารถโหลดภาพได้: {image_path}")

        # แปลงเป็น grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # ปรับ contrast และ brightness
        gray = cv2.convertScaleAbs(gray, alpha=1.2, beta=10)

        return img, gray

    def detect_and_compute_features(self, gray_img: np.ndarray) -> Tuple[list, np.ndarray]:
        """
        หา keypoints และ descriptors ในภาพ

        Args:
            gray_img (np.ndarray): ภาพ grayscale

        Returns:
            Tuple[list, np.ndarray]: keypoints และ descriptors
        """
        keypoints, descriptors = self.detector.detectAndCompute(gray_img, None)
        return keypoints, descriptors

    def match_features(self, desc1: np.ndarray, desc2: np.ndarray) -> list:
        """
        จับคู่ features ระหว่างสองภาพ

        Args:
            desc1 (np.ndarray): descriptors ของภาพแรก
            desc2 (np.ndarray): descriptors ของภาพที่สอง

        Returns:
            list: รายการของ good matches
        """
        if desc1 is None or desc2 is None:
            return []

        if self.feature_detector == 'SIFT':
            # ใช้ FLANN matcher สำหรับ SIFT
            matches = self.matcher.knnMatch(desc1, desc2, k=2)

            # Apply Lowe's ratio test
            good_matches = []
            for match_pair in matches:
                if len(match_pair) == 2:
                    m, n = match_pair
                    if m.distance < 0.7 * n.distance:
                        good_matches.append(m)
        else:
            # ใช้ BFMatcher สำหรับ ORB และ AKAZE
            matches = self.matcher.match(desc1, desc2)
            # เรียงลำดับตาม distance
            matches = sorted(matches, key=lambda x: x.distance)
            # เลือกเฉพาะ matches ที่ดี (25% แรก)
            good_matches = matches[:len(matches)//4]

        return good_matches

    def find_homography(self, kp1: list, kp2: list, matches: list) -> Optional[np.ndarray]:
        """
        หา Homography matrix จาก matched keypoints

        Args:
            kp1 (list): keypoints ของภาพแรก
            kp2 (list): keypoints ของภาพที่สอง
            matches (list): รายการของ good matches

        Returns:
            Optional[np.ndarray]: Homography matrix หรือ None
        """
        if len(matches) < self.min_match_count:
            print(f"จำนวน matches ไม่เพียงพอ: {len(matches)}/{self.min_match_count}")
            return None

        # แยก coordinates ของ matched points
        src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

        # หา Homography matrix ด้วย RANSAC
        H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        return H, mask

    def transform_image(self, img: np.ndarray, H: np.ndarray, target_shape: Tuple[int, int]) -> np.ndarray:
        """
        Transform ภาพด้วย Homography matrix

        Args:
            img (np.ndarray): ภาพต้นฉบับ
            H (np.ndarray): Homography matrix
            target_shape (Tuple[int, int]): ขนาดของภาพเป้าหมาย (width, height)

        Returns:
            np.ndarray: ภาพที่ถูก transform แล้ว
        """
        return cv2.warpPerspective(img, H, target_shape)

    def visualize_matches(self, img1: np.ndarray, kp1: list, img2: np.ndarray, kp2: list,
                         matches: list, H: Optional[np.ndarray] = None) -> np.ndarray:
        """
        แสดงผลการจับคู่ features

        Args:
            img1, img2: ภาพต้นฉบับ
            kp1, kp2: keypoints
            matches: รายการของ matches
            H: Homography matrix (optional)

        Returns:
            np.ndarray: ภาพที่แสดงผลการจับคู่
        """
        # สร้างภาพสำหรับแสดงผล matches
        draw_params = dict(matchColor=(0, 255, 0),    # สีเขียวสำหรับ matches
                          singlePointColor=None,
                          matchesMask=None,           # วาดทุก matches
                          flags=2)

        img_matches = cv2.drawMatches(img1, kp1, img2, kp2, matches, None, **draw_params)

        # ถ้ามี Homography แล้ว ให้วาดกรอบรอบวัตถุที่ตรงกัน
        if H is not None:
            h, w = img1.shape[:2]
            pts = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, H)

            # วาดกรอบในภาพที่สอง
            img2_with_box = img2.copy()
            cv2.polylines(img2_with_box, [np.int32(dst)], True, (0, 0, 255), 3, cv2.LINE_AA)

            # รวมภาพ
            img_matches = cv2.drawMatches(img1, kp1, img2_with_box, kp2, matches, None, **draw_params)

        return img_matches

    def compare_images(self, eye_level_path: str, top_down_path: str,
                      output_dir: str = "output") -> dict:
        """
        เปรียบเทียบภาพ Eye-Level กับ Top-Down

        Args:
            eye_level_path (str): path ของภาพ eye-level
            top_down_path (str): path ของภาพ top-down
            output_dir (str): โฟลเดอร์สำหรับบันทึกผลลัพธ์

        Returns:
            dict: ผลลัพธ์การเปรียบเทียบ
        """
        # สร้างโฟลเดอร์ output
        os.makedirs(output_dir, exist_ok=True)

        print("🔍 กำลังโหลดและปรับแต่งภาพ...")

        # โหลดภาพ
        img1, gray1 = self.load_and_preprocess_image(eye_level_path)
        img2, gray2 = self.load_and_preprocess_image(top_down_path)

        print(f"📏 ขนาดภาพ Eye-Level: {img1.shape}")
        print(f"📏 ขนาดภาพ Top-Down: {img2.shape}")

        # หา features
        print(f"🔎 กำลังหา features ด้วย {self.feature_detector}...")
        kp1, desc1 = self.detect_and_compute_features(gray1)
        kp2, desc2 = self.detect_and_compute_features(gray2)

        print(f"✅ พบ keypoints ในภาพ Eye-Level: {len(kp1)}")
        print(f"✅ พบ keypoints ในภาพ Top-Down: {len(kp2)}")

        # จับคู่ features
        print("🔗 กำลังจับคู่ features...")
        matches = self.match_features(desc1, desc2)
        print(f"✅ พบ good matches: {len(matches)}")

        results = {
            'eye_level_keypoints': len(kp1),
            'top_down_keypoints': len(kp2),
            'total_matches': len(matches),
            'homography_found': False,
            'confidence_score': 0.0
        }

        if len(matches) >= self.min_match_count:
            # หา Homography
            print("📐 กำลังคำนวณ Homography matrix...")
            homography_result = self.find_homography(kp1, kp2, matches)

            if homography_result is not None:
                H, mask = homography_result
                matches_mask = mask.ravel().tolist()
                inlier_matches = [m for i, m in enumerate(matches) if matches_mask[i]]

                results['homography_found'] = True
                results['inlier_matches'] = len(inlier_matches)
                results['confidence_score'] = len(inlier_matches) / len(matches)

                print(f"✅ พบ Homography! Inlier matches: {len(inlier_matches)}/{len(matches)}")
                print(f"📊 Confidence Score: {results['confidence_score']:.2f}")

                # แสดงผลการจับคู่
                img_matches = self.visualize_matches(img1, kp1, img2, kp2, inlier_matches, H)

                # Transform ภาพ eye-level ให้เป็น top-down view
                h, w = img2.shape[:2]
                transformed_img = self.transform_image(img1, H, (w, h))

                # บันทึกผลลัพธ์
                cv2.imwrite(os.path.join(output_dir, "matches_visualization.jpg"), img_matches)
                cv2.imwrite(os.path.join(output_dir, "transformed_eye_level.jpg"), transformed_img)
                cv2.imwrite(os.path.join(output_dir, "original_top_down.jpg"), img2)

                # สร้างการเปรียบเทียบแบบเคียงข้างกัน
                comparison = np.hstack((transformed_img, img2))
                cv2.imwrite(os.path.join(output_dir, "comparison.jpg"), comparison)

                print(f"💾 บันทึกผลลัพธ์ในโฟลเดอร์: {output_dir}")

            else:
                print("❌ ไม่สามารถหา Homography ได้")
                # แสดงผล matches ที่มีอยู่
                img_matches = self.visualize_matches(img1, kp1, img2, kp2, matches[:50])  # แสดงแค่ 50 matches แรก
                cv2.imwrite(os.path.join(output_dir, "failed_matches.jpg"), img_matches)
        else:
            print(f"❌ จำนวน matches ไม่เพียงพอสำหรับการหา Homography ({len(matches)}/{self.min_match_count})")
            if len(matches) > 0:
                img_matches = self.visualize_matches(img1, kp1, img2, kp2, matches)
                cv2.imwrite(os.path.join(output_dir, "insufficient_matches.jpg"), img_matches)

        return results


def main():
    """ฟังก์ชันหลักสำหรับการรันโปรแกรม"""
    parser = argparse.ArgumentParser(description='OpenCV Homography Matcher')
    parser.add_argument('--eye_level', required=True, help='Path to eye-level image')
    parser.add_argument('--top_down', required=True, help='Path to top-down image')
    parser.add_argument('--detector', default='SIFT', choices=['SIFT', 'ORB', 'AKAZE'],
                       help='Feature detector to use')
    parser.add_argument('--min_matches', type=int, default=10,
                       help='Minimum number of matches required')
    parser.add_argument('--output', default='output', help='Output directory')

    args = parser.parse_args()

    # สร้าง matcher
    matcher = HomographyMatcher(
        feature_detector=args.detector,
        min_match_count=args.min_matches
    )

    try:
        # เปรียบเทียบภาพ
        results = matcher.compare_images(
            args.eye_level,
            args.top_down,
            args.output
        )

        # แสดงผลสรุป
        print("\n" + "="*50)
        print("📋 สรุปผลการเปรียบเทียบ")
        print("="*50)
        print(f"Eye-Level Keypoints: {results['eye_level_keypoints']}")
        print(f"Top-Down Keypoints: {results['top_down_keypoints']}")
        print(f"Total Matches: {results['total_matches']}")

        if results['homography_found']:
            print(f"Inlier Matches: {results['inlier_matches']}")
            print(f"Confidence Score: {results['confidence_score']:.2f}")
            print("✅ การเปรียบเทียบสำเร็จ!")
        else:
            print("❌ ไม่พบความสัมพันธ์ที่เชื่อถือได้ระหว่างภาพทั้งสอง")

    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())

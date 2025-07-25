#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
สร้างภาพตัวอย่างที่เหมือนจริงสำหรับทดสอบ HomographyMatcher
ภาพเหล่านี้จำลองสถานการณ์จริงของการถ่ายภาพจากมุมมองต่างๆ
"""

import cv2
import numpy as np
import os


def create_university_campus():
    """
    สร้างภาพมหาวิทยาลัยจากมุมมอง Top-Down และ Eye-Level
    """
    print("🏫 สร้างภาพตัวอย่าง: มหาวิทยาลัย")

    os.makedirs("real_examples", exist_ok=True)

    # ภาพแผนผังมหาวิทยาลัย (Top-Down)
    campus_map = np.ones((900, 1200, 3), dtype=np.uint8) * 220  # พื้นหลังสีเทาอ่อน

    # วาดอาคารต่างๆ
    buildings = [
        # (x1, y1, x2, y2, color, name)
        (100, 150, 300, 350, (150, 100, 80), "หอสมุด"),
        (400, 100, 650, 280, (120, 150, 200), "อาคารวิศวกรรม"),
        (750, 150, 950, 300, (100, 180, 100), "อาคารวิทยาศาสตร์"),
        (150, 450, 350, 600, (200, 120, 100), "อาคารบริหาร"),
        (500, 400, 700, 550, (180, 150, 120), "โรงอาหาร"),
        (800, 450, 1000, 650, (140, 140, 200), "หอประชุม"),
        (100, 700, 250, 850, (160, 200, 140), "ศูนย์กีฬา"),
        (400, 650, 600, 800, (200, 180, 120), "หอพัก"),
    ]

    for x1, y1, x2, y2, color, name in buildings:
        # วาดอาคาร
        cv2.rectangle(campus_map, (x1, y1), (x2, y2), color, -1)
        cv2.rectangle(campus_map, (x1, y1), (x2, y2), (0, 0, 0), 2)

        # เพิ่มชื่ออาคาร
        text_x = x1 + (x2 - x1) // 2 - len(name) * 4
        text_y = y1 + (y2 - y1) // 2
        cv2.putText(campus_map, name, (text_x, text_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        # เพิ่มหน้าต่างอาคาร
        window_rows = max(2, (y2 - y1) // 80)
        window_cols = max(3, (x2 - x1) // 60)

        for i in range(window_rows):
            for j in range(window_cols):
                wx = x1 + 15 + j * ((x2 - x1 - 30) // window_cols)
                wy = y1 + 20 + i * ((y2 - y1 - 40) // window_rows)
                if wx + 12 < x2 and wy + 15 < y2:
                    cv2.rectangle(campus_map, (wx, wy), (wx + 12, wy + 15), (255, 255, 0), -1)
                    cv2.rectangle(campus_map, (wx, wy), (wx + 12, wy + 15), (0, 0, 0), 1)

    # วาดถนนและทางเดิน
    # ถนนหลัก
    cv2.rectangle(campus_map, (0, 380), (1200, 420), (100, 100, 100), -1)
    cv2.rectangle(campus_map, (350, 0), (390, 900), (100, 100, 100), -1)
    cv2.rectangle(campus_map, (700, 0), (740, 900), (100, 100, 100), -1)

    # เส้นกลางถนน
    for x in range(50, 1200, 100):
        cv2.rectangle(campus_map, (x, 395), (x + 40, 405), (255, 255, 255), -1)
    for y in range(50, 900, 100):
        cv2.rectangle(campus_map, (365, y), (375, y + 40), (255, 255, 255), -1)
        cv2.rectangle(campus_map, (715, y), (725, y + 40), (255, 255, 255), -1)

    # ลานกลาง (จุดสำคัญ)
    cv2.circle(campus_map, (550, 320), 80, (100, 200, 100), -1)  # สวนกลาง
    cv2.circle(campus_map, (550, 320), 80, (255, 255, 255), 3)
    cv2.putText(campus_map, "ลานกลาง", (520, 325),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

    # น้ำพุ
    cv2.circle(campus_map, (550, 320), 25, (0, 150, 255), -1)
    cv2.circle(campus_map, (550, 320), 25, (255, 255, 255), 2)

    # ต้นไม้
    tree_positions = [
        (250, 250), (450, 200), (600, 180), (850, 220),
        (200, 500), (300, 520), (450, 500), (650, 480),
        (750, 500), (900, 520), (300, 750), (500, 750)
    ]

    for x, y in tree_positions:
        cv2.circle(campus_map, (x, y), 15, (50, 150, 50), -1)
        cv2.circle(campus_map, (x, y), 15, (100, 200, 100), 2)

    # ป้ายบอกทาง
    cv2.rectangle(campus_map, (500, 50), (600, 80), (255, 255, 255), -1)
    cv2.rectangle(campus_map, (500, 50), (600, 80), (0, 0, 0), 2)
    cv2.putText(campus_map, "ENTRANCE", (510, 70),
               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)

    cv2.imwrite("real_examples/campus_map.jpg", campus_map)

    # ภาพมุมมองระดับตา (Eye-Level)
    street_view = np.ones((700, 1000, 3), dtype=np.uint8) * 200

    # ท้องฟ้าและเมฆ
    cv2.rectangle(street_view, (0, 0), (1000, 250), (220, 230, 180), -1)
    cv2.ellipse(street_view, (200, 120), (100, 40), 0, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(street_view, (700, 80), (80, 30), 0, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(street_view, (450, 150), (60, 25), 0, 0, 360, (255, 255, 255), -1)

    # อาคารหอสมุดด้านซ้าย
    library_pts = np.array([[0, 250], [200, 230], [200, 600], [0, 650]], np.int32)
    cv2.fillPoly(street_view, [library_pts], (150, 100, 80))
    cv2.polylines(street_view, [library_pts], True, (0, 0, 0), 3)

    # หน้าต่างหอสมุด
    for i in range(4):
        for j in range(8):
            wx = 20 + j * 20
            wy = 280 + i * 60
            if wx + 15 < 180:
                cv2.rectangle(street_view, (wx, wy), (wx + 15, wy + 25), (255, 255, 0), -1)
                cv2.rectangle(street_view, (wx, wy), (wx + 15, wy + 25), (0, 0, 0), 1)

    # ป้ายหอสมุด
    cv2.rectangle(street_view, (50, 580), (150, 620), (255, 255, 255), -1)
    cv2.rectangle(street_view, (50, 580), (150, 620), (0, 0, 0), 2)
    cv2.putText(street_view, "LIBRARY", (60, 605),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # อาคารวิศวกรรมกลาง
    engineering_pts = np.array([[300, 200], (550, 180), (550, 550), (300, 580)], np.int32)
    cv2.fillPoly(street_view, [engineering_pts], (120, 150, 200))
    cv2.polylines(street_view, [engineering_pts], True, (0, 0, 0), 3)

    # หน้าต่างอาคารวิศวกรรม
    for i in range(4):
        for j in range(10):
            wx = 320 + j * 22
            wy = 230 + i * 60
            if wx + 18 < 530:
                cv2.rectangle(street_view, (wx, wy), (wx + 18, wy + 28), (255, 255, 0), -1)
                cv2.rectangle(street_view, (wx, wy), (wx + 18, wy + 28), (0, 0, 0), 1)

    # ลานกลางและน้ำพุ (จุดสำคัญ)
    plaza_pts = np.array([[250, 580], [600, 560], [600, 650], [250, 700]], np.int32)
    cv2.fillPoly(street_view, [plaza_pts], (120, 180, 120))

    # น้ำพุ
    cv2.circle(street_view, (425, 615), 30, (0, 150, 255), -1)
    cv2.circle(street_view, (425, 615), 30, (255, 255, 255), 3)
    cv2.circle(street_view, (425, 615), 15, (255, 255, 255), -1)

    # ป้ายลานกลาง
    cv2.rectangle(street_view, (350, 520), (500, 550), (255, 255, 255), -1)
    cv2.rectangle(street_view, (350, 520), (500, 550), (0, 0, 0), 2)
    cv2.putText(street_view, "CENTRAL PLAZA", (360, 540),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    # อาคารวิทยาศาสตร์ด้านขวา
    science_pts = np.array([[650, 220], [1000, 250], [1000, 650], [650, 600]], np.int32)
    cv2.fillPoly(street_view, [science_pts], (100, 180, 100))
    cv2.polylines(street_view, [science_pts], True, (0, 0, 0), 3)

    # หน้าต่างอาคารวิทยาศาสตร์
    for i in range(4):
        for j in range(12):
            wx = 670 + j * 25
            wy = 260 + i * 70
            if wx + 20 < 980:
                cv2.rectangle(street_view, (wx, wy), (wx + 20, wy + 30), (255, 255, 0), -1)
                cv2.rectangle(street_view, (wx, wy), (wx + 20, wy + 30), (0, 0, 0), 1)

    # ถนน
    road_pts = np.array([[0, 580], [1000, 560], [1000, 700], [0, 700]], np.int32)
    cv2.fillPoly(street_view, [road_pts], (120, 120, 120))

    # เส้นถนน
    cv2.line(street_view, (0, 620), (1000, 605), (255, 255, 255), 3)
    cv2.line(street_view, (0, 660), (1000, 645), (255, 255, 255), 3)

    # เส้นกลางถนน
    for i in range(10):
        x1 = i * 100
        x2 = (i + 1) * 100 - 20
        y = 630 - i * 2
        cv2.line(street_view, (x1, y), (x2, y), (255, 255, 0), 2)

    # ต้นไม้
    trees = [(180, 530), (620, 510), (280, 520), (520, 500)]
    for x, y in trees:
        # ลำต้น
        cv2.line(street_view, (x, y), (x, y + 50), (139, 69, 19), 8)
        # ใบไม้
        cv2.circle(street_view, (x, y), 30, (50, 150, 50), -1)
        cv2.circle(street_view, (x, y), 30, (100, 200, 100), 2)

    # ไฟจราจร
    cv2.rectangle(street_view, (150, 450), (170, 570), (100, 100, 100), -1)
    cv2.circle(street_view, (160, 470), 10, (255, 0, 0), -1)
    cv2.circle(street_view, (160, 495), 10, (255, 255, 0), -1)
    cv2.circle(street_view, (160, 520), 10, (0, 255, 0), -1)

    # คน (sylhouette)
    people_positions = [(320, 600), (480, 590), (580, 585)]
    for x, y in people_positions:
        cv2.circle(street_view, (x, y - 20), 8, (50, 50, 50), -1)  # หัว
        cv2.line(street_view, (x, y - 12), (x, y + 15), (50, 50, 50), 4)  # ตัว
        cv2.line(street_view, (x - 8, y - 5), (x + 8, y - 5), (50, 50, 50), 3)  # แขน
        cv2.line(street_view, (x - 5, y + 15), (x - 5, y + 35), (50, 50, 50), 3)  # ขาซ้าย
        cv2.line(street_view, (x + 5, y + 15), (x + 5, y + 35), (50, 50, 50), 3)  # ขาขวา

    cv2.imwrite("real_examples/campus_street_view.jpg", street_view)

    print("✅ สร้างภาพตัวอย่างมหาวิทยาลัยเสร็จแล้ว:")
    print("   📁 real_examples/campus_map.jpg (Top-Down)")
    print("   📁 real_examples/campus_street_view.jpg (Eye-Level)")


def create_shopping_mall():
    """
    สร้างภาพห้างสรรพสินค้าจากมุมมอง Top-Down และ Eye-Level
    """
    print("\n🏬 สร้างภาพตัวอย่าง: ห้างสรรพสินค้า")

    # ภาพแผนผังห้าง (Top-Down)
    mall_map = np.ones((800, 1000, 3), dtype=np.uint8) * 230

    # กรอบอาคาร
    cv2.rectangle(mall_map, (50, 50), (950, 750), (180, 180, 180), -1)
    cv2.rectangle(mall_map, (50, 50), (950, 750), (0, 0, 0), 3)

    # ร้านค้าต่างๆ
    stores = [
        # ชั้น 1
        (80, 80, 200, 180, (255, 200, 200), "Fashion"),
        (220, 80, 340, 180, (200, 255, 200), "Electronics"),
        (360, 80, 480, 180, (200, 200, 255), "Books"),
        (500, 80, 620, 180, (255, 255, 200), "Sports"),
        (640, 80, 760, 180, (255, 200, 255), "Jewelry"),
        (780, 80, 900, 180, (200, 255, 255), "Cosmetics"),

        # ร้านอาหาร (กลาง)
        (200, 350, 800, 450, (255, 180, 120), "Food Court"),

        # ร้านอื่นๆ
        (80, 500, 200, 600, (180, 255, 180), "Supermarket"),
        (220, 500, 340, 600, (180, 180, 255), "Pharmacy"),
        (360, 500, 480, 600, (255, 180, 180), "Toy Store"),
        (500, 500, 620, 600, (180, 255, 255), "Home & Garden"),
        (640, 500, 760, 600, (255, 255, 180), "Coffee Shop"),
        (780, 500, 900, 600, (255, 180, 255), "Banking"),

        # ร้านด้านล่าง
        (80, 620, 200, 720, (200, 200, 200), "Cinema"),
        (220, 620, 480, 720, (150, 150, 150), "Department Store"),
        (500, 620, 900, 720, (170, 170, 170), "Anchor Store"),
    ]

    for x1, y1, x2, y2, color, name in stores:
        cv2.rectangle(mall_map, (x1, y1), (x2, y2), color, -1)
        cv2.rectangle(mall_map, (x1, y1), (x2, y2), (0, 0, 0), 2)

        # ชื่อร้าน
        text_x = x1 + (x2 - x1) // 2 - len(name) * 3
        text_y = y1 + (y2 - y1) // 2
        cv2.putText(mall_map, name, (text_x, text_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    # ทางเดินหลัก
    cv2.rectangle(mall_map, (80, 200), (920, 330), (240, 240, 240), -1)  # ทางเดินบน
    cv2.rectangle(mall_map, (80, 470), (920, 500), (240, 240, 240), -1)  # ทางเดินล่าง
    cv2.rectangle(mall_map, (480, 80), (520, 720), (240, 240, 240), -1)  # ทางเดินกลาง

    # ลิฟต์และบันได
    cv2.rectangle(mall_map, (450, 250), (490, 320), (150, 150, 150), -1)
    cv2.rectangle(mall_map, (450, 250), (490, 320), (0, 0, 0), 2)
    cv2.putText(mall_map, "LIFT", (460, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    cv2.rectangle(mall_map, (520, 250), (560, 320), (160, 160, 160), -1)
    cv2.rectangle(mall_map, (520, 250), (560, 320), (0, 0, 0), 2)
    cv2.putText(mall_map, "STAIR", (525, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)

    # Information Center
    cv2.circle(mall_map, (500, 285), 30, (255, 0, 0), -1)
    cv2.circle(mall_map, (500, 285), 30, (255, 255, 255), 2)
    cv2.putText(mall_map, "INFO", (480, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    # ทางเข้า-ออก
    entrances = [(480, 50), (100, 400), (900, 400), (480, 750)]
    for x, y in entrances:
        cv2.rectangle(mall_map, (x-20, y-10), (x+20, y+10), (0, 255, 0), -1)
        cv2.rectangle(mall_map, (x-20, y-10), (x+20, y+10), (0, 0, 0), 2)

    cv2.imwrite("real_examples/mall_map.jpg", mall_map)

    # ภาพมุมมองข้างใน (Eye-Level)
    mall_interior = np.ones((600, 900, 3), dtype=np.uint8) * 240

    # เพดาน
    cv2.rectangle(mall_interior, (0, 0), (900, 150), (250, 250, 250), -1)

    # ไฟเพดาน
    for x in range(100, 900, 200):
        cv2.rectangle(mall_interior, (x-20, 50), (x+20, 70), (255, 255, 0), -1)
        cv2.rectangle(mall_interior, (x-20, 50), (x+20, 70), (200, 200, 0), 2)

    # ร้านด้านซ้าย
    left_stores = np.array([[0, 150], [250, 140], [250, 480], [0, 500]], np.int32)
    cv2.fillPoly(mall_interior, [left_stores], (255, 200, 200))
    cv2.polylines(mall_interior, [left_stores], True, (0, 0, 0), 2)

    # ร้านด้านขวา
    right_stores = np.array([[650, 140], [900, 150], [900, 500], [650, 480]], np.int32)
    cv2.fillPoly(mall_interior, [right_stores], (200, 255, 200))
    cv2.polylines(mall_interior, [right_stores], True, (0, 0, 0), 2)

    # ป้ายร้าน
    cv2.rectangle(mall_interior, (50, 180), (200, 220), (255, 255, 255), -1)
    cv2.rectangle(mall_interior, (50, 180), (200, 220), (0, 0, 0), 2)
    cv2.putText(mall_interior, "FASHION STORE", (55, 205),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    cv2.rectangle(mall_interior, (700, 180), (850, 220), (255, 255, 255), -1)
    cv2.rectangle(mall_interior, (700, 180), (850, 220), (0, 0, 0), 2)
    cv2.putText(mall_interior, "ELECTRONICS", (705, 205),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    # ทางเดินกลาง
    cv2.rectangle(mall_interior, (250, 480), (650, 580), (220, 220, 220), -1)

    # ลายพื้น
    for i in range(8):
        x = 250 + i * 50
        cv2.line(mall_interior, (x, 480), (x, 580), (200, 200, 200), 1)

    # Information Center กลางห้าง
    cv2.circle(mall_interior, (450, 300), 40, (255, 0, 0), -1)
    cv2.circle(mall_interior, (450, 300), 40, (255, 255, 255), 3)
    cv2.putText(mall_interior, "INFO", (425, 310),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # โต๊ะ Information
    info_desk = np.array([[400, 350], [500, 350], [500, 400], [400, 400]], np.int32)
    cv2.fillPoly(mall_interior, [info_desk], (150, 150, 150))
    cv2.polylines(mall_interior, [info_desk], True, (0, 0, 0), 2)

    # คนในห้าง
    people = [(200, 450), (350, 420), (550, 440), (700, 430)]
    for x, y in people:
        cv2.circle(mall_interior, (x, y - 15), 6, (100, 100, 100), -1)  # หัว
        cv2.line(mall_interior, (x, y - 9), (x, y + 10), (100, 100, 100), 3)  # ตัว
        cv2.line(mall_interior, (x - 6, y - 3), (x + 6, y - 3), (100, 100, 100), 2)  # แขน
        cv2.line(mall_interior, (x - 3, y + 10), (x - 3, y + 25), (100, 100, 100), 2)  # ขา
        cv2.line(mall_interior, (x + 3, y + 10), (x + 3, y + 25), (100, 100, 100), 2)

    # ป้ายชี้ทาง
    cv2.rectangle(mall_interior, (350, 100), (550, 130), (255, 255, 255), -1)
    cv2.rectangle(mall_interior, (350, 100), (550, 130), (0, 0, 0), 2)
    cv2.putText(mall_interior, "INFORMATION CENTER", (360, 120),
               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)

    # ลูกศรชี้ลง
    arrow_pts = np.array([[450, 130], [440, 150], [460, 150]], np.int32)
    cv2.fillPoly(mall_interior, [arrow_pts], (255, 0, 0))

    cv2.imwrite("real_examples/mall_interior.jpg", mall_interior)

    print("✅ สร้างภาพตัวอย่างห้างสรรพสินค้าเสร็จแล้ว:")
    print("   📁 real_examples/mall_map.jpg (Top-Down)")
    print("   📁 real_examples/mall_interior.jpg (Eye-Level)")


def main():
    print("🎨 สร้างภาพตัวอย่างเหมือนจริงสำหรับทดสอบ HomographyMatcher")
    print("=" * 60)

    create_university_campus()
    create_shopping_mall()

    print("\n🎉 สร้างภาพตัวอย่างเสร็จสมบูรณ์!")
    print("=" * 60)
    print("📁 ไฟล์ที่สร้าง:")
    print("   • real_examples/campus_map.jpg")
    print("   • real_examples/campus_street_view.jpg")
    print("   • real_examples/mall_map.jpg")
    print("   • real_examples/mall_interior.jpg")
    print("\n💡 ใช้ไฟล์เหล่านี้กับคำสั่ง:")
    print("   python cli.py --eye real_examples/campus_street_view.jpg --top real_examples/campus_map.jpg")
    print("   python cli.py --eye real_examples/mall_interior.jpg --top real_examples/mall_map.jpg")


if __name__ == "__main__":
    main()

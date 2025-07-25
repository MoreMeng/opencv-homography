# OpenCV Homography Matcher

โปรแกรม Python สำหรับเปรียบเทียบภาพ Eye-Level (ภาพจากระดับสายตาคน) กับ Top-Down (ภาพจากโดรนหรือแผนที่) โดยใช้ Feature Matching และ Homography Transformation

## 🎯 วัตถุประสงค์

- เปรียบเทียบภาพที่ถ่ายจากมุมมองที่แตกต่างกัน
- หาจุดที่ตรงกันระหว่างภาพสองภาพ
- แปลงภาพจากมุมมองหนึ่งไปเป็นอีกมุมมองหนึ่ง
- วิเคราะห์ความเชื่อถือได้ของการจับคู่

## 🔧 การติดตั้ง

### 1. Clone หรือ Download โปรเจกต์

```bash
git clone <repository-url>
cd opencv-homography
```

### 2. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 3. ตรวจสอบการติดตั้ง

```bash
python -c "import cv2; print('OpenCV version:', cv2.__version__)"
```

## 🚀 การใช้งาน

### ตัวอย่างพื้นฐาน

```bash
# รันตัวอย่างด้วยภาพที่สร้างขึ้นอัตโนมัติ
python example_usage.py
```

### การใช้งานกับภาพของคุณเอง

```bash
python homography_matcher.py \
    --eye_level path/to/eye_level_image.jpg \
    --top_down path/to/top_down_image.jpg \
    --detector SIFT \
    --output results
```

### พารามิเตอร์ที่สำคัญ

- `--eye_level`: ไฟล์ภาพมุมมองระดับตา
- `--top_down`: ไฟล์ภาพมุมมองจากด้านบน
- `--detector`: ประเภท feature detector (`SIFT`, `ORB`, `AKAZE`)
- `--min_matches`: จำนวนการจับคู่ขั้นต่ำ (default: 10)
- `--output`: โฟลเดอร์สำหรับบันทึกผลลัพธ์

## 📊 Feature Detectors ที่รองรับ

### 1. SIFT (Scale-Invariant Feature Transform)
- **ข้อดี**: ความแม่นยำสูง, ทนต่อการเปลี่ยนแปลงขนาดและการหมุน
- **ข้อเสีย**: ช้า, ใช้หน่วยความจำมาก
- **เหมาะสำหรับ**: ภาพที่มีรายละเอียดมาก, การจับคู่ที่ต้องการความแม่นยำสูง

### 2. ORB (Oriented FAST and Rotated BRIEF)
- **ข้อดี**: เร็ว, ใช้หน่วยความจำน้อย
- **ข้อเสีย**: ความแม่นยำต่ำกว่า SIFT
- **เหมาะสำหรับ**: การประมวลผลแบบ real-time, ระบบที่มีทรัพยากรจำกัด

### 3. AKAZE (Accelerated-KAZE)
- **ข้อดี**: สมดุลระหว่างความเร็วและความแม่นยำ
- **ข้อเสีย**: อาจไม่เหมาะกับภาพบางประเภท
- **เหมาะสำหรับ**: การประมวลผลขนาดกลาง

## 📁 โครงสร้างไฟล์ผลลัพธ์

```
output/
├── matches_visualization.jpg    # ภาพแสดงการจับคู่ features
├── transformed_eye_level.jpg    # ภาพ eye-level ที่ถูก transform
├── original_top_down.jpg        # ภาพ top-down ต้นฉบับ
└── comparison.jpg               # การเปรียบเทียบแบบเคียงข้างกัน
```

## 🎨 ตัวอย่างการใช้งานใน Code

```python
from homography_matcher import HomographyMatcher

# สร้าง matcher
matcher = HomographyMatcher(
    feature_detector='SIFT',
    min_match_count=10
)

# เปรียบเทียบภาพ
results = matcher.compare_images(
    eye_level_path="eye_level.jpg",
    top_down_path="top_down.jpg",
    output_dir="results"
)

# ตรวจสอบผลลัพธ์
if results['homography_found']:
    print(f"✅ พบการจับคู่! Confidence: {results['confidence_score']:.2f}")
    print(f"Inlier matches: {results['inlier_matches']}")
else:
    print("❌ ไม่พบการจับคู่ที่เชื่อถือได้")
```

## 🔍 การตีความผลลัพธ์

### Confidence Score
- **0.7-1.0**: การจับคู่ที่เชื่อถือได้สูง
- **0.5-0.7**: การจับคู่ปานกลาง
- **0.3-0.5**: การจับคู่ที่อาจไม่แม่นยำ
- **< 0.3**: การจับคู่ที่ไม่น่าเชื่อถือ

### จำนวน Matches
- **> 50**: เหมาะสำหรับการใช้งานจริง
- **20-50**: ใช้งานได้แต่ควรระวัง
- **10-20**: ขั้นต่ำสำหรับการทดสอบ
- **< 10**: ไม่เพียงพอสำหรับ Homography

## 💡 เทคนิคการปรับปรุงผลลัพธ์

### 1. การเตรียมภาพ
- ปรับความคมชัด (contrast) และความสว่าง (brightness)
- ลดสัญญาณรบกวน (noise reduction)
- เลือกพื้นที่ที่มี features ชัดเจน

### 2. การตั้งค่าพารามิเตอร์
- ลดค่า `min_match_count` หากภาพมี features น้อย
- เปลี่ยน feature detector ตามลักษณะภาพ
- ปรับ ratio test threshold สำหรับ SIFT

### 3. การประมวลผลภาพ
```python
# ปรับปรุงคุณภาพภาพ
gray = cv2.convertScaleAbs(gray, alpha=1.2, beta=10)  # เพิ่ม contrast
gray = cv2.GaussianBlur(gray, (3, 3), 0)  # ลด noise
```

## 🐛 การแก้ไขปัญหาทั่วไป

### ปัญหา: ไม่พบ matches เพียงพอ
- **สาเหตุ**: ภาพมีความแตกต่างมาก หรือ features น้อย
- **แก้ไข**: ลด `min_match_count`, เปลี่ยน detector, ปรับปรุงคุณภาพภาพ

### ปัญหา: Homography ไม่แม่นยำ
- **สาเหตุ**: Matches มีจุดผิดพลาดมาก
- **แก้ไข**: เพิ่มค่า RANSAC threshold, กรองภาพให้ดีขึ้น

### ปัญหา: โปรแกรมช้า
- **สาเหตุ**: ใช้ SIFT กับภาพขนาดใหญ่
- **แก้ไข**: ลดขนาดภาพ, เปลี่ยนเป็น ORB หรือ AKAZE

## 📚 ทฤษฎีเบื้องหลัง

### Feature Matching
การหาจุดที่มีลักษณะเด่นในภาพ (keypoints) และการจับคู่จุดเหล่านั้นระหว่างสองภาพ

### Homography
การแปลงทางคณิตศาสตร์ที่สามารถเปลี่ยนมุมมองของภาพได้ โดยใช้ matrix 3x3

### RANSAC
อัลกอริทึมสำหรับกรองข้อมูลผิดพลาด (outliers) ออกจากการจับคู่

## 🔗 แหล่งข้อมูลเพิ่มเติม

- [OpenCV Documentation](https://docs.opencv.org/)
- [SIFT Paper](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf)
- [ORB Paper](https://www.willowgarage.com/sites/default/files/orb_final.pdf)
- [Homography Explained](https://docs.opencv.org/master/d9/dab/tutorial_homography.html)

## 🤝 การมีส่วนร่วม

หากพบปัญหาหรือต้องการปรับปรุง กรุณา:
1. เปิด Issue
2. ส่ง Pull Request
3. แชร์ตัวอย่างการใช้งาน

## 📄 License

MIT License - ดูรายละเอียดในไฟล์ LICENSE

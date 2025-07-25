# 🤝 Contributing to OpenCV Homography Matcher

ขอบคุณที่สนใจมีส่วนร่วมในการพัฒนา OpenCV Homography Matcher! การมีส่วนร่วมของคุณจะช่วยให้โปรเจกต์นี้ดีขึ้น

## 🚀 วิธีการมีส่วนร่วม

### 1. การรายงานปัญหา (Bug Reports)
หากพบข้อผิดพลาดหรือปัญหา:
- เปิด Issue ใหม่
- อธิบายปัญหาอย่างละเอียด
- ใส่ข้อมูล:
  - ระบบปฏิบัติการ
  - เวอร์ชัน Python
  - เวอร์ชัน OpenCV
  - ภาพตัวอย่างที่ทำให้เกิดปัญหา (ถ้าเป็นไปได้)

### 2. การขอฟีเจอร์ใหม่ (Feature Requests)
หากต้องการฟีเจอร์ใหม่:
- เปิด Issue พร้อมป้าย "enhancement"
- อธิบายฟีเจอร์ที่ต้องการ
- ยกตัวอย่างการใช้งาน
- อธิบายเหตุผลที่ฟีเจอร์นี้มีประโยชน์

### 3. การส่ง Pull Request
ก่อนส่ง PR:
1. Fork repository
2. สร้าง branch ใหม่ (`git checkout -b feature/amazing-feature`)
3. ทำการเปลี่ยนแปลง
4. เพิ่ม tests (ถ้าเป็นไปได้)
5. อัปเดต documentation
6. ทดสอบให้แน่ใจว่าทุกอย่างทำงานได้
7. Commit การเปลี่ยนแปลง (`git commit -m 'Add amazing feature'`)
8. Push ไป branch (`git push origin feature/amazing-feature`)
9. เปิด Pull Request

## 📝 Code Style Guidelines

### Python Style
- ปฏิบัติตาม PEP 8
- ใช้ 4 spaces สำหรับ indentation
- ใช้ descriptive variable names
- เพิ่ม docstrings สำหรับ functions และ classes

### Commit Messages
ใช้รูปแบบ:
```
type: brief description

Detailed explanation (ถ้าจำเป็น)

- Change 1
- Change 2
```

Types:
- `feat`: ฟีเจอร์ใหม่
- `fix`: แก้ไขข้อผิดพลาด
- `docs`: อัปเดต documentation
- `style`: การปรับแต่งรูปแบบโค้ด
- `refactor`: ปรับปรุงโครงสร้างโค้ด
- `test`: เพิ่มหรือแก้ไข tests
- `chore`: งานที่ไม่เกี่ยวกับโค้ดหลัก

## 🧪 การทดสอบ

ก่อนส่ง PR ให้ทดสอบ:

```bash
# ทดสอบการทำงานพื้นฐาน
python demo.py

# ทดสอบกับภาพตัวอย่าง
python example_usage.py

# ทดสอบ CLI
python cli.py --eye real_examples/campus_street_view.jpg --top real_examples/campus_map.jpg

# ทดสอบขั้นสูง
python advanced_test.py
```

## 📚 การเพิ่ม Documentation

### README Updates
- อัปเดต README.md หากเพิ่มฟีเจอร์ใหม่
- เพิ่มตัวอย่างการใช้งาน
- อัปเดต installation instructions

### Code Documentation
- เพิ่ม docstrings สำหรับ functions ใหม่
- ใช้ Google style docstrings:

```python
def new_function(param1: str, param2: int) -> bool:
    """
    Brief description of function.
    
    Args:
        param1 (str): Description of param1
        param2 (int): Description of param2
        
    Returns:
        bool: Description of return value
        
    Raises:
        ValueError: When invalid input is provided
    """
    pass
```

## 🎯 Areas for Contribution

### High Priority
- [ ] ปรับปรุงประสิทธิภาพการประมวลผล
- [ ] เพิ่ม unit tests
- [ ] ปรับปรุง error handling
- [ ] เพิ่มการรองรับรูปแบบภาพใหม่

### Medium Priority  
- [ ] เพิ่ม GUI interface
- [ ] ปรับปรุงการแสดงผลลัพธ์
- [ ] เพิ่ม configuration file support
- [ ] ปรับปรุง documentation

### Low Priority
- [ ] เพิ่ม video processing
- [ ] การรองรับ batch processing
- [ ] เพิ่ม web interface
- [ ] การส่งออกผลลัพธ์เป็น different formats

## 🔧 Development Setup

### Environment Setup
```bash
# Clone repository
git clone https://github.com/your-username/opencv-homography.git
cd opencv-homography

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# หรือ
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

### Development Workflow
```bash
# สร้าง branch ใหม่
git checkout -b feature/your-feature

# ทำการพัฒนา
# ...

# ทดสอบ
python -m pytest tests/
python demo.py

# Format code
black *.py
flake8 *.py

# Commit และ push
git add .
git commit -m "feat: add your feature"
git push origin feature/your-feature
```

## 📋 Code Review Process

Pull Requests จะได้รับการ review โดย:
1. ตรวจสอบ code style และ quality
2. ทดสอบการทำงาน
3. ตรวจสอบ documentation
4. ตรวจสอบ backward compatibility

## 🏆 Recognition

Contributors จะได้รับการกล่าวขอบคุณใน:
- README.md
- CHANGELOG.md
- Release notes

## 📞 ติดต่อ

หากมีคำถามเกี่ยวกับการมีส่วนร่วม:
- เปิด Discussion ใน GitHub
- สร้าง Issue พร้อมป้าย "question"

## 📜 Code of Conduct

### Our Pledge
เรามุ่งมั่นสร้างสภาพแวดลอมที่:
- เปิดกว้างและต้อนรับ
- หลากหลายและครอบคลุม
- ปลอดภัยและเป็นมิตร

### Standards
พฤติกรรมที่เหมาะสม:
- ใช้ภาษาที่เป็นมิตรและครอบคลุม
- เคารพความคิดเห็นที่แตกต่าง
- ให้ constructive feedback
- โฟกัสที่ดีที่สุดสำหรับชุมชน

พฤติกรรมที่ไม่เหมาะสม:
- การใช้ภาษาหรือภาพที่ไม่เหมาะสม
- การคุกคามหรือการโจมตี
- การก่อกวนหรือพฤติกรรมไม่เหมาะสม

ขอบคุณที่ช่วยทำให้ OpenCV Homography Matcher ดีขึ้น! 🎉

@echo off
echo OpenCV Homography Matcher - Quick Start
echo ========================================

REM ตรวจสอบว่ามีภาพในโฟลเดอร์หรือไม่
if not exist "my_images\eye_level\*.jpg" if not exist "my_images\eye_level\*.png" (
    echo ❌ ไม่พบภาพ Eye-Level ในโฟลเดอร์ my_images/eye_level/
    echo กรุณาวางภาพในโฟลเดอร์ดังกล่าวก่อน
    pause
    exit /b
)

if not exist "my_images\top_down\*.jpg" if not exist "my_images\top_down\*.png" (
    echo ❌ ไม่พบภาพ Top-Down ในโฟลเดอร์ my_images/top_down/
    echo กรุณาวางภาพในโฟลเดอร์ดังกล่าวก่อน
    pause
    exit /b
)

echo 🔍 กำลังค้นหาภาพ...
for %%f in (my_images\eye_level\*.jpg my_images\eye_level\*.png) do set "EYE_LEVEL=%%f"
for %%f in (my_images\top_down\*.jpg my_images\top_down\*.png) do set "TOP_DOWN=%%f"

echo 📷 Eye-Level: %EYE_LEVEL%
echo 🗺️ Top-Down: %TOP_DOWN%

echo.
echo 🚀 เริ่มการเปรียบเทียบ...
C:/Python313/python.exe cli.py --eye "%EYE_LEVEL%" --top "%TOP_DOWN%" --benchmark --output my_results

echo.
echo ✅ เสร็จสิ้น! ดูผลลัพธ์ในโฟลเดอร์ my_results/
pause

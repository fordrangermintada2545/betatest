import requests
import os

# 1. ตั้งค่าที่อยู่ไฟล์บน GitHub (ใช้ URL แบบ Raw)
VERSION_URL = "https://raw.githubusercontent.com/ชื่อของคุณ/ชื่อโปรเจกต์/main/version.txt"
APP_URL = "https://raw.githubusercontent.com/ชื่อของคุณ/ชื่อโปรเจกต์/main/my_app.py"

current_version = "1.0" # เวอร์ชันที่อยู่ในเครื่องผู้ใช้ขณะนั้น

def check_for_update():
    print("กำลังตรวจสอบการอัปเดต...")
    try:
        # ดึงเลขเวอร์ชันล่าสุดจาก GitHub
        response = requests.get(VERSION_URL)
        latest_version = response.text.strip()

        if latest_version > current_version:
            print(f"พบเวอร์ชันใหม่ ({latest_version})! กำลังดาวน์โหลด...")
            
            # ดาวน์โหลดไฟล์โปรแกรมใหม่มาทับไฟล์เดิม
            app_response = requests.get(APP_URL)
            with open("my_app.py", "wb") as f:
                f.write(app_response.content)
            
            print("อัปเดตเสร็จแล้ว! กำลังเปิดโปรแกรม...")
        else:
            print("คุณใช้เวอร์ชันล่าสุดแล้ว")
            
    except:
        print("ไม่สามารถเชื่อมต่ออินเทอร์เน็ตได้ จะเปิดโปรแกรมเดิมที่มีอยู่")

# รันระบบเช็คอัปเดตก่อนเข้าโปรแกรม
check_for_update()

# หลังจากอัปเดตเสร็จ (หรือถ้าไม่อัปเดต) ก็สั่งรันโปรแกรมหลัก
os.system("python my_app.py")
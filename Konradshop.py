import customtkinter as ctk
import requests
import subprocess
import os
import sys

# --- [ CONFIGURATION ] ---
SECRET_CODE = "Konradshop324152"
DB_BASE_URL = "https://konradshop-default-rtdb.asia-southeast1.firebasedatabase.app/keys"

def get_hwid():
    try:
        cmd = 'powershell -command "(Get-CimInstance -Class Win32_ComputerSystemProduct).UUID"'
        uuid = subprocess.check_output(cmd, shell=True).decode().strip()
        if not uuid or "00000000" in uuid:
            cmd = 'powershell -command "(Get-CimInstance -Class Win32_BIOS).SerialNumber"'
            uuid = subprocess.check_output(cmd, shell=True).decode().strip()
        return uuid
    except:
        return "UNKNOWN_DEVICE_ID"

# --- Class หน้าเมนูหลัก ---
class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("KonradShop Dashboard")
        self.geometry("450x450")
        ctk.set_appearance_mode("dark")

        ctk.CTkLabel(self, text="เมนูจัดการโปรแกรม", font=("Inter", 20, "bold")).pack(pady=30)

        def run_eat():
            target_exe = "EAT.exe"
            if os.path.exists(target_exe):
                try:
                    # ส่ง SECRET_CODE ไปหา EAT.exe
                    subprocess.Popen([target_exe, SECRET_CODE])
                except Exception as e:
                    print(f"Error: {e}")
            else:
                from tkinter import messagebox
                messagebox.showerror("Error", f"ไม่พบไฟล์ {target_exe}")

        ctk.CTkButton(self, text="Marcro Eat", 
                       command=run_eat, width=280, height=60).pack(pady=20)
        def run_eat():
            target_exe = "Bootfps.exe"
            if os.path.exists(target_exe):
                try:
                    # ส่ง SECRET_CODE ไปหา Bootfps.exe
                    subprocess.Popen([target_exe, SECRET_CODE])
                except Exception as e:
                    print(f"Error: {e}")
            else:
                from tkinter import messagebox
                messagebox.showerror("Error", f"ไม่พบไฟล์ {target_exe}")

        ctk.CTkButton(self, text="BootFps", 
                       command=run_eat, width=280, height=60).pack(pady=20)
        ctk.CTkButton(self, text="ออกจากระบบ", command=sys.exit, fg_color="gray").pack(pady=10)
# --- Class หน้า Login ---
class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("KonradShop Security System")
        self.geometry("450x450")
        ctk.set_appearance_mode("dark")
        
        self.my_hwid = get_hwid()

        self.label = ctk.CTkLabel(self, text="KONRAD SHOP", font=("Inter", 26, "bold"))
        self.label.pack(pady=(40, 20))

        self.login_btn = ctk.CTkButton(self, text="เข้าสู่ระบบ (เครื่องที่ลงทะเบียนแล้ว)", 
                                       command=self.check_existing_user, 
                                       width=320, height=50, corner_radius=10)
        self.login_btn.pack(pady=10)

        ctk.CTkLabel(self, text="----------------- หรือ -----------------", font=("Inter", 12)).pack(pady=10)

        self.key_entry = ctk.CTkEntry(self, placeholder_text="กรอก License Key ของคุณ", 
                                      width=320, height=40, justify="center")
        self.key_entry.pack(pady=10)

        self.activate_btn = ctk.CTkButton(self, text="ยืนยันคีย์เปิดใช้งานครั้งแรก", 
                                          command=self.activate_new_key,
                                          width=320, height=50, corner_radius=10,
                                          fg_color="#28a745", hover_color="#218838")
        self.activate_btn.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="สถานะ: พร้อมตรวจสอบ", font=("Inter", 12))
        self.status_label.pack(pady=20)

    def check_existing_user(self):
        try:
            # ดึงข้อมูลมาเช็ค HWID
            response = requests.get(f"{DB_BASE_URL}.json", timeout=7)
            all_keys = response.json()

            if all_keys:
                for key, info in all_keys.items():
                    if info.get('hwid') == self.my_hwid:
                        self.status_label.configure(text="✅ สำเร็จ! กำลังเข้าสู่หน้าเมนู...", text_color="green")
                        # แก้ไขตรงนี้: เรียกใช้ self.switch_to_menu()
                        self.after(1000, self.switch_to_menu)
                        return
            
            self.status_label.configure(text="❌ เครื่องนี้ยังไม่ถูกลงทะเบียน", text_color="#FF5555")
        except Exception as e:
            self.status_label.configure(text="⚠️ การเชื่อมต่อขัดข้อง", text_color="yellow")
            print(f"Error Detail: {e}")

    def activate_new_key(self):
        user_key = self.key_entry.get().strip()
        if not user_key:
            self.status_label.configure(text="⚠️ กรุณากรอกคีย์", text_color="orange")
            return

        try:
            response = requests.get(f"{DB_BASE_URL}/{user_key}.json", timeout=7)
            data = response.json()

            if data:
                if data.get('status') == 'unused':
                    update_data = {"status": "used", "hwid": self.my_hwid}
                    requests.patch(f"{DB_BASE_URL}/{user_key}.json", json=update_data)
                    self.status_label.configure(text="✅ ลงทะเบียนสำเร็จ!", text_color="green")
                    # แก้ไขตรงนี้: เรียกใช้ self.switch_to_menu()
                    self.after(1000, self.switch_to_menu)
                else:
                    self.status_label.configure(text="❌ คีย์นี้ถูกใช้งานไปแล้ว", text_color="#FF5555")
            else:
                self.status_label.configure(text="❌ ไม่พบคีย์นี้ในระบบ", text_color="#FF5555")
        except:
            self.status_label.configure(text="⚠️ การเชื่อมต่อขัดข้อง", text_color="yellow")

    def switch_to_menu(self):
        self.destroy() # ปิดหน้า Login
        main_app = MainMenu() # เปิดหน้าเมนู
        main_app.mainloop()

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
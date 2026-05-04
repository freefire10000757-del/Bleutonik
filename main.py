#!/usr/bin/env python3
"""
Hack .tronel v1.0 - Wallpaper Changer for Android
تغيير خلفية الجهاز بشكل وهمي للاختبارات المصرح بها
"""

import jnius
import os
import sys
import platform
import tempfile
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation

# ========== أذونات Android ==========

def request_permissions():
    """طلب أذونات Android"""
    try:
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.SET_WALLPAPER
        ])
    except:
        pass

# ========== تغيير الخلفية على Android ==========

class AndroidWallpaper:
    """تغيير خلفية Android عبر JNI"""
    
    @staticmethod
    def set_wallpaper(image_path):
        """تغيير خلفية Android"""
        try:
            from jnius import autoclass
            
            # جلب السياق
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Context = autoclass('android.content.Context')
            WallpaperManager = autoclass('android.app.WallpaperManager')
            BitmapFactory = autoclass('android.graphics.BitmapFactory')
            
            activity = PythonActivity.mActivity
            wallpaper_manager = WallpaperManager.getInstance(activity)
            
            # فك الصورة
            bitmap = BitmapFactory.decodeFile(image_path)
            wallpaper_manager.setBitmap(bitmap)
            
            return True
        except Exception as e:
            print(f"[!] خطأ في تغيير الخلفية: {e}")
            return False
    
    @staticmethod
    def create_wallpaper():
        """إنشاء صورة خلفية حمراء"""
        path = os.path.join(tempfile.gettempdir(), "tronel_wallpaper.png")
        
        # نستخدم مكتبة PIL إذا كانت موجودة، وإلا ننشئ صورة بسيطة
        try:
            from PIL import Image, ImageDraw
            
            img = Image.new('RGB', (1080, 1920), (10, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # تدرج أحمر
            for y in range(1920):
                r = int(180 * (1 - y / 1920)) + 40
                for x in range(0, 1080, 5):
                    draw.point((x, y), fill=(r, 0, 0))
            
            # رسم النص
            for i, line in enumerate([
                "████████╗██████╗  ██████╗ ███╗   ██╗███████╗██╗",
                "╚══██╔══╝██╔══██╗██╔═══██╗████╗  ██║██╔════╝██║",
                "   ██║   ██████╔╝██║   ██║██╔██╗ ██║█████╗  ██║",
                "   ██║   ██╔══██╗██║   ██║██║╚██╗██║██╔══╝  ██║",
                "   ██║   ██║  ██║╚██████╔╝██║ ╚████║███████╗███████╗",
                "   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚══════╝"
            ]):
                draw.text((20, 100 + i * 45), line, fill=(255, 0, 0))
            
            draw.text((50, 450), "⚠️ SYSTEM COMPROMISED ⚠️", fill=(255, 50, 50))
            draw.text((50, 550), "Your device wallpaper has been changed!", fill=(200, 50, 50))
            draw.text((50, 650), "This is an authorized security test.", fill=(150, 50, 50))
            
            img.save(path)
            return path
            
        except ImportError:
            # إنشاء صورة BMP بسيطة
            return AndroidWallpaper._create_bmp_wallpaper(path)
    
    @staticmethod
    def _create_bmp_wallpaper(path):
        """إنشاء صورة BMP بدون PIL"""
        import struct
        w, h = 1080, 1920
        row = ((w * 3 + 3) // 4) * 4
        
        with open(path, 'wb') as f:
            f.write(b'BM')
            f.write(struct.pack('<I', 54 + row * h))
            f.write(struct.pack('<HH', 0, 0))
            f.write(struct.pack('<I', 54))
            f.write(struct.pack('<I', 40))
            f.write(struct.pack('<i', w))
            f.write(struct.pack('<i', -h))
            f.write(struct.pack('<HH', 1, 24))
            f.write(b'\x00' * 24)
            
            for y in range(h):
                r = int(180 * (1 - y / h)) + 30
                row_data = bytes([0, 0, r]) * w
                f.write(row_data + b'\x00' * (row - w * 3))
        
        return path


# ========== تطبيق Kivy ==========

class TronelApp(App):
    """تطبيق Hack .tronel"""
    
    def build(self):
        # طلب الأذونات
        request_permissions()
        
        # إعداد النافذة
        Window.size = (400, 700)
        Window.borderless = True
        
        self.root = FloatLayout()
        
        # الخلفية
        with self.root.canvas.before:
            Color(0.08, 0, 0, 1)
            self.rect = Rectangle(size=Window.size, pos=self.root.pos)
        
        self.root.bind(size=self._update_rect, pos=self._update_rect)
        
        # شعار TRONEL
        self.logo = Label(
            text="[color=FF0000]████████╗██████╗  ██████╗ ███╗   ██╗███████╗██╗\n"
                 "╚══██╔══╝██╔══██╗██╔═══██╗████╗  ██║██╔════╝██║\n"
                 "   ██║   ██████╔╝██║   ██║██╔██╗ ██║█████╗  ██║\n"
                 "   ██║   ██╔══██╗██║   ██║██║╚██╗██║██╔══╝  ██║\n"
                 "   ██║   ██║  ██║╚██████╔╝██║ ╚████║███████╗███████╗\n"
                 "   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚══════╝[/color]",
            font_size=11,
            markup=True,
            font_name='monospace',
            pos_hint={'center_x': 0.5, 'center_y': 0.85},
            size_hint=(1, 0.25)
        )
        self.root.add_widget(self.logo)
        
        # رابط التحميل
        self.dl_label = Label(
            text="[color=FF6600]⬇️ Downloading system payload... ⬇️[/color]",
            font_size=16,
            markup=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            size_hint=(1, 0.05)
        )
        self.root.add_widget(self.dl_label)
        
        # بروجرس بار
        self.progress = ProgressBar(
            max=100, value=0,
            pos_hint={'center_x': 0.5, 'center_y': 0.58},
            size_hint=(0.8, 0.04)
        )
        self.root.add_widget(self.progress)
        
        # نص الحالة
        self.status = Label(
            text="[color=888888]Initializing...[/color]",
            font_size=14,
            markup=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.52},
            size_hint=(1, 0.04)
        )
        self.root.add_widget(self.status)
        
        # تحذير
        self.warning = Label(
            text="[color=FF0000]⚠️ DO NOT CLOSE THIS APP ⚠️[/color]",
            font_size=18,
            markup=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.20},
            size_hint=(1, 0.05)
        )
        self.root.add_widget(self.warning)
        
        # النتيجة النهائية
        self.result = Label(
            text="",
            font_size=16,
            markup=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.12},
            size_hint=(1, 0.08)
        )
        self.root.add_widget(self.result)
        
        # زر إغلاق (مخفي في البداية)
        self.close_btn = Button(
            text="EXIT",
            size_hint=(0.3, 0.06),
            pos_hint={'center_x': 0.5, 'center_y': 0.05},
            background_color=(0.8, 0, 0, 1),
            color=(1, 1, 1, 1),
            opacity=0
        )
        self.close_btn.bind(on_press=self.exit_app)
        self.root.add_widget(self.close_btn)
        
        # بدء التسلسل
        Clock.schedule_once(self.run_sequence, 1)
        
        return self.root
    
    def _update_rect(self, inst, val):
        self.rect.pos = inst.pos
        self.rect.size = inst.size
    
    def run_sequence(self, dt):
        """تشغيل التسلسل الوهمي"""
        Clock.schedule_once(self.step1, 0)
    
    def step1(self, dt):
        self.dl_label.text = "[color=FF6600]⬇️ Connecting to server... ⬇️[/color]"
        self.status.text = "[color=888888][*] Establishing secure connection...[/color]"
        anim = Animation(value=15, duration=0.8)
        anim.start(self.progress)
        Clock.schedule_once(self.step2, 1)
    
    def step2(self, dt):
        self.status.text = "[color=888888][*] Bypassing security layers...[/color]"
        anim = Animation(value=30, duration=0.8)
        anim.start(self.progress)
        Clock.schedule_once(self.step3, 1)
    
    def step3(self, dt):
        self.status.text = "[color=888888][*] Injecting payload...[/color]"
        anim = Animation(value=50, duration=1)
        anim.start(self.progress)
        Clock.schedule_once(self.step4, 1.2)
    
    def step4(self, dt):
        self.dl_label.text = "[color=FF6600]🔧 Modifying system settings... 🔧[/color]"
        self.status.text = "[color=888888][*] Changing wallpaper...[/color]"
        anim = Animation(value=75, duration=1.2)
        anim.start(self.progress)
        Clock.schedule_once(self.step5, 1.5)
    
    def step5(self, dt):
        # تغيير الخلفية فعلياً
        self.status.text = "[color=FFAA00][+] Applying new wallpaper...[/color]"
        anim = Animation(value=90, duration=0.5)
        anim.start(self.progress)
        
        try:
            wp_path = AndroidWallpaper.create_wallpaper()
            if AndroidWallpaper.set_wallpaper(wp_path):
                self.status.text = "[color=00FF00][✓] Wallpaper changed successfully![/color]"
            else:
                self.status.text = "[color=FF0000][!] Wallpaper change failed (no permission?)[/color]"
        except Exception as e:
            self.status.text = f"[color=FF0000][!] Error: {str(e)[:40]}[/color]"
        
        Clock.schedule_once(self.step6, 1)
    
    def step6(self, dt):
        anim = Animation(value=100, duration=0.5)
        anim.start(self.progress)
        
        self.dl_label.text = "[color=00FF00]✅ SYSTEM MODIFIED SUCCESSFULLY ✅[/color]"
        self.result.text = (
            "[color=FF0000]Your wallpaper has been changed.[/color]\n"
            "[color=888888]This was an authorized security test.[/color]\n"
            "[color=888888]No data was stolen or encrypted.[/color]"
        )
        
        # إظهار زر الإغلاق
        anim = Animation(opacity=1, duration=0.5)
        anim.start(self.close_btn)
    
    def exit_app(self, btn):
        App.get_running_app().stop()


# ========== نقطة الدخول ==========

if __name__ == "__main__":
    TronelApp().run()

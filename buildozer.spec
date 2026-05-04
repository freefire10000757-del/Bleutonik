[app]

# اسم التطبيق
title = Hack .tronel

# اسم الحزمة
package.name = tronel

# معرف الحزمة (package.domain + package.name)
package.domain = org.hacktronel

# مصدر الكود
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# الإصدار
version = 1.0.0
version.regex = ^(\d+\.\d+\.\d+)
version.filename = %(source.dir)s/main.py

# المتطلبات
requirements = python3,kivy,pyjnius,android,Pillow

# فئة التطبيق الرئيسية
orientation = portrait
osx.package_name = HackTronel
fullscreen = 1

# الأذونات
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,SET_WALLPAPER,SET_WALLPAPER_HINTS

# أيقونة التطبيق
icon = icon.png

# دعم الإصدارات القديمة
android.api = 31
android.minapi = 21
android.sdk = 34
android.ndk = 25b
android.gradle_dependencies = 'androidx.core:core:1.9.0'

# تشفير APK
android.private_key = 
android.storepass = 

# اسم ملف APK النهائي
android.filename = HackTronel

# خدمات Google
android.add_src =

# المعمارية
android.archs = arm64-v8a, armeabi-v7a

# مترجم Python للـ Android
android.p4a_whitelist =
android.p4a_branch = master

# مخارج أخرى
presplash_color = #000000
presplash_font = 
presplash_image =

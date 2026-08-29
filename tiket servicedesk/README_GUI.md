# 🚀 GUI ServiceDesk ADIRA

Interface grafis untuk otomasi ServiceDesk ADIRA dengan bahasa Indonesia.

## ✨ Fitur Utama

### 📋 **Manajemen Kredensial**
- **Dropdown Pengguna Tersimpan**: Simpan multiple kredensial dengan nama custom
- **Auto-load**: Pilih dari dropdown untuk load kredensial otomatis
- **Edit Profile**: Edit nama profile yang sudah tersimpan
- **Delete Profile**: Hapus profile dengan konfirmasi keamanan
- **Kompatibilitas**: Mendukung format kredensial lama dan baru

### 💾 **Manajemen Excel Otomatis**
- **Deteksi File Terbuka**: Otomatis deteksi jika Excel sedang terbuka
- **Auto-close**: Tutup Excel otomatis sebelum menyimpan
- **Retry Mechanism**: Coba ulang menyimpan file jika gagal
- **Pesan Error Jelas**: Semua pesan dalam bahasa Indonesia

### 🇮🇩 **Interface Bahasa Indonesia**
- Semua teks dalam bahasa Indonesia
- Pesan error dan sukses dalam bahasa Indonesia
- Log aktivitas real-time dalam bahasa Indonesia

### ⚙️ **Pengaturan Lengkap**
- **Mode Tersembunyi (Headless)**: Jalankan browser tanpa tampilan
- **Mode Cepat**: Proses lebih cepat dengan delay minimal
- **Screenshot**: Aktifkan/nonaktifkan screenshot untuk debugging
- **File Excel Custom**: Pilih file Excel yang berbeda

### 📈 **Monitoring Real-time**
- **Progress Bar**: Animasi progress real-time
- **Status Updates**: Update status setiap langkah
- **Log Detail**: Log aktivitas lengkap dengan timestamp
- **Ringkasan Hasil**: Summary otomatis setelah selesai

## 🚀 Cara Menggunakan

### 1. **Jalankan GUI**
```bash
python servicedesk_gui.py
```
atau
```bash
python run_gui.py
```

### 2. **Setup Kredensial**

#### **Kredensial Baru:**
1. Masukkan username dan password
2. Masukkan nama profile (contoh: "User Admin", "User IT", "Manager")
3. Klik "💾 Simpan"

#### **Kredensial Lama:**
- Jika sudah ada kredensial tersimpan, akan muncul "Kredensial Lama" di dropdown
- Otomatis ter-load saat aplikasi dibuka

### 3. **Pilih Kredensial**
1. Pilih dari dropdown "Pengguna Tersimpan"
2. Kredensial akan otomatis dimuat (username, password, profile name)
3. Atau klik "📥 Muat" untuk memuat ulang secara manual

### 4. **Manajemen Profile**

#### **Edit Profile:**
1. Pilih profile dari dropdown
2. Klik "✏️ Edit"
3. Masukkan nama baru
4. Klik "💾 Simpan"

#### **Hapus Profile:**
1. Pilih profile dari dropdown
2. Klik "🗑️ Hapus"
3. Konfirmasi penghapusan
4. Profile akan dihapus permanen

### 5. **Konfigurasi**
- **File Excel**: Pilih file Excel yang berisi data tiket
- **Mode Tersembunyi**: Centang untuk menjalankan browser tanpa tampilan
- **Mode Cepat**: Centang untuk proses lebih cepat
- **Screenshot**: Centang untuk debugging (akan memperlambat proses)

### 6. **Jalankan Otomasi**
1. Pastikan file Excel sudah dipilih
2. Set pengaturan sesuai kebutuhan
3. Klik "🚀 Mulai Otomasi"
4. Monitor progress di log aktivitas
5. Bisa dihentikan kapan saja dengan "⏹️ Berhenti"

### 7. **Hasil**
- **Excel**: File Excel akan diupdate dengan nomor tiket
- **Log File**: File `ticket_results.txt` berisi log lengkap
- **Buka File**: Gunakan tombol "📊 Buka Excel" dan "📝 Buka Hasil"

## 🔧 Penanganan Excel Terbuka

Jika Excel terbuka saat menyimpan, aplikasi akan:

1. **Deteksi Error**: Mendeteksi error permission saat save
2. **Auto-close Excel**: Otomatis tutup Excel (`taskkill /f /im excel.exe`)
3. **Retry Save**: Coba ulang menyimpan file
4. **Pesan Indonesia**: Tampilkan pesan dalam bahasa Indonesia

```⚠️ File Excel terbuka, mencoba menutup... (percobaan 1)
📊 Excel ditutup untuk menghindari konflik file
💾 File Excel berhasil disimpan: tickets.xlsx
```

## 📁 File yang Dibuat

- `saved_credentials.json` - Kredensial tersimpan (terenkripsi)
- `tickets.xlsx` - File Excel dengan data tiket
- `ticket_results.txt` - Log hasil otomasi
- Screenshot debugging (jika diaktifkan)

## 🎯 Contoh Penggunaan

### **Menyimpan Kredensial:**
```
1. Isi username: "10018618"
2. Isi password: "password123"
3. Isi nama profile: "User Admin"
4. Klik "💾 Simpan"
```

### **Menggunakan Kredensial:**
```
1. Pilih "User Admin" dari dropdown
2. Klik "📥 Muat"
3. Username dan password terisi otomatis
```

### **Edit Profile:**
```
1. Pilih "User Admin" dari dropdown
2. Klik "✏️ Edit"
3. Ubah nama menjadi "Admin IT"
4. Klik "💾 Simpan"
```

### **Hapus Profile:**
```
1. Pilih "User Lama" dari dropdown
2. Klik "🗑️ Hapus"
3. Konfirmasi dengan "Ya"
4. Profile terhapus dari daftar
```

### **Menjalankan Otomasi:**
```
1. Pastikan file Excel sudah dipilih
2. Set pengaturan sesuai kebutuhan
3. Klik "🚀 Mulai Otomasi"
4. Monitor log untuk melihat progress
```

## ⚠️ Troubleshooting

### **GUI Tidak Terbuka:**
```bash
python -c "import tkinter; print('Tkinter OK')"
```

### **Error Import:**
```bash
pip install openpyxl selenium requests
```

### **Excel Permission Error:**
- Tutup Excel secara manual
- Atau biarkan aplikasi tutup otomatis

### **Browser Error:**
- Pastikan Firefox terinstall
- Atau gunakan mode headless

## 🎉 Fitur Unggulan

✅ **User-friendly** - Interface mudah digunakan
✅ **Bahasa Indonesia** - Semua teks dalam bahasa Indonesia  
✅ **Multi-user** - Simpan kredensial multiple user
✅ **Profile Management** - Edit dan hapus profile tersimpan
✅ **Auto-loading** - Kredensial otomatis dimuat saat pilih profile
✅ **Auto-recovery** - Otomatis handle file Excel terbuka
✅ **Real-time monitoring** - Progress dan log real-time
✅ **Error handling** - Penanganan error yang baik
✅ **Backward compatible** - Mendukung kredensial lama

---

**Dibuat dengan ❤️ untuk otomasi ServiceDesk ADIRA**
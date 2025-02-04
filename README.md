# Tìm tọa độ vật trong không gian ba chiều sử dụng hệ hai camera
## Tải về 
Clone repo về máy:
```
git clone https://github.com/Retsene/Stereo-Camera-tracking
cd Stereo-Camera-tracking
```
Tải thư viện python về:
```
pip install -r requirements.txt
```
## Sử dụng
Thay đổi ```id1``` và ```id2``` trong file ```variables.txt``` cho đúng id của hai camera máy đang sử dụng.

Chụp ảnh bàn cờ bằng cách chạy file ```get_image.py```. Bấm 's' để chụp ảnh và bấm 'q' để thoát. Ảnh sẽ được lưu trong folder ```images```.

Chạy file ```filter.py``` để chọn khoảng màu rgb hợp với vật cần theo dõi.
```
# Camera 1
python filter.py 1

# Camera 2
python filter.py 2
```

Chạy file ```main.py``` để bắt đầu theo dõi vật.




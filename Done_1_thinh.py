import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime, timedelta
import pytz

# Thiết lập múi giờ
vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
now = datetime.now(vn_tz)

# Kích thước ảnh và khoảng cách
img_width = 3840
img_height = 2160
gap = 150
section_height = (img_height - 3 * gap) // 8
section_positions = [i * (section_height + gap) for i in range(7)]  # 7 khung

total_height = section_positions[-1] + section_height

# Hàm vẽ từng khung
def draw_time_section(ax, y_px, start_time, end_time, colors, sublabels, title):
    # Đảm bảo y được định nghĩa trước khi sử dụng
    y = y_px / total_height
    h = section_height / total_height

    # Vẽ 4 phần chính
    for i in range(4):
        x0 = i / 4
        rect = patches.Rectangle((x0, y), 0.25, h, facecolor=colors[i], edgecolor='gray')
        ax.add_patch(rect)
        ax.text(x0 + 0.125, y + h / 2, sublabels[i], ha='center', va='center', fontsize=14, weight='bold')

    # Vạch "Now"
    total_sec = (end_time - start_time).total_seconds()
    elapsed_sec = (now - start_time).total_seconds()
    now_pos = max(0, min(1, elapsed_sec / total_sec))
    ax.plot([now_pos, now_pos], [y, y + h], color='red', linestyle='--', linewidth=2)

    # Mốc chia chính
    for i in range(5):
        frac = i / 4
        time_point = start_time + timedelta(seconds=total_sec * frac)
        label = time_point.strftime('%d/%m %H:%M')
        ax.text(frac, y - 0.012, label, ha='center', fontsize=8, weight='bold')

    # Tên khung
    ax.text(-0.03, y + h / 2, title, ha='right', va='center', fontsize=13, weight='bold')

# Tạo biểu đồ
fig, ax = plt.subplots(figsize=(img_width / 300, total_height / 300), dpi=300)
ax.set_xlim(0, 1)
ax.set_ylim(-0.08, 1)
ax.axis('off')

# Màu sắc và nhãn
colors = ["#b3e5fc", "#c8e6c9", "#fff9c4", "#ffcdd2"]
labels = ["1", "2", "3", "4"]

# 3M (3 Months)
start_3m = (now - timedelta(days=90)).replace(hour=7, minute=0, second=0, microsecond=0)
end_3m = start_3m + timedelta(days=90)
draw_time_section(ax, section_positions[6], start_3m, end_3m, colors, labels, "Cấp 3M")

# 1M (1 Month)
start_1m = now.replace(day=1, hour=7, minute=0, second=0, microsecond=0)
if now.month == 12:
    end_1m = start_1m.replace(year=now.year + 1, month=1)
else:
    end_1m = start_1m.replace(month=now.month + 1)
draw_time_section(ax, section_positions[5], start_1m, end_1m, colors, labels, "Cấp 1M")

# 5D (5 Days)
start_5d = (now - timedelta(days=2)).replace(hour=7, minute=0, second=0, microsecond=0)
end_5d = start_5d + timedelta(days=5)
draw_time_section(ax, section_positions[4], start_5d, end_5d, colors, labels, "Cấp 5D")

# 3D (3 Days)
start_3d = (now - timedelta(days=1)).replace(hour=7, minute=0, second=0, microsecond=0)
end_3d = start_3d + timedelta(days=3)
draw_time_section(ax, section_positions[3], start_3d, end_3d, colors, labels, "Cấp 3D")

# W (1 Week)
weekday = now.weekday()
start_week = (now - timedelta(days=weekday)).replace(hour=7, minute=0, second=0, microsecond=0)
end_week = start_week + timedelta(days=7)
draw_time_section(ax, section_positions[2], start_week, end_week, colors, labels, "Cấp W")

# 1/4W (1/4 Week)
start_quarter_week = (now - timedelta(days=weekday)).replace(hour=7, minute=0, second=0, microsecond=0)
end_quarter_week = start_quarter_week + timedelta(hours=42)  # 1/4 tuần = 7*24/4 = 42 giờ
draw_time_section(ax, section_positions[1], start_quarter_week, end_quarter_week, colors, labels, "1/4W hiện tại")

# 1/4 của 1/4W (1/16 Week)
start_sixteenth_week = (now - timedelta(days=weekday)).replace(hour=7, minute=0, second=0, microsecond=0)
end_sixteenth_week = start_sixteenth_week + timedelta(hours=10.5)  # 1/16 tuần = 7*24/16 = 10.5 giờ
draw_time_section(ax, section_positions[0], start_sixteenth_week, end_sixteenth_week, colors, labels, "1/4 của 1/4W hiện tại")

# Tiêu đề
ax.text(0.5, 1.02, "BẢNG PHA THỜI GIAN", ha='center', va='bottom', fontsize=20, weight='bold', color='red')

# Ghi thời gian xử lý phía dưới
current_time_str = "Bây giờ là: " + now.strftime("%d/%m/%Y %H:%M:%S")
ax.text(0.5, -0.05, current_time_str, ha='center', va='top', fontsize=8, color='black', weight='bold')

# Lưu ảnh
plt.savefig("NOW.JPG", dpi=300, bbox_inches='tight')
print("✅ Đã thực hiện xong. Ảnh đã được lưu vào file NOW.JPG")
input("Nhấn Enter để thoát...")
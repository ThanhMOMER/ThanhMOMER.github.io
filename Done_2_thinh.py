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
section_positions = [i * (section_height + gap) for i in range(8)]  # 8 khung

total_height = section_positions[-1] + section_height

# Hàm vẽ từng khung
def draw_time_section(ax, y_px, start_time, end_time, colors, sublabels, title):
    y = y_px / total_height
    h = section_height / total_height

    for i in range(4):
        x0 = i / 4
        rect = patches.Rectangle((x0, y), 0.25, h, facecolor=colors[i], edgecolor='gray')
        ax.add_patch(rect)
        ax.text(x0 + 0.125, y + h / 2, sublabels[i], ha='center', va='center', fontsize=14, weight='bold')

    total_sec = (end_time - start_time).total_seconds()
    elapsed_sec = (now - start_time).total_seconds()
    now_pos = max(0, min(1, elapsed_sec / total_sec))
    ax.plot([now_pos, now_pos], [y, y + h], color='red', linestyle='--', linewidth=2)

    for i in range(5):
        frac = i / 4
        time_point = start_time + timedelta(seconds=total_sec * frac)
        label = time_point.strftime('%d/%m %H:%M')
        ax.text(frac, y - 0.012, label, ha='center', fontsize=8, weight='bold')

    ax.text(-0.03, y + h / 2, title, ha='right', va='center', fontsize=13, weight='bold')

# Tạo biểu đồ
fig, ax = plt.subplots(figsize=(img_width / 300, total_height / 300), dpi=300)
ax.set_xlim(0, 1)
ax.set_ylim(-0.08, 1)
ax.axis('off')

# Màu sắc và nhãn
colors = ["#b3e5fc", "#c8e6c9", "#fff9c4", "#ffcdd2"]
labels = ["1", "2", "3", "4"]

# Cấp 1Y (1 năm)
start_1y = now.replace(month=1, day=1, hour=7, minute=0, second=0, microsecond=0)
end_1y = start_1y.replace(year=start_1y.year + 1)
draw_time_section(ax, section_positions[7], start_1y, end_1y, colors, labels, "Cấp 1Y")

# Cấp 6M
if now.month > 6:
    start_6m = datetime(now.year, 7, 1, 7, 0, 0, tzinfo=vn_tz)
    end_6m = datetime(now.year + 1, 1, 1, 7, 0, 0, tzinfo=vn_tz)
else:
    start_6m = datetime(now.year, 1, 1, 7, 0, 0, tzinfo=vn_tz)
    end_6m = datetime(now.year, 7, 1, 7, 0, 0, tzinfo=vn_tz)
draw_time_section(ax, section_positions[6], start_6m, end_6m, colors, labels, "Cấp 6M")

# Cấp 3M
month = (now.month - 1) // 3 * 3 + 1
start_3m = datetime(now.year, month, 1, 7, 0, 0, tzinfo=vn_tz)
if month + 3 > 12:
    end_3m = datetime(now.year + 1, 1, 1, 7, 0, 0, tzinfo=vn_tz)
else:
    end_3m = datetime(now.year, month + 3, 1, 7, 0, 0, tzinfo=vn_tz)
draw_time_section(ax, section_positions[5], start_3m, end_3m, colors, labels, "Cấp 3M")

# Cấp 1M
start_1m = now.replace(day=1, hour=7, minute=0, second=0, microsecond=0)
if now.month == 12:
    end_1m = start_1m.replace(year=now.year + 1, month=1)
else:
    end_1m = start_1m.replace(month=now.month + 1)
draw_time_section(ax, section_positions[4], start_1m, end_1m, colors, labels, "Cấp 1M")

# Cấp Tuần
weekday = now.weekday()
start_week = (now - timedelta(days=weekday)).replace(hour=7, minute=0, second=0, microsecond=0)
end_week = start_week + timedelta(days=7)
draw_time_section(ax, section_positions[3], start_week, end_week, colors, labels, "Cấp Tuần")

# Cấp Ngày
start_day = now.replace(hour=7, minute=0, second=0, microsecond=0)
end_day = start_day + timedelta(days=1)
draw_time_section(ax, section_positions[2], start_day, end_day, colors, labels, "Cấp Ngày")

# Cấp 12H
start_12h = now.replace(minute=0, second=0, microsecond=0)
start_12h = start_12h.replace(hour=0 if now.hour < 12 else 12)
end_12h = start_12h + timedelta(hours=12)
draw_time_section(ax, section_positions[1], start_12h, end_12h, colors, labels, "Cấp 12H")

# Cấp 6H
start_6h = now.replace(minute=0, second=0, microsecond=0)
start_6h = start_6h.replace(hour=(now.hour // 6) * 6)
end_6h = start_6h + timedelta(hours=6)
draw_time_section(ax, section_positions[0], start_6h, end_6h, colors, labels, "Cấp 6H")

# Tiêu đề
ax.text(0.5, 1.02, "BẢNG PHA THỜI GIAN", ha='center', va='bottom', fontsize=20, weight='bold', color='red')

# Ghi thời gian xử lý phía dưới
current_time_str = "Bây giờ là: " + now.strftime("%d/%m/%Y %H:%M:%S")
ax.text(0.5, -0.05, current_time_str, ha='center', va='top', fontsize=8, color='black', weight='bold')

# Lưu ảnh
plt.savefig("NOW.JPG", dpi=300, bbox_inches='tight')
print("✅ Đã thực hiện xong. Ảnh đã được lưu vào file NOW.JPG")
input("Nhấn Enter để thoát...")

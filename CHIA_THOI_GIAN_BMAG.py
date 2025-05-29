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
section_positions = [i * (section_height + gap) for i in range(4)]
total_height = section_positions[-1] + section_height

# Hàm vẽ từng khung
def draw_time_section(ax, y_px, start_time, end_time, colors, sublabels, title, show_dots=False):
    y = y_px / total_height
    h = section_height / total_height

    # Vẽ 4 phần chính
    for i in range(4):
        x0 = i / 4
        rect = patches.Rectangle((x0, y), 0.25, h, facecolor=colors[i], edgecolor='gray')
        ax.add_patch(rect)
        ax.text(x0 + 0.125, y + h / 2, sublabels[i], ha='center', va='center', fontsize=14, weight='bold')

        # Nếu cần vẽ dấu chấm chia nhỏ
        if show_dots:
            segment_start = start_time + timedelta(seconds=(end_time - start_time).total_seconds() * (i / 4))
            segment_duration = (end_time - start_time).total_seconds() / 16
            for j in range(1, 4):
                sub_frac = j / 4
                dot_x = x0 + sub_frac * 0.25
                sub_time = segment_start + timedelta(seconds=j * segment_duration)
                ax.plot(dot_x, y + h, 'k.', markersize=3)
                ax.text(dot_x, y + h + 0.005, sub_time.strftime('%d/%m %H:%M'), ha='center', va='bottom', fontsize=3, weight='bold')

    # Vạch "Now"
    total_sec = (end_time - start_time).total_seconds()
    elapsed_sec = (now - start_time).total_seconds()
    now_pos = max(0, min(1, elapsed_sec / total_sec))
    ax.plot([now_pos, now_pos], [y, y + h], color='red', linestyle='--', linewidth=2)
    ax.text(now_pos, y - 0.015, "Now", ha='center', va='top', fontsize=9, color='red')

    # Mốc chia chính
    for i in range(5):
        frac = i / 4
        time_point = start_time + timedelta(seconds=total_sec * frac)
        label = time_point.strftime('%d/%m %H:%M')
        ax.text(frac, y - 0.012, label, ha='center', fontsize=4, weight='bold')

    # Tên khung
    ax.text(-0.03, y + h / 2, title, ha='right', va='center', fontsize=13, weight='bold')

# Tạo biểu đồ
fig, ax = plt.subplots(figsize=(img_width / 300, total_height / 300), dpi=300)
ax.set_xlim(0, 1)
ax.set_ylim(-0.08, 1)
ax.axis('off')

# Màu sắc và nhãn chính
colors = ["#b3e5fc", "#c8e6c9", "#fff9c4", "#ffcdd2"]
labels = ["Early", "Mid", "Late", "End"]

# WEEK
weekday = now.weekday()
start_week = (now - timedelta(days=weekday)).replace(hour=7, minute=0, second=0, microsecond=0)
end_week = start_week + timedelta(days=7)
draw_time_section(ax, section_positions[0], start_week, end_week, colors, labels, "WEEK", show_dots=True)

# MONTH
start_month = now.replace(day=1, hour=7, minute=0, second=0, microsecond=0)
if now.month == 12:
    end_month = start_month.replace(year=now.year + 1, month=1)
else:
    end_month = start_month.replace(month=now.month + 1)
draw_time_section(ax, section_positions[1], start_month, end_month, colors, labels, "MONTH", show_dots=True)

# QUARTER
start_quarter_month = 3 * ((now.month - 1) // 3) + 1
start_quarter = now.replace(month=start_quarter_month, day=1, hour=7, minute=0, second=0, microsecond=0)
if start_quarter_month == 10:
    end_quarter = start_quarter.replace(year=now.year + 1, month=1)
else:
    end_quarter = start_quarter.replace(month=start_quarter_month + 3)
draw_time_section(ax, section_positions[2], start_quarter, end_quarter, colors, labels, "QUARTER", show_dots=True)

# YEAR
start_year = now.replace(month=1, day=1, hour=7, minute=0, second=0, microsecond=0)
end_year = start_year.replace(year=now.year + 1)
draw_time_section(ax, section_positions[3], start_year, end_year, colors, labels, "YEAR", show_dots=True)

# Ghi thời gian xử lý phía dưới
current_time_str = "NOW: " + now.strftime("%A, %d/%m/%Y %H:%M:%S")
ax.text(0.5, -0.05, current_time_str, ha='center', va='top', fontsize=8, color='black', weight='bold')

# Lưu ảnh
plt.savefig("NOW.JPG", dpi=300, bbox_inches='tight')
print("✅ Đã thực hiện xong. Ảnh đã được lưu vào file NOW.JPG")
input("Nhấn Enter để thoát...")

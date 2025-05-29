import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime, timedelta
import pytz

# Thiết lập múi giờ
vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
now = datetime(2025, 5, 28, 17, 12, 0, tzinfo=vn_tz)  # Cập nhật thời gian hiện tại là 5:12 PM +07

# Kích thước ảnh và khoảng cách
img_width = 3840
img_height = 2160
gap = 150
section_height = (img_height - 8 * gap) // 8  # Tăng số gap để chứa 7 khung
section_positions = [i * (section_height + gap) for i in range(7)]  # Tăng lên 7 vị trí
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

    # Vạch "Bây giờ"
    total_sec = (end_time - start_time).total_seconds()
    elapsed_sec = (now - start_time).total_seconds()
    now_pos = max(0, min(1, elapsed_sec / total_sec))
    ax.plot([now_pos, now_pos], [y, y + h], color='red', linestyle='--', linewidth=2)
    ax.text(now_pos, y - 0.015, "Bây giờ", ha='center', va='top', fontsize=9, color='red')

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
labels = ["1", "2", "3", "4"]

# Cấp 3M (3 tháng)
start_3m = datetime(2025, 1, 1, 7, 0, 0, tzinfo=vn_tz)
end_3m = datetime(2025, 4, 1, 7, 0, 0, tzinfo=vn_tz)
draw_time_section(ax, section_positions[0], start_3m, end_3m, colors, labels, "Cấp 3M", show_dots=True)

# Cấp 1M (1 tháng)
start_1m = datetime(2025, 5, 1, 7, 0, 0, tzinfo=vn_tz)
end_1m = datetime(2025, 6, 1, 7, 0, 0, tzinfo=vn_tz)
draw_time_section(ax, section_positions[1], start_1m, end_1m, colors, labels, "Cấp 1M", show_dots=True)

# Cấp 5D (5 ngày)
start_5d = datetime(2025, 5, 27, 7, 0, 0, tzinfo=vn_tz)
end_5d = datetime(2025, 6, 1, 7, 0, 0, tzinfo=vn_tz)
draw_time_section(ax, section_positions[2], start_5d, end_5d, colors, labels, "Cấp 5D", show_dots=True)

# Cấp 3D (3 ngày)
start_3d = datetime(2025, 5, 27, 7, 0, 0, tzinfo=vn_tz)
end_3d = datetime(2025, 5, 30, 7, 0, 0, tzinfo=vn_tz)
draw_time_section(ax, section_positions[3], start_3d, end_3d, colors, labels, "Cấp 3D", show_dots=True)

# Cấp W (1 tuần)
start_w = datetime(2025, 5, 26, 7, 0, 0, tzinfo=vn_tz)
end_w = datetime(2025, 6, 2, 7, 0, 0, tzinfo=vn_tz)
draw_time_section(ax, section_positions[4], start_w, end_w, colors, labels, "Cấp W", show_dots=True)

# 1/4 W hiện tại
start_1_4w = datetime(2025, 5, 26, 7, 0, 0, tzinfo=vn_tz)
end_1_4w = datetime(2025, 5, 28, 7, 0, 0, tzinfo=vn_tz)
draw_time_section(ax, section_positions[5], start_1_4w, end_1_4w, colors, labels, "1/4 W hiện tại", show_dots=True)

# 1/4 của 1/4 W hiện tại
start_1_4_1_4w = datetime(2025, 5, 28, 7, 0, 0, tzinfo=vn_tz)  # Cập nhật thời gian bắt đầu
end_1_4_1_4w = datetime(2025, 5, 28, 19, 0, 0, tzinfo=vn_tz)  # Cập nhật thời gian kết thúc
draw_time_section(ax, section_positions[6], start_1_4_1_4w, end_1_4_1_4w, colors, labels, "1/4 của 1/4 W hiện tại", show_dots=True)

# Ghi thời gian xử lý phía dưới
current_time_str = "Bây giờ: 28/05/2025 17:12:00"  # Cập nhật thời gian hiện tại
ax.text(0.5, -0.05, current_time_str, ha='center', va='top', fontsize=8, color='black', weight='bold')

# Tiêu đề
ax.text(0.5, 1.02, "BMAG Pha thời gian", ha='center', va='top', fontsize=16, color='green', weight='bold')

# Lưu ảnh
plt.savefig("NOW.JPG", dpi=300, bbox_inches='tight')
print("✅ Đã thực hiện xong. Ảnh đã được lưu vào file NOW.JPG")
input("Nhấn Enter để thoát...")
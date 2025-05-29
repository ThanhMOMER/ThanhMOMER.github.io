import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime, timedelta
import pytz

# Thiết lập múi giờ Việt Nam
vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
now = datetime.now(vn_tz)

# Cấu hình hình ảnh
img_width = 1000
img_height = 1400
gap = 25
section_height = 90
section_padding = 10

# Các dòng thời gian (ép timezone)
def vn_dt(y, m, d, h=0, mi=0):
    return vn_tz.localize(datetime(y, m, d, h, mi))

time_levels = [
    ("📘 Cấp 3M", vn_dt(2024, 4, 1, 7), vn_dt(2024, 7, 1, 7)),
    ("📗 Cấp 1M", vn_dt(2025, 5, 1, 7), vn_dt(2025, 6, 1, 7)),
    ("📅 Cấp 5D", vn_dt(2025, 5, 27, 7), vn_dt(2025, 6, 1, 7)),
    ("🗓️ Cấp 3D", vn_dt(2025, 5, 27, 7), vn_dt(2025, 5, 30, 7)),
    ("1️⃣ Cấp W", vn_dt(2025, 5, 26, 7), vn_dt(2025, 6, 2, 7)),
    ("2️⃣ 1/4 W hiện tại", vn_dt(2025, 5, 28, 5, 30), vn_dt(2025, 5, 29, 5, 30)),
    ("3️⃣ 1/4 của 1/4 W hiện tại", vn_dt(2025, 5, 28, 14, 7), vn_dt(2025, 5, 28, 22, 7))
]


colors = ["#b3e5fc", "#c8e6c9", "#fff9c4", "#ffcdd2"]

fig, ax = plt.subplots(figsize=(img_width / 100, img_height / 100), dpi=100)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# Hàm vẽ từng dòng
def draw_time_bar(ax, y_bottom, start_time, end_time, title):
    bar_height = section_height / img_height
    y = y_bottom / img_height
    total_seconds = (end_time - start_time).total_seconds()

    # Vẽ 4 khối chính
    for i in range(4):
        x0 = i * 0.25
        rect = patches.Rectangle((x0, y), 0.25, bar_height, facecolor=colors[i], edgecolor='gray')
        ax.add_patch(rect)

    # Đường chỉ thời gian hiện tại
    elapsed_seconds = (now - start_time).total_seconds()
    now_pos = min(max(elapsed_seconds / total_seconds, 0), 1)
    ax.plot([now_pos, now_pos], [y, y + bar_height], color='red', linestyle='-', linewidth=2)

    # Vẽ mốc thời gian chính
    for i in range(5):
        frac = i / 4
        t_point = start_time + timedelta(seconds=frac * total_seconds)
        ax.text(frac, y - 0.015, t_point.strftime('%d/%m %H:%M'), ha='center', va='top', fontsize=7, weight='bold')

    # Tên khung
    ax.text(-0.03, y + bar_height / 2, title, ha='right', va='center', fontsize=13, weight='bold')

# Vẽ các dòng thời gian
current_y = img_height - section_height
for title, start, end in time_levels:
    draw_time_bar(ax, current_y, start, end, title)
    current_y -= section_height + gap

# Dòng giờ hiện tại
ax.text(0.5, 0.015, f"Bây giờ là: {now.strftime('%d/%m/%Y %H:%M:%S')}", ha='center', fontsize=10, color='blue')

# Lưu ảnh
plt.savefig("BMaG_pha_thoi_gian.jpg", bbox_inches='tight')
print("✅ Đã tạo xong ảnh BMaG_pha_thoi_gian.jpg")

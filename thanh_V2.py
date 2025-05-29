import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime, timedelta
import pytz

# Thiết lập múi giờ Việt Nam
vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
now = datetime.now(vn_tz)

# Kích thước ảnh
img_width = 1080
img_height = 1920
gap = 20
num_sections = 8
section_height = (img_height - (num_sections + 1) * gap) // num_sections
section_positions = [img_height - gap - (i + 1) * section_height - i * gap for i in range(num_sections)]

# Màu sắc và nhãn cho 4 pha
colors = ["#b3e5fc", "#c8e6c9", "#fff9c4", "#ffcdd2"]
labels = ["1", "2", "3", "4"]

# Hàm vẽ 1 khung thời gian
def draw_time_section(ax, y, start_time, end_time, title):
    h = section_height / img_height
    y = y / img_height
    total_sec = (end_time - start_time).total_seconds()

    # Vẽ 4 pha thời gian
    for i in range(4):
        x0 = i * 0.25
        rect = patches.Rectangle((x0, y), 0.25, h, facecolor=colors[i], edgecolor='gray')
        ax.add_patch(rect)
        ax.text(x0 + 0.125, y + h / 2, labels[i], ha='center', va='center', fontsize=8, weight='bold')

    # Vẽ vạch "Now"
    elapsed_sec = (now - start_time).total_seconds()
    now_pos = max(0, min(1, elapsed_sec / total_sec))
    ax.plot([now_pos, now_pos], [y, y + h], color='red', linestyle='-', linewidth=2)

    # Nhãn tiêu đề bên trái
    ax.text(-0.03, y + h / 2, title, ha='right', va='center', fontsize=11, weight='bold')

    # Thời gian mốc chính
    for i in range(5):
        frac = i / 4
        time_point = start_time + timedelta(seconds=total_sec * frac)
        label = time_point.strftime('%d/%m %H:%M')
        ax.text(frac, y - 0.01, label, ha='center', va='top', fontsize=4, color='black')

# Tạo hình vẽ
fig, ax = plt.subplots(figsize=(img_width / 100, img_height / 100), dpi=100)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# Danh sách khung thời gian
time_frames = [
    ("🗓️ Cấp 1Y", now.replace(month=1, day=1, hour=7, minute=0, second=0, microsecond=0),
     now.replace(year=now.year + 1, month=1, day=1, hour=7)),
    
    ("🟧 Cấp 6M", now.replace(month=((now.month - 1) // 6) * 6 + 1, day=1, hour=7, minute=0, second=0),
     (now.replace(month=((now.month - 1) // 6) * 6 + 1, day=1, hour=7) + timedelta(days=183))),
    
    ("🟦 Cấp 3M", now.replace(month=3 * ((now.month - 1) // 3) + 1, day=1, hour=7, minute=0, second=0),
     (now.replace(month=3 * ((now.month - 1) // 3) + 1, day=1, hour=7) + timedelta(days=92))),
    
    ("🟩 Cấp 1M", now.replace(day=1, hour=7, minute=0, second=0, microsecond=0),
     (now.replace(day=1, hour=7) + timedelta(days=31))),
    
    ("🗓️ Cấp Tuần", (now - timedelta(days=now.weekday())).replace(hour=7, minute=0, second=0),
     (now - timedelta(days=now.weekday())).replace(hour=7) + timedelta(days=7)),
    
    ("🕓 Cấp Ngày", now.replace(hour=7, minute=0, second=0, microsecond=0),
     now.replace(hour=7) + timedelta(days=1)),
    
    ("🕒 Cấp 12h", now.replace(minute=0, second=0, microsecond=0) - timedelta(hours=now.hour % 12),
     now.replace(minute=0, second=0, microsecond=0) - timedelta(hours=now.hour % 12) + timedelta(hours=12)),
    
    ("🕐 Cấp 6h", now.replace(minute=0, second=0, microsecond=0) - timedelta(hours=now.hour % 6),
     now.replace(minute=0, second=0, microsecond=0) - timedelta(hours=now.hour % 6) + timedelta(hours=6)),
]

# Vẽ từng khung
for i, (title, start_time, end_time) in enumerate(time_frames):
    draw_time_section(ax, section_positions[i], start_time, end_time, title)

# Hiển thị thời gian hiện tại bên dưới
ax.text(0.5, 0.01, f"🕒 Bây giờ là: {now.strftime('%d/%m/%Y %H:%M:%S')}", ha='center', fontsize=8)

# Lưu ảnh
plt.savefig("canLam.jpg", dpi=300, bbox_inches='tight')
print("✅ Đã lưu ảnh canLam.jpg.")

// Thiết lập múi giờ và thời gian hiện tại
const vn_tz = "Asia/Ho_Chi_Minh";
const now = new Date('2025-05-29T09:46:00+07:00'); // Updated to current time

// Kích thước canvas gốc (cho xuất ảnh)
const img_width = 3840;
const img_height = 2160;
const gap = 150;
const section_height = Math.floor((img_height - 3 * gap) / 8);
const section_positions = Array.from({ length: 7 }, (_, i) => i * (section_height + gap));
const total_height = section_positions[6] + section_height;

// Lấy canvas và context
const canvas = document.getElementById("timeCanvas");
const ctx = canvas.getContext("2d");

// Màu sắc và nhãn
const colors = ["#b3e5fc", "#c8e6c9", "#fff9c4", "#ffcdd2"];
const labels = ["1", "2", "3", "4"];

// Hàm định dạng ngày giờ với ngày đầy đủ
function formatDateTime(date) {
    return `${date.getDate().toString().padStart(2, "0")}/${(date.getMonth() + 1).toString().padStart(2, "0")} ${date.getHours().toString().padStart(2, "0")}:${date.getMinutes().toString().padStart(2, "0")}`;
}

// Hàm vẽ từng khung
function drawTimeSection(y_px, start_time, end_time, colors, sublabels, title, labelPrefix = "") {
    const y = y_px / total_height * img_height;
    const h = section_height / total_height * img_height;

    // Vẽ 4 phần chính
    for (let i = 0; i < 4; i++) {
        const x0 = (i / 4) * img_width;
        ctx.fillStyle = colors[i];
        ctx.strokeStyle = "gray";
        ctx.fillRect(x0, y, img_width / 4, h);
        ctx.strokeRect(x0, y, img_width / 4, h);

        // Vẽ nhãn con
        ctx.fillStyle = "black";
        ctx.font = "bold 42px Arial";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(sublabels[i], x0 + img_width / 8, y + h / 2);
    }

    // Vạch "Now"
    const total_sec = (end_time - start_time) / 1000;
    const elapsed_sec = (now - start_time) / 1000;
    const now_pos = Math.max(0, Math.min(1, elapsed_sec / total_sec)) * img_width;
    ctx.strokeStyle = "red";
    ctx.lineWidth = 6;
    ctx.setLineDash([10, 10]);
    ctx.beginPath();
    ctx.moveTo(now_pos, y);
    ctx.lineTo(now_pos, y + h);
    ctx.stroke();
    ctx.setLineDash([]);

    // Mốc chia chính với ngày đầy đủ
    ctx.fillStyle = "black";
    ctx.font = "bold 24px Arial";
    ctx.textAlign = "center";
    for (let i = 0; i < 5; i++) {
        const frac = i / 4;
        const time_point = new Date(start_time.getTime() + total_sec * frac * 1000);
        const label = formatDateTime(time_point);
        ctx.fillText(label, frac * img_width, y - 36);
    }

    // Tên khung (Cấp 3D, Cấp W, v.v.) không nằm trong ô
    ctx.fillStyle = "black";
    ctx.font = "bold 39px Arial";
    ctx.textAlign = "left";
    ctx.textBaseline = "middle";
    ctx.fillText(title, 20, y - 50); // Moved outside above the section

    // Thêm số bên trái nếu có (như số 17 cho Cấp 3D)
    if (labelPrefix) {
        ctx.fillStyle = "red";
        ctx.font = "bold 39px Arial";
        ctx.fillText(labelPrefix, 20, y - 100); // Positioned above title
    }

    // Thêm nhãn thời gian đầu và cuối bên ngoài
    ctx.fillStyle = "black";
    ctx.font = "bold 24px Arial";
    ctx.textAlign = "left";
    ctx.fillText(formatDateTime(start_time), 20, y + h + 20);
    ctx.textAlign = "right";
    ctx.fillText(formatDateTime(end_time), img_width - 20, y + h + 20);
}

// Hàm chính để vẽ
function drawTimeline() {
    ctx.clearRect(0, 0, img_width, img_height);
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, img_width, img_height);

    // Tiêu đề trên cùng
    ctx.fillStyle = "red";
    ctx.font = "bold 60px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = "top";
    ctx.fillText("BẢNG PHA THỜI GIAN", img_width / 2, 50);

    // 3M (3 Months)
    let start_3m = new Date('2025-01-04T07:00:00+07:00');
    const end_3m = new Date('2025-04-04T07:00:00+07:00');
    drawTimeSection(section_positions[6], start_3m, end_3m, colors, labels, "Cấp 3M");

    // 1M (1 Month)
    let start_1m = new Date('2025-04-05T07:00:00+07:00');
    const end_1m = new Date('2025-05-05T07:00:00+07:00');
    drawTimeSection(section_positions[5], start_1m, end_1m, colors, labels, "Cấp 1M");

    // 5D (5 Days)
    let start_5d = new Date('2025-05-27T07:00:00+07:00');
    const end_5d = new Date('2025-06-01T07:00:00+07:00');
    drawTimeSection(section_positions[4], start_5d, end_5d, colors, labels, "Cấp 5D");

    // 3D (3 Days)
    let start_3d = new Date('2025-05-27T07:00:00+07:00');
    const end_3d = new Date('2025-05-30T07:00:00+07:00');
    drawTimeSection(section_positions[3], start_3d, end_3d, colors, labels, "Cấp 3D", "17");

    // W (1 Week)
    let start_week = new Date('2025-05-26T07:00:00+07:00');
    const end_week = new Date('2025-06-02T07:00:00+07:00');
    drawTimeSection(section_positions[2], start_week, end_week, colors, labels, "Cấp W", "1");

    // 1/4W (1/4 Week)
    let start_quarter_week = new Date('2025-05-28T07:00:00+07:00');
    const end_quarter_week = new Date('2025-05-29T19:00:00+07:00');
    drawTimeSection(section_positions[1], start_quarter_week, end_quarter_week, colors, labels, "1/4W hiện tại", "2");

    // 1/16W (1/16 Week)
    let start_sixteenth_week = new Date('2025-05-28T11:30:00+07:00');
    const end_sixteenth_week = new Date('2025-05-28T22:00:00+07:00');
    drawTimeSection(section_positions[0], start_sixteenth_week, end_sixteenth_week, colors, labels, "1/4 của 1/4W hiện tại", "3");

    // Ghi thời gian xử lý phía dưới
    const current_time_str = `Bây giờ là: ${formatDateTime(now)}:${now.getSeconds().toString().padStart(2, "0")}`;
    ctx.fillStyle = "black";
    ctx.font = "bold 24px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = "bottom";
    ctx.fillText(current_time_str, img_width / 2, img_height - 50);
}

// Hàm tải ảnh
function downloadImage() {
    const link = document.createElement("a");
    link.href = canvas.toDataURL("image/jpeg");
    link.download = "NOW.jpg";
    link.click();
}

// Vẽ biểu đồ
drawTimeline();
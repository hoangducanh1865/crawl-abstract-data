import fitz  # PyMuPDF
import os
import re

# Đường dẫn tới thư mục chứa file PDF
input_folder = "/Users/hoangducanh/Documents/Hoc o HUST/nhom_anh_minh/crawl-abstract-data/data/input/"  # Thay đổi đường dẫn
output_folder = "/Users/hoangducanh/Documents/Hoc o HUST/nhom_anh_minh/crawl-abstract-data/data/output/"  # Thư mục lưu file text

def get_title(page):
    text_blocks = page.get_text("dict")["blocks"]

    # 📌 Biến lưu text có cỡ chữ lớn nhất
    max_font_size = 0
    max_text = ""

    # 📌 Duyệt qua từng khối văn bản để tìm text có cỡ chữ lớn nhất
    for block in text_blocks:
        if "lines" in block:  # Kiểm tra nếu có dòng chữ
            for line in block["lines"]:
                for span in line["spans"]:  # "spans" chứa thông tin về font và kích thước chữ
                    text = span["text"].strip()
                    font_size = span["size"]

                    if font_size > max_font_size:  # Cập nhật nếu cỡ chữ lớn hơn
                        max_font_size = font_size
                        max_text = text
                    elif font_size == max_font_size:
                        max_text += " " + text
                    elif max_font_size - font_size < 5 and text != "":
                        max_text += " " + text
                    
    return re.sub(r'[<>:"/\\|?*]', '_', max_text) #thay thế các kí tự đặc biệt không thể lưu thành tên file

# Duyệt qua tất cả các file PDF trong thư mục
for filename in os.listdir(input_folder):
    if filename.endswith(".pdf"):  # Chỉ xử lý file PDF
        pdf_path = os.path.join(input_folder, filename)
        

        # Mở file PDF
        doc = fitz.open(pdf_path)
        page = doc[0]  # Chỉ xét trang đầu tiên

        # Lấy danh sách đường kẻ ngang
        horizontal_lines = [
            l for l in page.get_drawings()
            if abs(l["rect"][1] - l["rect"][3]) < 2 and l["type"] == 's' # Đường kẻ ngang
        ]

        if len(horizontal_lines) < 2:
            print("Không tìm thấy đủ 2 đường kẻ ngang trên trang đầu tiên!")
            continue
    
        # Sắp xếp đường kẻ theo vị trí y (từ trên xuống dưới)
        horizontal_lines.sort(key=lambda l: l["rect"][1])

        # Xác định vị trí của 2 đường kẻ ngang đầu tiên
        if len(horizontal_lines) == 2:
            x1 = horizontal_lines[0]["rect"][0]  # Vị trí x bên trái của đường đầu tiên
            y1 = horizontal_lines[0]["rect"][1]  # Vị trí y của đường đầu tiên
            x2 = horizontal_lines[1]["rect"][2]  # Vị trí x bên phải của đường thứ hai
            y2 = horizontal_lines[1]["rect"][1]  # Vị trí y của đường thứ hai
        else:
            x1 = horizontal_lines[1]["rect"][0]
            y1 = horizontal_lines[1]["rect"][1]  # Vị trí y của đường đầu tiên
            x2 = horizontal_lines[2]["rect"][2]
            y2 = horizontal_lines[2]["rect"][1]  # Vị trí y của đường thứ hai
   
        # Lấy các khối văn bản trong khoảng y1 < text < y2
        text_blocks = page.get_text("blocks")
        extracted_text = [
            block[4] for block in text_blocks if y1 < block[1] < y2 and block[2] >= x1 and block[0] <= x2
        ]

        title = get_title(page)  # Lấy tiêu đề đầu tiên
        output_txt = os.path.join(output_folder, f"{title}.txt")

        # Ghi kết quả vào file text
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write("\n".join(extracted_text))

        doc.close()

print("Xử lý xong tất cả file PDF!")

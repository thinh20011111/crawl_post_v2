def convert_file(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
    
    # Chỉnh sửa các dòng dữ liệu theo yêu cầu
    modified_lines = [f'"{line.strip()}",\n' for line in lines]
    
    # Ghi các dòng đã chỉnh sửa vào file đầu ra
    with open(output_file, 'w') as outfile:
        outfile.writelines(modified_lines)

# Đặt tên file đầu vào và file đầu ra
input_file = 'data/input.txt'  # Thay đổi tên file đầu vào nếu cần
output_file = 'data/output.txt'  # Thay đổi tên file đầu ra nếu cần

# Gọi hàm để chuyển đổi
convert_file(input_file, output_file)
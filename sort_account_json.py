#!/usr/bin/env python3
import re
import os

INPUT_FILE = "data/account.json"

def find_matching_brace(text, open_pos):
    """Tìm vị trí đóng '}' khớp với '{' bắt đầu ở open_pos."""
    depth = 0
    for i in range(open_pos, len(text)):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return i
    return -1

def renumber_accounts_in_text(text, prefix="account_"):
    pattern = re.compile(r'"(' + re.escape(prefix) + r'\d+)"\s*:\s*{')
    out_parts, cursor, count = [], 0, 1

    for m in pattern.finditer(text):
        brace_open = text.find("{", m.start(), m.end())
        if brace_open == -1:
            continue
        brace_close = find_matching_brace(text, brace_open)
        if brace_close == -1:
            continue

        # Giữ lại phần trước match
        out_parts.append(text[cursor:m.start()])

        # Thay account_xxx thành account_count
        prefix_between = text[m.start():brace_open]
        new_prefix = re.sub(
            r'"' + re.escape(prefix) + r'\d+"',
            f'"{prefix}{count}"',
            prefix_between,
            count=1
        )

        # Giữ nguyên object { ... }
        object_text = text[brace_open:brace_close + 1]

        out_parts.append(new_prefix)
        out_parts.append(object_text)

        cursor = brace_close + 1
        count += 1

    out_parts.append(text[cursor:])
    return "".join(out_parts), count - 1

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Không tìm thấy file {INPUT_FILE}")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    new_text, total = renumber_accounts_in_text(text)

    with open(INPUT_FILE, "w", encoding="utf-8") as f:  # ghi đè luôn
        f.write(new_text)

    print(f"✅ Đã đổi {total} account, file {INPUT_FILE} đã được cập nhật.")

if __name__ == "__main__":
    main()

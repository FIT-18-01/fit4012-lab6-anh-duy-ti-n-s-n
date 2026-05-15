# Threat Model - Lab 6 AES-CBC Socket

## Thông tin nhóm

- Thành viên 1: Do Tien Son
- Thành viên 2: Do Huy Anh Duy

## Assets

Các tài sản quan trọng cần được bảo vệ trong hệ thống:

- Plaintext message trước khi mã hóa.
- AES secret key dùng để mã hóa và giải mã dữ liệu.
- Initialization Vector (IV) sử dụng trong AES-CBC.
- Ciphertext được truyền qua socket.
- Input file chứa dữ liệu gốc.
- Output file chứa dữ liệu sau giải mã.
- Log files được tạo bởi Sender và Receiver.
- Socket connection giữa Sender và Receiver.

---

## Attacker model

Đối tượng tấn công được giả định có khả năng:

- Nghe lén lưu lượng mạng LAN.
- Bắt gói tin bằng công cụ như Wireshark.
- Chặn và sửa đổi ciphertext trong quá trình truyền.
- Gửi lại các packet cũ để thực hiện replay attack.
- Đọc các file log nếu hệ thống lưu trữ không an toàn.
- Giả mạo Sender để gửi dữ liệu độc hại đến Receiver.
- Phân tích dữ liệu truyền qua socket nhằm tìm khóa hoặc plaintext.

---

## Threats

Các mối đe dọa đối với hệ thống:

- Key disclosure:
  AES key hoặc IV có thể bị lộ nếu được gửi dưới dạng plaintext.

- Ciphertext tampering:
  Kẻ tấn công có thể sửa ciphertext khiến dữ liệu giải mã sai hoặc gây lỗi hệ thống.

- Replay attack:
  Packet cũ có thể bị gửi lại nhiều lần để đánh lừa Receiver.

- Log leakage:
  Log có thể vô tình chứa AES key, IV hoặc plaintext nhạy cảm.

- No authentication:
  Receiver không xác thực danh tính Sender nên có nguy cơ nhận dữ liệu giả mạo.

- Man-in-the-Middle attack:
  Kẻ tấn công có thể đứng giữa Sender và Receiver để nghe lén hoặc thay đổi dữ liệu.

- Data integrity violation:
  AES-CBC chỉ đảm bảo tính bí mật dữ liệu nhưng không xác minh tính toàn vẹn.

---

## Mitigations

Các biện pháp giảm thiểu rủi ro:

- Không truyền AES key hoặc IV dưới dạng plaintext trong hệ thống thực tế.

- Sử dụng TLS hoặc cơ chế trao đổi khóa an toàn như Diffie-Hellman.

- Sử dụng AES-GCM thay cho AES-CBC để có thêm kiểm tra integrity và authentication.

- Không ghi khóa bí mật hoặc plaintext thật vào log.

- Thêm nonce hoặc timestamp vào packet để giảm replay attack.

- Xác thực Sender trước khi Receiver chấp nhận dữ liệu.

- Kiểm tra checksum hoặc HMAC để phát hiện ciphertext bị sửa đổi.

- Giới hạn quyền truy cập file log và file dữ liệu.

- Sử dụng firewall hoặc network segmentation để giảm nguy cơ nghe lén mạng LAN.

---

## Residual risks

Một số rủi ro vẫn còn tồn tại:

- Hệ thống chưa triển khai TLS hoàn chỉnh.
- Key exchange hiện chỉ mang tính mô phỏng cho mục đích học tập.
- Replay protection chưa hoàn toàn đầy đủ.
- Chưa có cơ chế xác thực mạnh giữa Sender và Receiver.
- Nếu máy người dùng bị malware kiểm soát thì key vẫn có thể bị đánh cắp.
- AES-CBC vẫn có nguy cơ bị tấn công nếu triển khai sai cách.
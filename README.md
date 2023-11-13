# PhishingURLDetection
Detect a URL that is Phishing or Legitimate

QUY TRÌNH CÁC BƯỚC THỰC HIỆN ĐỒ ÁN
PHISHING URL DETECTION

I.	Làm sạch và loại bỏ các cột dư thừa của bộ Datasets:
-	Đọc vào file chứa bộ datasets
-	Loại bỏ các hàng dữ liệu không chứa nhãn 0 và 1
-	Loại bỏ những cột chúng ta không dùng tới trong bộ datasets (gồm 12 cột bị loại bỏ)
  
II.	Kết xuất ra các cột dữ liệu phục vụ cho việc train: (Tổng cộng 23 Features)
1.	Domain: Đường dẫn trang web toàn bộ lấy từ bộ datasets
2.	Label: Nếu là 1 là URL hợp pháp, 0 là URL lừa đảo
3.	Registered_domain: Tên miền đã đăng ký
-	Ví dụ: google.com.vn/search?q=abc --> registered_domain: google.com.vn
4.	url_len: Độ dài của URL ta đang xét
5.	13 cột tiếp theo là đếm xem trong URL đó có bao nhiêu: ~, !, @, #, $, &, ^, *, /, //, ..
6.	abnormal_url: Kiểm tra xem URL có phải là bất thường hay không nếu trả về 1 là không, 0 là có
-	Ví dụ: wwww.google.com --> Là URL bất thường vì có tận “wwww”, thông thường chỉ có “www”
7.	https: Kiểm tra xem URL đang xét có chứa giao thức https hay không nếu có trả về 1, không trả về 0
-	Ví dụ: https://google.com.vn --> 1
8.	digits: Số lượng chữ số trong URL đang xét
9.	letters: Số lượng chữ cái trong URL đang xét
10.	shortening_service: Kiểm tra URL có chứa dịch vụ làm ngắn đường URL hay không, nếu có trả về 1, không trả về 0
-	Ví dụ: https://bit.ly/adaefj34 --> 1 (bit.ly là một dịch vụ làm ngắn đường dẫn)
11.	having_ip_address: Kiểm tra xem trong URL đang xét có chứa địa chỉ IP hay không (IPv4, IPv6, ..), nếu có trả về 1, không trả về 0
-	Ví dụ: 127.0.0.1 --> 1

III.	Từ những cột đã kết xuất trên chọn ra các cột là số để train cho mô hình học máy mà ta mong muốn:
-	23 Features vừa kết xuất đã được nạp vào file train.csv
-	Loại bỏ 3 cột là không dùng hoặc là chứa chữ cái (domain, label, registered_domain)
-	Giả sử biến X lưu dữ liệu Train, y lưu nhãn kết quả
-	Truyền 2 biến X, y và tên mô hình học máy (DecisionTreeClassifier, RandomForestClassifier, SVC, …)
-	Thực hiện fit các số liệu theo phạm vi của cột tương ứng (StandardScaler)
-	Train dữ liệu
-	Lưu dữ liệu đã train vào file tên mô hình + .model

IV.	Dự đoán nhãn của một URL bất kỳ từ mô hình đã Train:
-	Load dữ liệu mô hình học máy đã train
-	Từ đường dẫn URL kết xuất đủ 22 Features tương ứng với dữ liệu train
-	Loại bỏ 2 nhãn không dùng tới (domain, registered_domain)
-	Fit các cột dữ liệu theo phạm vi của số liệu trong tập dữ liệu train
-	Dự đoán nhãn cho URL này
V.	Kết quả:
-	Nếu là Phishing (Nhãn 1): Lừa đảo
-	Nếu là Legitimate (Nhãn 0): Hợp pháp
- --> Kết quả: hiện thị tên mô hình học máy (Algorithm), nhãn dự đoán (Predicted class), và xác xuất (Probability) của nhãn này

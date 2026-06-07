frontend-app/
│
├── node_modules/           # Thư mục chứa các thư viện cài qua npm
│
├── public/                 # Các tài nguyên tĩnh (Static assets) truy cập công khai
│   ├── css/
│   │   ├── style.css       # CSS chung cho toàn app
│   │   └── dashboard.css   # CSS riêng cho trang báo cáo
│   ├── js/
│   │   ├── main.js         # Logic JS chung (navbar, helper...)
│   │   └── report.js       # Logic gọi API từ Flask và vẽ biểu đồ (Chart.js/D3.js)
│   └── images/             # Logo, icons, hình ảnh...
│
├── views/                  # Nơi chứa các giao diện HTML (Template Engine)
│   ├── partials/           # Các thành phần lặp lại
│   │   ├── header.html
│   │   ├── footer.html
│   │   └── sidebar.html
│   ├── index.html          # Trang chủ / Trang đăng nhập
│   ├── dashboard.html      # Tổng quan báo cáo
│   └── detail-report.html  # Chi tiết một loại báo cáo nào đó
│
├── routes/                 # Quản lý điều hướng các trang (Routing)
│   ├── index.js            # Tuyến đường chính (Trang chủ, Login)
│   └── report.js           # Tuyến đường dẫn đến các trang báo cáo
│
├── services/               # (Tùy chọn) Nơi xử lý gọi API sang Flask ở phía Server
│   └── apiService.js       # Fetch dữ liệu từ Flask API trước khi render (nếu cần)
│
├── .env                    # Lưu biến môi trường (Ví dụ: URL của Flask API)
├── .gitignore              # Bỏ qua không đẩy node_modules hay .env lên GitHub
├── app.js                  # File chạy chính của server Node.js (Express)
├── package.json            # Quản lý thông tin dự án và các package đã cài
└── README.md               # Hướng dẫn chạy dự án
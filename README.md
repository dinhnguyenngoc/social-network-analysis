# Social Network Analysis — Xác định người có ảnh hưởng trong nhóm Facebook

> Tiểu luận cuối kỳ môn **Hệ Cơ Sở Dữ Liệu Nâng Cao (GCOS134)** — Chương trình Thạc sĩ
> Công nghệ Thông tin, Trường Đại học Công nghệ TP.HCM (HUTECH), lớp 24SCT11, 07/2024.

Phân tích hoạt động trong một nhóm Facebook để **xác định những thành viên có ảnh hưởng
nhất**. Dự án minh họa một pipeline dữ liệu hoàn chỉnh: thu thập dữ liệu (web scraping) →
mô hình hóa trên graph database **OrientDB** → tính điểm ảnh hưởng bằng **công thức trọng số
kết hợp thuật toán PageRank** → phục vụ kết quả qua REST API.

Trọng tâm học thuật của đề tài là khai thác **OrientDB** — một multi-model NoSQL database
thiên về graph — cho bài toán dữ liệu mạng xã hội nhiều quan hệ (Users ↔ Posts ↔ Comments ↔ Groups).

## Quy trình thực nghiệm

```
Admin/Scheduler ─► Add FB Group URL/ID ─► URL Queue ─► Fetch URL ──(error)──► DLQ
                                                          │ (200 OK)
                                                          ▼
                                                      Parse URL ─► Data ETL ─► Master Database (OrientDB)
                                                                                     ▲
                                                                       Event Trigger │
                                                          End user ─► Modern WebApp ──┘
```

## Pipeline & công nghệ

| # | Giai đoạn | Công nghệ | Vị trí trong repo |
|---|-----------|-----------|-------------------|
| 1 | Thu thập posts / comments / members từ FB group (qua `mbasic.facebook.com`) | Selenium, BeautifulSoup4, pandas → CSV | `fb_scraping/` |
| 2 | Mô hình hóa & lưu trữ dạng đồ thị | OrientDB (Docker), pyorientdb, HTTP REST API | `research/`, `docs/orientdb.md` |
| 3 | Tính điểm ảnh hưởng | Công thức `influence_score` có trọng số + PageRank trên đồ thị | OrientDB Functions / xử lý ngoài |
| 4 | Thử nghiệm dự đoán (phụ) | scikit-learn — Random Forest trên Google Colab | `data_modeling/random_forest.ipynb` |
| 5 | Phục vụ kết quả | Flask API | `api/main_app.py` |

## Mô hình dữ liệu trên OrientDB

Dữ liệu được tổ chức thành **đồ thị có hướng** (Property Graph):

- **Vertex (V):** `Groups`, `Users`, `Posts`, `Comments`
- **Edge (E):** `HasJoined`, `MadePost`, `HasComment`, `MadeComment`, `HasCommentedBy`

```sql
-- Ví dụ graph traversal trong OrientDB Studio
MATCH {Class: Groups}-HasJoined-{Class: Users}-MadePost-{Class: Posts}
      -HasComment-{Class: Comments}-MadeComment-{Class: Users}
RETURN $pathelements
```

Truy vấn thống kê được đóng gói thành **OrientDB Functions** (SQL/JavaScript) để tái sử dụng,
ví dụ `top10UsersByPosts`, `countUsers`:

```sql
CREATE FUNCTION top10UsersByPosts
  "SELECT author_id, COUNT(post_id) AS totalPosts
   FROM Posts GROUP BY author_id ORDER BY totalPosts DESC LIMIT 10"
  LANGUAGE SQL
```

## Cách tính điểm ảnh hưởng

Mỗi vertex `Users` tổng hợp các thuộc tính: `total_posts`, `total_reactions_on_posts`,
`total_comments_on_posts`, `total_comments_on_others_posts`, `total_reactions_on_others_posts`.

**1. Influence score (trọng số tuyến tính):**

```
influence_score = total_posts                    * 0.15
                + total_reactions_on_posts        * 0.25
                + total_comments_on_posts         * 0.35
                + total_comments_on_others_posts  * 0.15
                + total_reactions_on_others_posts * 0.10
```

**2. PageRank** chạy trên đồ thị tương tác giữa các `Users` để đo mức độ "trung tâm" /
lan tỏa, với hệ số giảm dần `d = 0.85`:

```
PR(A) = (1 - d) + d * Σ ( PR(Tᵢ) / C(Tᵢ) )
```

Hai chỉ số bổ sung cho nhau: `influence_score` phản ánh độ tương tác trực tiếp,
`pagerank_score` phản ánh vị thế trong mạng lưới quan hệ.

## Dữ liệu thu thập

Thiết kế trường dữ liệu tham khảo bài báo *Predicting Influential Users in Online Social
Networks*. Chi tiết: `docs/info_collected.txt`.

- **Posts**: `groupCode`, `postId`, `authorId`, `time`, `isShared`, `reactions`
- **Comments**: `postId`, `commentId`, `authorId`, `reactions`
- **Members**: `memberId`, `memberType` (0 = admin/moderator, 1 = thành viên khác)

## Cài đặt & chạy

### Yêu cầu
- Python 3.x, Google Chrome + `chromedriver`
- Docker (cho OrientDB)

### 1. Thu thập dữ liệu
```bash
pip install selenium beautifulsoup4 pandas
# Tạo fb_credentials.txt (KHÔNG commit) theo định dạng:
#   email = "your_email"
#   pass  = "your_password"
python -m fb_scraping.main      # sinh ra posts.csv, comments.csv
```

### 2. Khởi động OrientDB
```bash
# Lưu ý: dùng bản 2.2.x để tương thích pyorient client
docker run -d --name orientdb -p 2424:2424 -p 2480:2480 \
  -e ORIENTDB_ROOT_PASSWORD=root orientdb:2.2.35
# OrientDB Studio: http://localhost:2480
```

### 3. Phân tích & dự đoán (thử nghiệm)
Mở `data_modeling/random_forest.ipynb` trên Google Colab.

### 4. Chạy API
```bash
pip install flask numpy
python api/main_app.py          # http://127.0.0.1:5000
```

## Cấu trúc thư mục

```
.
├── fb_scraping/        # Module crawler (Selenium + BeautifulSoup4)
├── research/           # Thử nghiệm OrientDB CRUD, REST API, các bản scraping nháp
├── data_modeling/      # Notebook Random Forest (thử nghiệm)
├── api/                # Flask API phục vụ dự đoán
└── docs/               # Proposal, slide báo cáo, đánh giá OrientDB, mô tả dữ liệu
```

## Trạng thái & kiến trúc mục tiêu

Đây là đồ án môn học (proof-of-concept). Một số phần còn ở mức thử nghiệm: API dự đoán là
bản khung, thu thập `members` đang tạm tắt, mô hình Random Forest dùng tập feature tối giản.

Báo cáo có phác thảo một **kiến trúc triển khai mục tiêu** (chưa hiện thực hóa hoàn chỉnh
trong repo): tách Crawler / Influence-Calc thành service riêng, Master–Slave Database,
frontend trên Netlify + CDN, thông báo sự kiện qua Slack Webhook. Xem thư mục `docs/`.

### Hướng phát triển
- Mở rộng đa dạng nguồn dữ liệu, hỗ trợ các trang web phức tạp hơn.
- Tăng hiệu suất bằng đa luồng / phân tán hóa quá trình thu thập & xử lý.
- Tích hợp **Spark** (Spark Connect) để chạy PageRank trên dữ liệu lớn.
- Phát triển giao diện người dùng hoàn chỉnh.

## ⚠️ Lưu ý đạo đức & pháp lý

Code thu thập dữ liệu Facebook chỉ phục vụ **mục đích học tập, nghiên cứu**. Việc scraping
có thể vi phạm Điều khoản dịch vụ của Facebook. **Không** commit thông tin đăng nhập
(`fb_credentials.txt`) và không thu thập / phát tán dữ liệu cá nhân khi chưa có sự đồng ý.

## Nhóm thực hiện — Nhóm 9

| Học viên | MSHV |
|----------|------|
| Nguyễn Ngọc Đỉnh | 2440861001 |
| Hà Anh Dũng | 2440861003 |
| Nguyễn Minh Trung Nghĩa | 2441861021 |

GVHD: PGS. TS. Nguyễn Thị Thúy Loan

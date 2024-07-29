# Đánh giá ưu và khuyết điểm của OrientDB so với 1 số cơ sở dữ liệu cùng loại, và phân tích hiệu suất của cơ sở dữ liệu

![](https://github.com/dinhnguyenngoc/social-network-analysis/blob/main/docs/pros-con-orientdb.jpg)

OrientDB là multi-model NoSQL database, quảng cáo là chú trọng đến graph database cho phép kết hợp nhiều loại data model trong một database.

Type: 

Data storage: 

- Documents:
- Graphs:


## Các tính năng chính của OrientDB
- Relationship Focus: Nhiều user chuyển từ MongoDB sang vì hỗ trợ LINK relationship. LINK, LINKSET, LINKLIST, LINKMAP. More: https://orientdb.com/docs/2.2.x/Tutorial-Relationships.html
- Graph Traversal: Hỗ trợ tốt duyệt qua các dữ liệu có kết nối (e.g., finding recommendations, computing shortest paths, or detecting patterns).
- Flexibility: Hỗ trợ Multi-model bao gồm document model, graph model, key-value model, objetc model. Có thể sử dụng một hoặc kết hợp cùng lúc.

```
CREATE CLASS Project EXTENDS V
CREATE PROPERTY Project.name STRING
CREATE PROPERTY Project.description STRING
CREATE PROPERTY Project.startDate DATE
CREATE PROPERTY Project.endDate DATE

INSERT INTO Project SET name = 'Project A', description = 'Description of Project A', startDate = '2024-07-01', endDate = '2024-12-31'
```

- SQL-like Syntax: Cú pháp tương tự SQL, sẽ có một số từ khóa đặc thù như LINK LINKSET LINKLIST LINKMAP/ VERTEX EDGE
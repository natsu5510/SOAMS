# SOAMS

## 複製專案到本地

### 1. 複製儲藏庫到本地端

```bash
git clone https://github.com/natsu5510/SOAMS.git
```

### 2. 切換到專案資料夾下

```
cd SOAMS/
```

### 3. 設定本地使用者名稱與信箱

```bash
git config --local user.name 你的學號
```

```bash
git config --local user.email 你的學號@mail.nuk.edu.tw
```

### 4. 切換到自己的分支

```bash
git checkout -t origin/你的學號
```

> [!NOTE] push 上 github
> - 使用 `-u origin 你的學號` 設定上游(只有第一次git push要打)
> 
> ```bash
> git push -u origin 你的學號
> ```
> 
> - 往後push只要打
> 
> ```bash
> git push
> ```

## 設定資料庫

### 創建 `config.py` 輸入內容：

```python
MYSQL_PASSWORD = '你的MYSQL密碼'
MYSQL_USER = '你的MYSQL用戶名'
DATABASE_URI = '資料庫URI'
SECRET_KEY = '隨便一個字串'
```
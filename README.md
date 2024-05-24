# 1. 先複製儲藏庫到本地端
```git
git clone https://github.com/natsu5510/SOAMS.git
```
# 2. 切換到專案資料夾下
```
cd SOAMS/
```
# 3. 設定使用者名稱與信箱
```git
git config --local user.name 你的學號
```
```git
git config --local user.email 你的學號@mail.nuk.edu.tw
```
# 4. 切換到自己的分支
```git
git checkout -t origin/你的學號
```
# 5. 完成commit後push上github
## 使用 `-u origin 你的學號` 設定上游(只有第一次git push要打)
```git
git push -u origin 你的學號
```
## 往後push只要打
```git
git push
```
# 1 . 配置
命令|作用
:---|:---
git config --global user.name "yourname"                    |配置本地git的用户名
git config --global user.email "email@example.com"          |配置本地git的Email地址
git config --global color.ui true                           |Git会适当地显示不同的颜色

# 2. 初始化
命令|作用
:---|:---
git init                            |把目录变成Git可以管理的仓库

# 3. 把文件添加到仓库
命令|作用
:---|:---
git add <filename1> <filename2>     |指定文件
git add --all                       |全部
git add --force                     |强制

# 4. 提交
命令|作用
:---|:---
git commit -m <"message">   |把文件提交到仓库, 并添加描述message

# 5. 工作区状态
命令|作用
:---|:---
git status                  |查看工作区的状态

# 6. 修改内容
命令|作用
:---|:---
git diff 				    |比较 工作区 文件与 暂存区文件 的区别（上次git add 的内容） 
git diff --cached 			|比较 暂存区 文件与 仓库分支 里（上次git commit 后的内容）的区别
git diff HEAD -- filename 	|比较 工作区 文件与 仓库分支 里（上次git commit 后的内容）的区别

# 7. 历史版本
命令|作用
:---|:---
git log						                        |查看详细LOG
git log --pretty=oneline		                    |查看简易LOG
git log --pretty=oneline --abbrev-commit            |查看简易LOG，缩写版本号
git log --graph --pretty=oneline --abbrev-commit    |查看简易LOG，缩写版本号，带图示

# 8. 未来的版本
命令|作用
:---|:---
git reflog |查看未来的版本

# 9. 回滚操作
命令|作用
:---|:---
git reset --hard <commit_id>	|通过版本号设置HEAD指向
git reset --hard HEAD^			|直接回到上个版本
git reset --hard HEAD^^			|直接回到上上个版本

# 10. 撤销修改
命令|作用
:---|:---
git checkout -- <filename>		|把文件在工作区的修改全部撤销
git reset HEAD <filename>		|把文件在暂存区的修改撤销掉，取消Add

# 11. 删除
命令|作用
:---|:---
git rm <filename>				|把在工作区的文件删除, 需要另外commit

# 12. 分支
命令|作用
:---|:---
git branch						    |查看分支列表
git branch <name>				    |创建分支
git checkout <name>  <from>		    |切换分支 ， from表示来源
git checkout -b <name> <from>		|创建分支 + 切换分支 ， from表示来源
git merge <name>					|合并某分支到当前分支, fast forward模式 , 不保留合并过程
git merge --no-ff -m "message" dev	|合并某分支到当前分支, 非fast forward模式, 保留合并过程
git branch -d <name>				|删除分支
git branch -D <name>				|强制删除分支

# 13. 缓存区
命令|作用
:---|:---
git stash							|另存缓存区
git stash list					    |查看已另存缓存区
git stash apply stash@{0}			|提取指定缓存区
git stash drop stash@{0}			|删除指定缓存区
git stash pop						|提取并删除最后一次保存的缓存区

# 14. 远程库
命令|作用
:---|:---
>ssh-keygen -t rsa -C "youremail@example.com"				|创建SSH Key, 生成<.ssh\id_rsa> 和 <.ssh\id_rsa.pub> 这两个文件
git remote add origin git@server-name:path/repo-name.git 	|关联指定远程库 ， 起名为origin
git remote  												|查看当前指定的远程库 ， 显示为别名，例如：origin
git remote -v  												|查看当前指定的远程库 ， 显示为详细内容，远程库的具体地址

# 15. 从远程库克隆一个本地库
命令|作用
:---|:---
git clone git@server-name:path/repo-name.git 			|通过SSH，	较快
git clone https://server-name/path/repo-name.git 		|通过http，	较慢

# 16. 推送 与 获取
命令|作用
:---|:---
git branch --set-upstream-to=origin/<from> <name>  	|创建本地分支和远程分支的链接关系
git push -u origin master	                        |首次往origin推送master分支
git push origin master		                        |后面往origin推送master分支
git pull					                        |从远程库获得最新内容
git rebase					                        |把本地未push的LOG分叉提交历史整理成直线 ， 变基

# 17. 标签
命令|作用
:---|:---
git tag <tagname>									|创建一个新标签
git tag <tagname> <commit_id>						|往指定版本创建一个新标签
git tag -a <tagname> -m <"message"> <commit_id>  	|创建带有说明的标签
git tag											    |查看所有标签
git show <tagname>								    |查看标签信息
git tag -d <tagname>								|删除一个本地标签
git push origin <tagname>							|推送一个本地标签
git push origin --tags								|推送全部未推送过的本地标签
git push origin :refs/tags/<tagname>                |删除一个远程标签








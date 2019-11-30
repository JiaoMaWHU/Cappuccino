在ubuntu 19.04上使用Jenkins-cli
# 安装Java和Jenkins
参照`https://juejin.im/post/5b6329c2e51d4519044ab85f`<br>
需记录初始化的账号和密码

# tmp
https://jenkins.io/doc/book/managing/cli/#using-the-cli-client

# 使用Jenkins-cli
找到Jenkins-cli的位置。默认位于/var/cache/jenkins/war/WEB-INF/。
```
sudo find / -name "*cli.jar"
```
试验是否可用。可用则显示cli的选项及功能
```
sudo java -jar /var/cache/jenkins/war/WEB-INF/jenkins-cli.jar -h
```
显示已创建的job。其中`USER`、`SCRETE`分别为初始化的用户名和密码。`URL`为访问Jenkins的URL
```
sudo java -jar /var/cache/jenkins/war/WEB-INF/jenkins-cli.jar -auth USER:SCRETE -s URL list-jobs
```
导出名为`JOB-NAME`的job的配置到`CONFIG.xml`。可以在已创建的job的文件夹下查看，文件名为config.xml。
```
sudo java -jar /var/cache/jenkins/war/WEB-INF/jenkins-cli.jar -auth USER:SCRETE -s URL get-job JOB-NAME > CONFIG.xml
```
根据配置`CONFIG.xml`创建job。
```
sudo java -jar /var/cache/jenkins/war/WEB-INF/jenkins-cli.jar -auth USER:SCRETE -s URL create-job JOB-NAME < CONFIG.xml
```
创建的job所在路径，每个job都有相应的文件夹
```
/var/lib/jenkins/jobs
```
运行名称为`JOB-NAME`的job。可以通过查看实际输出和Jenkins Web判断是否成功
```
sudo java -jar /var/cache/jenkins/war/WEB-INF/jenkins-cli.jar -auth USER:SCRETE -s URL build JOB-NAME
```

# 添加测试依赖的Python库
安装python-nose、pylint、coverage in Jenkins shell command
```
sudo pip install LIB
```

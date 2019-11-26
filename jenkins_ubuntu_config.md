在ubuntu 19.04上使用Jenkins-cli
# 安装Java和Jenkins
参照`https://juejin.im/post/5b6329c2e51d4519044ab85f`<br>
需记录初始化的账号和密码

# 使用Jenkins-cli
找到Jenkins-cli的位置。默认位于/var/cache/jenkins/war/WEB-INF/。
```
sudo find / -name "cli.jar"
```
试验是否可用。可用则显示cli的选项及功能
```
sudo java -jar /var/cache/jenkins/war/WEB-INF/Jenkins-cli.jar -h
```
显示已创建的job。其中`USER`、`SCRETE`分别为初始化的用户名和密码。`URL`为访问Jenkins的URL
```
sudo java -jar /var/cache/jenkins/war/WEB-INF/Jenkins-cli.jar -auth USER:SCRETE -s URL list-jobs
```
导出名为`JOB-NAME`的job的配置到`CONFIG.xml`。可以在已创建的job的文件夹下查看，文件名为config.xml。
```
sudo java -jar /var/cache/jenkins/war/WEB-INF/Jenkins-cli.jar -auth USER:SCRETE -s URL get-job JOB-NAME > CONFIG.xml
```
根据配置`CONFIG.xml`创建job。
```
sudo java -jar /var/cache/jenkins/war/WEB-INF/Jenkins-cli.jar -auth USER:SCRETE -s URL create-job JOB-NAME < CONFIG.xml
```
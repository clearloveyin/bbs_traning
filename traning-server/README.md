# 把项目部署到免费版heroku手顺
## 1，注册heroku账号
## 2，创建你的应用，创建成功会返回一个url  
heroku create application_name
## 3，本地git增加remote，把上面返回的url替换下面的url
git remote add prod https://git.heroku.com/application_name.git
## 4, 编译前端，把dist文件的内容复制到flask的app下
index.html复制到templates文件下  
把static整个文件复制到app文件下
## 5，增加到达登陆页面的接口
@app.route('/', methods=['get'])  
def index():  
  return render_template('index.html')
## 6，配置Procfile文件，不要有后缀名，注意不要指定端口，或者heroku会报错  
web: gunicorn start:app  --start是你的flask启动文件
## 7，创建数据库，创建成功会往环境变量里面塞入数据库的信息，环境变量字段为：DATABASE_URL  
heroku addons:create heroku-postgresql:hobby-dev --app application_name
## 8，查看环境变量：heroku config  
设置环境变量：heroku config:set APP_SETTINGS=config.ProductionConfig
## 9，config 文件获取环境变量的方法  
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
## 10，迁移数据库  
可以在heroku执行迁移命令，但我遇到了一个问题，报找不到migrations文件夹的错误；  
也可以在本地执行迁移命令，要把DATABASE_URL配置到config中，如下：  
SQLALCHEMY_DATABASE_URI = 'postgres://eurczfydmrjive:dca46aadb46ebcf2bbc06bf37432f9a04f0a06dc68f8c0d2255ae96b59c38eaa@ec2-184-72-223-163.compute-1.amazonaws.com:5432/d6julun39c92p1'
## 11，初始化数据库  
利用pgAdmin连接上面的数据库，找到你的数据库"d6julun39c92p1"  
添加管理员账号：user_id：1， user_name: admin  
增加角色信息：1，role_id: 1, role_name: admin  
            2, role_id: 2, role_name: moderator  
## 12, 把代码提交到heroku服务器上：  
git add .  
git commit -m 'mmm'  
git push prod master  
##14, 启动服务  
heroku open




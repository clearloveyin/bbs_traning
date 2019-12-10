# 编译前端生成dist文件夹
npm run build
# 复制index.html到template文件夹下
rm /Users/yuyin/Desktop/workerspace/traning-release/app/templates/index.html
cp dist/index.html /Users/yuyin/Desktop/workerspace/traning-release/app/templates/index.html
# 复制index.html到template文件夹下
rm -rf /Users/yuyin/Desktop/workerspace/traning-release/app/static/*
cp -r dist/static/. /Users/yuyin/Desktop/workerspace/traning-release/app/static

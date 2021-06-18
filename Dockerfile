# 基础镜像
FROM python:3.8-alpine
# 创建人
LABEL author=ZirenWang
# 环境变量
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
# 修改apk源为国内
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
# 安装必须的包
#RUN apk add --no-cache gcc musl-dev libxslt-dev libffi-dev python3-dev openssl-dev cargo
RUN apk add gcc musl-dev libxslt-dev libffi-dev openssl-dev
# 设置工作文件夹目录
WORKDIR /scrapy
# 修改pip源为国内
RUN pip install --upgrade pip -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
# 拷贝
COPY requirements.txt requirements.txt
# 安装代码需要的pip包
RUN pip3 install --no-cache-dir -r requirements.txt
# 拷贝文件
COPY . .
# 开发端口
EXPOSE 5000
# TODO 设置保持启动脚本
CMD ["sh","while true; do sleep 1; done;"]
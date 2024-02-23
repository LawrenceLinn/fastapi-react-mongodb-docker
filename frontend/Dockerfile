FROM node:20-slim as builder

WORKDIR /app

COPY package*.json /app/

RUN npm ci

COPY ./ /app/

ARG FRONTEND_ENV=production
ARG VITE_BACKEND_API_URL
ARG VITE_PWD_SIGNUP_ENABLED
ARG VITE_GA_TRACKING_ID

ENV VITE_APP_ENV=${FRONTEND_ENV}

# Comment out the next line to disable tests
# RUN npm run test:unit


RUN npm run build


FROM nginx:1.23.1

# # Remove default nginx configuration
# RUN rm /etc/nginx/conf.d/*

# # Remove default nginx static assets
# RUN rm -rf /usr/share/nginx/html/*

# # Copy built app and nginx conf
# COPY --from=builder /app/dist/ /usr/share/nginx/html
# COPY ./nginx.conf /etc/nginx/conf.d

# 移除默认的 Nginx 配置和静态资源
RUN rm /etc/nginx/conf.d/default.conf
RUN rm -rf /usr/share/nginx/html/*

# 将构建的前端应用复制到 Nginx 服务目录
COPY --from=builder /app/dist/ /usr/share/nginx/html

# 复制 SSL 证书和私钥到容器内
COPY .cert/cert.pem /etc/nginx/ssl/cert.pem
COPY .cert/key.pem /etc/nginx/ssl/key.pem

# 复制自定义的 Nginx 配置文件到容器
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# 在自定义 Nginx 配置中，确保你配置了 SSL，类似这样:
# listen 443 ssl;
# ssl_certificate /etc/nginx/ssl/cert.pem;
# ssl_certificate_key /etc/nginx/ssl/key.pem;

# 暴露 HTTPS 端口
EXPOSE 443
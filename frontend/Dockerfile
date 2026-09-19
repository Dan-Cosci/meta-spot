FROM alpine:latest

WORKDIR /app

RUN apk add nodejs npm curl nginx

COPY package*.json ./

RUN npm ci

EXPOSE 80

COPY . .

RUN npm run build

COPY nginx.conf /etc/nginx/http.d/default.conf

CMD ["nginx", "-g", "daemon off;"]

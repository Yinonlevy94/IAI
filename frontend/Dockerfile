# frontend dockerfile - two stages: build react, serve with nginx

# stage 1: build the react app
FROM node:20-alpine AS builder

WORKDIR /app

# copy package files first for better caching
# why? if these don't change, docker reuses this layer = faster builds
COPY package*.json ./

# install dependencies (including dev deps, vite needs them)
RUN npm ci

# copy source code
COPY . .

# build the app with vite
# creates optimized static files in /dist (minified, compressed, ready for production)
RUN npm run build

# stage 2: serve the files with nginx
FROM nginx:alpine

# remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# use our config (handles spa routing, caching, health checks)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# copy built files from stage 1
COPY --from=builder /app/dist /usr/share/nginx/html

# security: create non-root user
# why? k8s security policies require it, also just safer
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser && \
    chown -R appuser:appuser /usr/share/nginx/html && \
    chown -R appuser:appuser /var/cache/nginx && \
    chown -R appuser:appuser /var/log/nginx && \
    chown -R appuser:appuser /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && \
    chown -R appuser:appuser /var/run/nginx.pid

# switch to non-root user
USER appuser

# use port 8080 (non-root users can't bind to port 80)
EXPOSE 8080

# health check endpoint for kubernetes
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

# start nginx (daemon off keeps it in foreground for docker)
CMD ["nginx", "-g", "daemon off;"]
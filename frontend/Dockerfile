# --- Build Stage ---
FROM node:lts-bookworm AS builder

# Use non-root user for building (optional, more secure)
RUN useradd -m builder
USER builder

WORKDIR /home/builder/app

# Copy only what's needed first for caching and reproducibility
COPY --chown=builder:builder package.json package-lock.json ./
RUN npm install

# Copy the rest of the app
COPY --chown=builder:builder src ./src
COPY --chown=builder:builder public ./public
COPY --chown=builder:builder .env.production ./.env
COPY --chown=builder:builder index.html vite.config.js ./

RUN npm run build

# --- Runtime Stage ---
FROM nginx:latest AS runtime

# Remove default nginx config
RUN rm -f /etc/nginx/conf.d/default.conf

# Set working directory for NGINX html root
WORKDIR /usr/share/nginx/html

# Copy built frontend from builder stage
COPY --from=builder --chown=nginx:nginx /home/builder/app/dist ./

# Copy custom NGINX configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Ensure correct permissions
RUN chmod -R 755 /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    sed -i 's,/var/run/nginx.pid,/tmp/nginx.pid,' /etc/nginx/nginx.conf

EXPOSE 80
USER nginx

CMD ["nginx", "-g", "daemon off;"]
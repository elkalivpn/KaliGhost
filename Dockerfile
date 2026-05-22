FROM node:22-alpine AS builder

WORKDIR /app

COPY package.json bun.lock* ./

RUN npm install -g bun && \
    bun install --frozen-lockfile

COPY . .

RUN bun run build

# Production stage
FROM node:22-alpine

WORKDIR /app

ENV NODE_ENV=production \
    NEXT_PUBLIC_API_URL=http://localhost:5001 \
    NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:5001/socket.io

COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000 || exit 1

CMD ["node", "server.js"]

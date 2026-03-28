# Task 5: Dockerfile for Search UI
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package.json .
RUN npm install

# Copy source code
COPY public/ ./public/
COPY src/ ./src/

EXPOSE 3000

CMD ["npm", "start"]
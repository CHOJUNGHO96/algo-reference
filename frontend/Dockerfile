FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy application
COPY . .

# Expose Vite dev server port
EXPOSE 3000

# Run dev server with host binding
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]

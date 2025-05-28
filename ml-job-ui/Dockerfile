# Use official lightweight Node.js 20 image
FROM node:20-alpine

# Set working directory for React UI application
WORKDIR /ml-job-ui

# Copy React dependency definitions first to leverage Docker layer caching
COPY package*.json ./

# Install application dependencies
RUN npm install

# Copy all UI application source code into the container
COPY . .

# Make any shell scripts in ./scripts executable
RUN chmod +x ./scripts/*.sh

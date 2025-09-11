# File: FFA/frontend/Dockerfile (located at FFA/frontend/Dockerfile)

FROM node:20-alpine
WORKDIR /app

# Copy package.json first.
# 'package.json' is now relative to the build context (which is FFA/frontend/).
COPY package.json ./

# Install Node.js dependencies using npm.
RUN npm install

# Copy the rest of the frontend application code.
# '.' refers to the build context (FFA/frontend/) and its contents.
# This copies everything from FFA/frontend/ into /app in the container.
COPY . .

EXPOSE 5173
CMD ["npm", "run", "dev"]


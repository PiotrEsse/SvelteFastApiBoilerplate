FROM mcr.microsoft.com/devcontainers/python:3.11

# Install Node.js LTS using nvm (already available in base image)
ENV NODE_VERSION=20
RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} && nvm alias default ${NODE_VERSION}"

# Install global tooling helpful for both frontend and backend
RUN npm install -g npm@latest openapi-typescript

# Default workdir expected by the devcontainer.json (if added later)
WORKDIR /workspaces

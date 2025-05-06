FROM node:19.5.0-alpine

WORKDIR /app

COPY . /app/

RUN npm install
RUN npm run build

RUN npm install -g serve

EXPOSE 5173

CMD ["npm", "run", "dev"]



FROM node:6.11.4
ENV APP_DIR /home/node/app
RUN mkdir -p $APP_DIR
WORKDIR $APP_DIR
COPY app/package.json .
RUN npm install
COPY app/ $APP_DIR
CMD ["node", "index.js"]

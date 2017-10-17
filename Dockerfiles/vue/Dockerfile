FROM node:6.11.4

ENV APP_DIR /home/node/app
ENV NODE_USER node
ENV NODE_GROUP node
 
RUN npm install --global vue-cli \
    && mkdir -p $APP_DIR \
    && chown -R $NODE_USER:$NODE_GROUP $APP_DIR

WORKDIR $APP_DIR

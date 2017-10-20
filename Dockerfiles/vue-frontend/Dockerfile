FROM jest10820/vue

COPY package.json $APP_DIR/package.json
RUN npm install
COPY . $APP_DIR/
#RUN chown -R $NODE_USER:$NODE_GROUP $APP_DIR

#USER $NODE_USER
RUN npm run build

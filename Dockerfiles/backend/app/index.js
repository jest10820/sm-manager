'use strict';

const restify = require('restify');
const logger = require('./logger');

const server = restify.createServer();

server.listen(8080, () => {
  logger.info('Server listening on port', 8080);
});

server.get('/hello', (req, res, next) => {
  res.send('Hello world');
  return next();
});


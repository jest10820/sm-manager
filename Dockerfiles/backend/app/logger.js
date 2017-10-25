const winston = require('winston');

module.exports = new winston.Logger({
  transports: [
    new (winston.transports.Console)({
      level: 'info',
      timestamp: true,
      label: 'sm-backend'
    })
  ],
  exitOnError: false
});


/**
 * Copyright 2019, Symph Inc.
 */

'use strict';

const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res
    .status(200)
    .send('Hello World!')
    .end();
});

// Start the server
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`App listening on port ${PORT}`);
});

module.exports = app;

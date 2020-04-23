/**
 * Copyright 2019, Symph Inc.
 */

'use strict';

const express = require('express');
const app = express();

const { getPricePerKilo, getPartners } = require('./models');

const API_V1_PATH = '/api/v1/';


/**
 * Get Price per kilo of rice
 */
app.get(`${API_V1_PATH}price-per-kilo`, async (req, res) => {
  const price_per_kilo = await getPricePerKilo();
  res
    .status(200)
    .send({
      price_per_kilo
    })
    .end();
});


/**
 * List partner stores
 */
app.get(`${API_V1_PATH}partners`, async (req, res) => {
  const partners = await getPartners();
  res
    .status(200)
    .send(partners)
    .end();
});


app.get('/', async (req, res) => {
  const partners = await getPartners();
  res
    .status(200)
    .send('Welcome to BigasPadala')
    .end();
});


// Start the server
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`App listening on port ${PORT}`);
});

module.exports = app;

/**
 * Copyright 2019, Symph Inc.
 */

'use strict';

const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const {
  getPricePerKilo,
  getPartners,
  createPaymentIntent,
  createPaymentMethod,
} = require('./models');

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

/**
 * Create paymongo payment intent
 */
app.post(`${API_V1_PATH}create-payment-intent`, async (req, res) => {
  const amount  = req.body.amount;

  try {
    const result = await createPaymentIntent(amount);

    res
      .status(201)
      .send({
        id: result.data.id,
        client_key: result.data.attributes.client_key,
      })
      .end();
  } catch(e) {
    res
      .status(400)
      .send(e)
      .end();
  }
});


app.post(`${API_V1_PATH}create-payment-method`, async (req, res) => {
  try {
    const result = await createPaymentMethod({
      card_number: req.body.card_number,
      exp_month: req.body.exp_month,
      exp_year: req.body.exp_year,
      cvc: req.body.cvc
    });

    res
      .status(201)
      .send(result)
      .end()
  } catch(e) {
    res
      .status(400)
      .send(e)
      .end();
  }
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

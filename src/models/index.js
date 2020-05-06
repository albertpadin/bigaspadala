const {Datastore} = require('@google-cloud/datastore');
const Paymongo = require('paymongo');

const datastore = new Datastore();
const paymongo = new Paymongo(process.env.PAYMONGO_SECRET_KEY);


async function getPricePerKilo() {
  const query = datastore
    .createQuery('Config')
    .filter('__key__', '=', datastore.key(['Config', 'price_per_kilo']));

  const [price_per_kilo] = await datastore.runQuery(query);
  return price_per_kilo[0].value;
}


/**
 * Array of registered partner stores
 */
async function getPartners() {
  // sample data
  // [{
  //   "contact_number": "0982132",
  //   "timestamp": "2020-04-24T18:15:00.000Z",
  //   "stock": "low",
  //   "name": "Arnelle Store",
  //   "coordinates": {
  //     "latitude":89,
  //     "longitude":87
  //   }
  // }]
  const query = datastore
    .createQuery('Partners')
    .order('name', {descending: false});

  const [partners] = await datastore.runQuery(query);
  return partners;
}


/**
 * Create payment intent in paymongo
 */
async function createPaymentIntent(amount, metadata) {
  const perKiloPrice = await getPricePerKilo();
  const kilos = parseInt(amount / perKiloPrice);
  const payload = {
    data: {
      attributes: {
        amount: amount * 100,  // this is in cents so we multiply by 100
        currency: 'PHP',
        payment_method_allowed: ['card'],
        statement_descriptor: `${kilos} kilos of rice`,
      }
    }
  };

  const result = await paymongo.paymentIntents.create(payload);
  return result;
}

/**
 * Attach a payment method to a payment intent
 */
async function attachPaymentMethodToIntent(intentId, methodId) {
  const payload = {
    data: {
      attributes: {
        payment_method: methodId
      }
    }
  };
  await paymongo.paymentIntents.attach(intentId, payload);
  const result = await paymongo.paymentIntents.retrieve(intentId);

  if (result.data && result.data.attributes && result.data.attributes.status === 'awaiting_next_action') {
    return {
      status: result.data.attributes.status,
      next_action: result.data.attributes.next_action,
      payment_method_options: result.data.attributes.payment_method_options
    }
  }
  return result;
}


async function getPaymentIntentDetail(intentId) {
  const result = await paymongo.paymentIntents.retrieve(intentId);
  return result;
}



/**
 * Create a payment method in paymongo. DO NOT USE THIS IN PROD, just for
 * testing
 */
async function createPaymentMethod(details) {
  const payload = {
    data: {
      attributes: {
        type: 'card',
        details: {
          ...details
        }
      }
    }
  };
  const result = await paymongo.paymentMethods.create(payload);
  return result;
}


module.exports = {
  getPricePerKilo,
  getPartners,
  createPaymentIntent,
  createPaymentMethod,
  attachPaymentMethodToIntent,
  getPaymentIntentDetail,
}
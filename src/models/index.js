const {Datastore} = require('@google-cloud/datastore');

const datastore = new Datastore();


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


module.exports = {
  getPricePerKilo,
  getPartners
}
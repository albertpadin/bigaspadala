async function getPricePerKilo() {
  // TODO: get the value from database
  return 50;
}


/**
 * Array of registered partner stores
 */
async function getPartners() {
  // TODO: get values from the database
  return [
    {
      name: "Store 1",
      coordinate: {
        latitude: 10.123,
        longitude: 123.45,
      },
      contact_number: "09191234567",
      stock: "high"
    },
    {
      name: "Store 2",
      coordinate: {
        latitude: 20.123,
        longitude: 93.45,
      },
      contact_number: "09191234568",
      stock: "low"
    }
  ]
}


module.exports = {
  getPricePerKilo,
  getPartners
}
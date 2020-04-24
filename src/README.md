# Quickstart for Node.js in the App Engine standard environment

This is the sample application for the
[Quickstart for Node.js in the App Engine standard environment][tutorial]
tutorial found in the [Google App Engine Node.js standard environment][appengine]
documentation.

- [Setup](#setup)
- [Running locally](#running-locally)
- [Deploying to App Engine](#deploying-to-app-engine)
- [Running the tests](#running-the-tests)
- [React Frontend](#react-frontend)

## Setup

Before you can run or deploy the sample, you need to do the following:

1.  Refer to the [appengine/README.md][readme] file for instructions on
    running and deploying.
1.  Install dependencies:

        npm install

## Running locally

    npm start

## Deploying to App Engine

    gcloud app deploy

## Running the tests

See [Contributing][contributing].

[appengine]: https://cloud.google.com/appengine/docs/standard/nodejs
[tutorial]: https://cloud.google.com/appengine/docs/standard/nodejs/quickstart
[readme]: ../../README.md
[contributing]: https://github.com/GoogleCloudPlatform/nodejs-docs-samples/blob/master/CONTRIBUTING.md

## React Frontend

This project uses [ReactJS](https://reactjs.org/) for the frontend. The frontend
code needs to be built separately using the following commands:

```bash
npm run build

# During development, to auto-build on change
npm run watch
```

The build files are placed in the `frontend-dist` directory. Hosting these files
should make sure to serve this is a single-page application (i.e. all server-side
routes should serve the same page) in order for React Router's client-side routing
to work.

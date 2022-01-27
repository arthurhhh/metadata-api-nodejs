const express = require('express')
const path = require('path')
const moment = require('moment')
const { HOST } = require('./src/constants')
const db = require('./src/database')
const get_content = require('./access_token')
const fs = require("fs")
const {spawn} = require('child_process')

const PORT = process.env.PORT || 5000

const app = express()
  .set('port', PORT)
  .set('views', path.join(__dirname, 'views'))
  .set('view engine', 'ejs')

// Static public files
app.use(express.static(path.join(__dirname, 'public')))

app.get('/', function(req, res) {
  res.send('Get ready for OpenSea!');
})

app.get('/api/token/:token_id', async function(req, res) {
  var token_id = req.params.token_id;
  var mark = await get_content(token_id);
  const strArray = mark.split(":", 2);
  const name = strArray[0];
  const value = strArray[1];

  var url;
  const python = spawn('python3', ['picture_generator.py', name, value, token_id]);
  // collect data from script
  python.stdout.on('data', function(output) {
    console.log('Pipe data from python script ...');
    url = output.toString();
  });
  python.on( 'error', ( err ) => {
    throw `failed to initialize command : "${ err }"`;
  } );
  // in close event we are sure that stream from child process is closed
  python.on('close', (code) => {
    const data = {
      'name': name,
      'description': '"' + value + '"',
      'attributes': {},
      'image': url
    };
    console.log("URL: " + url);
    res.send(data);
  }); 

});

app.listen(app.get('port'), function() {
  console.log('Node app is running on port', app.get('port'));
})
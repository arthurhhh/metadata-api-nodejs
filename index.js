const express = require('express')
const path = require('path')
const moment = require('moment')
const { HOST } = require('./src/constants')
const { spawn } = require('child_process');
const db = require('./src/database')
const get_content = require('./access_token')
const fs = require("fs")

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
  token_id = req.params.token_id
  const {name, value} = await get_content(token_id)
  if(!fs.existsSync('./public/images/' + token_id + '.png')) {
    spawn('python3', ['picture_generator.py', name, value, token_id])
  }
  const data = {
    'name': name,
    'description': '"' + value + '"',
    'attributes': {
    },
    'image': `${HOST}/images/${token_id}.png`
  }
  res.send(data)
})

app.listen(app.get('port'), function() {
  console.log('Node app is running on port', app.get('port'));
})
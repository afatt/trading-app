const express = require('express');
const app = express();
const router = express.Router();

const path = __dirname + '/views/';
const port = 8080;

var mysql = require('mysql');

var con = mysql.createConnection({
    host: '35.192.53.116',
    user: 'root',
    password: 'A11igat0rdunkf@rm',
    database: 'userinfo'
});

con.connect(function(err) {
  if (err) throw err;
  con.query("SELECT * FROM users", function (err, result, fields) {
    if (err) throw err;
    console.log(result);
  });
});

const axios = require('axios');

async function makePostRequest() {

    const config = {
        method: 'get',
        url: 'https://api.robinhood.com/api-token-auth/',
        data: {
            username: 'afatt90@gmail.com',
            password: 'THISismylogin@87'
        },
        headers: { 'Accept': 'application/json' }
    }

    let res = await axios(config)

    console.log(res.request._header);
}

makeRequest();

router.get('/', function(req,res){
  res.sendFile(path + 'home.html');
});

router.get('/get_started', function(req,res){
  res.sendFile(path + 'get_started.html');
});

app.use(express.static(path));
app.use('/', router);

app.listen(port, function () {
  console.log('Example app listening on port 8080!')
})

var express = require('express');
var router = express.Router();


// define routes here

router.get('/', (req, res) => {
    res.send('hellow world!')
})

router.post('/', (req, res) => {
    res.send('got a post request')
});

router.put('/user', (req, res) => {
    res.send('got a put request')
});

router.delete('/user', (req, res) => {
    res.send('got a delete request')
});

module.exports = router;
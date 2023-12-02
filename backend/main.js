const express=require('express');
const app=express();
let  router = express.Router()
const fs = require('fs');
const {PythonShell} =require('python-shell');

router.use(express.static(__dirname));


router.get("/",(req, res) => {
    
    res.sendFile(__dirname + '/main.html')

})
module.exports = router

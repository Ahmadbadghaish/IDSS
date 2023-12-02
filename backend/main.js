const express=require('express');
const app=express();
let  router = express.Router()
const fs = require('fs');
const {PythonShell} =require('python-shell');

router.use(express.static('public'));
router.use('/css', express.static(__dirname + 'public/style.css'))
router.use('/js', express.static(__dirname + 'public/function.js'))
router.use('/css', express.static(__dirname + 'public/style2.css'))
router.use('/js', express.static(__dirname + 'public/scripts.js'))

router.get("/upload",(req, res) => {
    res.render('main.html')
})
module.exports = router

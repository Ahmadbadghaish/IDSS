const express=require('express');
const app=express();
const fs = require('fs');
const {PythonShell} =require('python-shell');

router.use(express.static('public'));
router.use('/css', express.static(__dirname + 'public/style.css'))
router.use('/js', express.static(__dirname + 'public/function.js'))
router.use('/css', express.static(__dirname + 'public/style2.css'))
router.use('/js', express.static(__dirname + 'public/scripts.js'))

router.get("/upload",(req, res) => {
    res.render('upload.html')
})

router.post("/upload", (req, res, next)=>{

let pyshell = new PythonShell('team2.py', { mode: 'json' },function  (err, results));
 
fs.createReadStream(req)
.pipe(csv())
.on('data', (row) => {
   pyshell.send(row);
})
res.send(results)
});
 
const port=8000;
app.listen(port, ()=>console.log(`Server connected to ${port}`));

module.exports = router

const express=require('express');
const app=express();
const fs = require('fs');
const {PythonShell} =require('python-shell');
let filledarray=[]


router.use(express.static('public'));
router.use('/css', express.static(__dirname + 'public/style.css'))
router.use('/js', express.static(__dirname + 'public/function.js'))
router.use('/css', express.static(__dirname + 'public/style2.css'))
router.use('/js', express.static(__dirname + 'public/scripts.js'))

router.get("/upload",(req, res) => {
    res.render('upload.html')
})

router.post("/upload", (req, res, next)=>{
    
fs.createReadStream(req)
.pipe(csv())
.on('data', (row) => {
filledarray.push(row)
})
.on('end', () => {
console.log('s');
});
    
let options = {
  mode: 'text',
  pythonOptions: ['-u'], 
  args: [   JSON.stringify(filledarray)]
};
 
PythonShell.run('team2.py', options, function (err, results) {
  res.send(results)
});
 

});

module.exports = router

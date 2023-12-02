const express=require('express');
const app=express();
let  router = express.Router()
const fs = require('fs');
const {PythonShell} =require('python-shell');
let filledarray=[]



router.post('/upload', (req, res, next)=>{
    
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
 
PythonShell.run('python\main.py', options, function (err, results) {
  res.send(results)
});
 

});

module.exports = router

const express = require('express')
let upload=require('./pythonshell')
let main=require('./main')
const app = express()
const port = 3000
const fs = require('fs');
const {PythonShell} =require('python-shell');
let filledarray=[]


app.use('/upload',express.static(__dirname));

app.get('/upload',(req, res) => {
    res.sendFile(__dirname + '/upload.html')
})


app.post('/upload', (req, res, next)=>{
    
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
     
    PythonShell.run('main.py', options, function (err, results) {
      res.sendFile(results)
    });
     
    
    });




app.use('/',main)


app.listen(port, () => console.log(`listening on port 
${port}!`))

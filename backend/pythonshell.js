const express=require('express');
const app=express();
const fs = require('fs');
const {PythonShell} =require('python-shell');


app.get("/", (req, res, next)=>{

let pyshell = new PythonShell('team2.py', { mode: 'json' });
 
fs.createReadStream('data.csv')
.pipe(csv())
.on('data', (row) => {
   pyshell.send(row);
})

});
 
const port=8000;
app.listen(port, ()=>console.log(`Server connected to ${port}`));


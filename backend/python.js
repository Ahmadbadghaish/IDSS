const express=require('express');
const app=express();
 
const {PythonShell} =require('python-shell');
 
app.get("/", (req, res, next)=>{
    let options = {
        mode: 'text',
        pythonOptions: ['-u'], // get print results in real-time 
        args: ['shubhamk314'] //An argument which can be accessed in the script using sys.argv[1]
    };
     
 
    PythonShell.run('python_test.py', options, function (err, result){
          if (err) throw err;
          console.log('result: ', result.toString());
          res.send(result.toString())
    });
});
 
const port=8000;
app.listen(port, ()=>console.log(`Server connected to ${port}`));

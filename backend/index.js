const express = require('express')
let upload=require('./pythonshell')
let main=require('./main')
const app = express()
const port = 3000

app.use('/upload',upload)

app.use('/',main)


app.listen(port, () => console.log(`listening on port 
${port}!`))

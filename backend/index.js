const express = require('express')
let project=require('./pythonshell')
let main=require('./main')
const app = express()
const port = 3000

app.use('/',main)
app.use('/upload',project)


app.listen(port, () => console.log(`listening on port 
${port}!`))

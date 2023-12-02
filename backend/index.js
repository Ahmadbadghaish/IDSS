const express = require('express')
let project=require('./project')
let main=require('./main')
const app = express()
const port = 3000

app.use('/upload',project)
app.use('/',main)

app.listen(port, () => console.log(`listening on port 
${port}!`))

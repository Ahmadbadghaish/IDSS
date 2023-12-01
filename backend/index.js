const express = require('express')
const app = express()
const port = 3000

app.use('/project',project)
app.use('/',main)

app.listen(port, () => console.log(`listening on port 
${port}!`))

const Router = require('express')
const router = new Router()
const productRouter = require('./productRouter')
const userRouter = require('./userRouter')
const adminRouter = require('./adminRouter')
const reviewRouter = require('./reviewRouter')

router.use('/user', userRouter)
router.use('/product', productRouter)
router.use('/admin', adminRouter)
router.use('/reviews', reviewRouter)

module.exports = router
const Router = require('express')
const router = new Router()
const productController = require('../controllers/productController')
const reviewController = require('../controllers/reviewController')

router.post('/', reviewController.create)
router.get('/', productController.getAll)
router.get('/:id', productController.getOne)

module.exports = router
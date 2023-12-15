const uuid = require('uuid')
const path = require('path');
const {Product, Genre} = require('../models/models')
const ApiError = require('../error/ApiError');
const { Sequelize } = require('sequelize');

class ProductController {
    async getAll(req, res) {
        let {genre, priceFrom, priceTo} = req.query
        let products;
        if (!genre && !priceFrom && !priceTo) {
            products = await Product.findAll()
        }
        else if (genre && !priceFrom && !priceTo) {
            const genreIds = JSON.parse(genre);

            products = await Product.findAll({
                include: [{
                    model: Genre,
                    where: {
                        id: {
                            [Sequelize.Op.in]:genreIds
                        }
                    }
                }]
            })
        }
        else if (!genre && (priceFrom || priceTo)) {
            if (!priceFrom)
            {
                priceFrom = 0
            }
            if (!priceTo)
            {
                priceTo = 10000
            }
            
            products = await Product.findAll({
                where: {
                    price: {
                        [Sequelize.Op.between]: [priceFrom, priceTo]
                    }
                }
            });
        }
        else {
            if (!priceFrom)
            {
                priceFrom = 0
            }
            if (!priceTo)
            {
                priceTo = 10000
            }

            const genreIds = JSON.parse(genre);

            products = await Product.findAll({
                where: {
                    price: {
                        [Sequelize.Op.between]: [priceFrom, priceTo]
                    }
                },
                include: [{
                    model: Genre,
                    where: {
                        id: {
                            [Sequelize.Op.in]:genreIds
                        }
                    }
                }]
            });
        }
        return res.json(products)
    }

    async getOne(req, res) {
        const {id} = req.params
        const product = await Product.findOne(
            {
                where: {id}
            },
        )
        return res.json(product)
    }

}

module.exports = new ProductController()
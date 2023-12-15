const uuid = require('uuid')
const path = require('path');
const {Review} = require('../models/models')
const ApiError = require('../error/ApiError');

class ReviewController {
    async create(req, res, next) {
        try {
            const {author, text, date, rate } = req.body;
            const review = await Review.create({author, text, date, rate });

            return res.json(review);
        } catch (e) {
            next(ApiError.badRequest(e.message));
        }
    }

    async get(req, res, next){
        const reviews = await Review.findAll();
        return res.json(reviews)
    }
}

module.exports = new ReviewController();
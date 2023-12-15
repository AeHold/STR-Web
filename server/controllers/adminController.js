const uuid = require('uuid')
const path = require('path');
const bcrypt = require('bcrypt')
const fs = require('fs')
const {Product, Genre, Review, User, ProductGenre} = require('../models/models')
const {Sequelize} = require('sequelize')
const ApiError = require('../error/ApiError');

class adminController{
    async productGet(req, res){
        var products = await Product.findAll()

        return res.json(products)
    }

    async productGetOne(req, res){
        const {id} = req.params
        
        const product = await Product.findOne(
            {
                where: {id}
            },
        )
        return res.json(product)
    }

    async productUpdate(req, res){
        var { name, author, description, price, genres, amount } = req.query;
        const {id} = req.params
        const {img} = req.files
        let posterUrl = uuid.v4() + ".jpg"
        img.mv(path.resolve(__dirname, '..', 'static', fileName))

        const existingProduct = await Product.findOne({where: {id}});

        existingProduct.name = name;
        existingProduct.author = author;
        existingProduct.description = description;
        existingProduct.price = price;
        existingProduct.genres = genres;
        existingProduct.amount = amount;


        await existingProduct.save();

        if (genres) {
            genres = JSON.parse(genres)

            await ProductGenre.destroy({ where: { productId: id } });

            for (var genreId of genres) {
                await ProductGenre.create({ ProductId: id, GenreId: genreId });
              }
        };
        return res.json(existingProduct);

    }

    async productDelete(req, res){
        const {id} = req.params
        var product = Product.destroy({where:{id}});
        return res.json(product);
    }

    async productCreate(req, res){
        let {name, author, description, price, genreId, amount} = req.query

        const product = await Product.create({name, author, description, price, genreId, amount});

        const { data } = req.files.file;
        
        const filePath = path.join(__dirname+'/images/', product.id+'.png');

        fs.writeFileSync(filePath, data)

        return res.json(product)
    }
    
    async userGet(req, res){
        var users = await User.findAll()

        return res.json(users)
    }

    async userGetOne(req, res){
        const {id} = req.params
        
        const user = await User.findOne(
            {
                where: {id}
            },
        )
        return res.json(user)
    }

    async userUpdate(req, res){
        const { email, password, role } = req.query;
        const {id} = req.params
        const userToUpdate = await User.findOne({
            where: {id}
        });

        console.log(req.query)

        if (email) userToUpdate.email = email;
        if (password) userToUpdate.password = password;
        if (role) userToUpdate.role = role;
        console.log(userToUpdate)

        await userToUpdate.save();

        return res.json(userToUpdate)
    }

    async userDelete(req, res){
        const {id} = req.params
        var user = User.destroy({where:{id}});
        return res.json(user);
    }

    async userCreate(req, res){
        const { email, password, role } = req.query;

        var hashPassword
        if (password) {
            hashPassword = await bcrypt.hash(password, 1)
        }
        
        const newUser = await User.create({
        email: email,
        password: hashPassword,
        role: role || 'user' 
        });

        return res.json(newUser)
    }
    
    async genresGet(req, res){
        var genres = await Genre.findAll()

        return res.json(genres)
    }

    async genresGetOne(req, res){
        const {id} = req.params
        
        const genre = await Genre.findOne(
            {
                where: {id}
            },
        )
        return res.json(genre)
    }

    async genresUpdate(req, res){
        const {id} = req.params
        const { name } = req.query;

        const genreToUpdate = await Genre.findOne(
            {
                where: {id}
            },
        )

        if (name) genreToUpdate.name = name;
        await genreToUpdate.save();

        return res.json(genreToUpdate)
    }
    async genresDelete(req, res){
        const {id} = req.params
        var genre = Genre.destroy({where:{id}});
        return res.json(genre);
    }

    async genresCreate(req, res){
        const { name } = req.query;


        const newGenre = await Genre.create({
            name: name
        });
        return res.json(newGenre);
    }
    
    async reviewsGet(req, res){
        var reviews = await Review.findAll()

        return res.json(reviews)
    }

    async reviewsGetOne(req, res){
        const {id} = req.params
        
        const review = await Review.findOne(
            {
                where: {id}
            },
        )
        return res.json(review)
    }

    async reviewsUpdate(req, res){
        const {id} = req.params; 
        const reviewToUpdate = await Review.findOne(
            {
                where: {id}
            },
        )

        const { text, rate, date , userId} = req.query;

        if (text) reviewToUpdate.text = text;
        if (rate) reviewToUpdate.rate = rate;
        if (date) reviewToUpdate.date = date;
        if (userId) reviewToUpdate.userId = userId;

        await reviewToUpdate.save();
        return res.json(reviewToUpdate)
    }

    async reviewsDelete(req, res){
        const {id} = req.params
        var review = Review.destroy({where:{id}});
        return res.json(review);
    }

    async reviewsCreate(req, res){
        const { text, rate, date, userId } = req.query;

        const newReview = await Review.create({
        text: text,
        rate: rate,
        date: date,
        userId: userId
        });

        console.log(newReview)

        return res.json(newReview)
    }
}

module.exports = new adminController()

const sequelize = require('../db')
const {DataTypes} = require('sequelize')

const User = sequelize.define('user', {
    id: {type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true},
    email: {type: DataTypes.STRING, unique: true,},
    password: {type: DataTypes.STRING},
    role: {type: DataTypes.STRING, defaultValue: "USER"},
})

const Product = sequelize.define('product', {
    id: {type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true},
    name: {type: DataTypes.STRING, unique: true,},
    author: {type: DataTypes.STRING},
    description: {type: DataTypes.STRING},
    price: {type: DataTypes.INTEGER},
    amount: {type: DataTypes.INTEGER},
})

const Genre = sequelize.define('type', {
    id: {type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true},
    name: {type: DataTypes.STRING, unique: true, allowNull: false},
})

const Review = sequelize.define('review', {
    id: {type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true},
    text: {type: DataTypes.STRING},
    date:{type:DataTypes.DATE},
    rate: {type: DataTypes.INTEGER, allowNull: false},
})

const ProductGenre = sequelize.define('product_genre', {
    id: {type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true},
})

Product.belongsToMany(Genre, {through: ProductGenre})
Genre.belongsToMany(Product, {through: ProductGenre})

User.hasMany(Review)
Review.belongsTo(User)

module.exports = {
    User,
    Product,
    Genre,
    Review
}
const {Sequelize} = require('sequelize')

module.exports = new Sequelize(
        'bookshop',
        'postgres',
        'postgres',
        {
            dialect: 'postgres',
            host: 'localhost',
            port: 6401
        }
)
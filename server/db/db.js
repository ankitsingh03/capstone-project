const Sequelize = require('sequelize')
const db = new Sequelize(
  process.env.DATABASE_URL || 'postgresql://ankushproject:ankush@localhost:5432/ankushdb', {
    logging: false
  }
)
module.exports = db

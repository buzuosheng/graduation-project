'use strict';

module.exports = app => {
  const { STRING } = app.Sequelize;

  const Tv = app.model.define('tv', {
    title: {
      type: STRING(255),
      primaryKey: true,
    },
    alias: STRING(255),
    url: STRING(50),
    tv_img: STRING(70),
    director: STRING(20),
    actors: STRING(50),
    tv_type: STRING(50),
    c_or_r: STRING(10),
    first_time: STRING(10),
    series: STRING(10),
    single: STRING(10),
    rate: STRING(10),
    votes_num: STRING(10),
    synopsis: STRING(255),
  }, {
    freezeTableName: true,
    tableName: 'tv',
    timestamps: false,
  });

  return Tv;
};


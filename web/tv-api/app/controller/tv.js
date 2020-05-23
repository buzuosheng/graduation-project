'use strict';

const Controller = require('egg').Controller;

class TvController extends Controller {
  async index() {
    const _ctx = this.ctx;
    const tv = await _ctx.model.Tv.findAll();
    _ctx.body = tv;
  }
}

module.exports = TvController;

var express = require('express');
var router = express.Router();
var logger = require("../utils/logger");
var MoviesController = require('../controllers/moviesController');

router.get('/movies', function (request, response) {
    var query = request.query.query;
    var from = request.query.from;
    var size = request.query.size;
    var filters = getFilters(request);
    var moviesController = new MoviesController();
    moviesController.searchAll(query, filters, from, size, function(err, res) {
        if (err) {
            logger.error("Error calling movies.searchAll", err);
            response.status(500).end();
        }

        response.status(200).send(res);
    })
});

function getFilters(request) {
    var filters = [];
    for (var propName in request.query) {
        if (request.query.hasOwnProperty(propName) &&
            propName != 'query' &&
            propName != 'from' &&
            propName != 'size') {
            filters.push({propName: request.query.propName});
        }
    }
    return filters;
}

module.exports = router;
var package = require(“./package.json”);
var grounder = require(“./lib/grounder.js”);
console.log(“loaded ” + package.name + “, version ” + package.version);
exports.handler = function (event, context) {
grounder.handleRequest(event, context.done);
}
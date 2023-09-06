const path = require("path");

module.exports = {
	entry: "./static/ts/index.ts",
	output: {
		filename: "index.js",
		path: path.resolve(__dirname, "static", "js"),
	},

	module: {
		rules: [
			{
				exclude: /node_modules/,
				test: /\.ts$/,
				use: "ts-loader",
			},
		],
	},

	resolve: {
		extensions: [".js", ".ts"],
	},
};

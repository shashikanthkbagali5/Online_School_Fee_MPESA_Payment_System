;(function (undefined) {
	'use strict';

	require.config({
		baseUrl: './src/js',
		paths: {
			jquery: [
				'https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min',
				'../../vendor/jquery/dist/jquery.min.js'
			],
			bootstrap: [
				'../../vendor/bootstrap/dist/js/bootstrap.min'
			],
			maskloader: [
				'../../dist/jquery.maskloader'
			]
		},
		shim: {
			'jquery.maskloader': ['jquery'],
			'bootstrap': ['jquery'],
			'maskloader': ['jquery']
		}
	});

	requirejs(['jquery', 'bootstrap'], function ($) {
		$.noConflict();
		require(['App']);
	});

})();
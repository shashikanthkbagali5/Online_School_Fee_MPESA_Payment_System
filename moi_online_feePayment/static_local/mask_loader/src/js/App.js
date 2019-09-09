define('App', ['jquery', 'maskloader'], function($){



	$('#bt-body').click(function(e){
		e.stopPropagation();
		var maskloader = $('body').maskLoader({
			imgLoader: './dist/giphy.gif'
		});

		setTimeout(function(){
			maskloader.destroy();
		},3000);
	});

	$('#bt-panel').click(function(e){
		e.stopPropagation();
		var maskloader = $('.panel-info').maskLoader({
			imgLoader:'./dist/ele-running.gif'
		});

		setTimeout(function(){
			maskloader.destroy();
		},3000);
	});

	$('#bt-formgroup').click(function(e){
		e.stopPropagation();
		var maskloader = $('form').maskLoader({
			imgLoader: './dist/preloaders.gif'
		});

		setTimeout(function(){
			maskloader.destroy();
		},10000);
	});


	/**
	* Exemplo de handle ajax.
	*/

	$.ajax({
		url:'http://cep.correiocontrol.com.br/82400470.json',
		maskLoaderSettings: {
			element:$('body').first(),
			background:'black',
			opacity:'0.2',
			textAlert:'TEST'
		},
		success:function(data){
			console.log(data);
		}
	});


});

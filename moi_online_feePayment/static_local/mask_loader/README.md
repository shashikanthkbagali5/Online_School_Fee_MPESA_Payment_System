jQuery Mask Loader
==================

Simple Jquery plugin preloader for ajax, etc. Easy to use.

Demo page: http://rafaelortegabueno.com/jquery_maskloader/


Installation
------------
1. Installation via Bower:
```bash
bower install maskloader
```
* your HTML file:
```html
<html>
  <head>
    <title>Mask Loader Example</title>
    <link rel="stylesheet" type="text/css" href="bower_components/maskLoader/dist/maskloader.css"/>
  </head>
  <body>
    <!-- Your html -->
    
    <script type="text/javascript" src="bower_components/jquery/dist/jquery.min.js"/>
    <script type="text/javascript" src="bower_components/maskLoader/dist/jquery.maskloader.js"/>
    <script type="text/javascript">
      // YOUR JS CODES
    </script>
  </body>
</html>
```

Basic Usage:
------------
```javascript
// When use ajax, before send requests
// You can use any element that serves as a container html, tags like "body", classes and ids
var maskloader = $('body').maskLoader();

// After success callback execute
maskloader.destroy();
```

Options:
--------
```javascript
var maskloader = $('.container').maskLoader({
  'fade': true,
  'z-index': '999',
  'background': 'white', // Background overlay
  'opacity': '0.6', // Opacity overlay
  'imgLoader': false, // Path for image preloader :)
  'autoCreate':true // If false, you will have to run the "create" function. Ex: $('body').maskLoader().create(); 
});
```

jQuery Ajax default Handle:
------------
```javascript
$.ajax({
  url:'http://cep.correiocontrol.com.br/82400470.json',
		maskLoaderSettings: {
			element:$('body'),
			background:'black',
			opacity:'0.2',
			textAlert:'TEST'
		},
		success:function(data){
			console.log(data);
		}
});
```

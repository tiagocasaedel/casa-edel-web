
var app = angular.module('app', [
								'ngRoute',
								'ngAnimate',
								'angulartics',
								'angulartics.google.analytics',
								'slickCarousel',
		  					    'ngFileUpload',
								'ngResource',
								'ngMap',
								'ngResource',
								'LocalStorageModule',
								'ngclipboard'
							    ]);


/***************
	 CONFIG
****************/

app.config(config);

config.$inject = ['$routeProvider', '$locationProvider', '$httpProvider'];

function config($routeProvider, $locationProvider, $httpProvider){


	$routeProvider.
		when('/home',{
			templateUrl: 'views/home.html',
			controller: 'home',
			controllerAs: 'vm'
		}).
		when('/productos/', {
			templateUrl: 'views/productos-g.html',
			controller: 'productos.linea',
			controllerAs: 'vm'
		}).
		when('/productos/linea-gabinetes', {
			templateUrl: 'views/productos-g.html',
			controller: 'productos.linea',
			controllerAs: 'vm'
		}).
		when('/productos/linea-gabinetes/:id', {
			templateUrl: 'views/productos-g-cat-prod.html',
			controller: 'productos.g.cat.prod',
			controllerAs: 'vm'
		}).
		when('/novedades/', {
			templateUrl: 'views/novedades.html',
			controller: 'novedades',
			controllerAs: 'vm'
		}).
		when('/novedades/:id', {
			templateUrl: 'views/novedades.detalle.html',
			controller: 'novedades.detalle',
			controllerAs: 'vm'
		}).
		when('/descargas/', {
			templateUrl: 'views/descargas.html',
			controller: 'descargas',
			controllerAs: 'vm'
		}).
		when('/descargas/:id', {
			templateUrl: 'views/descargas.html',
			controller: 'descargas',
			controllerAs: 'vm'
		}).
		when('/sobre-genrod/', {
			templateUrl: 'views/nosotros.html',
			controller: 'nosotros',
			controllerAs: 'vm'
		}).
		when('/nuestras-plantas/', {
			templateUrl: 'views/plantas.html',
			controller: 'plantas',
			controllerAs: 'vm'
		}).
		when('/historia/', {
			templateUrl: 'views/historia.html',
			controller: 'historia',
			controllerAs: 'vm'
		}).
		when('/rrhh/', {
			templateUrl: 'views/rrhh.html',
			controller: 'rrhh',
			controllerAs: 'vm'
		}).
		when('/contacto/', {
			templateUrl: 'views/consultas.html',
			controller: 'consultas',
			controllerAs: 'vm'
		}).
		when('/instalaciones-seguras/', {
			templateUrl: 'views/instalaciones.html',
			controller: 'instalaciones',
			controllerAs: 'vm'
		}).
		when('/politica-de-privacidad/', {
			templateUrl: 'views/politica-de-privacidad.html',
			controller: 'politica',
			controllerAs: 'vm'
		}).
		otherwise({
			redirectTo: '/home'
		});

	$locationProvider.html5Mode(true);

}


/***************
	 RUN
****************/

app.run(run);

run.$inject = ['$rootScope', '$timeout', '$window', '$location', '$http'];

function run($rootScope, $timeout, $window, $location, $http){

	$rootScope.form = JSON.parse(localStorage.getItem('genrod_form')) || { name: '', email: '', tipo: '', file: '' }
	$rootScope.first = false;
	if($rootScope.form.name)
		$rootScope.first = true;
	

	$(window).load(function(){
		$timeout(function(){
			$('html').addClass('loaded');			
			$timeout(function () {
				// $('main').removeClass('enter-y');
			}, 1000)
		}, 1000)
	});

	$rootScope.changing = false;
	$rootScope.$on('$routeChangeStart', function($event, next, current) {
		$rootScope.showNav = false;
		$rootScope.activeNav = false;
		$('html').addClass('changing').removeClass('loaded');			
  	});

	$rootScope.$on('$routeChangeSuccess', function(){
		//ga('send', 'pageview', $location.path());
		if(dataLayer)
			dataLayer.push({
				event: 'route',
				attributes: {
					route: $location.path()
				}
			});
		$('body,html').animate({'scrollTop': 0},1200);
		$rootScope.showNav = false;
		$timeout(function () {
			// $('main').removeClass('enter-y');
			$('html').removeClass('changing').addClass('loaded');		
		}, 2000)
	});

	$rootScope.toggleNav = function(){
		$rootScope.showNav = !$rootScope.showNav;
	}

	$rootScope.consulta = function (name) {
		$rootScope.consultaPor = name;
		$location.path('contacto');
	}
	
	var divName = 'pointer';
	var offX = 10;          
	var offY = 10;          

	function mouseX(evt) { if (!evt) evt = window.event; if (evt.pageX) return evt.pageX; else if (evt.clientX) return evt.clientX + (document.documentElement.scrollLeft ? document.documentElement.scrollLeft : document.body.scrollLeft); else return 0; }
	function mouseY(evt) { if (!evt) evt = window.event; if (evt.pageY) return evt.pageY; else if (evt.clientY) return evt.clientY + (document.documentElement.scrollTop ? document.documentElement.scrollTop : document.body.scrollTop); else return 0; }

	function follow(evt) {
		var obj = $('#pointer');
		// obj.left = (parseInt(mouseX(evt)) - offX) + 'px';
		// obj.top = (parseInt(mouseY(evt)) - offY) + 'px';
		obj.stop().animate({ left: (parseInt(mouseX(evt)) - offX) + 'px', top: (parseInt(mouseY(evt)) - offY) + 'px' }, 500, 'easeOutCirc')
	}
	document.onmousemove = follow;

}

app.directive('linkeable',
	function ($timeout) {
		return {
			restrict: 'A',
			link: function ($scope, $element) {
				$element.hover(function () {
					$('#pointer').addClass('big');
					if($element.hasClass('green-bg'))
						$('#pointer').addClass('white');
				}, function(){
					$('#pointer').removeClass('big white');
				});
				$element.click(function () {
					$('#pointer').addClass('big2');
					$timeout(function(){
						$('#pointer').removeClass('big2');
					}, 100)
				});
			}
		};
	});

app.directive('descarga',
	function ($timeout) {
		return {
			restrict: 'A',
			link: function ($scope, $element) {
				$element.click(function(){
					if ($element.parent().hasClass('active')) {
						$element.parent().removeClass('active');
						$element.parent().find('.body').slideUp();
					} else {
						$('.descarga').removeClass('active');
						$('.descarga .body').slideUp();
						$element.parent().addClass('active');
						$element.parent().find('.body').slideDown();
						$timeout(function(){
							$('html,body').animate({ scrollTop: $element.parent().offset().top - 30}, 500);
						}, 500)
					}
				})
			}
		};
	});


/***************
	 COMMON
****************/

app.service('Common', Common);

Common.$inject = ['$rootScope', '$timeout', '$http'];

function Common($rootScope, $timeout, $http){

	this.functions = function(){

		// var url = window.location.pathname;
		// $http.get('/api/seo').
		//   then(function(response) {
		// 		var out = null;
		// 		if(response.data.length > 0)
		// 			response.data.forEach(function(d){
		// 				if(d.link == url)
		// 					out = d;
		// 			})
		// 		if(out) $rootScope.tit = out.tags.title;
		//   });

		// if(window.innerWidth > 1100){

			var controller = new ScrollMagic.Controller();
			var showArray = [];
			var count = 0;
			$rootScope.consultaPor = '';

			setTimeout(function() {

				$('.show-me').each(function(i,v){

					var $self = $(this);
					var id = '#' + $self.attr('id');
					var off = $self.attr('data-offset') || -200;

					showArray[i] = new ScrollMagic.Scene({
						triggerElement: id,
						duration: $self.outerHeight(),
						offset: off
					})
					.addTo(controller);

					showArray[i].on('enter',function(){
						$self.addClass('show');
					});
					showArray[i].on('leave',function(){
						// $self.removeClass('show');
					});

				});

			}, 2000);

			// setTimeout(function() {
			// 	if(window.innerWidth > 1000)
			// 		parallax();
			// }, 1000);
			// function parallax(){
			// 	$(window).scroll(function() {
			// 		if($rootScope.scroll){
			// 			$('[data-speed]').each(function() {
			// 		    	var $scroll = $(this);
			// 		    	var yPos    = -(($(window).scrollTop() - $scroll.closest('.parallax').offset().top) / $scroll.data('speed'));
			// 		    	var top     = yPos + 'px';
			// 		    	TweenLite.to($scroll, 1, {y: top, ease: "Circ.easeOut"});
			//
			// 		    });
			// 	    	var scroll = Math.max(document.body.scrollTop,document.documentElement.scrollTop);
			// 		}
			//     });
			// }
		// }

	}

}


/**********************
    HOME CONTROLLER
**********************/

app.controller('home', home);

home.$inject = ['Common', '$rootScope', '$timeout', '$interval', '$window', '$http'];

function home(Common, $rootScope, $timeout, $interval, $window, $http){

	var vm = this;
	$rootScope.tit = 'GENROD / Instalaciones seguras';
	$rootScope.section = 'home';

	Common.functions();

	vm.goDown = function(){
		$('html, body').animate({'scrollTop': window.innerHeight}, 700);
	}

	vm.slickConfig = {
		fade: true,
		autoplay: true,
		dots: true,
		autoplaySpeed: 5000,
		arrows: false,
		pauseOnHover: false,
		event: {
			afterChange: function (event, slick, currentSlide, nextSlide) {
				if (currentSlide == 1){
					vm.black = 'white';
				} else if (currentSlide == 2){
					vm.black = 'black';
				} else {
					vm.black = '';
				}
			},
		}
	};


}

/**********************
    PRODUCTOS CONTROLLER
**********************/

app.controller('productos', productos);

productos.$inject = ['Common', '$rootScope', '$timeout', '$interval', '$window', '$http'];

function productos(Common, $rootScope, $timeout, $interval, $window, $http) {

	var vm = this;
	$rootScope.tit = 'GENROD / Productos';
	$rootScope.section = 'productos';

	Common.functions();

	vm.goDown = function () {
		$('html, body').animate({ 'scrollTop': window.innerHeight }, 700);
	}

}


/**********************
    PRODUCTOS CONTROLLER
**********************/

app.controller('productos.linea', productoslinea);

productoslinea.$inject = ['Common', '$rootScope', '$timeout', '$interval', '$window', '$http'];

function productoslinea(Common, $rootScope, $timeout, $interval, $window, $http) {

	var vm = this;
	$rootScope.tit = 'GENROD / Productos';
	$rootScope.section = 'productos';

	Common.functions();

	vm.goDown = function () {
		$('html, body').animate({ 'scrollTop': window.innerHeight }, 700);
	}

	$http.get('products.json').then(function (res) {
		vm.products = res.data;
	});

	vm.viewTipo = function (id) {
		vm.active = id;
	}

}

/**********************
    PRODUCTOS E CAT CONTROLLER
**********************/

app.controller('productos.e.cat', productoscat);

productoscat.$inject = ['Common', '$rootScope', '$timeout', '$routeParams', '$window', '$http'];

function productoscat(Common, $rootScope, $timeout, $routeParams, $window, $http) {

	var vm = this;
	$rootScope.tit = 'GENROD / Productos';
	$rootScope.section = 'productos';
	vm.id = $routeParams.cat;

	Common.functions();

	vm.goDown = function () {
		$('html, body').animate({ 'scrollTop': window.innerHeight }, 700);
	}
	
	$http.get('products.json').then(function (res) {
		vm.products = res.data;
		vm.products.electric.forEach(function(c){
			if(c.url == vm.id){
				vm.categoria = c;
			}
		})
	});
}


/**********************
    PRODUCTOS E CAT PROD CONTROLLER
**********************/

app.controller('productos.e.cat.prod', productosecatprod);

productosecatprod.$inject = ['Common', '$rootScope', '$timeout', '$routeParams', '$window', '$http'];

function productosecatprod(Common, $rootScope, $timeout, $routeParams, $window, $http) {

	var vm = this;
	$rootScope.tit = 'GENROD / Productos';
	$rootScope.section = 'productos';
	vm.active = 2;
	vm.cat = $routeParams.cat;
	vm.id = $routeParams.id;

	Common.functions();

	vm.goDown = function () {
		$('html, body').animate({ 'scrollTop': window.innerHeight }, 700);
	}

	vm.slickConfig = {
		fade: true,
		autoplay: true,
		dots: true,
		autoplaySpeed: 5000,
		arrows: false,
		pauseOnHover: false
	};

	vm.slickConfig2 = {
		arrows: false,
		slidesToShow: 5,
		responsive: [
			{
				breakpoint: 1101,
				settings: {
					slidesToShow: 3
				}
			},
			{
				breakpoint: 500,
				settings: {
					slidesToShow: 1
				}
			}
		]
	};

	vm.slickConfig3 = {
		arrows: false,
		fade: true,
		initialSlide: 2
	};

	vm.beforeSlide = function () {
		$('#tipos').slick('slickPrev');
	}

	vm.nextSlide = function () {
		$('#tipos').slick('slickNext');
	}

	vm.viewTipo = function (id) {
		vm.active = id;
		$('#descripciones').slick('slickGoTo', id);
	}

	console.log(vm.cat, vm.id);
	$http.get('products.json').then(function (res) {
		vm.products = res.data;
		vm.products.electric.forEach(function (c) {
			if (c.url == vm.cat) {
				vm.categoria = c;
				console.log(vm.categoria);
				if(vm.id == 'detalle'){
					vm.product = c;
				} else {
					c.products.forEach(function(p){
						if(p.url == vm.id){
							vm.product = p;
							console.log(vm.product);
						}
					})
				}
			}
		})
	});

}


/**********************
    PRODUCTOS G CAT PROD CONTROLLER
**********************/

app.controller('productos.g.cat.prod', productoscatprod);

productoscatprod.$inject = ['Common', '$rootScope', '$timeout', '$routeParams', '$window', '$http'];

function productoscatprod(Common, $rootScope, $timeout, $routeParams, $window, $http) {

	var vm = this;
	$rootScope.tit = 'GENROD / Productos';
	$rootScope.section = 'productos';
	vm.active = 2;
	vm.id = $routeParams.id;

	Common.functions();

	vm.goDown = function () {
		$('html, body').animate({ 'scrollTop': window.innerHeight }, 700);
	}

	vm.slickConfig = {
		fade: true,
		autoplay: true,
		dots: true,
		autoplaySpeed: 5000,
		arrows: false,
		pauseOnHover: false
	};

	vm.slickConfig2 = {
		arrows: false,
		slidesToShow: 5,
		responsive: [
			{
				breakpoint: 1101,
				settings: {
					slidesToShow: 3
				}
			},
			{
				breakpoint: 500,
				settings: {
					slidesToShow: 1,
					initialSlide: 2					
				}
			}
		],
		event: {
			afterChange: function (event, slick, currentSlide, nextSlide) {
				if (window.innerWidth <= 500) {
					vm.viewTipo(currentSlide);
				}
			},
		}
	};

	if (window.innerWidth <= 500) {
		$('slick#tipos').slick('slickGoTo', 0);
	}

	vm.slickConfigC = {
		arrows: false,
		slidesToShow: 3,
		responsive: [
			{
				breakpoint: 500,
				settings: {
					slidesToShow: 1
				}
			}
		]
	};

	vm.slickConfig3 = {
		arrows: false,
		fade: true,
		initialSlide: 2
	};

	vm.beforeSlide = function () {
		$('#tipos').slick('slickPrev');
	}

	vm.nextSlide = function () {
		$('#tipos').slick('slickNext');
	}

	vm.beforeSlide2 = function () {
		$('#complementos').slick('slickPrev');
	}

	vm.nextSlide2 = function () {
		$('#complementos').slick('slickNext');
	}

	vm.viewTipo = function (id) {
		vm.active = id;
		$('#descripciones').slick('slickGoTo', id);
	}

	$http.get('products.json').then(function (res) {
		vm.products = res.data;
		vm.products.gabinetes.forEach(function (c) {
			if (c.url == vm.id) {
				vm.product = c;
			}
		})
	});

}

/**********************
    NOVEDADES CONTROLLER
**********************/

app.controller('novedades', novedades);

novedades.$inject = ['Common', '$rootScope', '$timeout', '$interval', '$window', '$http'];

function novedades(Common, $rootScope, $timeout, $interval, $window, $http) {

	var vm = this;
	$rootScope.tit = 'GENROD / Novedades';
	$rootScope.section = 'novedades';

	Common.functions();

	vm.goDown = function () {
		$('html, body').animate({ 'scrollTop': window.innerHeight }, 700);
	}

	$http.get('/api/noticias')
		.then(function(resp){
			vm.novedades = resp.data;
			vm.novedades.forEach(function(n){
				n.items.forEach(function (i) {
					if (i.class == 'texto' && !n.text) {
						n.text = strip(i.text);
					}
				})
			})
		})
		.catch(function(err){
			console.log(err);
		})

	function strip(html) {
		var tmp = document.createElement("DIV");
		tmp.innerHTML = html;
		return tmp.textContent || tmp.innerText || "";
	}

}


/**********************
    NOVEDADES DETALLE CONTROLLER
**********************/

app.controller('novedades.detalle', novedadesdet);

novedadesdet.$inject = ['Common', '$rootScope', '$timeout', '$routeParams', '$window', '$http'];

function novedadesdet(Common, $rootScope, $timeout, $routeParams, $window, $http) {

	var vm = this;
	$rootScope.tit = 'GENROD / Novedades';
	$rootScope.section = 'novedades';
	vm.id = $routeParams.id;

	Common.functions();

	vm.goDown = function () {
		$('html, body').animate({ 'scrollTop': window.innerHeight }, 700);
	}

	$http.get('/api/noticias')
		.then(function (resp) {
			vm.novedades = resp.data;
			vm.novedades.forEach(function (n) {
				if(n.url == vm.id){
					vm.novedad = n;
				} else {
					n.items.forEach(function (i) {
						if (i.class == 'texto' && !n.text) {
							n.text = strip(i.text);
						}
					})
				}
			})
		})
		.catch(function (err) {
			console.log(err);
		})

	function strip(html) {
		var tmp = document.createElement("DIV");
		tmp.innerHTML = html;
		return tmp.textContent || tmp.innerText || "";
	}

}



/**********************
    DESCARGAS CONTROLLER
**********************/

app.controller('descargas', descargas);

descargas.$inject = ['Common', '$rootScope', '$timeout', '$routeParams', '$window', '$http'];

function descargas(Common, $rootScope, $timeout, $routeParams, $window, $http) {

	var vm = this;
	$rootScope.tit = 'GENROD / Descargas';
	$rootScope.section = 'descargas';
	vm.id = $routeParams.id;
	$timeout(function(){
		if (vm.id) {
			var id = '#d-' + vm.id;
			$(id).click();
		}
	}, 2000)

	Common.functions();

	vm.goDown = function () {
		$('html, body').animate({ 'scrollTop': window.innerHeight }, 700);
	}

}


/**********************
	NOSOTROS CONTROLLER
**********************/

app.controller('nosotros', nosotros);

nosotros.$inject = ['Common', '$rootScope', '$timeout', '$interval', '$location', '$http'];

function nosotros(Common, $rootScope, $timeout, $interval, $location, $http) {

	var vm = this;
	$rootScope.tit = 'GENROD / Nosotros';
	$rootScope.section = 'nosotros';

	Common.functions();

	vm.goDown = function () {
		$('html, body').animate({ 'scrollTop': window.innerHeight }, 700);
	}


}

/**********************
	HISTORIA CONTROLLER
**********************/

app.controller('historia', historia);

historia.$inject = ['Common', '$rootScope', '$timeout', '$interval', '$location', '$http'];

function historia(Common, $rootScope, $timeout, $interval, $location, $http) {

	var vm = this;
	$rootScope.tit = 'GENROD / Historia';
	$rootScope.section = 'historia';

	Common.functions();

	vm.goDown = function () {
		$('html, body').animate({ 'scrollTop': window.innerHeight }, 700);
	}


}

/**********************
	INSTALACIONES CONTROLLER
**********************/

app.controller('instalaciones', instalaciones);

instalaciones.$inject = ['Common', '$rootScope', '$timeout', '$interval', '$location', '$http'];

function instalaciones(Common, $rootScope, $timeout, $interval, $location, $http) {

	var vm = this;
	$rootScope.tit = 'GENROD / Instalaciones seguras';
	$rootScope.section = 'instalaciones';

	Common.functions();

	vm.goDown = function () {
		$('html, body').animate({ 'scrollTop': window.innerHeight }, 700);
	}


}

/**********************
	RRHH CONTROLLER
**********************/

app.controller('rrhh', rrhh);

rrhh.$inject = ['Common', '$rootScope', '$timeout', '$scope', '$location', '$http', 'Upload'];

function rrhh(Common, $rootScope, $timeout, $scope, $location, $http, Upload) {

	var vm = this;
	$rootScope.tit = 'GENROD / RRHH';
	$rootScope.section = 'rrhh';
	vm.loadingP = 0;
	vm.loading = false;
	vm.sended = false;
	vm.form = {
		name: '',
		email: '',
		provincia: '',
		areadepostulacion: '',
		localidad: '',
		file: '',
		tel: '',
		consulta: ''
	}

	Common.functions();

	vm.goDown = function () {
		$('html, body').animate({ 'scrollTop': window.innerHeight }, 700);
	}

	vm.uploadImagen = function (file) {
		// var name = Math.floor((Math.random() * 1000) + 1) + '-' + file.name;
		Upload.upload({
			url: '/upload-rrhh',
			headers: { 'Content-Type': file.type },
			method: 'POST',
			// data: { 'name': name, 'route': 'colecciones/' },
			file: file,
		}).then(function (resp) {
			// message(file.name + ' subido correctamente.');
			vm.form.file = resp.data;
			vm.loadingP = 'success';
			// f.imagen = name;
		}, function (resp) {
			$scope.success = 'Error: ' + resp.status + ', por favor intente nuevamente';
		}, function (evt) {
			vm.loadingP = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
		});
	}

	vm.send = function () {
		vm.sended = true;
		console.log('send');
		if (vm.form.name.length > 3 && validateEmail(vm.form.email) && vm.form.localidad.length > 3 && vm.form.provincia && vm.form.file && vm.form.tel.length > 3 && !isNaN(vm.form.tel)) {
			vm.loading = true;
			vm.message = 'Enviando...';
			$http.post('/api/rrhh', vm.form)
				.then(function (response) {
					vm.message = 'Gracias ' + vm.form.name + ' por tu tiempo, tus datos ya se han enviado al departamento de RRHH.';
					$timeout(function () {
						vm.form = {
							name: '',
							email: '',
							provincia: '',
							areadepostulacion: '',
							localidad: '',
							file: '',
							tel: '',
							consulta: ''
						}
						vm.message = '';
						vm.sended = false;
						vm.loading = false;
						window.location.reload();
					}, 2500)
				}).catch(function (err) {
					console.log(err);
				});
		} else {
			vm.message = 'Por favor, completa todos los campos obligatorios correctamente.';
		}
	}

	function validateEmail(email) {
		var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
		return re.test(String(email).toLowerCase());
	}


}

/**********************
	PLANTAS CONTROLLER
**********************/

app.controller('plantas', plantas);

plantas.$inject = ['Common', '$rootScope', '$timeout', '$interval', '$location', '$http'];

function plantas(Common, $rootScope, $timeout, $interval, $location, $http) {

	var vm = this;
	$rootScope.tit = 'GENROD / Nuestras plantas';
	$rootScope.section = 'plantas';

	Common.functions();

	vm.goDown = function () {
		$('html, body').animate({ 'scrollTop': window.innerHeight }, 700);
	}

	vm.goToMap = function(id){
		$('html, body').animate({ 'scrollTop': $('#ubicacion').offset().top }, 700);
		vm.activeMarker = id;
	}

	vm.showCopied = function(e){
		var e = $(e.currentTarget).parent().find('.copiedLink');
		console.log(e);
		e.addClass('show');
		$timeout(function () {
			e.removeClass('show');
		}, 1500);
	}

}

/**********************
	CONTACTO CONTROLLER
**********************/

app.controller('consultas', contacto);

contacto.$inject = ['Common', '$rootScope', '$timeout', '$interval', '$location', '$http'];

function contacto(Common, $rootScope, $timeout, $interval, $location, $http) {

	var vm = this;
	$rootScope.section = 'consultas';
	$rootScope.tit = 'GENROD / Consultas';
	vm.loading = false;
	vm.sended = false;
	vm.form = {
		name: '',
		email: '',
		tel: '',
		provincia: '',
		localidad: '',
		tipo: '',
		consulta: '',
		asunto: 'Consulta'
	}

	if ($rootScope.consultaPor){
		vm.form.consulta = 'Me gustaría consultar por ' + $rootScope.consultaPor;
		vm.form.asunto = $rootScope.consultaPor;
	}

	Common.functions();

	vm.goDown = function () {
		$('html, body').animate({ 'scrollTop': window.innerHeight }, 700);
	}

	vm.send = function(){
		vm.sended = true;
		if (vm.form.name.length > 3 && validateEmail(vm.form.email) && vm.form.consulta.length > 10 && vm.form.tipo){
			vm.loading = true;
			vm.message = 'Enviando...';
			$http.post('/api/consultas', vm.form)
				.then(function (response) {
					vm.message = 'Gracias ' + vm.form.name + ' por tu tiempo, nos pondremos en contacto con vos a la brevedad.';
					$timeout(function () {
						vm.form = {
							name: '',
							email: '',
							provincia: '',
							localidad: '',
							tel: '',
							consulta: '',
							asunto: 'Consulta'
						}
						vm.message = '';
						vm.sended = false;
						vm.loading = false;
						ga('send', 'event', {
							eventCategory: 'Contacto',
							eventAction: 'Envío'
						});
						window.location.reload();
					}, 2500)
				}).catch(function (err) {
					console.log(err);
				});
		} else {
			vm.message = 'Por favor, completa todos los campos obligatorios correctamente.';
		}
	}
	
	function validateEmail(email) {
		var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
		return re.test(String(email).toLowerCase());
	}

}

/**********************
	DOWNLOAD CONTROLLER
**********************/

app.controller('download', download);

download.$inject = ['Common', '$rootScope', '$timeout', '$interval', '$location', '$http'];

function download(Common, $rootScope, $timeout, $interval, $location, $http) {

	var vm = this;
	vm.loading = false;
	vm.sended = false;
	vm.downloadOpen = false;
	$rootScope.downloadOpen = false;

	Common.functions();

	vm.goDown = function () {
		$('html, body').animate({ 'scrollTop': window.innerHeight }, 700);
	}

	vm.send = function () {
		vm.sended = true;
		if ($rootScope.form.name.length > 3 && validateEmail($rootScope.form.email) && $rootScope.form.tipo) {
			vm.loading = true;
			vm.message = 'Enviando...';
			$http.post('/api/descargas', $rootScope.form)
				.then(function (response) {
					vm.thx = true;
					localStorage.setItem('genrod_form', JSON.stringify($rootScope.form));
				}).catch(function (err) {
					console.log(err);
				});
		} else {
			vm.message = 'Por favor, completa todos los campos obligatorios correctamente.';
		}
	}

	$rootScope.download = function(file, word){
		$rootScope.downloadOpen = true;
		vm.downloadOpen = true;
		$rootScope.form.file = 'archivos/'+file;
		$rootScope.file = 'http://www.genrod.com.ar/archivos/' + file;
		$rootScope.word = word;
		if(!$rootScope.first){
			$rootScope.first = true;
		} else {
			vm.send();
		}
		ga('send', 'event', { eventCategory: 'Descargas', eventAction: 'Descarga de archivo', eventLabel: file });
	}

	function validateEmail(email) {
		var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
		return re.test(String(email).toLowerCase());
	}

}

app.controller('politica', politica);

politica.$inject = ['Common', '$rootScope', '$timeout', '$interval', '$window', '$http'];

function politica(Common, $rootScope, $timeout, $interval, $window, $http) {

	var vm = this;
	$rootScope.tit = 'GENROD / Políticas de Privacidad';
	$rootScope.section = 'politica';

	Common.functions();

	vm.goDown = function () {
		$('html, body').animate({ 'scrollTop': window.innerHeight }, 700);
	}

}


/**********************
    FOOTER CONTROLLER
**********************/

app.controller('footer', footer);

footer.$inject = ['Common', '$rootScope', '$timeout', '$interval', '$location', '$http'];

function footer(Common, $rootScope, $timeout, $interval, $location, $http) {

	var vm = this;
	vm.dd = false;
	vm.form = {
		email: '',
		tipo: ''
	}

	var times = 0;
	vm.submit = function () {
		console.log('footer send');
		if (validateEmail(vm.form.email) && vm.form.tipo){
			if (times == 0) {
				times = 1;
				ga('send', 'event', {
					eventCategory: 'Suscripciones',
					eventAction: 'Suscripción',
					eventLabel: vm.form.tipo
				});
				ga('send', 'event', {
					eventCategory: 'Suscripción'
				});
				$http.post('/api/suscripciones', vm.form).
					then(function (response) {
						vm.message = '¡Gracias por suscribirte!';
						$timeout(function () {
							times = 0;
							vm.form = {
								tipo: '',
								email: ''
							}
							vm.message = '';
						}, 5000)
					});
			}
		} else {
			vm.message = 'Por favor, completa ambos campos correctamente.';
		}
	}

	function validateEmail(email) {
		var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
		return re.test(String(email).toLowerCase());
	}

}

app.filter("trust", ['$sce', function ($sce) {
	return function (htmlCode) {
		return $sce.trustAsHtml(htmlCode);
	}
}]);

app.filter('truncate', function(){
	return function(text){
		return text ? text.length > 150 ? text.substring(0, 150) + '...' : text : null;
	}
})

app.filter('youtube', function ($sce) {
	return function (str) {
		var i = str.indexOf('=');
		return $sce.trustAsResourceUrl('https://www.youtube.com/embed/' + str.substr(i + 1).split('&')[0]);
	};
});




$.easing.jswing = $.easing.swing;

$.extend($.easing,
	{
		def: 'easeOutQuad',
		swing: function (x, t, b, c, d) {
			//alert($.easing.default);
			return $.easing[$.easing.def](x, t, b, c, d);
		},
		easeInQuad: function (x, t, b, c, d) {
			return c * (t /= d) * t + b;
		},
		easeOutQuad: function (x, t, b, c, d) {
			return -c * (t /= d) * (t - 2) + b;
		},
		easeInOutQuad: function (x, t, b, c, d) {
			if ((t /= d / 2) < 1) return c / 2 * t * t + b;
			return -c / 2 * ((--t) * (t - 2) - 1) + b;
		},
		easeInCubic: function (x, t, b, c, d) {
			return c * (t /= d) * t * t + b;
		},
		easeOutCubic: function (x, t, b, c, d) {
			return c * ((t = t / d - 1) * t * t + 1) + b;
		},
		easeInOutCubic: function (x, t, b, c, d) {
			if ((t /= d / 2) < 1) return c / 2 * t * t * t + b;
			return c / 2 * ((t -= 2) * t * t + 2) + b;
		},
		easeInQuart: function (x, t, b, c, d) {
			return c * (t /= d) * t * t * t + b;
		},
		easeOutQuart: function (x, t, b, c, d) {
			return -c * ((t = t / d - 1) * t * t * t - 1) + b;
		},
		easeInOutQuart: function (x, t, b, c, d) {
			if ((t /= d / 2) < 1) return c / 2 * t * t * t * t + b;
			return -c / 2 * ((t -= 2) * t * t * t - 2) + b;
		},
		easeInQuint: function (x, t, b, c, d) {
			return c * (t /= d) * t * t * t * t + b;
		},
		easeOutQuint: function (x, t, b, c, d) {
			return c * ((t = t / d - 1) * t * t * t * t + 1) + b;
		},
		easeInOutQuint: function (x, t, b, c, d) {
			if ((t /= d / 2) < 1) return c / 2 * t * t * t * t * t + b;
			return c / 2 * ((t -= 2) * t * t * t * t + 2) + b;
		},
		easeInSine: function (x, t, b, c, d) {
			return -c * Math.cos(t / d * (Math.PI / 2)) + c + b;
		},
		easeOutSine: function (x, t, b, c, d) {
			return c * Math.sin(t / d * (Math.PI / 2)) + b;
		},
		easeInOutSine: function (x, t, b, c, d) {
			return -c / 2 * (Math.cos(Math.PI * t / d) - 1) + b;
		},
		easeInExpo: function (x, t, b, c, d) {
			return (t == 0) ? b : c * Math.pow(2, 10 * (t / d - 1)) + b;
		},
		easeOutExpo: function (x, t, b, c, d) {
			return (t == d) ? b + c : c * (-Math.pow(2, -10 * t / d) + 1) + b;
		},
		easeInOutExpo: function (x, t, b, c, d) {
			if (t == 0) return b;
			if (t == d) return b + c;
			if ((t /= d / 2) < 1) return c / 2 * Math.pow(2, 10 * (t - 1)) + b;
			return c / 2 * (-Math.pow(2, -10 * --t) + 2) + b;
		},
		easeInCirc: function (x, t, b, c, d) {
			return -c * (Math.sqrt(1 - (t /= d) * t) - 1) + b;
		},
		easeOutCirc: function (x, t, b, c, d) {
			return c * Math.sqrt(1 - (t = t / d - 1) * t) + b;
		},
		easeInOutCirc: function (x, t, b, c, d) {
			if ((t /= d / 2) < 1) return -c / 2 * (Math.sqrt(1 - t * t) - 1) + b;
			return c / 2 * (Math.sqrt(1 - (t -= 2) * t) + 1) + b;
		},
		easeInElastic: function (x, t, b, c, d) {
			var s = 1.70158; var p = 0; var a = c;
			if (t == 0) return b; if ((t /= d) == 1) return b + c; if (!p) p = d * .3;
			if (a < Math.abs(c)) { a = c; var s = p / 4; }
			else var s = p / (2 * Math.PI) * Math.asin(c / a);
			return -(a * Math.pow(2, 10 * (t -= 1)) * Math.sin((t * d - s) * (2 * Math.PI) / p)) + b;
		},
		easeOutElastic: function (x, t, b, c, d) {
			var s = 1.70158; var p = 0; var a = c;
			if (t == 0) return b; if ((t /= d) == 1) return b + c; if (!p) p = d * .3;
			if (a < Math.abs(c)) { a = c; var s = p / 4; }
			else var s = p / (2 * Math.PI) * Math.asin(c / a);
			return a * Math.pow(2, -10 * t) * Math.sin((t * d - s) * (2 * Math.PI) / p) + c + b;
		},
		easeInOutElastic: function (x, t, b, c, d) {
			var s = 1.70158; var p = 0; var a = c;
			if (t == 0) return b; if ((t /= d / 2) == 2) return b + c; if (!p) p = d * (.3 * 1.5);
			if (a < Math.abs(c)) { a = c; var s = p / 4; }
			else var s = p / (2 * Math.PI) * Math.asin(c / a);
			if (t < 1) return -.5 * (a * Math.pow(2, 10 * (t -= 1)) * Math.sin((t * d - s) * (2 * Math.PI) / p)) + b;
			return a * Math.pow(2, -10 * (t -= 1)) * Math.sin((t * d - s) * (2 * Math.PI) / p) * .5 + c + b;
		},
		easeInBack: function (x, t, b, c, d, s) {
			if (s == undefined) s = 1.70158;
			return c * (t /= d) * t * ((s + 1) * t - s) + b;
		},
		easeOutBack: function (x, t, b, c, d, s) {
			if (s == undefined) s = 1.70158;
			return c * ((t = t / d - 1) * t * ((s + 1) * t + s) + 1) + b;
		},
		easeInOutBack: function (x, t, b, c, d, s) {
			if (s == undefined) s = 1.70158;
			if ((t /= d / 2) < 1) return c / 2 * (t * t * (((s *= (1.525)) + 1) * t - s)) + b;
			return c / 2 * ((t -= 2) * t * (((s *= (1.525)) + 1) * t + s) + 2) + b;
		},
		easeInBounce: function (x, t, b, c, d) {
			return c - $.easing.easeOutBounce(x, d - t, 0, c, d) + b;
		},
		easeOutBounce: function (x, t, b, c, d) {
			if ((t /= d) < (1 / 2.75)) {
				return c * (7.5625 * t * t) + b;
			} else if (t < (2 / 2.75)) {
				return c * (7.5625 * (t -= (1.5 / 2.75)) * t + .75) + b;
			} else if (t < (2.5 / 2.75)) {
				return c * (7.5625 * (t -= (2.25 / 2.75)) * t + .9375) + b;
			} else {
				return c * (7.5625 * (t -= (2.625 / 2.75)) * t + .984375) + b;
			}
		},
		easeInOutBounce: function (x, t, b, c, d) {
			if (t < d / 2) return $.easing.easeInBounce(x, t * 2, 0, c, d) * .5 + b;
			return $.easing.easeOutBounce(x, t * 2 - d, 0, c, d) * .5 + c * .5 + b;
		}
	});

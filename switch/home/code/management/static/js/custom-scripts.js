
(function ($) {
    "use strict";
    var mainApp = {

        initFunction: function () {
            /*MENU 
            ------------------------------------*/
            $('#main-menu').metisMenu();
			
            $(window).bind("load resize", function () {
                if ($(this).width() < 768) {
                    $('div.sidebar-collapse').addClass('collapse')
                } else {
                    $('div.sidebar-collapse').removeClass('collapse')
                }
            });

            /* MORRIS BAR CHART
			-----------------------------------------*/
            Morris.Bar({
                element: 'morris-bar-chart',
                data: [{
                    m: 'Jan',
                    a: 100,
                    b: 90,
					c: 80
                }, {
                    m: 'Feb',
                    a: 75,
                    b: 65,
					c: 55
                }, {
                    m: 'Mar',
                    a: 50,
                    b: 40,
					c: 55
                }, {
                    m: 'Apr',
                    a: 75,
                    b: 65,
					c: 55
                }, {
                    m: 'May',
                    a: 50,
                    b: 40,
					c: 55
                }, {
                    m: 'Jun',
                    a: 75,
                    b: 65,
					c: 55
                }, {
                    m: 'Jul',
                    a: 100,
                    b: 90,
					c: 80
                }, {
                    m: 'Aug',
                    a: 100,
                    b: 90,
					c: 80
                }, {
                    m: 'Jul',
                    a: 100,
                    b: 90,
					c: 80
                }, {
                    m: 'Oct',
                    a: 100,
                    b: 90,
					c: 80
                }, {
                    m: 'Nov',
                    a: 100,
                    b: 90,
					c: 80
                }, {
                    m: 'Dec',
                    a: 100,
                    b: 90,
					c: 80
                }],
                xkey: 'm',
                ykeys: ['a', 'b','c'],
                labels: ['Dell', 'Cisco', 'Juniper'],
				 barColors: [
    '#e96562','#414e63',
    '#7EC0EE' 
  ],
                hideHover: 'auto',
                resize: true
            });
	 


            /* MORRIS DONUT CHART
			----------------------------------------*/
            Morris.Donut({
                element: 'morris-donut-chart',
                data: [{
                    label: "4GRAN",
                    value: 200
                }, {
                    label: "5GRAN",
                    value: 25
                }, {
                    label: "Cloud",
                    value: 133
                },{
                    label: "CloudCore",
                    value: 20
                }, {
                    label: "E2E",
                    value: 32
                }, {
                    label: "DX",
                    value: 12
                }, {
                    label: "ECE",
                    value: 18
                }, {
                    label: "Hetran",
                    value: 60
                }, {
                    label: "SRAN",
                    value: 160
                }],
				   colors: [
    'gray','#414e63',
    '#C6E2FF','#7CCD7C',
	'#CD3278','#00F5FF',
	'#EED2EE','#BCEE68',
	'#B23AEE',
  ],
                resize: true
            });

            /* MORRIS AREA CHART
			----------------------------------------*/

            Morris.Area({
                element: 'morris-area-chart',
                data: [{
                    period: '2018-6-15',
                    offline: 266,
                    backupfailed: 200,
                    nonstandardname: 2647
                }, {
                    period: '2018-6-14',
                    offline: 2778,
                    backupfailed: 2294,
                    nonstandardname: 2441
                }, {
                    period: '2018-6-13',
                    offline: 4912,
                    backupfailed: 1969,
                    nonstandardname: 2501
                }, {
                    period: '2018-6-12',
                    offline: 3767,
                    backupfailed: 3597,
                    nonstandardname: 5689
                }, {
                    period: '2018-6-11',
                    offline: 6810,
                    backupfailed: 1914,
                    nonstandardname: 2293
                }, {
                    period: '2018-6-10',
                    offline: 5670,
                    backupfailed: 4293,
                    nonstandardname: 1881
                }, {
                    period: '2018-6-9',
                    offline: 4820,
                    backupfailed: 3795,
                    nonstandardname: 1588
                }],
                xkey: 'period',
                ykeys: ['offline', 'backupfailed', 'nonstandardname'],
                labels: ['offline', 'backupfailed', 'nonstandardname'],
                pointSize: 2,
                hideHover: 'auto',
				  pointFillColors:['#ffffff'],
				  pointStrokeColors: ['black'],
				  lineColors:['gray','#EED2EE','#BCEE68'],
                resize: true
            });

            /* MORRIS LINE CHART
			----------------------------------------*/
            Morris.Line({
                element: 'morris-line-chart',
                data: [
					  { y: '2018-01', a: 50, b: 90, c:100, d:200, e:300, f:400, g:500, h:600, i:700},
					  { y: '2018-02', a: 165,  b: 185, c:100, d:200, e:300, f:400, g:500, h:600, i:700},
					  { y: '2018-03', a: 150,  b: 130, c:100, d:200, e:300, f:400, g:500, h:600, i:700},
					  { y: '2018-04', a: 175,  b: 160, c:100, d:200, e:300, f:400, g:500, h:600, i:700},
					  { y: '2018-05', a: 80,  b: 65, c:100, d:200, e:300, f:400, g:500, h:600, i:700},
					  { y: '2018-06', a: 90,  b: 70, c:100, d:200, e:300, f:400, g:500, h:600, i:700},
					  { y: '2018-07', a: 100, b: 125, c:100, d:200, e:300, f:400, g:500, h:600, i:700},
					  { y: '2018-08', a: 155, b: 175, c:100, d:200, e:300, f:400, g:500, h:600, i:700},
					  { y: '2018-09', a: 80, b: 85, c:100, d:200, e:300, f:400, g:500, h:600, i:700},
					  { y: '2018-10', a: 145, b: 155, c:100, d:200, e:300, f:400, g:500, h:600, i:700},
					  { y: '2018-11', a: 160, b: 195, c:100, d:200, e:300, f:400, g:500, h:600, i:700},
					  { y: '2018-12', a: 160, b: 195, c:100, d:200, e:300, f:400, g:500, h:600, i:700}
				],
            
				 
      xkey: 'y',
      ykeys: ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'],
      labels: ['4GRAN', '5GRAN', 'Cloud', 'CloudCore', 'E2E', 'DX', 'ECE', 'Hetran', 'SRAN'],
      fillOpacity: 0.6,
      hideHover: 'auto',
      behaveLikeLine: true,
      resize: true,
      pointFillColors:['#ffffff'],
      pointStrokeColors: ['black'],
      lineColors:['gray','#414e63','#C6E2FF','#7CCD7C','#CD3278','#00F5FF','#EED2EE','#BCEE68','#B23AEE']
	  
            });
           
        
            $('.bar-chart').cssCharts({type:"bar"});
            $('.donut-chart').cssCharts({type:"donut"}).trigger('show-donut-chart');
            $('.line-chart').cssCharts({type:"line"});

            $('.pie-thychart').cssCharts({type:"pie"});
       
	 
        },

        initialization: function () {
            mainApp.initFunction();

        }

    }
    // Initializing ///

    $(document).ready(function () {
		$(".dropdown-button").dropdown();
		$("#sideNav").click(function(){
			if($(this).hasClass('closed')){
				$('.navbar-side').animate({left: '0px'});
				$(this).removeClass('closed');
				$('#page-wrapper').animate({'margin-left' : '260px'});
				
			}
			else{
			    $(this).addClass('closed');
				$('.navbar-side').animate({left: '-260px'});
				$('#page-wrapper').animate({'margin-left' : '0px'}); 
			}
		});
		
        mainApp.initFunction(); 
    });

	$(".dropdown-button").dropdown();
	
}(jQuery));

"use strict";
$(function(){
    window.mapApp = {
	templates: {
	    busOptionsTemplate :_.template($('#busOptionsTemplate').html())},

	busSelect: $('#busSelect'),
	firstBusOption: $('#firstBusOption')
    };


    // initialize route selection
    mapApp.busSelect.chosen().change(function(e){
	mapApp.router.navigateToBus(this.value);
    });

    // initialize models
    var BusModel = Backbone.Model.extend({});
    var BusCollection = Backbone.Collection.extend({
	model:BusModel,
	url:'api/bus/',
	comparator:function(item) {
	    return item.get("code");
	}
    });
    
    var BusView = Backbone.View.extend({
	el:mapApp.busSelect.get(0),
	render:function(){
	    mapApp.busSelect.html(mapApp.templates.busOptionsTemplate({options:this.collection}));
	    $('#busSelect').trigger('liszt:updated');
	}
    });

    
    mapApp.BusModel = BusModel;
    mapApp.BusCollection = BusCollection;
    mapApp.BusView = BusView;
    mapApp.busCollection = new BusCollection();
    
    mapApp.busCollection.fetch({
	success:_.bind(function(models,xhr,options){
	    this.busCollection.add({code:'',no:'Bir hat seciniz',route:''});
	    this.busView = new BusView({collection:this.busCollection});
	    this.busView.render();
	},mapApp),
	error:function(models,xhr,options){
	    alert('Server bağlantısında bir problem oluştu.');
	}
    });



    ////////////
    // ROUTER //
    ////////////
    mapApp.Router = Backbone.Router.extend({
	routes:{
	    '': 'init',
	    'route/:route': 'setRoute'
	},
	
	init:function(){

	    if(mapApp.initialized){
		if(mapApp.busLayer)
		    mapApp.map.removeLayer(mapApp.busLayer);
		return;}
		
	    mapApp.initialized = true;
	    
	    // initialize map
	    var map = new L.Map('map', {
		center: new L.LatLng(41.05760862509861, 29.15771484375),
		zoom: 10
	    });
    
	    mapApp.map = map;
    
	    // create a CloudMade tile layer
	    var cloudmadeUrl = 'http://{s}.tile.cloudmade.com/86d0023a1a8a4283b4a901eb512cf615/997/256/{z}/{x}/{y}.png',
	    cloudmadeLayer = new L.TileLayer(cloudmadeUrl, {maxZoom: 18});
    
	    // add the CloudMade layer to the map
	    map.addLayer(cloudmadeLayer);

	    
	},
	setRoute: function(route){
	    if(!mapApp.initialized)
		this.init();

	    $.getJSON('/api/busstop/?route=' + route,
		      function(data,result,xhr){
			  var geojson = new L.GeoJSON();
			  if(mapApp.busLayer)
			      mapApp.map.removeLayer(mapApp.busLayer);

			  mapApp.busLayer = geojson;
			  geojson.on('featureparse', function(e) {
			      e.layer.bindPopup(e.properties.title);
			  });
			  geojson.addData(data);
			  mapApp.map.addLayer(geojson);			  

		      }
		     );
	},

	navigateToBus: function(code){
	    this.navigate('route/' + code,{trigger:true});
	}
    });
    
    //initialize router
    mapApp.router = new mapApp.Router();
    Backbone.history.start();
});

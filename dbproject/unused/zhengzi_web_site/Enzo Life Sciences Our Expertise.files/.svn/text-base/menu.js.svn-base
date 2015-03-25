var Accordion2 = Fx.Elements.extend({

	options: {
		onActive: Class.empty,
		onBackground: Class.empty,
		display: 0,
		show: false,
		height: true,
		width: false,
		opacity: true,
		fixedHeight: false,
		fixedWidth: false,
		wait: false,
		alwaysHide: false,
		itemsOpen:[]
	},

	initialize: function(){
		var options, togglers, elements, container;
		$each(arguments, function(argument, i){
			switch($type(argument)){
				case 'object': options = argument; break;
				case 'element': container = $(argument); break;
				default:
					var temp = $$(argument);
					if (!togglers) togglers = temp;
					else elements = temp;
			}
		});
		this.togglers = togglers || [];
		this.elements = elements || [];
		this.container = $(container);
		this.setOptions(options);
		this.previous = -1;
		if (this.options.alwaysHide) this.options.wait = true;
		if ($chk(this.options.show)){
			this.options.display = false;
			this.previous = this.options.show;
		}
		if (this.options.start){
			this.options.display = false;
			this.options.show = false;
		}
		this.effects = {};
		if (this.options.opacity) this.effects.opacity = 'fullOpacity';
		if (this.options.width) this.effects.width = this.options.fixedWidth ? 'fullWidth' : 'offsetWidth';
		if (this.options.height) this.effects.height = this.options.fixedHeight ? 'fullHeight' : 'scrollHeight';
		for (var i = 0, l = this.togglers.length; i < l; i++) this.addSection(this.togglers[i], this.elements[i]);
		this.elements.each(function(el, i){
			if (this.options.show === i){
				this.fireEvent('onActive', [this.togglers[i], el]);
			} else {
				for (var fx in this.effects) el.setStyle(fx, 0);
			}
		}, this);
		this.parent(this.elements);
		if ($chk(this.options.display)) this.display(this.options.display);
	},

	/*
	Property: addSection
		Dynamically adds a new section into the accordion at the specified position.

	Arguments:
		toggler - (dom element) the element that toggles the accordion section open.
		element - (dom element) the element that stretches open when the toggler is clicked.
		pos - (integer) the index where these objects are to be inserted within the accordion.
	*/

	addSection: function(toggler, element, pos){
		toggler = $(toggler);
		element = $(element);
		var test = this.togglers.contains(toggler);
		var len = this.togglers.length;
		this.togglers.include(toggler);
		this.elements.include(element);
		if (len && (!test || pos)){
			pos = $pick(pos, len - 1);
			toggler.injectBefore(this.togglers[pos]);
			element.injectAfter(toggler);
		} else if (this.container && !test){
			toggler.inject(this.container);
			element.inject(this.container);
		}
		var idx = this.togglers.indexOf(toggler);
		toggler.addEvent('click', this.display.bind(this, idx));
		if (this.options.height) element.setStyles({'padding-top': 0, 'border-top': 'none', 'padding-bottom': 0, 'border-bottom': 'none'});
		if (this.options.width) element.setStyles({'padding-left': 0, 'border-left': 'none', 'padding-right': 0, 'border-right': 'none'});
		element.fullOpacity = 1;
		if (this.options.fixedWidth) element.fullWidth = this.options.fixedWidth;
		if (this.options.fixedHeight) element.fullHeight = this.options.fixedHeight;
		element.setStyle('overflow', 'hidden');
		if (!test){
			for (var fx in this.effects) element.setStyle(fx, 0);
		}
		return this;
	},

	/*
	Property: display
		Shows a specific section and hides all others. Useful when triggering an accordion from outside.

	Arguments:
		index - integer, the index of the item to show, or the actual element to show.
	*/

	showThis: function(i){
		if (this.options.height) this.h = {'height': [this.elements[i].offsetHeight, this.options.fixedHeight || this.elements[i].scrollHeight]};
		if (this.options.width) this.w = {'width': [this.elements[i].offsetWidth, this.options.fixedWidth || this.elements[i].scrollWidth]};
		if (this.options.opacity) this.o = {'opacity': [this.now[i]['opacity'] || 0, 1]};
	},
 
	
	
	display: function(index){
		index = ($type(index) == 'element') ? this.elements.indexOf(index) : index;
		if ((this.timer && this.options.wait) || (index === this.previous && !this.options.alwaysHide)) return this;
		this.previous = index;
		var obj = {};
		this.elements.each(function(el, i){
			obj[i] = {};
			var hide = (i != index) || (this.options.alwaysHide && (el.offsetHeight > 0));
			this.fireEvent(hide ? 'onBackground' : 'onActive', [this.togglers[i], el]);
			for (var fx in this.effects) obj[i][fx] = hide ? 0 : el[this.effects[fx]];
		}, this);
		return this.start(obj);
	},

	display2: function(index){
		index = ($type(index) == 'element') ? this.elements.indexOf(index) : index;
		if ((this.timer && this.options.wait) || (index === this.previous && !this.options.alwaysHide)) return this;
		this.previous = index;
		var obj = {};
		this.elements.each(function(el, i){
			obj[i] = {};
			var hide = (i != index) || (this.options.alwaysHide && (el.offsetHeight > 0));
			this.fireEvent(hide ? 'onBackground' : 'onActive', [this.togglers[i], el]);
			
			//for (var fx in this.effects) obj[i][fx] = hide ? 0 : el[this.effects[fx]];
		}, this);
		return this.start(obj);
	},
	
	showThisHideOpen: function(index){return this.display(index);}

});

Fx.Accordion2 = Accordion2;


var accordion= '';var accordion2 = '';

//$('main-navi').style.visibility="hidden";	


function accordionSet(){
accordion = new Accordion2('span.toggle', 'ul.content', {
	display:false,
	alwaysHide:true,
	duration: 0,
	opacity: false,
	onActive: function(toggler, element){
		toggler.addClass('act');
		parentelement = element;
	},

	onBackground: function(toggler, element){
		toggler.removeClass('act');		
	}
});	

accordion2 = new Accordion2('span.toggle2', 'ul.content2', {
	display:false,
	alwaysHide:true,
	opacity: false,
	onActive: function(toggler, element){
		toggler.addClass('act2');
		parentelement.setStyle('height', 'auto');
	},

	onBackground: function(toggler, element){
		toggler.removeClass('act2');		
	}
});
//ul#top > li

}

  function checkHashold(){
    var found = false;
    var offset = 0;
    var tmp = 0;

    $$('#rgaccordmenu li span.toggle').each(function(anchorid, i) {
      //alert(anchorid.className);
      if (anchorid.hasClass('open') && !found) {
          accordion.display(offset);
          found = true;
      } else {
        offset++;
      }
    });
//alert(found);
    if (!found) accordion.display(1);
  }

  function checkHash(){
    var found = false;
    var offset = 0;
    var tmp = 0;
    
    //var aaa = $('rgaccordmenu').getElements('span[class=empty1]');
    
$$('#rgaccordmenu ul.content').each(function(toggleid, i) {
    
    var aa = toggleid.getElements('a');
	aa.each(function(anchorid, ii) {
      
      if (anchorid.hasClass('act3') && !found) {
	//alert(offset);
	  accordion.display(offset);
          found = true;
      } 
    });
    if (!found) {
	    offset++;
    }
});
//alert(found);
    if (!found && $('rgaccordmenu').getElements('span[class=empty1]').length==0) accordion.display(1);
  }

  
  function checkHash2(){
    var found = false;
    var offset = 0;
    var tmp = 0;

    $$(' span.toggle2').each(function(anchorid, i) {

      if (anchorid.hasClass('open') && !found) {

          accordion2.display(offset);
          found = true;
      } else {
        offset++;
      }
    });
    //if (!found) accordion2.display(0);    
  }

 
//window.addEvent('domready', function(){

function mainMenuInit(){ 
	var x = new Chain();
	x.chain(accordionSet);
	x.chain(checkHash);
	x.chain(function(){
		$('main-navi').style.visibility="visible";		
	});
	//x.chain(checkHash2);
	x.callChain();
	x.callChain.delay(0, x);
	x.callChain.delay(0, x);
}

//});





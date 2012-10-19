(function($) {
    var TAG = '{IMAGE:{name}}';
    var query_url = '/admin/images/image/filter_images/?q=';

    var container = $('.images-container'),
        searchForm = container.find('.form-search');

    function filter(objects) {
        // TODO: use object ids instead of names
        var names = $.map(objects,function(ob) { return ob.name });
        
        container.find('.items a img').each(function(i,img) {
        	var $img = $(img), title = $img.attr('title'), match = names.indexOf(title) >= 0, $items = container.find('.items div');
        	if(!match) {
        		$img.parent().hide();
        		return;
        	}
        	$($items.get(Math.ceil((i+1)/6)-1)).append($img.parent().show());
        	container.find('.items div:gt('+(Math.ceil(names.length/6)-1)+')').hide();
        });
    }

    function reset() {
        container.find('.items a').show();
    }

    function insertTag(img) {
        var title = $(img).attr('title'),
            tag = TAG.replace('{name}',title),
            textArea = $('#id_source'),
            text = textArea.val();

        if(text.indexOf(tag) < 0) {
            textArea.val(text + ' ' + tag);
        }
    }

    container.find('img').bind('click', function(e) {
        e.preventDefault();
        insertTag(this);
    });

    searchForm.find('button').bind('click', function(e) {
    	e.preventDefault();
        var terms = searchForm.find('input').val();
        if(terms === '') {
            reset();
            return;
        }
        $.getJSON(query_url + terms).success(filter);
    });
    
    function updateWidth(scrollable) {
		var a_items = $('.items div', scrollable).first().find('a')
		var width = 10*(a_items.length-1);
		a_items.each(function(index, el){
	    	width+=$(el).width();
	    });
		scrollable.css('width', width);
	}
	
	updateWidth($('.scrollable', container));
    container.find(".scrollable").scrollable();

})(jQuery);

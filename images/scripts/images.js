(function($) {
    var TAG = '{IMAGE:{name}}';
    var query_url = '/admin/images/image/filter_images/?q=';

    var container = $('#images-container'),
        searchForm = container.find('.form-search');

    function filter(objects) {
        // TODO: use object ids instead of names
        var names = $.map(objects,function(ob) { return ob.name });
        container.find('.items a img').each(function(i,img) {
            var $img = $(img),
                title = $img.attr('title'),
                match = names.indexOf(title) >= 0;

            $img.parent().toggle(match);
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

    container.find(".scrollable").scrollable();

})(jQuery);

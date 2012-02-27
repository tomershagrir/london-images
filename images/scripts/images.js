(function($) {

    var TAG = '{IMAGE:{name}}';
    var query_url = '/admin/images/image/filter_images/?q=';

    $('body').live('london_ready', function(){

        var container = $('#images-container');

        function filter(objects) {
            // TODO: use object ids instead of names
            var names = $.map(objects,function(ob) { return ob.name });
            container.find('.items a img').each(function(i,img) {
                var $img = $(img);
                var title = $img.attr('title');
                var match = names.indexOf(title) >= 0;
                $img.parent().toggle(match);
            });
        }

        function reset() {
            container.find('.items a').show();
        }

        function insertTag(img) {
            var title = $(img).attr('title');
            var tag = TAG.replace('{name}',title);
            var textArea = $('#id_source');
            var text = textArea.val();
            if(text.indexOf(tag) < 0) {
                textArea.val(text + ' ' + tag);
            }
        }

        container.find('img').live('click', function(e) {
            e.preventDefault();
            insertTag(this);
        });

        container.find('.form-search button').live('click', function(e) {
            e.preventDefault();
            var terms = container.find('.form-search input').val();
            if(terms === '') {
                reset();
                return;
            }
            $.getJSON(query_url + terms).success(filter);
        });

//        $('.scrollable').scrollable({ vertical: true, mousewheel: true });
    });

})(jQuery);

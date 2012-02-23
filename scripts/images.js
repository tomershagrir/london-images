Images = (function($) {
    var TAG = '{IMAGE:{name}}';
    var self = {
        init: function() {
            $('#images-container img').live('click', function(e) {
                e.preventDefault();
                var title = $(this).attr('title');
                var tag = TAG.replace('{name}',title);
                var textArea = $('#id_source');
                var text = textArea.val();
                if(text.indexOf(tag) < 0) {
                    textArea.val(text + ' ' + tag);
                }
            });
        }
    };
    return self;
})(jQuery);

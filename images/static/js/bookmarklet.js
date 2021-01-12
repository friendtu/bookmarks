(function(){
    var jquery_version='3.3.1';
    var site_url='http://127.0.0.1:8000/';
    var static_url=site_url+'static/';
    var min_width=100;
    var min_height=100;

    function bookmarklet(msg){
        //Here goes our bookmarklet code
        //load css
        var css=jQuery('<link>');
        css.attr({
            rel: "stylesheet",
            type: "text/css",
            href: static_url+'css/bookmarklet.css?r='+Math.floor(Math.random()*9999999999)
        });
        jQuery('head').append(css);
        //load html
        box_html='<div id="bookmarklet"><a href="#" id="close">&times;</a><h1>Select an image to bookmark:</h1><div class="images"></div></div>';
        jQuery('body').append(box_html);

        jQuery('#bookmarklet #close').click(function(){
            jQuery('#bookmarklet').remove();
        });

        jQuery.each(jQuery('img[src$="jpg"]'),
            function(index,image){    
                if (jQuery(image).width()>=min_width && jQuery(image).height()>=min_height) {
                    image_url=jQuery(image).attr('src');
                    jQuery('#bookmarklet .images').append('<a href="#"><img src="'+ image_url+'" /></a>');
                }
            });

        jQuery('#bookmarklet .images a').click(function(){
            
            selected_image=jQuery(this).children('img').attr('src');
            jQuery('#bookmarklet').hide();

            url_to_create_image=site_url+'images/create/?url='+encodeURIComponent(selected_image)+
                    '&title='+encodeURIComponent(jQuery('title').text());
            alert("create image: "+url_to_create_image);
            window.open(url_to_create_image,'_blank');
        });
    }

    //Check if jQuery is loaded
    if(typeof window.jQuery!='undefined') {
        bookmarklet();
    } else {
        var script=document.createElement('script');
        script.src='https://cdn.bootcdn.net/ajax/libs/jquery/'+jquery_version+'/jquery.min.js';
        //https://ajax.googleapis.com/ajax/libs/jquery/'+ jquery_version+'/jquery/slim.min.js';
        document.head.append(script);

        var attempts=15;
        (function(){
            if(typeof window.jQuery=='undefined'){
                if (--attempts>0){
                    window.setTimeout(arguments.callee,250)
                } else {
                    alert('An error occurred while loading jQuery')
                }
            } else {
                bookmarklet();
            }
        })();
    }
})();
/*
 * Display the menu items on smaller screens
 */
$(function () {
    var pull = $('#pull');
    menu = $('nav ul');
    //menuHeight = menu.height();

    $(pull).on('click', function (e) {
        menu.slideToggle();
    });
});

/*
 * 用于控制菜单栏的选中情况
 */
var urlstr = location.href;
var urlstatus=false;
$("#nav li a").each(function () {
    var _urlstr = urlstr.replace(/\//g, '')
    var _href = $(this).attr('href').replace(/\//g, '')
    if(_href.indexOf('http') === -1) {
        _href = location.origin.replace(/\//g, '') + _href
    }

    // console.log('urlstr:', _urlstr)
    // console.log('href:', _href)

    if (_urlstr === _href && $(this).attr('href')!='') {
      // console.log($(this).attr('href'))
      $(this).parent().addClass('selectedli');
      urlstatus = true;
    } else {
      $(this).parent().removeClass('selectedli');
    }
});

// if (!urlstatus) {$("#nav li").eq(3).addClass('selectedli'); }

/*
 * Display the navbar back to normal after resize
 */
$(window).resize(function () {
    var w = $(window).width();
    if (w > 320 && menu.is(':hidden')) {
        menu.removeAttr('style');
    }
});


/*
 * Make the header images move on scroll
 */
$(window).scroll(function () {
    var x = $(this).scrollTop();   
    $('#main').css('background-position', '100% ' + parseInt(-x/3) + 'px' + ', 0%, center top');
});

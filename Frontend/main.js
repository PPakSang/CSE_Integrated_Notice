var first_page = $('.page')
for (i = 10; i > 1; i--) {
    first_page.after('<li class="page"><a href="#">' + i + '</a></li>')
}

// initialize


var navs = $('.nav_box li');
var nav_title = $('.nav_title');


navs.on('click', function(e) {

    navs.removeClass('active');
    this.classList.add('active');
    nav_title.text(this.innerText + ' 공지사항')
})


// 종합, 컴퓨터학부 ...




var pages = $('.pagination .page')
pages.on('click', function(e) {
    pages.removeClass('active');
    this.classList.add('active');
    console.log('클릭이벤트')

    if (e.target.innerText == pages.length.toString()) {
        $('.pagination .rbtn').addClass('disabled')
    } else {
        $('.pagination .rbtn').removeClass('disabled')
    }
    if (e.target.innerText == 1) {
        $('.pagination .lbtn').addClass('disabled')
    } else {
        $('.pagination .lbtn').removeClass('disabled')
    }
})


var lbtn = $('.pagination .lbtn')
var rbtn = $('.pagination .rbtn')
lbtn.on('click', function() {

    if (lbtn.hasClass('disabled')) {
        return;
    } else {
        var test = $('.pagination .active');
        var test2 = $('.page');
        console.log(test2.index(test));
        test2[test2.index(test) - 1].click()
    }
})

rbtn.on('click', function() {

    if (rbtn.hasClass('disabled')) {
        return;
    } else {
        var test = $('.pagination .active');
        var test2 = $('.page');
        console.log(test2.index(test));
        test2[test2.index(test) + 1].click()
    }
})



// page 번호 및 버튼 이벤트




var tag_all = $('.tag_all')
for (i = 0; i < 5; i++) {
    tag_all.before('<li><label for="tag' + i + '">#멘토링' + i + '</label><input id="tag' + i + '" value="클릭' + i + '" type="checkbox"></li>')
}
var tag_box = $('.tag_box li input[type ="checkbox"]')
var tag_label = $('.tag_box label')
tag_box.on('click', function(e) {

    var data = []

    for (i = 0; i < tag_box.length; i++) {

        if ($('#tag' + i).is(':checked')) {
            data.push($('#tag' + i).prop('value'))
        }
    }

    tag_all.prop('value', data.toString())

})

tag_label.on('click', function() {
    this.classList.toggle('text-muted')
})


// 태그 추가하기(ajax 구현필요)



var tag_var = $('.tag_box span')

tag_var.on('click', function() {
    console.log(1)
    tag_var[0].classList.toggle('glyphicon-chevron-down')
    tag_var[0].classList.toggle('glyphicon-chevron-up')
    $('.tag_box')[0].classList.toggle('auto_height')
})
// initialize


var navs = $('.nav_box li a');
var nav_title = $('.nav_title');



// origin 클릭했을때
navs.on('click', function(e) {
    $('.tag_box label').removeClass('text-muted');
    $('input:checked').prop('checked', false);

    navs.removeClass('active');
    this.classList.add('active');
    nav_title.text(this.innerText + ' 공지사항');
    $.ajax({
        url: "getpageinfo/",
        data: {
            "origin": e.target.text,
            "num": 1,
            "tags": ""
        },
        dataType: "json",


        success: function(data) {

            $('.content').html(data.posts)
            add_pagination(data)

        },
        error: function(e) {

        }

    })

})

// 종합, 컴퓨터학부 ...
var first_page = $('.page_num')


function add_pagination(data) {
    var page_html = "<li class='lbtn page-item disabled'><a class='page-link' tabindex='-1' aria-disabled='true'>&laquo;</a></li>"
    var pagination = $('.pagination')
        // console.log(data.posts_len)
    for (i = 1; i <= data.posts_len; i++) {
        page_html = page_html + '<li class="page_num page-item"><a class="page-link">' + i + '</a></li>'
    }
    page_html = page_html + "<li class='rbtn page-item'><a class='page-link'>&raquo;</a></li>"
    pagination.html(page_html)
    $('.page_num')[0].classList.add('active')
    pages = $('.pagination .page_num')

    pages.on('click', function(e) {
        pages.removeClass('active');
        this.classList.add('active');


        $.ajax({
            url: "getpageinfo/",
            data: {
                "origin": $('.nav-link.active').text(),
                "num": $('.page-item.active').text(),
                "tags": ""
            },
            dataType: "json",
            success: function(data) {
                $('.content').html(data.posts)
            }
        })



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
    var lbtn = $('.lbtn')
    var rbtn = $('.rbtn')
    lbtn.on('click', function() {
        if (lbtn.hasClass('disabled')) {
            return;
        } else {
            var active_page = $('.pagination .active');
            var page_all = $('.page_num');
            // console.log(page_all.index(active_page));
            page_all[page_all.index(active_page) - 1].click()
        }
    })

    rbtn.on('click', function() {

        if (rbtn.hasClass('disabled')) {
            return;
        } else {
            var active_page = $('.pagination .active');
            var page_all = $('.page_num');
            // console.log(page_all.index(active_page));
            page_all[page_all.index(active_page) + 1].click()
        }
    })
}



var pages
$.ajax({
    url: "getpageinfo/",
    data: {
        "origin": '컴퓨터학부',
        "num": 1,
        "tags": ""
    },
    dataType: "json",
    success: function(data) {
        $('.content').html(data.posts)
        add_pagination(data)
        get_tags(data)
        tags_effect()


    },
    error: function(e) {

    }
})










// page 번호 및 버튼 이벤트


// 태그 자동 추가 ---- data에서 날라온 태그 기준
function get_tags(data) {
    var tag_all = $('.tag_all')
    var tag_box = $('.tag_box')
    tag_box.html('<li class="tag_nav"><i class="bi bi-chevron-down"></i></li>')
    var tag_nav = $('.tag_nav')
    tags = JSON.parse(data.tags)
    console.log(tags)
    for (i = tags.length - 1; i >= 0; i--) {
        tags[i].fields.name
        tag_nav.after('<li><label for="tag' + i + '">#' + tags[i].fields.name + '</label><input id="tag' + i + '" value="' + tags[i].fields.name + '" type="checkbox"></li>')
    }
    tag_box.append('<input class="tag_all" type="text">')

}


// for (i = 0; i < 20; i++) {
//     tag_all.before('<li><label for="tag' + i + '">#멘토링' + i + '</label><input id="tag' + i + '" value="컴학_전체" type="checkbox"></li>')
// }

// 태그들 다 집어넣고 그 태그에 효과 붙이기
function tags_effect() {
    var tag_all = $('.tag_all')
    var tag_box = $('.tag_box li input[type ="checkbox"]')
    var tag_label = $('.tag_box label')
    var tag_var = $('.tag_box i')

    tag_var.on('click', function() {
        console.log(1)
        tag_var[0].classList.toggle('bi-chevron-down')
        tag_var[0].classList.toggle('bi-chevron-up')
        $('.tag_box')[0].classList.toggle('auto_height')
    })

    // 태그 클릭했을 시
    tag_box.on('click', function(e) {

        var data = []

        for (i = 0; i < tag_box.length; i++) {

            if ($('#tag' + i).is(':checked')) {
                data.push($('#tag' + i).prop('value'))
            }
        }

        tag_all.prop('value', data.toString())
        console.log(tag_all.prop('value'))

        $.ajax({
            url: "getpageinfo/",
            data: {
                "origin": $('.nav-link.active').text(),
                "num": $('.page-item.active').text(),
                "tags": tag_all.prop('value')
            },
            dataType: "json",
            success: function(data) {
                $('.content').html(data.posts)
                add_pagination(data)
            }

        })



    })

    tag_label.on('click', function() {
        this.classList.toggle('text-muted')
    })
}

// 태그 추가하기(ajax 구현필요)
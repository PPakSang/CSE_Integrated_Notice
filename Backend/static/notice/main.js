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
            add_pagination(1,data.posts_len)
            get_tags(data)
            tags_effect()


        },
        error: function(e) {

        }
    })
// initialize


var navs = $('.nav_box li a');
var nav_title = $('.nav_title');



// origin 클릭했을때
navs.off('click').on('click', function(e) {
    $('.tag_box label').removeClass('text-muted');
    $('input:checked').prop('checked', false);
    
    

    navs.removeClass('active');
    this.classList.add('active');
    navs.removeClass('fw-bold')
    e.target.classList.add('fw-bold')
    nav_title.text(this.innerText + ' 공지사항');
    $.ajax({
        url: "getpageinfo/",
        data: {
            "origin": e.target.text,
            "search" : $(".search").val(),
            "num": 1,
            "tags": ""
        },
        dataType: "json",


        success: function(data) {

            $('.content').html(data.posts)
            add_pagination(1,data.posts_len)
            get_tags(data)
            tags_effect()

        },
        error: function(e) {

        }

    })
    
})

// 종합, 컴퓨터학부 ...
var first_page = $('.page_num')



//num -> 몇번부터 띄울건지, max_len 유효성 검사용
function add_pagination(num,max_len) {
    var page_html = "<li class='lbtn page-item'><a class='page-link' taonex='-1' aria-disabled='true'>&laquo;</a></li>"
    var pagination = $('.pagination')
        // console.log(data.posts_len)
    for (i = num; i <num+5; i++) {
        if(i > max_len){
            break;
        }
        page_html = page_html + '<li class="page_num page-item"><a class="page-link">' + i + '</a></li>'
    }
    page_html = page_html + "<li class='rbtn page-item'><a class='page-link'>&raquo;</a></li>"
    pagination.html(page_html)
    $('.page_num')[0].classList.add('active')
    pages = $('.pagination .page_num')

    pages.on('click', function(e) {
        pages.removeClass('active');
        this.classList.add('active');
        var tag_all = $('.tag_all')

        $.ajax({
            url: "getpageinfo/",
            data: {
                "origin": $('.nav-link.active').text(),
                "search": $(".search").val(),
                "num": $('.page-item.active').text(),
                "tags": tag_all.val()
            },
            dataType: "json",
            success: function(data) {
                $('.content').html(data.posts)
            }
        })
    })
    // 버튼추가
    var lbtn = $('.lbtn')
    var rbtn = $('.rbtn')
    if (num == 1){
        lbtn.addClass('disabled')
    }
    lbtn.on('click', function() {
        if (lbtn.hasClass('disabled')) {
            return;
        } else {
            var active_page = $('.pagination .active');
            var page_all = $('.page_num');
            // console.log(page_all.index(active_page));
            // page_all[page_all.index(active_page) - 1].click()
            add_pagination(num-5,max_len)
        }
    })
    // console.log(num,max_len)
    if (num+5 > max_len){
        
        rbtn.addClass('disabled')
    }

    rbtn.on('click', function() {
        if (rbtn.hasClass('disabled')) {
            return;
        } else {
            var active_page = $('.pagination .active');
            var page_all = $('.page_num');
            // console.log(page_all.index(active_page));
            // page_all[page_all.index(active_page) + 1].click()
            add_pagination(num+5,max_len)
            
        }
    })
}



//  검색하였을 때
function setSearchResult() {
    var keyword = $(".search").val()
    if (keyword != "") {
        $.ajax({
            url: "getpageinfo/",
            data: {
                "search": $(".search").val(),
                "num": 1
            },
            dataType: "json",
            success: function (data) {
                $('.content').html(data.posts)
                $('.nav_box').hide();
                $(".tag_boundary").hide();
                $('.nav_title').html($(".search").val()+"에 대한 검색결과입니다.")
                add_pagination(1,data.posts_len)
            },
            error: function (e) {
                console.log("검색 오류")
            }
        })
    }
}

$("#icon-search").off('click').on('click', function(e) {
    setSearchResult();
})

$("#search-box").off('keypress').on('keypress', function (e) {
    if (e.keyCode == 13) {
        setSearchResult();
    }
});












// page 번호 및 버튼 이벤트


// 태그 자동 추가 ---- data에서 날라온 태그 기준
function get_tags(data) {
    var tag_all = $('.tag_all')
    var tag_box = $('.tag_box')
    tag_box.html('<li class="tag_nav"><i class="bi bi-chevron-down"></i></li>')
    var tag_nav = $('.tag_nav')
    tags = JSON.parse(data.tags)
    // console.log(tags)
    for (i = tags.length - 1; i >= 0; i--) {
        tags[i].fields.name
        tag_nav.after('<li class="tag"><label class="tag_list text-muted" for="tag' + i + '">#' + tags[i].fields.name + '</label><input id="tag' + i + '" value="' + tags[i].fields.name + '" type="checkbox"></li>')    
    }
    tag_box.append('<input class="tag_all" type="text">')

}


// 태그들 다 집어넣고 그 태그에 효과 붙이기
function tags_effect() {
    var tag_all = $('.tag_all')
    var tag_box = $('.tag_box li input[type ="checkbox"]')
    var tag_label = $('.tag_box label')
    var tag_var = $('.tag_box i')

    tag_var.on('click', function() {
        // console.log(1)
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
        // console.log(tag_all.prop('value'))

        $.ajax({
            url: "getpageinfo/",
            data: {
                "origin": $('.nav-link.active').text(),
                "num": 1,
                "tags": tag_all.prop('value')
            },
            dataType: "json",
            success: function(data) {
                $('.content').html(data.posts)
                add_pagination(1,data.posts_len)
            }

        })



    })

    tag_label.on('click', function() {
        this.classList.toggle('fw-bold')
        this.classList.toggle('text-muted')
    })
}

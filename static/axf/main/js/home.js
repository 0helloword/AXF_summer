$(function() {
    initTopSwiper();
    initSwipeMenu();
});

function initTopSwiper(){
    var swiper=new Swiper("#topSwiper",{
        loop:true,
        autoplay:3000,//时间间隔3s
        pagination: '.swiper-pagination',
    });
}
function initSwipeMenu() {
     var swiper=new Swiper("#swiperMenu",{
         slidesPerView:3, //一页显示3个
    });
}
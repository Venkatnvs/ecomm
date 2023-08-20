gsap.registerPlugin(ScrollTrigger);
let tl = gsap.timeline();
tl.from(".header_main_logo , .header_main_logo_tit, .search-bar, .login_btn_gsap, .nvs-cart",
{
    opacity:0,
    scale:0,
    y:-500,
    duration: 0.5,
    rotation:10,
    ease: "power3.inOut",
    stagger:0.1,
})
tl.from(".sidebar-nav",
{
    opacity:0,
    scale:0,
    x:-500,
    duration: 0.5,
    ease: "power3.inOut",
    stagger:0.1,
})
tl.from("#main_product_details", 
    {
        opacity: 0,
        x: 20,
        duration: 0.4,
        scale:0,
        ease:"power3.inOut",
});
tl.from(".copyright, .credits", 
    {
        duration: 1,
        y:-400,
        opacity:0,
        scale:0,
        ScrollTrigger: {
            trigger: ".copyright, .credits",
            start:"top 70%",
            markers:true,
            scrub: true,
            scroller: "#main"
        }
});
const swiper = new Swiper('.swiper', {
    // Optional parameters
    direction: 'vertical',
    loop: 0,

    // If we need pagination
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },

    // Navigation arrows
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },

  });


// steam js code
$(document).ready(function() {
    var steamGrp = [steamLeft, steamRight, steamMid],
        steamLeft = $('svg #steam-left'),
        steamRight = $('#steam-right'),
        steamMid = $('#steam-mid'),
        svg = $('svg'),
        rotate = new TimelineMax({paused:false, repeat: -1}),
        pulse = new TimelineMax({paused:false, repeat: -1, yoyo:true}),
        rise = new TimelineMax({paused:false, repeat: -1});


    rotate.to([steamLeft, steamRight, steamMid], 2, {rotationY:"+=360deg", transformOrigin:"50% 50%", ease: Linear.easeOut});

    pulse.set([steamLeft, steamRight, steamMid], {opacity: "0", ease: Linear.easeInOut})
         .to([steamLeft, steamRight, steamMid], 1.5, {opacity: ".75", ease: Linear.easeInOut});

    rise.staggerTo([steamMid, steamLeft, steamRight], 2, {y: "-=50px", ease: Linear.easeOut}, .5);
  });


  const iconFeature = new ol.Feature({
  geometry: new ol.geom.Point(
    ol.proj.fromLonLat([51.37021008190133, 35.73501442579978])
  ),
  name: "Somewhere near Nottingham",
});

const map = new ol.Map({
  target: "map",
  key: "web.5EAHhge5tbEecvsbcaQkO2LJrak46QXoAG7zgQBN",
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM(),
    }),
    new ol.layer.Vector({
      source: new ol.source.Vector({
        features: [iconFeature],
      }),
      style: new ol.style.Style({
        image: new ol.style.Icon({
          anchor: [0.5, 46],
          anchorXUnits: "fraction",
          anchorYUnits: "pixels",
          src: "http://labs.google.com/ridefinder/images/mm_20_red.png",
        }),
      }),
    }),
  ],
  view: new ol.View({
    center: ol.proj.fromLonLat([51.37021008190133, 35.73501442579978]),
    zoom: 15,
  }),
});

$(".check_reserve").on("click", () => {
   $('.swal2-container').hide()
})
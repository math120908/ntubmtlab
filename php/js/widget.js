$(document).ready(function(){
  $("div.ukagaka").mouseenter(function(){
	  $("img.ukagaka").attr("src","img/org2.png");
  });

  $("div.ukagaka").mouseleave(function(){
	  $("img.ukagaka").attr("src","img/org1.png");
  });

 
  $("div.ukagaka").toggle(function(){
     $("div.ukagaka").animate({ height: 'hide', opacity: 'hide' }, 5000);
   },function(){
     $("div.ukagaka").animate({ height: 'show', opacity: 'show' }, 5000);
   });

});

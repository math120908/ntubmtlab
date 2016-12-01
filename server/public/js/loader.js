function Schedule(schedule) {
  this.schedule = schedule;
}
function setSchedule( datelist, schedule, place, $table ){
   var timelist = [6,8,9,10,11,12,13,14,15,16,17,18,19,20,21];
   tblheads = $table.find("thead > tr > th");
   //Set title
   for( var i=0 ; i<datelist.length ; ++i ){
      $(tblheads[i+1]).html( datelist[i].day + "<br>" + datelist[i].date );
      if( datelist[i].date == Date.today().toString('yyyy/MM/dd') )
         $(tblheads[i+1]).addClass('todaycel').prepend($("<span>",{"class":"glyphicon glyphicon-hand-right"}));
      else
         $(tblheads[i+1]).removeClass('todaycel');
   }
   tbltrs = $table.find("tbody > tr");

   AVL_IMAGE_CODE = '<img src="images/rent.gif" alt="" height="16" width="16">';
   //Set Content
   timelist.forEach( function(time,i){
      tbltds = $(tbltrs[i]).children();
      datelist.forEach( function(date,j){
         $(tbltds[j+1]).removeClass("success");
         $(tbltds[j+1]).removeClass("error");
         $newNode = $('<p>');
         if( place == "New 1" || place == "New 3" ){ 
            if(schedule[date.date][time]) dat = schedule[date.date][time][place];

            if( typeof(dat) === 'undefined' ) dat = {text:"?"};
            if( dat.remain + dat.used > 0 ){
               $aNode = $('<a>', {"href":dat.detailURL, "target":"_blank"});
               $(tbltds[j+1]).addClass(dat.remain?'success':'error');
               if(dat.remain) $aNode.append(AVL_IMAGE_CODE);
               $aNode.append(dat.remain);
               $newNode.append($aNode);

               if(dat.purchaseURL){
                  $newNode.append(
                     $('<a>', {"href":dat.purchaseURL, "target":"_blank"})
                     .attr( "target", "_blank" )
                     .html( '<font color=\"#FF5F45\">租</font>' )
                     );
               }
            }
            $newNode.append(dat.text);
         }else if(place == "Old"){
            if(schedule[date.date][time]) 
               dat = schedule[date.date][time][place];
            if( typeof(dat) === 'undefined' )
               $newNode.html('?');
            else if( !dat.abbr ){
               $newNode.append( $('<a>').css('color',"#0000FF").html(AVL_IMAGE_CODE+" 6") );
               $(tbltds[j+1]).addClass('success');
            }else
               $newNode.append(
                     $('<a>', {"href":dat.detailURL, "target":"_blank"}) 
                     .css('color',"#000000")
                     .html(dat.text));
         }
         $(tbltds[j+1]).html( $newNode );

      });
   });
}

function showSchedule( datelist ){
   schedule = {};
   $.ajaxSetup({async:false});
   datelist.forEach( function(date, idx){
      qurl = "q/" + date.date ;
      $.get( qurl , function( data ) {
         schedule[date.date] = data;
      }, "json" );
   });
   $.ajaxSetup({async:true});
   var placelist = {"1":"New 1","2":"New 3","3":"Old"};
   setSchedule( datelist, schedule, placelist["1"], $("table#schedule1") );
   setSchedule( datelist, schedule, placelist["2"], $("table#schedule2") );
   setSchedule( datelist, schedule, placelist["3"], $("table#schedule3") );
};
function showScheduleOneWeek( showday ){
   datelist = [];
   for(var i=0;i<7;++i){
      datelist.push( {date:showday.toString('yyyy/MM/dd'), day:showday.toString('dddd')} );
      showday.add(+1).day();
   }
   showSchedule( datelist );
}
function showScheduleOneDay( showday ){
   showSchedule([{date:showday.toString('yyyy/MM/dd'), day:showday.toString('dddd')}]);
}

function showWeek(i){
   if( Date.today().toString('ddd') == 'Sun' )
      startdate = Date.today().previous().mon();
   else
      startdate = Date.mon();
   showScheduleOneWeek( startdate.add(i).week() );
}

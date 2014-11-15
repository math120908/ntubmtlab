<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf8">
    <title>NTU Badminton Information System</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="NTU badminton information system">
    <meta name="author" content="small2kuo">

    <!-- Le styles -->
    <link href="bootstrap/css/bootstrap.css" rel="stylesheet">
    <style type="text/css">
      body {
        padding-top: 60px;
        padding-bottom: 40px;
      }
      .hero-unit{
         padding-top: 30px;
         padding-bottom: 30px;
      }
    </style>
    <link href="bootstrap/css/bootstrap-responsive.css" rel="stylesheet">

    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

    <!-- Fav and touch icons -->
    <link rel="apple-touch-icon-precomposed" sizes="144x144" href="ico/dead.gif">
    <link rel="apple-touch-icon-precomposed" sizes="114x114" href="ico/dead.gif">
    <link rel="apple-touch-icon-precomposed" sizes="72x72" href="ico/dead.gif">
    <link rel="apple-touch-icon-precomposed" href="ico/dead.gif">
    <link rel="shortcut icon" href="ico/dead.gif">

<link rel="stylesheet" id="mzry1992-Ukagaka-CSS" href="stylesheet/widget.css" type="text/css" media="all">
<script type="text/javascript" src="http://code.jquery.com/jquery-1.7.2.min.js"></script>
<script type="text/javascript" src="js/widget.js"></script>
  </head>

  <body>

    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <a class="brand" href="index.php">Badminton</a>
          <div class="nav-collapse collapse">
            <ul class="nav">
              <li class="active"><a href="index.php">Home</a></li>
              <li><a href="https://info2.ntu.edu.tw/facilities/Default.aspx">台大新體</a></li>
              <li><a href="http://ntusportscenter.ntu.edu.tw/">台大體育館</a></li>
              <li><a href="http://www.mc.ntu.edu.tw/staff/studentaffair/area/area.htm">台大醫體</a></li>
              <li><a href="http://view.officeapps.live.com/op/view.aspx?src=http%3A%2F%2Fwww.mc.ntu.edu.tw%2Fstaff%2Fstudentaffair%2Farea%2Fgym_<?=date('y')+89?>(1-12).xls">台大醫體(場地時間)</a></li>
              <li><a href="#intro">使用說明</a></li>
              <li><a href="#news">最新消息</a></li> 
              <li><a href="http://www.cwb.gov.tw/V7/forecast/week/week.htm">天氣預報</a></li>
              <!--<li><a href="http://ntusportscenter.ntu.edu.tw/ntu/front/news.aspx">WakeUpEarly</a></li>-->
            </ul>
          </div>
        </div>
      </div>
    </div>

    <div class="container">

       <!-- Main hero unit for a primary marketing message or call to action -->
       <div class="hero-unit">
<!--          <h2 align="center">NTU Sport Center--Places Look Up System</h2>-->
          <h2 align="center"><img src="img/logo.png" /></h2>
<!-- Button to trigger modal -->

   </div>

<div class="alert">
  <button type="button" class="close" data-dismiss="alert">&times;</button>
  <strong> Last Update: </strong>
<?
// ----------------------------------------------------------------------
// DB設定
// ----------------------------------------------------------------------
$client = new MongoClient();
$db = $client->badminton->data;

$lastupdate = $db->findOne( array("update"=>0) );
print $lastupdate['savetime'];
?>
</div>

<div class="alert alert-info">
<?
$today = date_create(date("Y-m-d"));
$dateobj = $today;
for($i=0;$i<2;++$i,date_add($dateobj, date_interval_create_from_date_string('1 month'))){
   $wakeup = $db->findOne( array("date"=>date_format($dateobj,'Y/m'),'place'=>"wakeup") );
   echo sprintf("%s<span><a href=\"%s\" target=\"_blank\">%s</a></span>"
      ,$i==0?"":"<br>",$wakeup['url'],$wakeup['title']);
}
?>
</div>
<!--
   <a href="#myModal" role="button" data-toggle="modal">說明</a>
   <div id="myModal" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
     <div class="modal-header">
       <button type="button" class="close" data-dismiss="modal" aria-hidden="true">Explain</button>
       <h3 id="myModalLabel">Explanation</h3>
     </div>
     <div class="modal-body">
      <table class="table table-hover span2"> <tr><td>新體3F<br>新體1F<br>舊體</td></tr> </table>
     </div>
     <div class="modal-footer">
       <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
       <button class="btn btn-primary">Save changes</button>
     </div>
   </div>
-->
<?
echo "<table class=\"table table-hover\">\n";
echo "<tr>\n";
for($i=0;$i<16;++$i){
   if($i==0)$str="Date<br>\n";
   else if($i==1)$str="6~8晨羽";
   else $str=($i+6)."~".($i+7)."";
   echo "<td style=\"vertical-align: middle;\"><strong>$str</strong></td>";
}
echo "</tr>\n";
$today = date_create(date("Y-m-d"));
$dateobj = $today;
for($i=0;$i<20;++$i,date_add($dateobj, date_interval_create_from_date_string('1 days'))){
   echo "<tr>\n";
   echo "<td style=\"vertical-align: middle;\">\n";
   echo date_format($dateobj,'m/d')."<br>\n".date_format($dateobj,'D');
   echo "</td>\n";
   $AVL_IMAGE = '<img src="https://info2.ntu.edu.tw/facilities/Image/14dot1b.gif" border="0">';

   $cursor = $db->find(array("date"=>date_format($dateobj,'Y/m/d')));
   $fields = array("New 1"=>array(),"New 3"=>array(),"Old"=>array());
   foreach ($cursor as $doc) {
      $fields[$doc['place']][$doc['time']] = $doc;
   } 

   for($ti=6;$ti<22;$ti+=$ti==6?2:1){
      $new1F = $fields['New 1'][$ti];
      $new3F = $fields['New 3'][$ti];
      $old = $fields['Old'][(floor($ti/2)*2)];

      $usedCnt = $new1F['used']+$new3F['used'];
      $remainCnt = $new1F['remain']+$new3F['remain'];
      echo "<td used=\"$usedCnt\" remain=\"$remainCnt\">";
      if( $new1F != NULL ){
         if( $new1F['remain']+$new1F['used']>0){
            echo sprintf("<a href=\"%s\" target=\"_blank\">\n",$new1F['detailURL']);
            if($new1F['remain']) echo $AVL_IMAGE;
            echo $new1F['remain']."</a>\n";
            if ( isset($new1F['purchaseURL']) && $new1F['purchaseURL']!=='' )
               echo "<a href=\"".$new1F['purchaseURL']."\" target=\"_blank\"><font color=\"#FF5F45\">租</font></a>";
         }else
            echo $new1F['text'];
      }
      echo "<br>\n";
      if( $new3F != NULL ){
         if( $new3F['remain']+$new3F['used']>0){
            echo sprintf("<a href=\"%s\" target=\"_blank\">\n",$new3F['detailURL']);
            if($new3F['remain']) echo $AVL_IMAGE;
            echo $new3F['remain']."</a>\n";
            if ( isset($new3F['purchaseURL']) && $new3F['purchaseURL']!=='' )
               echo "<a href=\"".$new3F['purchaseURL']."\" target=\"_blank\"><font color=\"#FF5F45\">租</font></a>";
         }else
            echo $new3F['text'];
      }
      echo "<br>\n";
      if( $old != NULL){
         if ($old['abbr']=='')
            echo sprintf("<a style=\"color: #0000FF\">$AVL_IMAGE 6</a>");
         else
            echo sprintf("<a href=\"%s\" target=\"_blank\" style=\"color: #000000;\">%s</a>\n",$old['detailURL'],$old['abbr']);
      }
      echo "</a>";
      echo "</td>\n";
   }
   echo "</tr>\n";
}

echo "</table>\n";
?>

   <h3 id="intro">說明</h3>
   <ul class="">
     <li class="active">表格三行分別代表: 新體1F,新體3F,舊體</li>
     <li>出現<img src="https://info2.ntu.edu.tw/facilities/Image/14dot1b.gif" border="0">代表有場</li>
     <li>舊體資料為網站提供資料，僅供參考。實際資訊需親自到舊體門口看公告才知道。
     <li>問號或空白代表資料尚未出現，請耐心等待(?)</li>
     <li>綠底是新體有場，紅底是新體場被借光了OAQ</li>
   </ul>

   <h3 id="news">最新消息</h3>
   <ul class="">
      <li>[2014/7/27] 更改圖像 requested by 慧詩XD.</li>
      <li>[2014/1/10] 增加網頁執行效率.</li>
      <li>[2013/7/26] 正式上線嚕.</li>
   </ul>


<!--V
        <div class="span4">
          <h2>Result II</h2>
          <p>to be continued... </p>
          <p><a class="btn" href="#">View details &raquo;</a></p>
       </div>
-->

<div id="fb-root"></div>
<script>
(function(d, s, id) {
   var js, fjs = d.getElementsByTagName(s)[0];
   if (d.getElementById(id)) return;
   js = d.createElement(s); js.id = id;
   js.src = "//connect.facebook.net/en_US/all.js#xfbml=1&appId=423097177803731";
   fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));
</script>

   <div class="fb-like" data-href="http://kiwilab.csie.org/badminton/" data-send="true" data-layout="button_count" data-width="450" data-show-faces="false" data-font="arial"></div>

<a href="https://twitter.com/share" class="twitter-share-button" data-url="http://kiwilab.csie.org/badminton/">Tweet</a>
<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+'://platform.twitter.com/widgets.js';fjs.parentNode.insertBefore(js,fjs);}}(document, 'script', 'twitter-wjs');</script>


      <hr>

      <footer>
        <p>&copy; Copyright Kiwilab, <a href="mailto:small2kuo+badminton@gmail.com">small2kuo</a>. </p>
      </footer>

    </div> <!-- /container -->

<div id="mzry">
   <div class="ukagaka">
      <img class="ukagaka" src="img/org1.png">
   </div>
</div>

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
<!--    <script src="bootstrap/js/bootstrap-transition.js"></script>
    <script src="bootstrap/js/bootstrap-modal.js"></script>
    <script src="bootstrap/js/bootstrap-alert.js"></script>
    <script src="bootstrap/js/bootstrap-dropdown.js"></script>
    <script src="bootstrap/js/bootstrap-scrollspy.js"></script>
    <script src="bootstrap/js/bootstrap-tab.js"></script>
    <script src="bootstrap/js/bootstrap-tooltip.js"></script>
    <script src="bootstrap/js/bootstrap-popover.js"></script>
    <script src="bootstrap/js/bootstrap-button.js"></script>
    <script src="bootstrap/js/bootstrap-collapse.js"></script>
    <script src="bootstrap/js/bootstrap-carousel.js"></script>
    <script src="bootstrap/js/bootstrap-typeahead.js"></script>
    <script src="bootstrap/js/bootstrap-fileupload.js"></script>-->

<script>
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
   (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-42824222-1', 'csie.org');
ga('send', 'pageview');

//$("td[used!=0][remain]").addClass('error');
$("td[used][remain]").each(function(idx){
   if($(this).attr('remain')>0) $(this).addClass('success');
   else if($(this).attr('used')>0) $(this).addClass('error');
});
</script>
  </body>
</html>

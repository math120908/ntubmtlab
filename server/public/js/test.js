Date.prototype.getMonthString = function(option="long"){
  return this.toLocaleString('en-US', {month: option});
}
Date.prototype.getWeekString = function(option="long"){
  return this.toLocaleString('en-US', {weekday: option});
}
Date.prototype.addDay = function(day){
  return new Date(this.getTime() + day * 24 * 60 * 60 * 1000);
}
Date.prototype.getFullDate = function(day){
  return this.getDate() < 10 ? `0${this.getDate()}` : this.getDate();
}
Date.prototype.moveToStartOfWeek = function(){
  return this.addDay(-this.getDay());
}
var range = (from, to) => Array.from(new Array(to-from), (x,i) => from+i);
var get = function(data, ...attrs){
  if (typeof(data) !== 'undefined' && attrs.length > 0){
    if (data.hasOwnProperty(attrs[0])){
      let attr = attrs[0];
      attrs.shift();
      return get(data[attr], ...attrs);
    }
    else return undefined;
  }
  return data;
}

class CourtAvaliableInfo extends React.Component{
  constructor(props){
    super(props);
    this.handleTouchToggle = this.handleTouchToggle.bind(this);
  }
  componentWillMount(){
    //React.initializeTouchEvents(true);
  }
  handleTouchToggle(e) {
    e.target.toggleClass('hover_effect');
  }
  render(){
    let data = this.props.data;
    if ( typeof data === 'undefined' ){
      return (<div className='css_td'> ? </div>);
    }else{
      let remain = Number(get(data, 'remain'));
      let used = Number(get(data, 'used'));

      let html;
      if ( remain+used == 0 ){
        html = (<span>X <span className="tooltiptext">{get(data, 'text')}</span> </span>);
      }else if(remain == 0){
        html = (<a href={get(data, 'detailURL')} target="_blank">{remain}
                </a>);
      }else{
        html = (<a href={get(data, 'purchaseURL')} target="_blank">{remain}
                </a>);
      }
      //.tooltiptext
      let classStyle = `css_td tooltip ${remain+used==0 ? "none" : remain==0?"failed":"success"}`;
      return (
        <div className={classStyle}
          onTouchStart={this.handleTouchToggle}
          onTouchCancel={this.handleTouchToggle}
          onTouchEnd={this.handleTouchToggle}>
          {html}
        </div>
      );
    };
  }
}

class PeriodDailySchedule extends React.Component{
  render(){
    var datetime = new Date(this.props.date+', '+this.props.time+':00:00 GMT+0800 (CST)');
    return(
      <div className='css_td'>
        <div className='css_table'>
          <div className='css_tr'>
            <CourtAvaliableInfo data={get(this.props.data, this.props.date, this.props.time, 'New 1')}/>
          </div>
          <div className='css_tr'>
            <CourtAvaliableInfo data={get(this.props.data, this.props.date, this.props.time, 'New 3')}/>
          </div>
          <div className='css_tr'>
            <CourtAvaliableInfo data={get(this.props.data, this.props.date, this.props.time, 'Old')}/>
          </div>
        </div>
        <table>
        </table>
      </div>
    );
  }
}

class PeriodWeeklySchedule extends React.Component{
  render(){
    var firstWeekDate = new Date(this.props.firstWeekDate);
    var dates = range(0, 7).map((shift) => firstWeekDate.addDay(shift));
    const events_in_row = dates.map((day, idx) =>
      <PeriodDailySchedule date={day.toDateString()} time={this.props.time} data={this.props.data} />
    );
    return (
      <div className='css_tr'>
        <div className='css_td'>
          <span className='time_mark'>{this.props.time}</span>
          <span className='locate_mark'>&nbsp;新1F&nbsp; </span> <br />
          <span className='locate_mark'>&nbsp;新3F&nbsp; </span> <br />
          <span className='locate_mark'>&nbsp;舊1F&nbsp; </span>
        </div>
        {events_in_row}
      </div>
    );
  }
}
class WeeklySchedule extends React.Component{
  render(){
    const timerows = ([6].concat(range(8, 22))).map((timestart, idx) =>
      <PeriodWeeklySchedule firstWeekDate={this.props.firstWeekDate} time={timestart} data={this.props.data} />
    );
    return(
      <div className='css_tbody'>
        {timerows}
      </div>
    );
  }
}

class WeeklyHeader extends React.Component{
  render(){
    var firstWeekDate = new Date(this.props.firstWeekDate);
    var dates = range(0, 7).map((shift) => firstWeekDate.addDay(shift));
    const weekdays = dates.map((day, idx) =>
      <div className='css_td' key={idx}>
        <span className='date'>{day.getFullDate()}</span> <br/>
        <span >{day.getWeekString('short')}</span>
      </div>
    );
    return(
        <div className='css_thead'>
          <div className='css_th'>
            <div className='css_td'> </div>
            {weekdays}
          </div>
        </div>
    );
  }
}

class Calendar extends React.Component{
  constructor(props){
    super(props);
    var today = new Date();
    this.state = {firstWeekDate: today.moveToStartOfWeek(), data:{} };
    this.previousWeek = this.previousWeek.bind(this);
    this.nextWeek = this.nextWeek.bind(this);
  }
  reloadData() {
    this.scheduleUrl = (date) => "q/" + date.getFullYear() + "/" + (date.getMonth()+1) + "/" + date.getDate();
    var dates = range(0, 7).map((shift) => this.state.firstWeekDate.addDay(shift));
    var dates_info_getter = dates.map( (date) =>
      new Promise( (resolve, reject) => {
        $.ajax({
          url: this.scheduleUrl(date),
          dataType: 'json',
          cache: false,
          success: function(data) {
            resolve([date,data]);
          }.bind(this),
          error: function(xhr, status, err) {
            console.error(this.state.firstWeekDate, status, err.toString());
          }.bind(this)
        });
      })
    );
    Promise.all(dates_info_getter).then(values => {
      this.setState((preState) => {
        values.forEach(([date, data]) => {
          preState.data[date.toDateString()] = data;
        });
        return {data: preState.data};
      });
    });
  }
  previousWeek(e){
    this.setState(
      (prevState) => ({firstWeekDate: prevState.firstWeekDate.addDay(-7), data:{}}),
      this.reloadData
    );
    console.log(this.state.firstWeekDate);
  }
  nextWeek(e){
    this.setState(
      (prevState) => ({firstWeekDate: prevState.firstWeekDate.addDay(+7), data:{}}),
      this.reloadData
    );
    console.log(this.state.firstWeekDate);
  }
  componentDidUpdate() {
  }
  componentDidMount() {
    this.reloadData();
  }
  componentDidUnmount() {
  }
  shouldComponentUpdate(nextProps, nextState){
    console.log(nextState.data);
    if (nextState.data != this.state.data)
      return Object.keys(nextState.data).length == 7;
    return true;
  }
  render(){
    return (
      <div>
        <div className="month">
        <ul>
          <li className="prev" style={{cursor: 'w-resize'}} onClick={this.previousWeek}>❮</li>
          <li className="next" style={{cursor: 'e-resize'}} onClick={this.nextWeek}>❯</li>
          <li style={{textAlign:"center"}}>{this.state.firstWeekDate.getMonthString()}<br />
            <span style={{fontSize:18+"px"}}>{this.state.firstWeekDate.getFullYear()}</span>
          </li>
        </ul>
        </div>
        <div id='css_table'>
          <WeeklyHeader firstWeekDate={this.state.firstWeekDate}/>
          <WeeklySchedule firstWeekDate={this.state.firstWeekDate} data={this.state.data}/>
        </div>
      </div>
    );
  }
}

ReactDOM.render(
  <Calendar />,
  document.getElementById('schedule')
);


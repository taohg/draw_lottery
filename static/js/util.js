Date.prototype.Format = function (fmt) {
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "h+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds() //秒
    };
    if (/(y+)/.test(fmt)){ //根据y的长度来截取年
	fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    }
    for (var k in o){
	if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    }
    return fmt;
}

function dateFormatter(date){
    return date.Format("yyyy-MM-dd");
}

function datetimeFormatter(date){
    return date.Format("yyyy-MM-dd hh:mm:ss");
}


var time1 = new Date().Format("yyyy-MM-dd");
var time2 = new Date(1469281964000).Format("yyyy-MM-dd hh:mm:ss");

/*重写JQuery easyui的datebox日期格式 */
$.fn.datebox.defaults.formatter = function(date){
    var y = date.getFullYear();
    var m = date.getMonth()+1;
    var d = date.getDate();
    return date.Format("yyyy-MM-dd")
}

$.fn.datebox.defaults.parser = function(s){
    var t = Date.parse(s);
    if (!isNaN(t)){
        return new Date(t);
    } else {
        return new Date();
    }
}

/*重写JQuery easyui的datetimebox日期格式 */
$.fn.datetimebox.defaults.formatter = function(date){
    var y = date.getFullYear();
    var m = date.getMonth()+1;
    var d = date.getDate();
    return date.Format("yyyy-MM-dd hh:mm:ss")
}

$.fn.datetimebox.defaults.parser = function(s){
    var t = Date.parse(s);
    if (!isNaN(t)){
        return new Date(t);
    } else {
        return new Date();
    }
}
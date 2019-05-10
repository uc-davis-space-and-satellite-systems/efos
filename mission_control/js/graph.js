var smoothie = new SmoothieChart({tooltip:true});
var smoothie2 = new SmoothieChart({tooltip:true});
var smoothie3 = new SmoothieChart({tooltip:true});

smoothie.streamTo(document.getElementById("mycanvas"));
smoothie2.streamTo(document.getElementById("mycanvas2"));
smoothie3.streamTo(document.getElementById("mycanvas3"));

// Data
var acc_x = new TimeSeries();
var acc_y = new TimeSeries();
var acc_z = new TimeSeries();
var mag_x = new TimeSeries();
var mag_y = new TimeSeries();
var mag_z = new TimeSeries();
var triad_x = new TimeSeries();
var triad_y = new TimeSeries();
var triad_z = new TimeSeries();

// Add data from socket tot he time series
$(function () {
    var socket = io();
    socket.on('data', function (msg) {
      msg = JSON.parse(msg)
      var now = new Date().getTime()
      acc_x.append(now, msg["acc_x"]);
      acc_y.append(now, msg["acc_y"]);
      acc_z.append(now, msg["acc_z"]);
      mag_x.append(now, msg["mag_x"]);
      mag_y.append(now, msg["mag_y"]);
      mag_z.append(now, msg["mag_z"]);
      triad_x.append(now, msg["triad_x"]);
      triad_y.append(now, msg["triad_y"]);
      triad_z.append(now, msg["triad_z"]);
      // console.log(accy);
    });

});

// Add to SmoothieChart
smoothie.addTimeSeries(acc_x, {lineWidth:2,strokeStyle:'gold'});
smoothie.addTimeSeries(acc_y, {lineWidth:2,strokeStyle:'red'});
smoothie.addTimeSeries(acc_z, {lineWidth:2,strokeStyle:'green'});

smoothie2.addTimeSeries(mag_x, {lineWidth:2,strokeStyle:'gold'});
smoothie2.addTimeSeries(mag_y, {lineWidth:2,strokeStyle:'red'});
smoothie2.addTimeSeries(mag_z, {lineWidth:2,strokeStyle:'green'});

smoothie3.addTimeSeries(triad_x, {lineWidth:2,strokeStyle:'gold'});
smoothie3.addTimeSeries(triad_y, {lineWidth:2,strokeStyle:'red'});
smoothie3.addTimeSeries(triad_z, {lineWidth:2,strokeStyle:'green'});

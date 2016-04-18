/* global $, Dashboard */

var dashboard = new Dashboard();

dashboard.addWidget('clock_widget', 'Clock');

dashboard.addWidget('users_widget', 'Knob', {
    getData: function () {
      Dashing.utils.get('users_widget/', this.gotData.bind(this));
    },
    gotData: function(data) {
        $.extend(this.scope, data);
    }
});


function bell(){
    var bellSound = new Audio("/static/sounds/bell.wav");
    bellSound.play();
}


function updateWidget(data) {
    $.each(dashboard.getWidgets(), function(i, widgetWrapper) {
        if (data.widget === widgetWrapper.name && widgetWrapper.widget.gotData){
            widgetWrapper.widget.gotData(data.payload);
        }
    });
}

window.addEventListener("websocket.open", function () {
    bell();
});

window.addEventListener("websocket.dashboard", function (e) {
    updateWidget(e.detail.payload);
});
window.addEventListener("websocket.response", function (e) {
   console.log(e.detail.payload);
});
window.addEventListener("websocket.db_event", function (e) {
    var payload = e.detail.payload;
    if (payload.created && payload.label === "users.user") {
        bell();
    }
});

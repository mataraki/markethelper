document.addEventListener('DOMContentLoaded', function() {

  fetch_events();
  setTimeout(function(){load_calendar()}, 100);
})

function load_calendar() {
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    height: 500,
    events: '/events',
    selectable: true,
    editable: true,
    
    select: function(event, allDay) {
        var title = prompt("Enter Event Title");
        var share = prompt("Enter Stock's Ticker");
        if (title) {
            var start = moment(event.start, 'DD.MM.YYYY').format('YYYY-MM-DD HH:mm:ss');
            var end = moment(event.end, 'DD.MM.YYYY').format('YYYY-MM-DD HH:mm:ss');
            $.ajax({
                type: "GET",
                url: '/add_event',
                data: {'title': title, 'share': share, 'start': start, 'end': end},
                dataType: "json",
                success: function (data) {
                    calendar.refetchEvents();
                    alert("Added Successfully");
                },
                error: function (data) {
                    alert('There is a problem!!!');
                }
            });
        }
    },
    eventResize: function(event) {
        var start = moment(event.event.start, 'DD.MM.YYYY').format('YYYY-MM-DD HH:mm:ss');
        var end = moment(event.event.end, 'DD.MM.YYYY').format('YYYY-MM-DD HH:mm:ss');
        var title = event.event.title;
        var id = event.event.id;
        $.ajax({
            type: "GET",
            url: '/update_event',
            data: {'title': title, 'start': start, 'end': end, 'id': id},
            dataType: "json",
            success: function (data) {
                calendar.refetchEvents();
                alert('Event Update');
            },
            error: function (data) {
                alert('There is a problem!!!');
            }
        });
    },

    eventDrop: function(event) {
        var start = moment(event.event.start, 'DD.MM.YYYY').format('YYYY-MM-DD HH:mm:ss');
        var end = moment(event.event.end, 'DD.MM.YYYY').format('YYYY-MM-DD HH:mm:ss');
        var title = event.event.title;
        var id = event.event.id;
        $.ajax({
            type: "GET",
            url: '/update_event',
            data: {'title': title, 'start': start, 'end': end, 'id': id},
            dataType: "json",
            success: function (data) {
                calendar.refetchEvents();
                alert('Event Update');
            },
            error: function (data) {
                alert('There is a problem!!!');
            }
        });
    },

    eventClick: function(event) {
        if (confirm("Are you sure you want to remove it?")) {
            var id = event.event.id;
            $.ajax({
                type: "GET",
                url: '/remove_event',
                data: {'id': id},
                dataType: "json",
                success: function (data) {
                    calendar.refetchEvents();
                    alert('Event Removed');
                },
                error: function (data) {
                    alert('There is a problem!!!');
                }
            });
        }
    },
  });
  calendar.render();
}

function fetch_events() {
  fetch('/events')
  .then(response => response.json())
  .then(events => {
      events_list = events;
  });
}
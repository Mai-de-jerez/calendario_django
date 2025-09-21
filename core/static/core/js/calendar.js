document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: window.innerWidth < 576 ? 'timeGridWeek' : 'dayGridMonth',
        locale: 'es',
        height: window.innerWidth < 576 ? 'auto' : 'parent',

        headerToolbar: {
            left: 'prev,next',
            center: 'title',
            right: 'today dayGridMonth,timeGridWeek,timeGridDay'
        },


        slotLabelFormat: {
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
        },

        events: '/eventos/api/eventos/',
        displayEventTime: false,
        fixedWeekCount: true,
        dayMaxEvents: true,

        eventClick: function (info) {
            window.location.href = info.event.url;
        },

        datesSet: function () {
            // Estilos responsivos solo en móvil
            if (window.innerWidth < 576) {
                const titleEl = document.querySelector('.fc-toolbar-title');
                if (titleEl) {
                    titleEl.style.fontSize = '1rem';
                    titleEl.style.lineHeight = '1.2';
                }

                calendarEl.querySelectorAll('.fc-button').forEach((btn) => {
                    btn.style.fontSize = '0.75rem';
                    btn.style.padding = '0.2rem 0.4rem';
                });

                const toolbar = document.querySelector('.fc-header-toolbar');
                if (toolbar) {
                    toolbar.style.flexDirection = 'column';
                    toolbar.style.alignItems = 'stretch';
                    toolbar.style.gap = '0.5rem';
                }
            }
        }
    });

    calendar.render();
});
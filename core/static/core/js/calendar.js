document.addEventListener('DOMContentLoaded', function() {
            var calendarEl = document.getElementById('calendar');
            var calendar = new FullCalendar.Calendar(calendarEl, {
                initialView: 'dayGridMonth',
                locale: 'es',
                height: 'parent',
                headerToolbar: {
                    left: 'prev,next',
                    center: 'title',
                    right: 'today dayGridMonth,timeGridWeek,timeGridDay'
                },
                
                slotLabelFormat: {
                    hour: '2-digit',
                    minute: '2-digit',
                    hour12: false // Esto asegura el formato de 24 horas
                },
                        
                events: '/eventos/api/eventos/',
                displayEventTime: false,
                fixedWeekCount: true,
                dayMaxEvents: true, // Activa el botón "+X más"

                eventClick: function(info) {
                // Redirige al usuario a la URL de detalles del evento
                window.location.href = info.event.url;
                }
            });
            calendar.render();
        });
from models import Event


def get_event_message_info(
    event: Event,
    in_english: bool = False,
) -> str:
    if in_english: 
        date_field_name = 'Date'
        event_date_string = event.date.strftime('%m.%d.%Y')
        location_field_name = 'Location'
        register_link_field_name = 'Registration link'
    
    else:
        date_field_name = 'Дата провения'
        event_date_string = event.date.strftime('%d.%m.%Y')
        location_field_name = 'Локация'
        register_link_field_name = 'Ссылка на регистрацию'
        
    return (
        f'<b>{event.name}</b>\n\n'
        f'<b>{date_field_name}:</b> {event_date_string}\n'
        f'<b>{location_field_name}:</b> {event.location}\n\n'
        f'<a href="{event.register_link}"><b>{register_link_field_name}</b></a>'
    )
    
    
    
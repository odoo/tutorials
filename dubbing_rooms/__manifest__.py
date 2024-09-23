{
    'name': 'DUBBING',
    'version': '17.0.1.0.0',
    'description': "Dubbing Rooms",
    'depends': [
        'base', 'project',
        'room'
    ],
    'data': [
        'security/ir.model.access.csv',

        'views/room_availability_views.xml',
        'views/room_room_views.xml',
        'views/room_booking_views.xml',
    ],
    'demo': [

    ],
    'installable': True,
    'license': 'LGPL-3'
}
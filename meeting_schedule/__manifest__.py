{
	'name': "Meeting Reservation",
	'depends': ['base','hr','calendar'],
	'application': True,
	'data': [
	    "security/ir.model.access.csv",
		"security/meeting_security.xml",
		"views/meeting_building_views.xml",
        "views/meeting_room_views.xml",
        "views/reservation_views.xml",
        "views/meeting_menus.xml",
	],
}
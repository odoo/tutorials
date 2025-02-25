from odoo import api, fields, models, _

class EventTemplateTicket(models.Model):
    _inherit = 'event.type.ticket'

    seats_max_per_buyer = fields.Integer(
        string='Max Tickert Per Buyer',
        help="Define the number of tickets single user can buy. If Set to 0 "
             "single user can buy all available tickets."
    )

    @api.model
    def _get_event_ticket_fields_whitelist(self):
        """ Whitelist of fields that are copied from event_type_ticket_ids to event_ticket_ids when
        changing the event_type_id field of event.event """
        return ['sequence', 'name', 'description', 'seats_max', 'seats_max_per_buyer']

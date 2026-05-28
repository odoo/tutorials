from datetime import timedelta

from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Types'
    _rec_name = 'type'
    _order = 'type'

    colour = fields.Selection(
        [
            ('red', 'Red'),
            ('green', 'Green'),
            ('yellow', 'Yellow')
        ]
    )
    offer_alert = fields.Integer(compute='_compute_offer_alert')
    offer_count = fields.Integer(compute='_compute_offer_count')
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_type_id')
    pricey_count = fields.Integer(compute='_compute_pricey_count')
    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='property_type_id')
    type = fields.Char(required=True)

    _check_name = models.Constraint(
        'UNIQUE (type)',
        "Property Type should be unique",
    )

    @api.depends('offer_ids.deadline')
    def _compute_offer_alert(self):
        for property in self:
            today = fields.Date.context_today(property)
            alert = timedelta(days=1)
            property.offer_alert = len(property.offer_ids.filtered(
                lambda o: o.deadline and abs(o.deadline - today) <= alert
                and o.status not in ['refused', 'accepted'])
            )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)

    @api.depends('property_ids.expected_price')
    def _compute_pricey_count(self):
        for property in self:
            property.pricey_count = len(property.property_ids.filtered(lambda prop: prop.expected_price > 100000))

    def action_see_offers(self):
        """
        Returns an action to display all offers associated with this property type.
        """
        self.ensure_one()
        action = self.env['ir.actions.actions']._for_xml_id('estate.estate_property_offer_action')
        action['domain'] = [('property_type_id', '=', self.id)]
        return action

    def action_pricey_property(self):
        """
        Displays high-value available properties of this specific type.
        """
        self.ensure_one()
        action = self.env['ir.actions.actions']._for_xml_id('estate.estate_property_action')
        action['domain'] = [
            ('expected_price', '>=', 100000),
            ('property_type_id', '=', self.id)
        ]
        action['context'] = {'search_default_available': 0}
        return action

    def action_offer_alert(self):
        """
        Filters for offers linked to this property type that have not been
        accepted or refused and where the deadline is today or in the future.
        """
        self.ensure_one()
        action = self.env['ir.actions.actions']._for_xml_id('estate.estate_property_offer_action')
        action['domain'] = [
            ('property_type_id', '=', self.id),
            ('deadline', '>=', fields.Date.context_today(self)),
            ('status', 'not in', ['refused', 'accepted'])
        ]
        return action

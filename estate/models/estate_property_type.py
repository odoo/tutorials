from odoo import fields, models, api


class EstatePropertyTypes(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Types'
    _order = 'sequence, name asc'

    name = fields.Char("Title", required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    sequence = fields.Integer('Sequence')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(
        string=' Number of Offers',
        compute='_compute_offer_count',
        store=True
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def action_open_offers(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Property Offers',
            'res_model': 'estate.property.offer',
            'view_mode': 'tree,form',
            'domain': [('property_type_id', '=', self.id)],
        }

    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)',
         'Name of the Property must be unique')
    ]

from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char("Estate Type", required=True)
    property_ids = fields.One2many('estate.property', inverse_name='property_type_id')
    sequence = fields.Integer('Sequence', default=1, help="Used to order types on the business needs")
    offer_ids = fields.One2many('estate.property.offer', inverse_name='property_type_id')
    _order = 'name desc'

    _sql_constraints = [
        ('name', 'UNIQUE(name)',
         'The name of the type should be unique.')
    ]

    def action_open_offers(self):
        self.ensure_one()
        return {
            'name': 'Property Offer',
            'views': [(False, 'list')],
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.offer_ids.ids)],
            'res_model': 'estate.property.offer'
        }

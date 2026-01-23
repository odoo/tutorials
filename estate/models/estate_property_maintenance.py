from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_is_zero


class PropertyMantainance(models.Model):
    _name = 'estate.property.maintenance'
    _description = 'show propety maintenance request'

    name = fields.Char(string="Title", required=True)
    cost = fields.Float()
    status = fields.Selection(selection=[(
        'new', "New"), ('approved', "Approved"), ('done', "Done")], default='new')
    property_id = fields.Many2one('estate.property')

    @api.onchange('status')
    def _onchange_status(self):
        for record in self:
            if record.status == 'approved' and float_is_zero(record.cost, precision_rounding=0.01):
                raise UserError(_("Cost must be greater than zero."))

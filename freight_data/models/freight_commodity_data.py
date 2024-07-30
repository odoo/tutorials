from odoo import api, fields, models
from odoo.exceptions import ValidationError


class FreightCommodityData(models.Model):
    _name = "freight.commodity.data"
    _description = "Freight Commodity Data Model"
    _inherits = {'freight.data': 'inherit_data'}

    inherit_data = fields.Many2one(
        comodel_name='freight.data',
        ondelete='cascade'
    )
    hs_code = fields.Char("HsCode", required=True)
    import_tax = fields.Float("Import Tax(%)")
    vat = fields.Float("VAT(%)")
    tag = fields.Many2many(
        comodel_name="freight.tags",
        string="Tag",
    )
    commodity_group = fields.Many2one(
        comodel_name="freight.commodity.group",
        string="Commodity Group",
        domain=[('status', '=', 'true')]
    )
    commodity_req = fields.Many2many(
        comodel_name="commodities.options",
        string="Commodity Req.",
    )
    created_by = fields.Many2one(
        'res.users',
        string="Created By",
        default=lambda self: self.env.user
    )
    created_on = fields.Date("Created On", copy=False, default=fields.Date.today())
    industry = fields.Many2one(
        comodel_name="res.partner.industry",
        string="Industry",
    )
    last_updated_by = fields.Many2one('res.users', string='Last Updated by', readonly=True)
    last_updated_on = fields.Date('Last Updated on', readonly=True)
    import_approval = fields.One2many(
        comodel_name="approval.import.description",
        inverse_name="import_id",
        string="Import Approval"
    )
    export_approval = fields.One2many(
        comodel_name="approval.export.description",
        inverse_name="import_id",
        string="Import Approval"
    )
    import_customs_req = fields.One2many(
        comodel_name="customs.import.description",
        inverse_name="import_id",
        string="Import Customs Req."
    )
    export_customs_req = fields.One2many(
        comodel_name="customs.export.description",
        inverse_name="import_id",
        string="Import Customs Req."
    )

    @api.constrains('hs_code')
    def _check_hs_code(self):
        for record in self:
            hs_code = record.hs_code.replace(" ", "")
            if not hs_code.isdigit():
                raise ValidationError("HS Code must only contain numbers and spaces.")
            if len(hs_code) != 10:
                raise ValidationError("HS Code must be 10 digits long, excluding spaces.")
            numbers = hs_code.split()
            for number in numbers:
                if int(number) % 2 != 0:
                    raise ValidationError("All numbers in the HS Code must be even.")

    def create(self, vals):
        vals['last_updated_by'] = self.env.user.id
        vals['last_updated_on'] = fields.Date.today()
        return super().create(vals)

    def write(self, vals):
        vals['last_updated_by'] = self.env.user.id
        vals['last_updated_on'] = fields.Date.today()
        return super().write(vals)

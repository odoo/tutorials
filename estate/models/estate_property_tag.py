from odoo import api, fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer("Color Index")

    # SQL Constraint
    _check_name = models.Constraint('UNIQUE(name)', "The name must be unique")

    local_datetime = fields.Char(
        compute='_compute_local_datetime', store=True)

    # Copmute Method - Depends Decorator
    @api.depends('create_date')
    def _compute_local_datetime(self):
        for record in self:
            if record.create_date:
                # user_tz = self.env.user.tz or 'Asia/Kolkata'
                local_dt = fields.Datetime.context_timestamp(
                    record, record.create_date
                )
                record.local_datetime = local_dt.strftime("%Y-%m-%d %H:%M:%S")
            else:
                record.local_datetime = False

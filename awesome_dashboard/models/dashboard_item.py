from odoo import models, fields, api


class DashboardItem(models.Model):
    _name = 'awesome_dashboard.dashboard.item'
    _description = "Dashboard Item"

    code = fields.Char(string="Code", required=True)
    property = fields.Selection(
        string="Property",
        required=True,
        selection=[
            ('average_quantity', "average_quantity"),
            ('average_time', "average_time"),
            ('nb_cancelled_orders', "nb_cancelled_orders"),
            ('nb_new_orders', "nb_new_orders"),
            ('orders_by_size', "orders_by_size"),
            ('total_amount', "total_amount"),
        ]
    )
    size = fields.Integer(string="Size", default=1)
    name = fields.Char(string="Name", required=True, translate=True)
    description = fields.Text(string="Description", required=True, translate=True)
    component_type = fields.Selection(
        string="Component Type",
        required=True,
        selection=[
            ('number_card', "Number"),
            ('pie_chart_chart', "PieChart"),
        ]
    )
    sequence = fields.Integer(string="Sequence", default=1)
    user_id = fields.Many2one(comodel_name='res.users', string="User", required=True, default=lambda self: self.env.user)

    _code_user_unique_idx = models.UniqueIndex(
        '(code, user_id)',
        "The code and user must be unique."
    )

    @api.model
    def get_by_current_user(self):
        return self.search_read([('user_id', '=', self.env.user.id)], [
            'code',
            'property',
            'size',
            'name',
            'description',
            'component_type',
            'sequence',
        ], order='sequence ASC')

# -*- coding: utf-8 -*-
import logging
import random
import time
from odoo import models, fields, api
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime, timedelta, date

_logger = logging.getLogger(__name__)


class TShirtOrder(models.Model):
    _name = 'awesome_tshirt.order'
    _description = 'Awesome T-shirt Orders'
    _rec_name = 'customer_id'
    _inherit = ['mail.thread']

    @api.model
    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    amount = fields.Float('Amount', compute='_compute_amount', store=True)
    customer_id = fields.Many2one('res.partner', string="Customer")
    image_url = fields.Char('Image', help="encodes the url of the image")
    is_late = fields.Boolean('Is late', compute='_compute_is_late')
    quantity = fields.Integer('Quantity', default="1")
    size = fields.Selection([
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL')], default='m', required="True")
    state = fields.Selection([
        ('new', 'New'),
        ('printed', 'Printed'),
        ('sent', 'Sent'),
        ('cancelled', 'Cancelled')], default='new', required="True", group_expand='_expand_states')

    @api.depends('quantity')
    def _compute_amount(self):
        for record in self:
            unit_price = 15
            if record.size == 's':
                unit_price = 12
            elif record.size in ['xl', 'xxl']:
                unit_price = 18
            if record.quantity > 5:
                unit_price = unit_price * 0.9
            record.amount = record.quantity * unit_price

    @api.depends('create_date')
    def _compute_is_late(self):
        for record in self:
            record.is_late = record.create_date < datetime.today() - timedelta(days=7)

    def print_label(self):
        """
        This method simulate the printing of a label. It is slow (> 500ms), and
        if randomly fails. It returns True if the label has been printed, False
        otherwise
        """
        time.sleep(0.5)
        if random.random() < 0.1:
            _logger.info('Printer not connected')
            return False
        _logger.info('Label printed')
        return True

    @api.model
    def get_empty_list_help(self, help):
        title = 'There is no t-shirt order'
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url = '%s/awesome_tshirt/order' % base_url
        content = 'People can make orders through the <a href=%(url)s>public page</a>.' % {'url': url}
        return """
            <p class="o_view_nocontent_smiling_face">%s</p>
            <p class="oe_view_nocontent_alias">%s</p>
        """ % (title, content)

    @api.model
    def get_statistics(self):
        """
        Returns a dict of statistics about the orders:
            'average_quantity': the average number of t-shirts by order
            'average_time': the average time (in hours) elapsed between the
                moment an order is created, and the moment is it sent
            'nb_cancelled_orders': the number of cancelled orders, this month
            'nb_new_orders': the number of new orders, this month
            'total_amount': the total amount of orders, this month
        """
        first_day = date.today().replace(day=1).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        last_day = datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        this_month_domain = [('create_date', '>=', first_day), ('create_date', '<=', last_day)]
        new_this_month_domain = expression.AND([this_month_domain, [('state', '=', 'new')]])
        nb_new_orders = self.search_count(new_this_month_domain)
        cancelled_this_month_domain = expression.AND([this_month_domain, [('state', '=', 'cancelled')]])
        nb_cancelled_orders = self.search_count(cancelled_this_month_domain)
        total_amount = self.read_group(new_this_month_domain, ['amount'], [])[0]['amount']
        total_quantity = self.read_group(this_month_domain, ['quantity'], [])[0]['quantity']
        nb_orders = self.search_count(this_month_domain)
        orders_by_size = self.read_group([['state', '!=', 'cancelled']], ['quantity'], ['size'])

        return {
            'average_quantity': 0 if not nb_orders else round(total_quantity / nb_orders, 2),
            'average_time': (random.random() * 44) + 4,  # simulate a delay between 4 and 48 hours
            'nb_cancelled_orders': nb_cancelled_orders,
            'nb_new_orders': nb_new_orders,
            'orders_by_size': {g['size']: g['quantity'] for g in orders_by_size},
            'total_amount': total_amount or 0,
        }

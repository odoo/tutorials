import logging
from datetime import datetime

import psycopg2

from odoo import api, fields, models, tools, _
from odoo.tools import float_is_zero
from odoo.exceptions import UserError
import base64

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = 'pos.order'

    state = fields.Selection(selection_add=[
        ('pay_later', 'Pay Later'),
    ], ondelete={'posted': 'set default'})

    @api.model
    def _complete_values_from_session(self, session, values):
        if values.get('state') and values['state'] in ('paid', 'pay_later') and not values.get('name'):
            values['name'] = self._compute_order_name(session)
        values.setdefault('pricelist_id', session.config_id.pricelist_id.id)
        values.setdefault('fiscal_position_id',
                          session.config_id.default_fiscal_position_id.id)
        values.setdefault('company_id', session.config_id.company_id.id)
        return values

    @api.model
    def _process_order(self, order, existing_order):
        """Create or update an pos.order from a given dictionary.

        :param dict order: dictionary representing the order.
        :param existing_order: order to be updated or False.
        :type existing_order: pos.order.
        :returns: id of created/updated pos.order
        :rtype: int
        """
        draft = True if order.get('state') == 'draft' else False
        done = True if order.get('state') == 'pay_later' else False
        pos_session = self.env['pos.session'].browse(order['session_id'])
        if pos_session.state == 'closing_control' or pos_session.state == 'closed':
            order['session_id'] = self._get_valid_session(order).id

        if order.get('partner_id'):
            partner_id = self.env['res.partner'].browse(order['partner_id'])
            if not partner_id.exists():
                order.update({
                    "partner_id": False,
                    "to_invoice": False,
                })

        pos_order = False
        combo_child_uuids_by_parent_uuid = self._prepare_combo_line_uuids(
            order)

        pos_vals = {key: value for key,
                    value in order.items() if key != 'name'}
        if not existing_order:
            pos_order = self.create({
                **pos_vals,
                'pos_reference': order.get('name')
            })
            pos_order = pos_order.with_company(pos_order.company_id)
        else:
            pos_order = existing_order

            # If the order is belonging to another session, it must be moved to the current session first
            if order.get('session_id') and order['session_id'] != pos_order.session_id.id:
                pos_order.write({'session_id': order['session_id']})

            # Save lines and payments before to avoid exception if a line is deleted
            # when vals change the state to 'paid'
            for field in ['lines', 'payment_ids']:
                if order.get(field):
                    existing_record_ids = self.env[pos_order[field]._name].browse(
                        [r[1] for r in order[field] if r[1] != 0]).exists().ids
                    existing_records_vals = [r for r in order[field] if r[0] not in [
                        1, 2, 3, 4] or r[1] in existing_record_ids]
                    pos_order.write({field: existing_records_vals})
                    order[field] = []

            del order['uuid']
            del order['access_token']
            pos_order.write(order)

        pos_order._link_combo_items(combo_child_uuids_by_parent_uuid)
        self = self.with_company(pos_order.company_id)
        self._process_payment_lines(order, pos_order, pos_session, draft, done)
        return pos_order._process_saved_order(draft, done)

    def _process_payment_lines(self, pos_order, order, pos_session, draft, done):
        """Create account.bank.statement.lines from the dictionary given to the parent function.

        If the payment_line is an updated version of an existing one, the existing payment_line will first be
        removed before making a new one.
        :param pos_order: dictionary representing the order.
        :type pos_order: dict.
        :param order: Order object the payment lines should belong to.
        :type order: pos.order
        :param pos_session: PoS session the order was created in.
        :type pos_session: pos.session
        :param draft: Indicate that the pos_order is not validated yet.
        :type draft: bool.
        """
        prec_acc = order.currency_id.decimal_places

        # Recompute amount paid because we don't trust the client
        order.with_context(backend_recomputation=True).write(
            {'amount_paid': sum(order.payment_ids.mapped('amount'))})

        if not draft and not done and not float_is_zero(pos_order['amount_return'], prec_acc):
            cash_payment_method = pos_session.payment_method_ids.filtered('is_cash_count')[
                :1]
            if not cash_payment_method:
                raise UserError(
                    _("No cash statement found for this session. Unable to record returned cash."))
            return_payment_vals = {
                'name': _('return'),
                'pos_order_id': order.id,
                'amount': -pos_order['amount_return'],
                'payment_date': fields.Datetime.now(),
                'payment_method_id': cash_payment_method.id,
                'is_change': True,
            }
            order.add_payment(return_payment_vals)
            order._compute_prices()

    def _process_saved_order(self, draft, done):
        self.ensure_one()
        if not draft and self.state != 'cancel':
            try:
                self.action_pos_order_paid()
            except psycopg2.DatabaseError:
                # do not hide transactional errors, the order(s) won't be saved!
                raise
            except Exception as e:
                _logger.error(
                    'Could not fully process the POS Order: %s', tools.exception_to_unicode(e))
            self._create_order_picking(done)
            self._compute_total_cost_in_real_time()

        if self.to_invoice and self.state == 'paid':
            self._generate_pos_order_invoice()

        return self.id

    def _create_order_picking(self, done):
        self.ensure_one()
        if self.shipping_date:
            self.sudo().lines._launch_stock_rule_from_pos_order_lines()
        else:
            if self._should_create_picking_real_time():
                picking_type = self.config_id.picking_type_id
                if self.partner_id.property_stock_customer:
                    destination_id = self.partner_id.property_stock_customer.id
                elif not picking_type or not picking_type.default_location_dest_id:
                    destination_id = self.env['stock.warehouse']._get_partner_locations()[
                        0].id
                else:
                    destination_id = picking_type.default_location_dest_id.id

                pickings = self.env['stock.picking']._create_picking_from_pos_order_lines(
                    destination_id, self.lines, picking_type, self.partner_id, done)
                pickings.write({'pos_session_id': self.session_id.id,
                                'pos_order_id': self.id, 'origin': self.name})

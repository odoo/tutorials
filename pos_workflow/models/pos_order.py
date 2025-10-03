import logging
from datetime import datetime
from random import randrange
from pprint import pformat

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
    def sync_from_ui(self, orders):
        """ Create and update Orders from the frontend PoS application.

        Create new orders and update orders that are in draft status. If an order already exists with a status
        different from 'draft' it will be discarded, otherwise it will be saved to the database. If saved with
        'draft' status the order can be overwritten later by this function.

        :param orders: dictionary with the orders to be created.
        :type orders: dict.
        :param draft: Indicate if the orders are meant to be finalized or temporarily saved.
        :type draft: bool.
        :Returns: list -- list of db-ids for the created and updated orders.
        """
        sync_token = randrange(100_000_000)  # Use to differentiate 2 parallels calls to this function in the logs
        _logger.info("PoS synchronisation #%d started for PoS orders references: %s", sync_token, [
                     self._get_order_log_representation(order) for order in orders])
        order_ids = []
        for order in orders:
            order_log_name = self._get_order_log_representation(order)
            _logger.debug("PoS synchronisation #%d processing order %s order full data: %s",
                          sync_token, order_log_name, pformat(order))

            if len(self._get_refunded_orders(order)) > 1:
                raise ValidationError(
                    _('You can only refund products from the same order.'))

            existing_order = self._get_open_order(order)
            if existing_order and existing_order.state in ('draft', 'pay_later'):
                order_ids.append(self._process_order(order, existing_order))
                _logger.info("PoS synchronisation #%d order %s updated pos.order #%d",
                             sync_token, order_log_name, order_ids[-1])
            elif not existing_order:
                order_ids.append(self._process_order(order, False))
                _logger.info("PoS synchronisation #%d order %s created pos.order #%d",
                             sync_token, order_log_name, order_ids[-1])
            else:
                # In theory, this situation is unintended
                # In practice it can happen when "Tip later" option is used
                order_ids.append(existing_order.id)
                _logger.info("PoS synchronisation #%d order %s sync ignored for existing PoS order %s (state: %s)",
                             sync_token, order_log_name, existing_order, existing_order.state)

        # Sometime pos_orders_ids can be empty.
        pos_order_ids = self.env['pos.order'].browse(order_ids)
        config_id = pos_order_ids.config_id.ids[0] if pos_order_ids else False

        for order in pos_order_ids:
            order._ensure_access_token()
            if not self.env.context.get('preparation'):
                order.config_id.notify_synchronisation(
                    order.config_id.current_session_id.id, self.env.context.get('login_number', 0))

        _logger.info("PoS synchronisation #%d finished", sync_token)
        return pos_order_ids.read_pos_data(orders, config_id)

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
        ready_pickings = self.picking_ids.filtered(
            lambda l: l.state not in ['cancel', 'done'])
        picking_type = self.config_id.picking_type_id
        if self.partner_id.property_stock_customer:
            destination_id = self.partner_id.property_stock_customer.id
        elif not picking_type or not picking_type.default_location_dest_id:
            destination_id = self.env['stock.warehouse']._get_partner_locations()[
                0].id
        else:
            destination_id = picking_type.default_location_dest_id.id
        if self.shipping_date:
            self.sudo().lines._launch_stock_rule_from_pos_order_lines()
        elif self.picking_ids and ready_pickings:
            pickings = self.env['stock.picking']._update_picking_from_pos_order_lines(
                destination_id, self.lines, picking_type, ready_pickings[0], self.partner_id)
            pickings.write({'pos_session_id': self.session_id.id,
                            'pos_order_id': self.id, 'origin': self.name})
        else:
            if self.picking_ids:
                self.picking_ids.write({'state': 'cancel'})
            if self._should_create_picking_real_time():
                pickings = self.env['stock.picking']._create_picking_from_pos_order_lines(
                    destination_id, self.lines, picking_type, self.partner_id, done)
                pickings.write({'pos_session_id': self.session_id.id,
                                'pos_order_id': self.id, 'origin': self.name})

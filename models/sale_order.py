# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero, float_compare, float_round

APPROVAL_REQUEST_ACCEPTED_STATES = ('draft',)
APPROVAL_ACCEPTED_STATES = ('awaiting_approval',)

class SaleOrder(models.Model):
    _inherit = "sale.order"


    state = fields.Selection([
        ('draft', 'Quotation'),
        ('awaiting_approval', 'Awaiting Approval'),
        ('approved_quotation', 'Approved quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    require_approval = fields.Boolean(compute='_compute_require_approval')

    @api.depends('company_id.so_double_validation')
    def _compute_require_approval(self):
        for each in self:
            # FIXME: Here we have use a static precision_digits as it is the value used in all the checks of the monetary fields in sale module
            each.require_approval = each.company_id.so_double_validation == 'two_step' and \
            float_compare(each.amount_total, each.company_id.so_double_validation_amount, precision_digits=2) >= 0


    def action_approval_request(self):
        if not self._check_approval_request():
            raise ValidationError(_("Some Quotation state doesn't allow to request approval!"))
        self._action_approval_request()

    def _check_approval_request(self):
        approval_request_accepted_states = tuple(set(self.mapped("state")).union(set(APPROVAL_REQUEST_ACCEPTED_STATES)))
        if approval_request_accepted_states != APPROVAL_REQUEST_ACCEPTED_STATES:
            return False
        return True


    def _action_approval_request(self):
        self.write({'state':'awaiting_approval'})

    def action_approval(self):
        if not self._check_approval():
            raise ValidationError(_("Some Quotation state doesn't allow the approval!"))
        self._action_approval()

    def _check_approval(self):
        approval_accepted_states = tuple(set(self.mapped("state")).union(set(APPROVAL_ACCEPTED_STATES)))
        if approval_accepted_states != APPROVAL_ACCEPTED_STATES:
            return False
        return True

    def _action_approval(self):
        self.write({'state':'approved_quotation'})

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        if self.env.context.get('mark_so_as_sent'):
            self.filtered(lambda o: o.state == 'approved_quotation').with_context(tracking_disable=True).write({'state': 'sent'})
        return super(SaleOrder,self).message_post(**kwargs)

    # FIXME : here we have overwritten the super method just to edit the warning message,there is not better approach?
    @api.ondelete(at_uninstall=False)
    def _unlink_except_draft_or_cancel(self):
        for order in self:
            if order.state not in ('draft', 'cancel'):
                raise UserError(
                    _('You can not delete a sent,awaiting Approval quotation or a confirmed sales order. You must first cancel it.'))
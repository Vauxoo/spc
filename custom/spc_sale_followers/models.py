# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class Lead(models.Model):

    _inherit = 'crm.lead'

    @api.multi
    def message_get_suggested_recipients(self):
        recipients = super(Lead, self).message_get_suggested_recipients()
        for lead_id, data in recipients.items():
            if data:
                recipients[lead_id] = []
        return recipients


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def message_subscribe(self, partner_ids=None, channel_ids=None, subtype_ids=None, force=True):
        for partner in partner_ids:
            if partner == self.partner_id.id:
                partner_ids.remove(partner)
        return super(SaleOrder, self).message_subscribe()

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


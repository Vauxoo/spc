# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models

class MaKeSale(models.TransientModel):

    _inherit = 'crm.make.sale'


    def makeOrder(self, cr, uid, ids, context=None):
        res = super(MaKeSale, self).makeOrder(cr, uid, ids, context=context)
        if res and 'res_id' in res.keys():
            sale_ids = res['res_id'] and isinstance(res['res_id'], list) or \
                [res['res_id']]
            for sale in self.pool.get('sale.order').browse(
                    cr, uid, sale_ids, context=context):
                origin = sale.origin.split(':')[1]
                sale.write({'name': sale.name + ' - ' + origin})
        return res

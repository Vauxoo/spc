import logging
from openerp import models
from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)


class ProcurementComputeAll(models.TransientModel):

    _inherit = 'procurement.order.compute.all'

    def procure_calculation(self, cr, uid, ids, context=None):
        """
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param ids: List of IDs selected
        @param context: A standard dictionary
        """
        return super(ProcurementComputeAll, self).procure_calculation(
            cr, SUPERUSER_ID, ids, context=context)

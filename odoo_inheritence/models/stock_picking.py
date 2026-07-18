from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    memo = fields.Char(string="Memo")

    def button_validate(self):
        for rec in self:
            if rec.sale_id:
                if not rec.sale_id.memo:
                    raise ValidationError(
                        "you are not available to put any data in memo field because you can't give any data in sale.order model")
                rec.memo = rec.sale_id.memo

        return super(StockPicking, self).button_validate()

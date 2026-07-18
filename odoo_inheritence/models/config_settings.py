from odoo import api, fields, models, tools


class ConfidSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_order_limit = fields.Float(string="Sale Order Limit")
    minimum_limit = fields.Float(string="Minimum Sale Order Limit")
from odoo import api, fields, models, tools


class ResPartner(models.Model):
    _inherit = 'res.partner'

    membership_type = fields.Selection([('silver', 'Silver'), ('gold', 'Gold'), ('platinum', 'Platinum')],
                                       string="Membership Type")

    is_net30_approved = fields.Boolean(string="Is Net30 Approved")
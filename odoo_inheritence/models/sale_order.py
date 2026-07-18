from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    confirmed_user_id = fields.Many2one('res.users', string="Confirmed User")
    name = fields.Char(string="Name", required=True)
    customer_id = fields.Many2one('res.partner', string="Patient")
    presc_line_ids = fields.One2many('hospital.prescription.line', 'sale_order_id',
                                     string="Prescription Lines")
    sample = fields.Char(string="Sample")
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True, ondelete='restrict')
    doctor_line = fields.Char(string="Doctor Line")
    appointment_date = fields.Date(string="Appointment Date")

    membership_type = fields.Selection(string="Membership Type", related='partner_id.membership_type', store=True)
    memo = fields.Char(string="Memo")

    def action_confirm(self):
        res = super().action_confirm()
        print("sucess...")
        self.confirmed_user_id = self.env.user.id
        return res

    def action_sample(self):
        return

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        for order in self:
            if order.presc_line_ids:
                order_lines_commands = []
                for presc_line in order.presc_line_ids:
                    if presc_line.medicine_name:
                        product = self.env['product.template'].search([
                            ('name', '=', presc_line.medicine_name)
                        ], limit=1)
                        print(product)
                        if product:
                            qty = presc_line.dosage
                            line_values = {
                                'product_template_id': product.id,
                                'product_uom_qty': qty,
                            }
                            order_lines_commands.append((0, 0, line_values))
                if order_lines_commands:
                    order.write({'order_line': order_lines_commands})
        return res

    # def action_confirm(self):
    #     res = super().action_confirm()
    #     if self.membership_type == 'platinum':
    #         return {
    #             'type': 'ir.actions.act_window',
    #             'tag': 'display_notification',
    #             'params': {
    #                 'title': 'Platinum',
    #                 'message': 'Customer has platinum membership.',
    #                 'type': 'success',
    #                 'sticky': False,
    #             }
    #         }
    #     return res

    @api.onchange('payment_term_id')
    def onchange_is_net30_approved(self):
        for rec in self:
            if rec.payment_term_id.name == 'net30':
                if not rec.partner_id.is_net30_approved:
                    raise ValidationError("you can't use net30 payment term because this customer is not approved")




class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    total_price = fields.Float(string="Total Price")
    remark_line = fields.Char(string="Remark Line")

    @api.onchange('product_template_id')
    def onchange_never_drop_ship(self):
        if self.product_template_id.never_drop_ship:
            raise ValidationError("This product has never dropped ship.")
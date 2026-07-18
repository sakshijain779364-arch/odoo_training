from odoo import api, fields, models, tools
from datetime import timedelta
from odoo.exceptions import ValidationError



class PropertyOffer(models.Model):
    _name = 'property.offer'
    _description = 'Property Offer'

    _sql_constraints = [
        (
            'check_price', 'CHECK(price > 0)',
            'The offer price must be strictly positive.'
        ),
    ]

    price = fields.Float(string="Price")
    status = fields.Selection([('offer_accepted', 'Offer Accepted'), ('offer_received', 'Offer Received')], copy=False)
    partner_id = fields.Many2one('res.partner',required=True)
    property_id = fields.Many2one('estate.property',required=True)
    validity = fields.Integer(string="Validity",default=5)
    date_deadline = fields.Date(string="Deadline",compute="_compute_date_deadline",inverse="_inverse_date_deadline")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for rec in self:
            create_date = rec.create_date or fields.Date.today()
            rec.date_deadline = create_date + timedelta(days=rec.validity)

    def _inverse_date_deadline(self):
        for rec in self:
            create_date = rec.create_date or fields.Date.today()
            rec.validity = (rec.date_deadline - create_date.date()).days

    def action_accept(self):
        for rec in self:
            rec.status = 'accepted'
            rec.property_id.buyer_id = rec.partner_id
            rec.property_id.selling_price = rec.price
        return True

    def action_refuse(self):
        for rec in self:
            rec.status = 'refused'
        return True

    @api.model
    def create(self, vals):
        property_record = self.env['estate.property'].browse(vals['property_id'])
        if property_record.offer_ids:
            highest_offer = max(property_record.offer_ids.mapped('price'))

            if vals['price'] < highest_offer:
                raise ValidationError(
                    "You cannot create an offer lower than an existing offer."
                )

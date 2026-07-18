from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_is_zero
from odoo.tools import float_compare
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    _sql_constraints = [
        (
            'check_expected_price', 'CHECK(expected_price > 0)',
            'The expected price must be strictly positive.'
        ),
        (
            'check_selling_price', 'CHECK(selling_price >= 0)',
            'The selling price must be positive.'
        ),
    ]

    name = fields.Char(required=True)
    description = fields.Text(string="Description")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(string='Selling Price', copy=False)
    postcode = fields.Integer(string='Postcode')
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string='Garden Orientation')
    available_dates = fields.Date( default=lambda self: fields.Date.today() + relativedelta(months=3),
    copy=False)
    property_type_id = fields.Many2one('property.type', string="Property Type")
    tag_ids = fields.Many2many("property.tag", string="Tags")
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    seller_id = fields.Many2one('res.users', string='Seller')
    offer_ids = fields.One2many('property.offer', 'property_id',string='Offers')
    total_area = fields.Integer(string='Total Area', compute='_compute_total_area')
    best_price = fields.Float(string='Best Price', compute='_compute_best_price')
    state = fields.Selection([('new', 'New'),('sold', 'Sold'),('cancel', 'Cancelled'),('offer_accepted', 'Offer Accepted'), ('offer_received', 'Offer Received'),], string='Status', copy=False , default='new')
    active = fields.Boolean(string='Active', default=True)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user
     )

    def action_cozy(self):
        return True

    def action_renovate(self):
        return True

    @api.depends('name')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('name')
    def _compute_best_price(self):
        for rec in self:
            rec.best_price = max(rec.offer_ids.mapped('price'), default=0.0)

    def action_sold(self):
        for rec in self:
            if self.state =='cancel':
                raise ValidationError('A cancelled property cannot be sold')
            self.state = 'sold'
            return True

    def action_cancel(self):
        for rec in self:
            if self.state == 'sold':
                raise ValidationError('A sold property cannot be cancelled')
            self.state = 'cancel'
            return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for rec in self:

            if not float_is_zero(rec.selling_price, precision_digits=2):
                minimum_price = rec.expected_price * 0.90

                if float_compare(rec.selling_price, minimum_price,
                        precision_digits=2
                ) < 0:
                    raise ValidationError(
                        "Selling price cannot be lower than 90% of expected price."
                    )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise ValidationError(
                    "Only new or cancelled properties can be deleted."
                )
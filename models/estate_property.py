from odoo import models, fields, api
from datetime import timedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Date Availability', copy=False,
                                    default=lambda self: fields.Date.today() + timedelta(days=90))
    active = fields.Boolean(string='Active')
    state = fields.Selection(
        string="State",
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        required=True,
        copy=False,
        default='new')
    expected_price = fields.Float(string='Expected Price')
    selling_price = fields.Float(string='Selling Price', copy=False, readonly=True)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)', default=0)
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')

    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)', default=0)
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string='Garden Orientation')

    # --------- Relationships ---------#

    # Many to One

    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)

    # Many to Many
    tags_id = fields.Many2many('estate.property.tag', string='Tags')

    # one to many
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # --------- Computed fields ---------#

    # Total area
    total_area = fields.Float(string="Total Area", compute='_compute_total_area', store=False, readonly=True)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # best price
    best_price = fields.Float(string='Best Offer', compute='_compute_best_price', store=False, readonly=True)

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for _property in self:
            if _property.offer_ids:
                _property.best_price = max(_property.offer_ids.mapped('price'))
            else:
                _property.best_price = 0.0

    # --------- On changes handlers ---------#
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10
        else:
            self.garden_orientation = ""
            self.garden_area = 0.0

    # --------- Buttons ---------#
    def cancel(self): 
        return True

    def sold(self):
        return True
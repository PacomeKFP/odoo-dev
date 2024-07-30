from datetime import timedelta
from odoo import models, fields


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
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')

    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
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

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'The property name must be unique.'),

    ]

    # Contraintes
    """
    - On ne peut pas preciser d'orientation pour le jardin si  on a pas de jardin
    - Pas de taille de jardin s'il n'y a pas de jardin 
    """

    """@api.constrains('expected_price', 'selling_price')
    def _check_price(self):
        for record in self:
            if record.selling_price and record.selling_price > record.expected_price:
                raise ValidationError('The selling price cannot be higher than the expected price.')
"""

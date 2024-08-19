from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError



class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(string='Status', selection=[('accepted', "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True, readonly=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline',
                                inverse='_inverse_date_deadline', store=True, readonly=True)

    property_type_id = fields.Many2one("estate.property.type", string="Property Type",
                                       related="property_id.property_type_id")

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - create_date).days

    # --------- Action Buttons ---------#

    def action_accept(self):
        for _offer in self:

            if _offer.property_id.state == "offer_accepted":
                raise UserError("There is already an accepted offer")

            if _offer.property_id.state == "cancelled":
                raise UserError("The Property sale have been canceled")

            # Chercher les autres offres sur la meme propriété et modifier
            property_offers = _offer.property_id.mapped("offer_ids")
            for offer in property_offers:
                offer.status = 'refused'

            _offer.status = 'accepted'
            _offer.property_id.state = "offer_accepted"
            _offer.property_id.buyer_id = _offer.partner_id.id
            _offer.property_id.selling_price = _offer.price

        return True

    def action_refuse(self):
        for _offer in self:
            _offer.status = 'refused'

        return True

    # --------- Constraints ---------#
    _sql_constraints = [
        ("price", "check(price>0)", "Offer Price must me positive"),
        ("validity", "check(validity>0)", "Validity must me positive"),
    ]

    # --------- On Create ---------#
    @api.model
    def create(self, vals_list):
        _property = self.env['estate.property'].browse(vals_list["property_id"])

        if not _property:
            raise UserError("The Specified Property does not exists")

        # verifier si le montant est suffisant
        if _property.best_price > vals_list['price']:
            raise UserError(
                f"The amount of the Offer must be at greater than actual best offer which is {_property.best_price}")

        # verifer si le truc n'est pas encore vendu
        if _property.state == "offer_accepted":
            raise UserError("An Offer has already been accepted")

        if _property.state == "sold":
            raise UserError("The Property has been already sold")

        if _property.state == "canceled":
            raise UserError("The Property has been canceled")

        ## Si tout est en regle,
        ### on modifie l'etat de la propriete si elle est nouvelle
        if _property.state == "new":
            _property.state = "offer_received"

        ### on cloture
        return super().create(vals_list)

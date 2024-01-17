from odoo import api, fields, models, _

class MarqueVoiture(models.Model):
    _name = 'location_cars.marque'
    _description = 'Marque de voiture'
    _rec_name = 'name'

    name = fields.Char('Marque', required=True)
    image_128 = fields.Binary("Logo", max_width=128, max_height=128, required=True)

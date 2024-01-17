from odoo import api, fields, models, _
class ModelVoiture(models.Model):
    _name = 'location_cars.model'
    _description = 'Model de voiture'

    brand_id = fields.Many2one('location_cars.marque', 'Marque', required=True, help='Manufacturer of the vehicle')
    name = fields.Char('Model name', required=True)
    image_128 = fields.Binary(related='brand_id.image_128', readonly=True)

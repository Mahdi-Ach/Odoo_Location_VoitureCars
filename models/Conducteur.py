import re

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Conducteur(models.Model):
    _name = 'location_cars.conducteur'
    _description = 'Conducteur de Vehicule'

    name = fields.Char("Nom",required=True)
    email = fields.Char("Email",required=True)
    phone = fields.Char("Phone",required=True)
    image_128 = fields.Binary("Image", max_width=128, max_height=128,required=True)
    _sql_constraints = [
        ('unique_email', 'unique(email)', 'email must be unique!'),
    ]
    @api.constrains('email')
    def _check_email_format(self):
        for record in self:
            if record.email and not self._is_valid_email(record.email):
                raise ValidationError(_("Invalid email address for the Conducteur."))


    @staticmethod
    def _is_valid_email(email):
        # Use a regular expression or any other method to check the email format
        # Here, we use a simple format check, but a more robust validation is recommended
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(regex, email):
            return True
        else:
            return False

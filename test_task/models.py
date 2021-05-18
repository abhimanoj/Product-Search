import json
from django.db import models
from django.utils import timezone
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())



class ProductTable(models.Model):
    product_id = models.AutoField(db_column='product_id', primary_key=True)
    name = models.CharField(max_length=100, db_column='name')
    description = models.TextField(db_column='description', blank = True) 
    is_active = models.CharField(db_column='is_active',  default='N', max_length=10, choices=((1, "Y"), (2, "N")), help_text="'Y' or 'N'")
    create_at = models.DateTimeField(db_column='create_at', default=timezone.now) 
    status    = models.CharField(max_length=100, db_column='status')

    def __str__(self):
        role_data = {}
        role_data['product_id'] = self.product_id
        role_data['name'] = self.name
        role_data['description'] = self.description
        role_data['is_active'] = self.is_active
        role_data['create_at'] = str(self.create_at)
        role_data['status'] = self.status

        return json.dumps(role_data)
 
    
    class Meta:
        db_table = "PRODUCT_DATA"

from flask_admin.contrib.sqla import ModelView
from wtforms import SelectMultipleField

from regions import REGIONS


class MultipleSelect(SelectMultipleField):

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = ",".join(valuelist)
        else:
            self.data = ""


class DriversAdmin(ModelView):
    form_columns = ('driver_telegram_id', 'work_regions', 'vehicle_type')
    column_labels = {
        'driver_telegram_id': 'Driver Telegram ID',
        'work_regions': 'Work Regions',
        'vehicle_type': 'Vehicle Type'
        }
    form_args = {'work_regions': {'render_kw': {"multiple": "multiple"}}}
    form_choices = {'work_regions': REGIONS}

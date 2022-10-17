from django.db import models
from core.models import User, TrackingModel
# Create your models here.


class Control(TrackingModel):

    class order_by(models.TextChoices):
        TITLE = 'TITLE'
        DESCRIPTION = 'DESCRIPTION'
        COMPLETE = 'COMPLETE'

    class complete_filters(models.TextChoices):
        NO = 'NO'
        YES = 'YES'
        ALL = 'ALL'

    title_order = models.BooleanField(default=True, null=False)
    description_order = models.BooleanField(default=True, null=False)
    complete_order = models.BooleanField(default=True, null=False)
    col_pri = models.CharField(max_length=255, choices=order_by.choices, default=order_by.TITLE)
    complete_filter = models.CharField(max_length=255, choices=complete_filters.choices, default=complete_filters.ALL)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return "{},{},{},{}".format(self.title_order, self.description_order, self.complete_order, self.col_pri)

    def get_title_order(self):
        if self.title_order == True:
            return 'asc'
        elif self.title_order == False:
            return 'dsc'
        else:
            return "Error"

    def get_description_order(self):
        if self.description_order == True:
            return 'asc'
        elif self.description_order == False:
            return 'dsc'
        else:
            return "Error"

    def get_complete_order(self):
        if self.complete_order == True:
            return 'asc'
        elif self.complete_order == False:
            return 'dsc'
        else:
            return "Error"


class Todo(TrackingModel):

    title = models.CharField(max_length=255)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

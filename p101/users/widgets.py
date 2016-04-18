import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from dashing.widgets import KnobWidget
from model_events.messaging import notify


User = get_user_model()


PLAN = getattr(settings, "USERS_QUATER_PLAN", 10000)
OFFSET1 = random.randint(1000, 2000)
OFFSET2 = random.randint(1000, 9000)
OFFSET1 = 0
OFFSET2 = 0

OBJ = locals()


class NewUsersWidget(KnobWidget):
    title = 'Users acquired'
    name = 'users_widget'
    _data = None

    def __init__(self, *args, **kwargs):
        super(NewUsersWidget, self).__init__(*args, **kwargs)
        OBJ[self.name] = self

    def _load_data(self):
        today = timezone.now().replace(hour=0, minute=0, second=0)
        return {
            "today": User.objects.filter(is_active=True, date_joined__gte=today).count() + OFFSET1,
            "total": User.objects.filter(is_active=True).count() + OFFSET2,
            "plan": PLAN
        }

    @property
    def stats(self):
        if not self._data:
            self._data = self._load_data()
        return self._data

    def get_data(self):
        return {
            "angleArc": 250,
            "angleOffset": -125,
            "displayInput": True,
            "displayPrevious": True,
            "step": 1,
            "min": 1,
            "max": self.stats['plan'],
            "readOnly": True
        }

    def get_detail(self):
        return "Today {}".format(self.stats['today'])

    def get_value(self):
        return self.stats['total']

    def get_context(self):
        ctx = super(NewUsersWidget, self).get_context()
        ctx.update({'value': self.get_value()})
        return ctx


@receiver(post_save, sender=User)
def on_new_user(sender, instance, created, **kwagrs):
    widget_name = NewUsersWidget.name
    if created:
        if not widget_name in OBJ:
            pass
        ctx = OBJ[widget_name].get_context()
        notify({"widget": widget_name , "payload": ctx}, message_type="dashboard")

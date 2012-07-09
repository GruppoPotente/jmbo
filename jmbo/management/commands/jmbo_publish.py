import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Q

from jmbo.models import ModelBase


class Command(BaseCommand):
    help = "Publish or unpublish Jmbo objects."

    @transaction.commit_on_success
    def handle(self, *args, **options):
        now = datetime.datetime.now()
        q1 = Q(publish_on__lte=now, retract_on__isnull=True)
        q2 = Q(publish_on__isnull=True, retract_on__gt=now)
        q3 = Q(publish_on__lte=now, retract_on__gt=now)
        ModelBase.objects.filter(state='unpublished').filter(q1|q2|q3).update(state='published')

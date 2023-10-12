

from django.core.management.base import BaseCommand
from ...models import LeagueBattle
from django.utils import timezone

class Command(BaseCommand):
    help = 'Updates the status of LeagueBattles based on time parameters.'

    def handle(self, *args, **kwargs):
        current_time = timezone.now()

        # Update the status of LeagueBattles
        for battle in LeagueBattle.objects.all():
            if current_time < battle.enrollment_start_time:
                battle.status = 'upcoming'
            elif battle.enrollment_start_time <= current_time <= battle.enrollment_end_time:
                battle.status = 'live'
            elif battle.battle_start_time <= current_time <= battle.battle_end_time:
                battle.status = 'live'
            elif current_time > battle.battle_end_time:
                battle.status = 'completed'

            battle.save()

        self.stdout.write(self.style.SUCCESS('Battle statuses updated successfully.'))

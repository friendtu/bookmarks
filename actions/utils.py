from .models import Action
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
import datetime



def create_action(user,verb,target=None):
    now = timezone.now()
    last_minute=now-datetime.timedelta(seconds=60)
    similar_actions=Action.objects.filter(user=user,verb=verb,created__gte=last_minute)

    if target:
        target_ct=ContentType.get_for_model(target)
        similar_actions=similar_actions.filter(target_ct=target_ct,target_id=target.target_id)
    
    if not similar_action:
        action=Action(user=user,verb=verb,target=target)
        action.save()
        return True
    return False

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from remindapp.models import Profile

def createUser(sender, instance, created, **kwargs):
    if created:
        created_profile = instance
        
        if not User.objects.filter(username = instance.profile_id).exists():
            
            created_user = User.objects.create_user(username = instance.profile_id, password = instance.profile_id)
            
            
            created_profile.user = created_user
            created_profile.save()
        
post_save.connect(createUser, sender= Profile)


def createProfile(sender, instance, created, **kwargs):
    if created:
        created_user = instance
        
        if not Profile.objects.filter(profile_id = created_user.username, user = created_user).exists():
            
            if created_user.is_superuser:
                Profile.objects.create(profile_id = created_user.username, user = created_user, is_admin = True)


post_save.connect(createProfile, sender= User)
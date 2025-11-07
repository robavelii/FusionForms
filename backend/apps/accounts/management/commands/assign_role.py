from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.accounts.models import Role

User = get_user_model()

class Command(BaseCommand):
    help = 'Assign a role to a user'

    def add_arguments(self, parser):
        parser.add_argument('--user', type=str, required=True, help='Username or email of the user')
        parser.add_argument('--role', type=str, required=True, help='Role name to assign')

    def handle(self, *args, **options):
        username_or_email = options['user']
        role_name = options['role']
        
        try:
            # Find user by username or email
            try:
                user = User.objects.get(username=username_or_email)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(email=username_or_email)
                except User.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'❌ User not found: {username_or_email}'))
                    return
            
            # Find role
            try:
                role = Role.objects.get(name=role_name)
            except Role.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Role not found: {role_name}'))
                return
            
            # Assign role
            old_role = user.role
            user.role = role.name
            user.save()
            
            self.stdout.write(self.style.SUCCESS(
                f'✅ Successfully assigned role "{role.name}" to user "{user.username}"\n'
                f'   Previous role: {old_role}\n'
                f'   New role: {user.role}'
            ))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error assigning role: {str(e)}'))
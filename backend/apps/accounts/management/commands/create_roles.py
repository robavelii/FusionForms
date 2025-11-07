from django.core.management.base import BaseCommand
from apps.accounts.models import Role

class Command(BaseCommand):
    help = 'Create standard roles for the application'

    def handle(self, *args, **options):
        roles = [
            {
                'name': 'super_admin',
                'description': 'Super Administrator with full system access'
            },
            {
                'name': 'admin', 
                'description': 'Administrator with user and form management access'
            },
            {
                'name': 'designer',
                'description': 'Form Designer with form creation and editing access'
            },
            {
                'name': 'analyst',
                'description': 'Data Analyst with submission viewing and reporting access'
            },
            {
                'name': 'viewer',
                'description': 'Viewer with read-only access to forms and submissions'
            }
        ]
        
        for role_data in roles:
            role, created = Role.objects.get_or_create(
                name=role_data['name'],
                defaults={'description': role_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created role: {role.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Role already exists: {role.name}'))
        
        self.stdout.write(self.style.SUCCESS('✅ Role creation completed!'))
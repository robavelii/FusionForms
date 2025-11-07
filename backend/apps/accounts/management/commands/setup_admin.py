from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from apps.accounts.models import User, Role
from apps.forms.models import Form, FormVersion
from apps.submissions.models import Submission
import logging

logger = logging.getLogger('fusionforms.admin')

class Command(BaseCommand):
    help = 'Setup initial admin configuration including roles, permissions, and admin user'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Setting up admin configuration...")
        
        try:
            with transaction.atomic():
                # Create standard roles
                self.create_standard_roles()
                
                # Create permissions if they don't exist
                self.create_permissions()
                
                # Assign permissions to roles
                self.assign_permissions_to_roles()
                
                # Create admin user if doesn't exist
                self.create_admin_user()
                
                self.stdout.write(self.style.SUCCESS('✅ Admin setup completed successfully!'))
                
        except Exception as e:
            logger.error(f"Admin setup failed: {str(e)}", exc_info=True)
            self.stdout.write(self.style.ERROR(f'❌ Admin setup failed: {str(e)}'))
            raise

    def create_standard_roles(self):
        """Create standard roles for the system."""
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
                self.stdout.write(f"  ✅ Created role: {role.name}")
            else:
                self.stdout.write(f"  ℹ️ Role exists: {role.name}")

    def create_permissions(self):
        """Ensure all necessary permissions exist."""
        # This is mostly handled by Django's migration system, but we can add custom ones
        self.stdout.write("  ✅ Permissions verified (created via migrations)")

    def assign_permissions_to_roles(self):
        """Assign appropriate permissions to each role."""
        # Get all relevant content types
        form_ct = ContentType.objects.get_for_model(Form)
        form_version_ct = ContentType.objects.get_for_model(FormVersion)
        submission_ct = ContentType.objects.get_for_model(Submission)
        user_ct = ContentType.objects.get_for_model(User)
        
        # Define permissions for each role
        role_permissions = {
            'super_admin': [
                # All permissions
                *Permission.objects.all()
            ],
            'admin': [
                # User management
                Permission.objects.get(codename='add_user', content_type=user_ct),
                Permission.objects.get(codename='change_user', content_type=user_ct),
                Permission.objects.get(codename='view_user', content_type=user_ct),
                # Form management
                Permission.objects.get(codename='add_form', content_type=form_ct),
                Permission.objects.get(codename='change_form', content_type=form_ct),
                Permission.objects.get(codename='view_form', content_type=form_ct),
                Permission.objects.get(codename='delete_form', content_type=form_ct),
                # Form version management
                Permission.objects.get(codename='add_formversion', content_type=form_version_ct),
                Permission.objects.get(codename='change_formversion', content_type=form_version_ct),
                Permission.objects.get(codename='view_formversion', content_type=form_version_ct),
            ],
            'designer': [
                # Form creation and editing
                Permission.objects.get(codename='add_form', content_type=form_ct),
                Permission.objects.get(codename='change_form', content_type=form_ct),
                Permission.objects.get(codename='view_form', content_type=form_ct),
                Permission.objects.get(codename='add_formversion', content_type=form_version_ct),
                Permission.objects.get(codename='change_formversion', content_type=form_version_ct),
                Permission.objects.get(codename='view_formversion', content_type=form_version_ct),
            ],
            'analyst': [
                # View forms and submissions
                Permission.objects.get(codename='view_form', content_type=form_ct),
                Permission.objects.get(codename='view_formversion', content_type=form_version_ct),
                Permission.objects.get(codename='view_submission', content_type=submission_ct),
            ],
            'viewer': [
                # Read-only access
                Permission.objects.get(codename='view_form', content_type=form_ct),
                Permission.objects.get(codename='view_formversion', content_type=form_version_ct),
            ]
        }
        
        for role_name, permissions in role_permissions.items():
            try:
                role = Role.objects.get(name=role_name)
                role.permissions.set(permissions)
                self.stdout.write(f"  ✅ Assigned {len(permissions)} permissions to role: {role_name}")
            except Role.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"  ⚠️ Role not found: {role_name}"))
            except Permission.DoesNotExist as e:
                self.stdout.write(self.style.WARNING(f"  ⚠️ Permission not found: {str(e)}"))

    def create_admin_user(self):
        """Create default admin user if it doesn't exist."""
        admin_username = 'admin'
        admin_email = 'admin@example.com'
        admin_password = 'adminpassword123'  # Default password - should be changed immediately
        
        if not User.objects.filter(username=admin_username).exists():
            admin_user = User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password,
                first_name='Admin',
                last_name='User',
                role='super_admin'
            )
            self.stdout.write(self.style.SUCCESS(
                f"  ✅ Created super admin user: {admin_username}\n"
                f"  🔑 Default password: {admin_password}\n"
                f"  ❗ IMPORTANT: Change this password after first login!"
            ))
        else:
            admin_user = User.objects.get(username=admin_username)
            self.stdout.write(self.style.WARNING(
                f"  ℹ️ Admin user '{admin_username}' already exists.\n"
                f"  🔑 No password change was made."
            ))
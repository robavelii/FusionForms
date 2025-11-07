#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging
from dotenv import load_dotenv

# Configure logging for management commands
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    level=logging.INFO,
    stream=sys.stdout
)
logger = logging.getLogger('fusionforms.management')

def setup_environment():
    """Load environment variables and configure settings."""
    # Load .env file if it exists (for local development)
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        logger.info("Loaded environment variables from .env file")
    
    # Set default settings module if not specified
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fusionforms.settings')
    
    # Ensure logs directory exists for file logging
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir, exist_ok=True)
            logger.info(f"Created logs directory at {log_dir}")
        except Exception as e:
            logger.warning(f"Could not create logs directory: {e}")

def is_testing_mode():
    """Check if we're running tests."""
    return 'test' in sys.argv or 'pytest' in sys.argv[0] or 'PYTEST_CURRENT_TEST' in os.environ

def main():
    """Run administrative tasks with enhanced error handling and setup."""
    try:
        # Setup environment before importing Django
        setup_environment()
        
        # Skip database setup for certain commands to avoid connection errors
        # during initial setup
        setup_needed_commands = [
            'runserver', 'migrate', 'makemigrations', 'collectstatic',
            'createsuperuser', 'setup_admin', 'setup_roles', 'create_roles',
            'assign_permissions', 'check_permissions'
        ]
        
        command_requires_setup = any(cmd in sys.argv for cmd in setup_needed_commands)
        
        if command_requires_setup or is_testing_mode():
            from django.core.management import execute_from_command_line
        else:
            # For commands that don't need full setup, use minimal import
            try:
                from django.core.management import execute_from_command_line
            except ImportError as exc:
                raise ImportError(
                    "Couldn't import Django. Are you sure it's installed and "
                    "available on your PYTHONPATH environment variable? Did you "
                    "forget to activate a virtual environment?"
                ) from exc
        
        # Special handling for setup_admin command
        if 'setup_admin' in sys.argv:
            logger.info("Running admin setup - this may take a moment...")
        
        # Special handling for first run
        if 'runserver' in sys.argv and not is_testing_mode():
            from django.conf import settings
            first_run_file = os.path.join(settings.BASE_DIR, '.first_run')
            if not os.path.exists(first_run_file):
                logger.info("=" * 60)
                logger.info("🚀 FIRST RUN DETECTED - Setting up initial configuration")
                logger.info("=" * 60)
                
                # Run migrations silently
                original_argv = sys.argv[:]
                sys.argv = ['manage.py', 'migrate', '--noinput']
                execute_from_command_line(sys.argv)
                sys.argv = original_argv
                
                # Run admin setup
                sys.argv = ['manage.py', 'setup_admin']
                execute_from_command_line(sys.argv)
                sys.argv = original_argv
                
                # Create first run file
                with open(first_run_file, 'w') as f:
                    f.write("Initial setup completed")
                
                logger.info("=" * 60)
                logger.info("✅ INITIAL SETUP COMPLETED SUCCESSFULLY!")
                logger.info("🔑 Default admin user created with username: 'admin'")
                logger.info("🔑 Default password: 'adminpassword123' - CHANGE THIS AFTER FIRST LOGIN!")
                logger.info("🔧 Access Django Admin at: http://localhost:8000/admin/")
                logger.info("📚 API Documentation at: http://localhost:8000/api/schema/swagger-ui/")
                logger.info("=" * 60)
        
        # Execute the command
        execute_from_command_line(sys.argv)
        
        # Special post-command messages
        if 'createsuperuser' in sys.argv and not is_testing_mode():
            logger.info("\n💡 TIP: After creating your superuser, you can assign roles using:")
            logger.info("   python manage.py assign_role --user <username> --role admin")
            
        if 'setup_admin' in sys.argv and not is_testing_mode():
            logger.info("\n✅ Admin setup completed successfully!")
            logger.info("🔑 Default admin credentials:")
            logger.info("   Username: admin")
            logger.info("   Password: adminpassword123")
            logger.info("❗ Please change the default password after first login!")
            logger.info("\n📚 Available management commands for admin tasks:")
            logger.info("   python manage.py create_roles          # Create standard roles")
            logger.info("   python manage.py assign_permissions    # Assign permissions to roles")
            logger.info("   python manage.py list_permissions      # List available permissions")
            logger.info("   python manage.py reset_admin           # Reset admin configuration")
    
    except Exception as e:
        logger.error(f"Management command failed: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
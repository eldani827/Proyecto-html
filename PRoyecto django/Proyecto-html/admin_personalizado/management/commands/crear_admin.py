from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


class Command(BaseCommand):
    help = 'Crea un usuario administrador con grupo "administrador"'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, required=True, help='Nombre de usuario')
        parser.add_argument('--email', type=str, required=True, help='Email del usuario')
        parser.add_argument('--password', type=str, required=True, help='Contraseña')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        # Crear grupo administrador si no existe
        admin_group, created = Group.objects.get_or_create(name='administrador')
        if created:
            self.stdout.write(self.style.SUCCESS('Grupo "administrador" creado'))

        # Crear usuario
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.groups.add(admin_group)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Usuario "{username}" creado exitosamente'))
            self.stdout.write(self.style.SUCCESS(f'Email: {email}'))
            self.stdout.write(self.style.SUCCESS(f'Grupo: administrador'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al crear usuario: {str(e)}'))

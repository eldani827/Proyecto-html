from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


class Command(BaseCommand):
<<<<<<< HEAD
    help = 'Crea un usuario administrador con grupo "administrador"'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, required=True, help='Nombre de usuario')
        parser.add_argument('--email', type=str, required=True, help='Email del usuario')
=======
    help = 'Crea un usuario administrador con el grupo "administrador"'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, required=True, help='Nombre de usuario')
        parser.add_argument('--email', type=str, required=True, help='Correo electrónico')
>>>>>>> Falcaoperez
        parser.add_argument('--password', type=str, required=True, help='Contraseña')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

<<<<<<< HEAD
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
=======
        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'El usuario "{username}" ya existe.'))
            return

        # Crear el usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=False,
            is_superuser=False
        )

        # Asignar al grupo "administrador"
        admin_group, created = Group.objects.get_or_create(name='administrador')
        user.groups.add(admin_group)

        self.stdout.write(
            self.style.SUCCESS(
                f'Usuario administrador "{username}" creado exitosamente y asignado al grupo "administrador".'
            )
        )
>>>>>>> Falcaoperez

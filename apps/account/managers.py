from django.contrib.auth.models import BaseUserManager

class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, first_name, last_name, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have email field")

        if not username:
            raise ValueError("User must have an username field")

        if not phone_number:
            raise ValueError("User must have a Phone Number")

        email = self.normalize_email(email)

        user = self.model(
            email = email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, username, password, phone_number=None, **extra_fields):
        extra_fields.setdefault("role", "admin")
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            **extra_fields
        )

        # user.is_admin=True
        # user.is_staff=True
        # user.is_superuser=True
        # user.save(using=self._db)
        return user
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Q

from .models.user_verification_code import UserVerificationCode

User = get_user_model()

# Evita AlreadyRegistered si alguien ya lo registró
try:
    admin.site.unregister(User)
except NotRegistered:
    pass


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """
    Admin para el CustomUser sin username/first_name/last_name.
    USERNAME_FIELD = 'email'
    """
    # === Listado ===
    list_display = (
        "user_name",
        "email",
        "name",
        "paternal_lastname",
        "maternal_lastname",
        "is_active",
        "is_staff",
        "created_at",
        "updated_at",
    )
    list_display_links = ("user_name", "email")
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "user_name",
        "email",
        "name",
        "paternal_lastname",
        "maternal_lastname",
        "document_number",
    )
    ordering = ("-updated_at", "-created_at")

    # === Formularios ===
    fieldsets = (
        ("Credenciales", {
            "fields": ("email", "password")  # <- quita 'username'
        }),
        ("Información personal", {
            "fields": (
                "user_name",
                "name",
                "paternal_lastname",
                "maternal_lastname",
                "document_number",
            ),
        }),
        ("Permisos", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
        }),
        ("Fechas", {
            "classes": ("collapse",),
            "fields": ("last_login", "created_at", "updated_at"),
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            # BaseUserAdmin respeta esto; como USERNAME_FIELD es 'email',
            # basta con incluir 'email' aquí. Incluimos también 'user_name'
            # para capturarlo al crear el usuario.
            "fields": ("email", "user_name", "password1", "password2"),
        }),
    )

    readonly_fields = ("last_login", "created_at", "updated_at")

    # Opcional: mejora UX en permisos
    filter_horizontal = ("groups", "user_permissions")


# =======================
# UserVerificationCode
# =======================

def _get(obj, *names, default="—"):
    for n in names:
        if hasattr(obj, n):
            return getattr(obj, n)
    return default

@admin.display(description="Tipo verificación")
def col_verification_type(obj):
    return _get(obj, "verification_type", "type")

@admin.display(description="Email destino")
def col_target_email(obj):
    return _get(obj, "target_email", "email")

@admin.display(boolean=True, description="Usado")
def col_is_used(obj):
    return bool(_get(obj, "is_used", "used", default=False))

@admin.display(description="Intentos")
def col_attempts(obj):
    return _get(obj, "attempts", "attempt_count", default=0)

@admin.display(description="Máx. intentos")
def col_max_attempts(obj):
    return _get(obj, "max_attempts", default="—")

@admin.display(description="Creado")
def col_created_at(obj):
    return _get(obj, "created_at", default="—")

@admin.display(description="Expira")
def col_expires_at(obj):
    return _get(obj, "expires_at", default="—")


class UsedListFilter(admin.SimpleListFilter):
    title = "Estado (usado)"
    parameter_name = "used"

    def lookups(self, request, model_admin):
        return (("yes", "Usado"), ("no", "No usado"))

    def queryset(self, request, queryset):
        val = self.value()
        if val == "yes":
            return queryset.filter(Q(is_used=True) | Q(used=True))
        if val == "no":
            return queryset.filter(
                Q(is_used=False) | Q(used=False) | Q(is_used__isnull=True) | Q(used__isnull=True)
            )
        return queryset


class VerificationTypeListFilter(admin.SimpleListFilter):
    title = "Tipo de verificación"
    parameter_name = "vtype"

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        values = set(qs.values_list("verification_type", flat=True)) | set(qs.values_list("type", flat=True))
        values = sorted([v for v in values if v])
        return tuple((v, v) for v in values)

    def queryset(self, request, queryset):
        v = self.value()
        if not v:
            return queryset
        return queryset.filter(Q(verification_type=v) | Q(type=v))


@admin.register(UserVerificationCode)
class UserVerificationCodeAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "code",
        "failed_attempts",
        "locked_until",
        "expires_at",
        "created_at",
        "updated_at",
    )
    list_filter = ("expires_at", "created_at", "updated_at")
    search_fields = (
        "user__user_name",  # si tu User tiene user_name
        "user__email",
        "code",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Información Básica", {"fields": ("user", "code")}),
        ("Estado", {"fields": ("failed_attempts", "locked_until")}),
        ("Vigencia", {"fields": ("expires_at",)}),
        ("Auditoría", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("user")


# Configuración del sitio admin
admin.site.site_header = "Administración de Usuarios"
admin.site.site_title = "Usuarios"
admin.site.index_title = "Panel de Administración"

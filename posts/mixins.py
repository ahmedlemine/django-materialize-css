from django.contrib.auth.mixins import AccessMixin


class UserIsOwnerMixin(AccessMixin):
    """Verify that the user is the owner of related object.
        owner_id_field => leave as is. but after '=' put
        the model field realted to owner. like 'user',
        'creator', 'created_by', 'author'. 
    """
    owner_id_field = 'creator' # 'creator' is from Post model

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or getattr(self.get_object(), self.owner_id_field) != request.user:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

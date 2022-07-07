from rest_framework import permissions

<<<<<<< HEAD
class TMPermissions(permissions.BasePermission):
=======
class ModulePermissions(permissions.BasePermission):
>>>>>>> Development
    '''
    This determines whether a user is authorized to create modules,edit modules,delete modules
    '''

    def has_permission(self, request, view):
        if request.user.user_type == 'TM':
            return True
        elif request.user.user_type == 'STUD':
            return False
        else:
            return False
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.IsAdminUser):
    # def has_permission(self, request, view):
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #     return request.user.is_staff
    
    # def has_permission(self,request, view):
        # admin_permission = super().has_permission(request, view)
        # admin_permission = bool(request.user and request.user.is_staff)
        # return request.method == 'GET' or admin_permission
      
      def has_permission(self, request, view):
            if request.method in permissions.SAFE_METHODS: # Here SAFE_METHODS is a tuple containing the HTTP methods that are considered safe, which are GET, HEAD, and OPTIONS. These methods are considered safe because they do not modify any resources on the server.
                return True
            else:
                return bool(request.user and request.user.is_staff)
              
class IsReviewUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.review_user == request.user or request.user.is_staff
      #obj.review_user we will get from the Review Model.
      #request.user is the user who is making the request. It is an instance of the User model. We can access the user who is making the request by using request.user.
      #request.user.is_staff is a boolean field that indicates whether the user is a staff member or not. It is used to check if the user has admin privileges. If the user is a staff member, they can perform any action on the object, regardless of whether they are the owner of the object or not.
"""
Context processors for accounts and global portal context.
Provides common variables to all templates automatically.
"""

def global_user_context(request):
    """
    Supplies global context data for templates across the entire application:
    - theme_preference: Read from client-side cookie (Unit 6: Cookies)
    - session_visit_count: Read from server-side session (Unit 6: Sessions)
    - current_student: Linked Student instance for the authenticated user, if any
    """
    context = {
        'theme_preference': request.COOKIES.get('theme_preference', 'light'),
        'session_visit_count': request.session.get('visit_count', 1),
        'current_student': None,
    }

    if request.user.is_authenticated:
        # Check if the logged in user is linked to a Student record
        try:
            if hasattr(request.user, 'student_profile'):
                context['current_student'] = request.user.student_profile
        except Exception:
            context['current_student'] = None

    return context


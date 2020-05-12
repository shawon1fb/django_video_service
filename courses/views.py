from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View

from member_ships.models import UserMembership
from .models import Course, Lesson


class CourseListView(ListView):
    model = Course


class CourseDetailView(DetailView):
    model = Course


class LessonDetailView(View):

    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        course_qs = Course.objects.filter(slug=course_slug)
        lesson = None
        course = None
        if course_qs.exists():
            course = course_qs.first()
        lesson_qs = course.lessons.filter(slug=lesson_slug)
        if lesson_qs.exists():
            lesson = lesson_qs.first()
        context = {
            'object': None
        }
        # print(request.user)
        # user_membership = UserMembership.objects.filter(user=request.user).first()
        # user_membership_type = user_membership.membership.membership_type
        # course_allowed_mem_types = course.allowed_membership.all()
        user_membership = get_object_or_404(UserMembership, user=request.user)
        print("user_member ship --------")
        print(user_membership)

        user_membership_type = user_membership.membership.membership_type
        course_allowed_mem_types = course.allowed_membership.all()

        if course_allowed_mem_types.filter(membership_type=user_membership_type).exists():
            context = {'object': lesson}
        return render(request, "courses/lesson_detail.html", context)

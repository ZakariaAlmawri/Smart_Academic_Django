import json

import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


from .models import Hall
from .models import SessionYearModel
from student_management_app.forms import AddStudentForm, EditStudentForm
from student_management_app.models import (
    Attendance,
    AttendanceReport,
    Courses,
    Semesters,
    Levels,
    CustomUser,
    FeedBackStaffs,
    FeedBackStudent,
    LeaveReportStaff,
    LeaveReportStudent,
    NotificationStaffs,
    NotificationStudent,
    SessionYearModel,
    Staffs,
    Students,
    Subjects,
    Hall,
    Schedules_m,
    Booking_hall,
  
    
)

halls = Hall.objects.all()
schedules =  Schedules_m.objects.all()
session_years = SessionYearModel.object.all()
semesters = Semesters.objects.all() 
levels = Levels.objects.all()
booking_halls =  Booking_hall.objects.all()

def admin_home(request):
    student_count1 = Students.objects.all().count()
    staff_count = Staffs.objects.all().count()
    subject_count = Subjects.objects.all().count()
    course_count = Courses.objects.all().count()
    semester_count = Semesters.objects.all().count()
    level_count = Levels.objects.all().count()
    hall_count = Hall.objects.all().count()
    schedule_count = Schedules_m.objects.all().count()
    booking_hall_count = Booking_hall.objects.all().count()

    

    session_list = []
    try:
        sessions = SessionYearModel.object.all()

        for ses in sessions:
            small_ses = (
                ses.id,
                str(ses.session_start_year) + "   TO  " + str(ses.session_end_year),
            )
            session_list.append(small_ses)
    except Exception:
        session_list = []

    course_all = Courses.objects.all()
    course_name_list = []
    subject_count_list = []
    student_count_list_in_course = []
    for course in course_all:
        subjects = Subjects.objects.filter(course_id=course.id).count()
        students = Students.objects.filter(course_id=course.id).count()
        
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)


    subjects_all = Subjects.objects.all()
    subject_list = []
    student_count_list_in_subject = []
    for subject in subjects_all:
        course = Courses.objects.get(id=subject.course_id.id)
        semester = Semesters.objects.get(id=subject.semester_id.id)
        level = Levels.objects.get(id=subject.level_id.id)
        q1 = Q(course_id=course)
        q2 = Q(semester_id=semester)
        q3 = Q(level_id=level)
        student_count=Students.objects.filter(q1 & q2 & q3).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count) 

        

    semester_list =[]
    semester_all = Semesters.objects.all()
    semester_name_list = []
    subject_count_list = []
    student_count_list_in_semester = []
    for semester in semester_all:
        subjects = Subjects.objects.filter(semester_id=semester.id).count()
        students = Students.objects.filter(semester_id=semester.id).count()
        semester_name_list.append(semester.semester_name)
        subject_count_list.append(subjects)
        student_count_list_in_semester.append(students)


    level_list= []
    level_all = Levels.objects.all()
    level_name_list = []
    subject_count_list = []
    student_count_list_in_level = []
    for level in level_all:
        subjects = Subjects.objects.filter(level_id=level.id).count()
        students = Students.objects.filter(level_id=level.id).count()
        level_name_list.append(level.level_name)
        subject_count_list.append(subjects)
        student_count_list_in_level.append(students)


    

    staffs = Staffs.objects.all()
    attendance_present_list_staff = []
    attendance_absent_list_staff = []
    staff_name_list = []
    for staff in staffs:
        subject_ids = Subjects.objects.filter(staff_id=staff.admin.id)
        attendance = Attendance.objects.filter(
            subject_id__in=subject_ids,
        ).count()
        leaves = LeaveReportStaff.objects.filter(
            staff_id=staff.id, leave_status=1
        ).count()
        attendance_present_list_staff.append(attendance)
        attendance_absent_list_staff.append(leaves)
        staff_name_list.append(staff.admin.username)

    students_all = Students.objects.all()
    attendance_present_list_student = []
    attendance_absent_list_student = []
    student_name_list = []
    for student in students_all:
        attendance = AttendanceReport.objects.filter(
            student_id=student.id, status=True
        ).count()
        absent = AttendanceReport.objects.filter(
            student_id=student.id, status=False
        ).count()
        leaves = LeaveReportStudent.objects.filter(
            student_id=student.id, leave_status=1
        ).count()
        attendance_present_list_student.append(attendance)
        attendance_absent_list_student.append(leaves + absent)
        student_name_list.append(student.admin.username)

    hall_all = Hall.objects.all()
    hall_name_list = []
    for hall in hall_all:
        hall_name_list.append(hall.name)

    

     

    
    

    schedule_all = Schedules_m.objects.all()
    schedule_name_list = []
    for schedule in schedule_all:
        course = Courses.objects.get(id=schedule.course_id.id)
        schedule_name_list.append(schedule.days)
        schedule_name_list.append(schedule.timee)
        schedule_name_list.append(schedule.timeeend)
        staff = CustomUser.objects.get(id=schedule.staff_id.id)
        hall = Hall.objects.get(id=schedule.hall_id.id)



    booking_hall_all = Booking_hall.objects.all()
    booking_hall_name_list = []
    for booking_hall in booking_hall_all:
        course = Courses.objects.get(id=booking_hall.course_id.id)
        booking_hall_name_list.append(booking_hall.days)
        booking_hall_name_list.append(booking_hall.timee)
        booking_hall_name_list.append(booking_hall.timeeend)
        staff = CustomUser.objects.get(id=booking_hall.staff_id.id)
        hall = Hall.objects.get(id=booking_hall.hall_id.id)





    return render(
        request,
        "hod_template/home_content.html",
        {
            "student_count": student_count1,
            "staff_count": staff_count,
            "subject_count": subject_count,
            "hall_count": hall_count,
            "hall_name_list": hall_name_list,
            "schedule_count": schedule_count,
            "schedule_name_list": schedule_name_list,
            "booking_hall_name_list":booking_hall_name_list,
            "booking_hal_count":booking_hall_count,
            "course_count": course_count,
            "course_name_list": course_name_list,
            "semester_count":semester_count,
            "semester_name_list":semester_name_list,
            "student_count_list_in_semester": student_count_list_in_semester,
            "level_count": level_count,
            "level_name_list": level_name_list,
            "student_count_list_in_level":student_count_list_in_level,
            "subject_count_list": subject_count_list,
            "session_list": session_list,
            "student_count_list_in_course": student_count_list_in_course,
            "student_count_list_in_subject": student_count_list_in_subject,
            "subject_list": subject_list,
            "staff_name_list": staff_name_list,
            "attendance_present_list_staff": attendance_present_list_staff,
            "attendance_absent_list_staff": attendance_absent_list_staff,
            "student_name_list": student_name_list,
            "attendance_present_list_student": attendance_present_list_student,
            "attendance_absent_list_student": attendance_absent_list_student,
           
        },
    )


def add_new_hall(request):
    return render(request, "hod_template/add_new_hall_template.html")

def add_hall_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        name=request.POST.get("name")
        capacity=request.POST.get("capacity")
        projector_available=request.POST.get("projector_available")
        try:
            hall_m = Hall(name=name, capacity=capacity, projector_available=projector_available)
            hall_m.save()
            messages.success(request, "Successfully Added hall")
            return HttpResponseRedirect(reverse("add_new_hall"))
        except Exception as e:
            print(e)
            messages.error(request, "Failed to Add hall")
            return HttpResponseRedirect(reverse("add_new_hall"))



def add_staff(request):
    return render(request, "hod_template/add_staff_template.html")


    

def add_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        try:
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                last_name=last_name,
                first_name=first_name,
                user_type=2,
            )
            user.staffs.address = address
            user.save()
            messages.success(request, "Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except Exception:
            messages.error(request, "Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))


def make_a_reservation(request):
    halls = Hall.objects.all()
    return render(request, "hod_template/make_a_reservation_template.html",
    {"halls":halls}
    )
        
    
def add_course(srequest):
    return render(request, "hod_template/add_course_template.html"
    )


def add_course_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        course = request.POST.get("course")
        course_name = request.POST.get("course_name")
        try:
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request, "Successfully Added Course")
            return HttpResponseRedirect(reverse("add_course"))
        except Exception as e:
            print(e)
            messages.error(request, "Failed To Add Course")
            return HttpResponseRedirect(reverse("add_course"))

def add_semester(request):
    return render(request, "hod_template/add_semester_template.html"
    )


def add_semester_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        semester = request.POST.get("semester")
        semester_name = request.POST.get("semester_name")
        try:
            semester_model = Semesters(semester_name=semester)
            semester_model.save()
            messages.success(request, "Successfully Added Course")
            return HttpResponseRedirect(reverse("add_semester"))
        except Exception as e:
            print(e)
            messages.error(request, "Failed To Add Course")
            return HttpResponseRedirect(reverse("add_semester"))


def add_level(request):
    return render(request, "hod_template/add_level_template.html"
    )


def add_level_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        level = request.POST.get("level")
        level_name = request.POST.get("level_name")
        try:
            level_model = Levels(level_name=level)
            level_model.save()
            messages.success(request, "Successfully Added level")
            return HttpResponseRedirect(reverse("add_level"))
        except Exception as e:
            print(e)
            messages.error(request, "Failed To Add level")
            return HttpResponseRedirect(reverse("add_level"))


def add_student(request):
    form = AddStudentForm()
    return render(
        request,
        "hod_template/add_student_template.html",
        {"form": form},
    )


def add_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            address = form.cleaned_data["address"]
            session_year_id = form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data["course"]
            semester_id = form.cleaned_data["semester"]
            level_id = form.cleaned_data["level"]
            sex = form.cleaned_data["sex"]

            profile_pic = request.FILES["profile_pic"]
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)

            try:
                user = CustomUser.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    last_name=last_name,
                    first_name=first_name,
                    user_type=3,
                )
                user.students.address = address
                course_obj = Courses.objects.get(id=course_id)
                user.students.course_id = course_obj
                semester_obj = Semesters.objects.get(id=semester_id)
                user.students.semester_id =semester_obj
                level_o = Levels.objects.get(id=level_id)
                user.students.level_id = level_o
                session_year = SessionYearModel.object.get(id=session_year_id)
                user.students.session_year_id = session_year
                user.students.gender = sex
                user.students.profile_pic = profile_pic_url
                user.save()
                messages.success(request, "Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
            except Exception as e:
                print(e)

                messages.error(request, "Failed to Add Student")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form = AddStudentForm(request.POST)
            return render(
                request,
                "hod_template/add_student_template.html",
                {"form": form},
            )


def create_schedules(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    halls = Hall.objects.all()
    subjects = Subjects.objects.all()
    return render(
        request,
        "hod_template/create_schedules_template.html",
        {"staffs": staffs, "courses": courses, "halls": halls, "subjects": subjects },
    )

  



def add_schedule_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        days = request.POST.get("days")
        timee = request.POST.get("timee")
        timeeend = request.POST.get("timeeend")
        course_id = request.POST.get("course")
        course = Courses.objects.get(id=course_id)
        staff_id = request.POST.get("staff")
        staff = CustomUser.objects.get(id=staff_id)
        name = request.POST.get("name")
        hall_id = request.POST.get("hall")
        hall = Hall.objects.get(id=hall_id)
        subject_id = request.POST.get("subject")
        subject = Subjects.objects.get(id=subject_id)
        
        # التحقق من حجز القاعة
        existing_schedule = Schedules_m.objects.filter(hall_id=hall, timee__lte=timeeend, timeeend__gte=timee , days=days).exists()
        if existing_schedule:
            messages.error(request, "The hall is booked at this time.")
            return HttpResponseRedirect(reverse("create_schedules"))
        
        try:
            schedule = Schedules_m(
                days=days, timee=timee, timeeend=timeeend, course_id=course, staff_id=staff, hall_id=hall, subject_id=subject
            )
            schedule.save()
            messages.success(request, "The table has been added successfully.")
            return HttpResponseRedirect(reverse("create_schedules"))
        except Exception as e:
            print(e)
            messages.error(request, "Failed to add Schedules  .")
            return HttpResponseRedirect(reverse("create_schedules"))



def booking_hall(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    halls = Hall.objects.all()
    subjects = Subjects.objects.all()
    return render(
        request,
        "hod_template/boooking_template.html",
        {"staffs": staffs, "courses": courses, "halls": halls, "subjects": subjects },
    )


    
def booking_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        days = request.POST.get("days")
        timee = request.POST.get("timee")
        timeeend = request.POST.get("timeeend")
        course_id = request.POST.get("course")
        course = Courses.objects.get(id=course_id)
        staff_id = request.POST.get("staff")
        staff = CustomUser.objects.get(id=staff_id)
        name = request.POST.get("name")
        hall_id = request.POST.get("hall")
        hall = Hall.objects.get(id=hall_id)
        subject_id = request.POST.get("subject")
        subject = Subjects.objects.get(id=subject_id)
        
        # التحقق من حجز القاعة
        existing_schedule = Booking_hall.objects.filter(hall_id=hall, timee__lte=timeeend, timeeend__gte=timee , days=days).exists()
        if existing_schedule:
            messages.error(request, "The hall is booked at this time.")
            return HttpResponseRedirect(reverse("booking_hall"))
        
        try:
            booking_hall = Booking_hall(
                days=days, timee=timee, timeeend=timeeend, course_id=course, staff_id=staff, hall_id=hall, subject_id=subject
            )
            booking_hall.save()
            messages.success(request, "The table has been added successfully.")
            return HttpResponseRedirect(reverse("booking_hall"))
        except Exception as e:
            print(e)
            messages.error(request, "Failed to add Schedules  .")
            return HttpResponseRedirect(reverse("booking_hall"))




def add_subject(request):
    courses = Courses.objects.all()
    semesters = Semesters.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    levels = Levels.objects.all()
    return render(
        request,
        "hod_template/add_subject_template.html",
        {"staffs": staffs, "courses": courses, "semesters":semesters, "levels": levels},
    )



def add_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name = request.POST.get("subject_name")
        credit = request.POST.get("credit")
        course_id = request.POST.get("course")
        course = Courses.objects.get(id=course_id)
        level_id = request.POST.get("level")
        level = Levels.objects.get(id=level_id)
        semester_id = request.POST.get("semester")
        semester = Semesters.objects.get(id=semester_id)
        staff_id = request.POST.get("staff")
        staff = CustomUser.objects.get(id=staff_id)

        try:
            subject = Subjects(
                subject_name=subject_name,credit=credit, course_id=course, staff_id=staff,level_id=level
            )
            
            subject.save()
            messages.success(request, "Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except Exception as a:
            print(a)
            messages.error(request, "Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))



def manage_staff(request):
    staffs = Staffs.objects.all()
    return render(
        request, "hod_template/manage_staff_template.html", {"staffs": staffs}
    )





def manage_student(request):
    students = Students.objects.all()
    return render(
        request,
        "hod_template/manage_student_template.html",
        {"students": students},
    )


def manage_course(request):
    courses = Courses.objects.all()
    return render(
        request,
        "hod_template/manage_course_template.html",
        {"courses": courses},
    )

def manage_semester(request):
    semesters = Semesters.objects.all()
    return render(
        request,
        "hod_template/manage_semester_template.html",
        {"semesters": semesters},
    )

def manage_level(request):
    levels = Levels.objects.all()
    return render(
        request,
        "hod_template/manage_level_template.html",
        {"levels": levels},
    )

def manage_subject(request):
    subjects = Subjects.objects.all()
    return render(
        request,
        "hod_template/manage_subject_template.html",
        {"subjects": subjects},
    )

def manage_schedule(request):
    schedules = Schedules_m.objects.all()
    return render(
        request,
        "hod_template/manage_schedules_template.html",
        {"schedules": schedules},
    )

def view_booking(request):
    booking_halls = Booking_hall.objects.all()
    return render(
        request,
        "hod_template/view_booking_hall_template.html",
        {"booking_halls": booking_halls},
    )

def edit_hall(request,hall_id):
    hall = Hall.objects.get(id=hall_id)
    return render(
        request,
        "hod_template/edit_hall_template.html",
        {"hall": hall, "id": hall_id},
    )


def edit_hall_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        hall_id = request.POST.get("hall_id")
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        projector_available = request.POST.get("projector_available")
        try:
            hall = Hall.objects.get(id=hall_id)
            hall.name = name
            hall.capacity = capacity
            hall.projector_available = projector_available
            hall.save()

            hall = Hall.objects.get(id=hall_id)
            hall.save()
            messages.success(request, "Successfully Edited Hall")
            return HttpResponseRedirect(
                reverse("edit_hall", kwargs={"hall_id": hall_id})
            )
        except Exception:
            messages.error(request, "Failed to Edit Hall")
            return HttpResponseRedirect(
                reverse("edit_hall", kwargs={"hall_id": hall_id})
            )

def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    return render(
        request,
        "hod_template/edit_staff_template.html",
        {"staff": staff, "id": staff_id},
    )


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        address = request.POST.get("address")

        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()
            messages.success(request, "Successfully Edited Staff")
            return HttpResponseRedirect(
                reverse("edit_staff", kwargs={"staff_id": staff_id})
            )
        except Exception:
            messages.error(request, "Failed to Edit Staff")
            return HttpResponseRedirect(
                reverse("edit_staff", kwargs={"staff_id": staff_id})
            )


def delete_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    try:
        staff.delete()
        messages.success(request, "Staff Deleted Successfully.")
        return redirect('manage_staff')
    except Exception as e:
        print(e)
        messages.error(request, "Failed to Delete Staff.")
        return redirect('manage_staff')



def edit_student(request, student_id):
    request.session["student_id"] = student_id
    student = Students.objects.get(admin=student_id)
    form = EditStudentForm()
    form.fields["email"].initial = student.admin.email
    form.fields["first_name"].initial = student.admin.first_name
    form.fields["last_name"].initial = student.admin.last_name
    form.fields["username"].initial = student.admin.username
    form.fields["address"].initial = student.address
    form.fields["course"].initial = student.course_id.id
    form.fields["semester"].initial = student.semester_id.id
    form.fields["level"].initial = student.level_id.id
    form.fields["sex"].initial = student.gender
    form.fields["session_year_id"].initial = student.session_year_id.id
    return render(
        request,
        "hod_template/edit_student_template.html",
        {"form": form, "id": student_id, "username": student.admin.username},
    )


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id = request.session.get("student_id")
        if student_id is None:
            return HttpResponseRedirect(reverse("manage_student"))

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            session_year_id = form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data["course"]
            semester_id = form.cleaned_data["semester"]
            level_id = form.cleaned_data["level"]
            sex = form.cleaned_data["sex"]

            if request.FILES.get("profile_pic", False):
                profile_pic = request.FILES["profile_pic"]
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                user = CustomUser.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()

                student = Students.objects.get(admin=student_id)
                student.address = address
                session_year = SessionYearModel.object.get(id=session_year_id)
                student.session_year_id = session_year
                student.gender = sex
                course = Courses.objects.get(id=course_id)
                student.course_id = course
                semester = Semesters.objects.get(id=semester_id)
                student.semester_id = semester
                level = Levels.objects.get(id=level_id)
                student.level_id = level
                if profile_pic_url is not None:
                    student.profile_pic = profile_pic_url
                student.save()
                del request.session["student_id"]
                messages.success(request, "Successfully Edited Student")
                return HttpResponseRedirect(
                    reverse("edit_student", kwargs={"student_id": student_id})
                )
            except Exception as a:
                print(a)
                messages.error(request, "Failed to Edit Student")
                return HttpResponseRedirect(
                    reverse("edit_student", kwargs={"student_id": student_id})
                )
        else:
            form = EditStudentForm(request.POST)
            student = Students.objects.get(admin=student_id)
            return render(
                request,
                "hod_template/edit_student_template.html",
                {
                    "form": form,
                    "id": student_id,
                    "username": student.admin.username,
                },
            )



def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    semesters = Semesters.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    levels = Levels.objects.all()
    
    return render(
        request,
        "hod_template/edit_subject_template.html",
        {
            "subject": subject,
            "staffs": staffs,
            "courses": courses,
            "semesters":semesters,
            "levels":levels,
            "id": subject_id,
        },
    )
    




def edit_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id = request.POST.get("subject_id")
        subject_name = request.POST.get("subject_name")
        credit =request.POST.get("credit")
        staff_id = request.POST.get("staff")
        course_id = request.POST.get("course")
        semester_id = request.POST.get("semester")
        level_id = request.POST.get("level")
        

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff
            course = Courses.objects.get(id=course_id)
            subject.course_id = course
            semester = Semesters.objects.get(id=semester_id)
            subject.semester_id = semester
            level = Levels.objects.get(id=level_id)
            subject.level_id = level
            
            subject.save()

            messages.success(request, "Successfully Edited Subject")
            return HttpResponseRedirect(
                reverse("edit_subject", kwargs={"subject_id": subject_id})
            )
        except Exception as e:
            print(e)
            messages.error(request, "Failed to Edit Subject")
            return HttpResponseRedirect(
                reverse("edit_subject", kwargs={"subject_id": subject_id})
            )


def edit_schedules(request, schedule_id):
    schedule = Schedules_m.objects.get(id=schedule_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    halls = Hall.objects.all()
    subjects = Subjects.objects.all()
    return render(
        request,
        "hod_template/edit_schedules_template.html",
        {
            "schedule": schedule,
            "staffs": staffs,
            "courses": courses,
            "halls": halls,
            "subjects": subjects,
            "id": schedule_id,
        },
    )


def edit_schedule_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        schedule_id = request.POST.get("schedule_id")
        days = request.POST.get("days")
        timee = request.POST.get("timee")
        timeeend = request.POST.get("timeeend")
        staff_id = request.POST.get("staff")
        course_id = request.POST.get("course")
        hall_id = request.POST.get("hall")
        subject_id = request.POST.get("subject")


       

        try:
            schedule = Schedules_m.objects.get(id=schedule_id)
            schedule.days = days
            schedule.timee = timee
            schedule.timeeend = timeeend
            staff = CustomUser.objects.get(id=staff_id)
            schedule.staff_id = staff
            course = Courses.objects.get(id=course_id)
            schedule.course_id = course
            hall = Hall.objects.get(id=hall_id)
            schedule.hall_id = hall
            subject = Subjects.objects.get(id=subject_id)
            schedule.subject_id = subject


           
            schedule.save()

            messages.success(request, "Successfully Edited schedule")
            return HttpResponseRedirect(
                reverse("edit_schedules", kwargs={"schedule_id": schedule_id})
            )   
        except Exception as e:  
            print(e)
            messages.error(request, "Failed to Edit schedule")
            return HttpResponseRedirect(
                reverse("edit_schedules", kwargs={"schedule_id": schedule_id})
            )



def edit_booking_hall(request, booking_hall_id):
    booking_hall = Booking_hall.objects.get(id=booking_hall_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    halls = Hall.objects.all()
    subjects = Subjects.objects.all()
    return render(
        request,
        "hod_template/edit_booking_hall_template.html",
        {
            "booking_hall": booking_hall,
            "staffs": staffs,
            "courses": courses,
            "halls": halls,
            "subjects": subjects,
            "id": booking_hall_id,
        },
    )



def edit_booking_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        booking_hall_id = request.POST.get("booking_hall_id")
        days = request.POST.get("days")
        timee = request.POST.get("timee")
        timeeend = request.POST.get("timeeend")
        staff_id = request.POST.get("staff")
        course_id = request.POST.get("course")
        hall_id = request.POST.get("hall")
        subject_id = request.POST.get("subject")

        try:
            booking_hall = Booking_hall.objects.get(id=booking_hall_id)
            booking_hall.days = days
            booking_hall.timee = timee
            booking_hall.timeeend = timeeend
            staff = CustomUser.objects.get(id=staff_id)
            booking_hall.staff_id = staff
            course = Courses.objects.get(id=course_id)
            booking_hall.course_id = course
            hall = Hall.objects.get(id=hall_id)
            booking_hall.hall_id = hall
            subject = Subjects.objects.get(id=subject_id)
            booking_hall.subject_id = subject
            booking_hall.save()

            messages.success(request, "Successfully Edited Booking")
            return HttpResponseRedirect(
                reverse("edit_booking_hall", kwargs={"booking_hall_id": booking_hall_id})
            )   
        except Exception as e:  
            print(e)
            messages.error(request, "Failed to Edit Booking")
            return HttpResponseRedirect(
                reverse("edit_booking_hall", kwargs={"booking_hall_id": booking_hall_id})
            )




def boooking(request, hall_id):
    schedule = Schedules_m.objects.all()
    courses = Courses.objects.all()
    staffs = CustomUser.objects.all()
    halls = Hall.objects.all()
    subjects = Subjects.objects.all()
    schedules = Schedules_m.objects.all()
    return render(
        request,
        "hod_template/boooking_template.html",
        { "staffs": staffs, 
         "courses": courses, 
         "halls": halls,
         "subjects": subjects, 
         "schedules": schedules
         },
    )

def save_booking(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        hall_id = request.POST.get("hall_id")
        schedule_id = request.POST.get("schedule_id")
        days = request.POST.get("days")
        timee = request.POST.get("timee")
        timeeend = request.POST.get("timeeend")
        staff_id = request.POST.get("staff")
        course_id = request.POST.get("course")
        hall_id = request.POST.get("hall")
        subject_id = request.POST.get("subject")

        try:
            schedule = Schedules_m.objects.get(id=schedule_id)
            hall = Hall.objects.get(id=hall_id)
            schedule.days = days
            schedule.timee = timee
            schedule.timeeend = timeeend
            staff = CustomUser.objects.get(id=staff_id)
            schedule.staff_id = staff
            course = Courses.objects.get(id=course_id)
            schedule.course_id = course
            subject = Subjects.objects.get(id=subject_id)
            schedule.subject_id = subject
            schedule.save()

            messages.success(request, "Successfully Edited schedule")
            return HttpResponseRedirect(
                reverse("boooking", kwargs={"hall_id": hall_id})
            )   
        except Exception as e:  
            print(e)
            messages.error(request, "Failed to Edit schedule")
            return HttpResponseRedirect(
                reverse("boooking", kwargs={"hall_id": hall_id})
            )

def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    return render(
        request,
        "hod_template/edit_course_template.html",
        {"course": course, "id": course_id},
    )


def edit_course_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course")
        

        try:
            course = Courses.objects.get(id=course_id)
            print(Courses.course_name)
            course.course_name = course_name
            course.save()
            messages.success(request, "Successfully Edited Course")
            return HttpResponseRedirect(
                reverse("edit_course", kwargs={"course_id": course_id})
            )
        except Exception as e:
            print(e)
            messages.error(request, "Failed to Edit Course")
            return HttpResponseRedirect(
                reverse("edit_course", kwargs={"course_id": course_id})
            )


def edit_semester(request, semester_id):
    semester = Semesters.objects.get(id=semester_id)
    return render(
        request,
        "hod_template/edit_semester_template.html",
        {"semester": semester, "id": semester_id},
    )


def edit_semester_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        semester_id = request.POST.get("semester_id")
        semester_name = request.POST.get("semester")
        

        try:
            semester = Semesters.objects.get(id=semester_id)
            print(Semesters.semester_name)
            semester.semester_name = semester_name
            semester.save()
            messages.success(request, "Successfully Edited semester")
            return HttpResponseRedirect(
                reverse("edit_semester", kwargs={"semester_id": semester_id})
            )
        except Exception as e:
            print(e)
            messages.error(request, "Failed to Edit semester")
            return HttpResponseRedirect(
                reverse("edit_semester", kwargs={"semester_id": semester_id})
            )

    
def edit_level(request, level_id):
    level = Levels.objects.get(id=level_id)
    return render(
        request,
        "hod_template/edit_level_template.html",
        {"level": level, "id": level_id},
    )


def edit_level_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        level_id = request.POST.get("level_id")
        level_name = request.POST.get("level")
        

        try:
            level = Levels.objects.get(id=level_id)
            print(Levels.level_name)
            level.level_name = level_name
            level.save()
            messages.success(request, "Successfully Edited Level")
            return HttpResponseRedirect(
                reverse("edit_level", kwargs={"level_id": level_id})
            )
        except Exception as e:
            print(e)
            messages.error(request, "Failed to Edit Level")
            return HttpResponseRedirect(
                reverse("edit_level", kwargs={"level_id": level_id})
            )

def add_session(request):
    return render(request, "hod_template/add_session_template.html")

def add_session_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        session_start_year = request.POST.get("session_start")
        session_end_year = request.POST.get("session_end")

        try:
            sessionyear = SessionYearModel(
                session_start_year=session_start_year,
                session_end_year=session_end_year,
            )
            sessionyear.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect(reverse("add_session"))
        except Exception:
            messages.error(request, "Failed to Add Session")
            return HttpResponseRedirect(reverse("add_session"))


def manage_session(request):
    session_year = SessionYearModel.object.all()
    return render(
        request,
        "hod_template/manage_session_template.html",
        {"session_years":session_years}

    )

def edit_session(request, session_id):
    session_year = SessionYearModel.object.get(id=session_id)
   
    return render(request, "hod_template/edit_session_template.html",
    {"session_year":session_year,"id":session_id})


def edit_session_save(request):
    if request.method != "POST":
           return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        session_id = request.POST.get('session_id')
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            session_year = SessionYearModel.object.get(id=session_id)
            session_year.session_start_year = session_start_year
            session_year.session_end_year = session_end_year
            session_year.save()

            messages.success(request, "Session Year Updated Successfully.")
            return redirect('/edit_session/'+session_id)
        except:
            messages.error(request, "Failed to Update Session Year.")
            return redirect('/edit_session/'+session_id)

def delete_session(request, session_id):
    session = SessionYearModel.object.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Session Deleted Successfully.")
        return redirect('manage_session')
    except:
        messages.error(request, "Failed to Delete Session.")
        return redirect('manage_session')


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def staff_feedback_message(request):
    feedbacks = FeedBackStaffs.objects.all()
    return render(
        request,
        "hod_template/staff_feedback_template.html",
        {"feedbacks": feedbacks},
    )


def student_feedback_message(request):
    feedbacks = FeedBackStudent.objects.all()
    return render(
        request,
        "hod_template/student_feedback_template.html",
        {"feedbacks": feedbacks},
    )


@csrf_exempt
def student_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")

    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except Exception:
        return HttpResponse("False")


@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")

    try:
        feedback = FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except Exception:
        return HttpResponse("False")


def staff_leave_view(request):
    leaves = LeaveReportStaff.objects.all()
    return render(
        request,
        "hod_template/staff_leave_view.html",
        {"leaves": leaves},
    )


def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    return render(
        request,
        "hod_template/student_leave_view.html",
        {"leaves": leaves},
    )


def student_approve_leave(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def student_disapprove_leave(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def staff_approve_leave(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))


def staff_disapprove_leave(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))


def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    courses = Courses.objects.all()
    semesters = Semesters.objects.all()
    levels = Levels.objects.all()
    session_year_id = SessionYearModel.object.all()
    return render(
        request,
        "hod_template/admin_view_attendance.html",
        {"subjects": subjects, "courses": courses, "semesters":semesters, "levels":levels, "session_year_id": session_year_id},
    )


@csrf_exempt
def admin_get_attendance_dates(request):
    subject = request.POST.get("subject")
    course = request.POST.get("course_id")
    semester = request.POST.get("semester_id")
    level = request.POST.get("level_id")
    session_year_id = request.POST.get("session_year_id")
    subject_obj = Subjects.objects.get(id=subject)
    session_year_obj = SessionYearModel.object.get(id=session_year_id)
    attendance = Attendance.objects.filter(
        subject_id=subject_obj, course_id=course, semester_id=semester, level_id=level,  session_year_id=session_year_obj
    )
    attendance_obj = []
    for attendance_single in attendance:
        data = {
            "id": attendance_single.id,
            "attendance_date": str(attendance_single.attendance_date),
            "course_id": attendance_single.course_id.id,
            "semester_id": attendance_single.semester_id.id,
            "level_id": attendance_single.level_id.id,
            "session_year_id": attendance_single.session_year_id.id,
        }
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj), safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    list_data = []

    for student in attendance_data:
        data_small = {
            "id": student.student_id.admin.id,
            "name": student.student_id.admin.first_name
            + " "
            + student.student_id.admin.last_name,
            "status": student.status,
        }
        list_data.append(data_small)
    return JsonResponse(
        json.dumps(list_data), content_type="application/json", safe=False
    )


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(
        request,
        "hod_template/admin_profile.html",
        {"user": user},
    )


def admin_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        # password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            # if password!=None and password!="":
            #     customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except Exception:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))


def admin_send_notification_student(request):
    students = Students.objects.all()
    return render(
        request,
        "hod_template/student_notification.html",
        {"students": students},
    )


def admin_send_notification_staff(request):
    staffs = Staffs.objects.all()
    return render(
        request,
        "hod_template/staff_notification.html",
        {"staffs": staffs},
    )


@csrf_exempt
def send_student_notification(request):
    id = request.POST.get("id")
    message = request.POST.get("message")
    student = Students.objects.get(admin=id)
    token = student.fcm_token
    url = "https://fcm.googleapis.com/fcm/send"
    body = {
        "notification": {
            "title": "Student Management System",
            "body": message,
            "click_action": "https://studentmanagementsystem22.herokuapp.com/student_all_notification",
            "icon": "http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg",
        },
        "to": token,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "key=SERVER_KEY_HERE",
    }
    data = requests.post(url, data=json.dumps(body), headers=headers)
    notification = NotificationStudent(student_id=student, message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")


@csrf_exempt
def send_staff_notification(request):
    id = request.POST.get("id")
    message = request.POST.get("message")
    staff = Staffs.objects.get(admin=id)
    token = staff.fcm_token
    url = "https://fcm.googleapis.com/fcm/send"
    body = {
        "notification": {
            "title": "Student Management System",
            "body": message,
            "click_action": "https://studentmanagementsystem22.herokuapp.com/staff_all_notification",
            "icon": "http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg",
        },
        "to": token,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "key=SERVER_KEY_HERE",
    }
    data = requests.post(url, data=json.dumps(body), headers=headers)
    notification = NotificationStaffs(staff_id=staff, message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")




   







          

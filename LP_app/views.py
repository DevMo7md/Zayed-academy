from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.http import JsonResponse
from .models import MonthlySubscription
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from .decorators import subscription_required
# Create your views here.
def landing(request):
    return render(request, 'LP_app/landing.html')

def home(request):

    try:
        videos = Lesson.objects.all()
        categories = Category.objects.all()
        # dashboard

        context = {
            'videos': videos,
            'categories': categories,
        }
        return render(request, 'LP_app/home.html', context)
    except:
        messages.error(request, "الفيديو المطلوب غير موجود!")
        return redirect('home')  # Redirect to main page if video doesn't exist

def lesson (request, foo):
    
    foo = foo.replace('-', ' ')
    try:
        if request.user.is_superuser or request.user.is_staff:
            category = Category.objects.get(name=foo)
            lessons = Lesson.objects.filter(category=category)
            categories = Category.objects.all()
            if 'search-bar' in request.GET:
                searched = request.GET['search-bar']
                if searched:
                    # Filter products based on the search query
                    lessons = lessons.filter(Q(title__icontains=searched) | Q(discrebtion__icontains=searched) | Q(grade__grade__icontains=searched))
                    if not lessons:
                        err = f'No results for {searched} \n Try checking your spelling or use more general terms'
        
            context = {
                'lessons': lessons,
                'categories': categories,
                'category': category,
            }
        else: 
            student = Student.objects.get(user=request.user)
            grade = student.alsaf
            category = Category.objects.get(name=foo)
            lessons = Lesson.objects.filter(Q(category=category) & Q(grade=grade))
            categories = Category.objects.all()
            if 'search-bar' in request.GET:
                searched = request.GET['search-bar']
                if searched:
                    # Filter products based on the search query
                    lessons = lessons.filter(Q(title__icontains=searched) | Q(discrebtion__icontains=searched))
                    if not lessons:
                        err = f'No results for {searched} \n Try checking your spelling or use more general terms'        
            context = {
                'lessons': lessons,
                'categories': categories,
                'category': category,
                
            }

        return render(request, 'LP_app/lessons.html', context)
    except Student.DoesNotExist:
        messages.error(request, "الطالب غير موجود.")
        return redirect('home')
    except Category.DoesNotExist:
        messages.error(request, "التصنيف المطلوب غير موجود.")
        return redirect('home')
    except Lesson.DoesNotExist:
        messages.error(request, "الدروس غير موجودة.")
        return redirect('home')
    except Exception as e:
        messages.error(request, f"حدث خطأ غير متوقع: {str(e)}")
        return redirect('home')


@subscription_required
def video(request, pk):

    lesson = Lesson.objects.get(id=pk)
    cat = lesson.category.id
    categories = Category.objects.all()
    grade = lesson.grade.id
    lessons = Lesson.objects.filter(Q(category=cat)&Q(grade=grade)).exclude(id=lesson.id)[:8]

    video = get_object_or_404(Lesson, id=pk)
    video.views += 1  # زيادة عدد المشاهدات
    video.save()

    
    
    context = {
        'lesson':lesson,
        'categories': categories,
        'video':video,
        'lessons':lessons
    }
    return render(request, 'LP_app/video.html', context)




    
def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "تم تسجيل الدخول بنجاح")
            return redirect('home')
        else:
            messages.warning(request, "عذراً اسم المستخدم او كلمة المرور غير صحيحه الرجاء المحاوله مره اخرى")
            return redirect('login')
        
    return render(request, 'LP_app/login.html', {})


def register(request):
    grade = Grade.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        second_name = request.POST['second_name']
        third_name = request.POST['third_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_num = request.POST['phone_num']
        dad_num = request.POST['dad_num']
        mom_num = request.POST['mom_num']
        school = request.POST['school']
        dad_job = request.POST['dad_job']
        government = request.POST['government']
        alsaf = request.POST['alsaf']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'عذراً كلمة المرور لا تتوافق مع بعضها')
            
            else:
                user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
                user.save()
                if alsaf:
                    try:
                        grade_instance = Grade.objects.get(id=alsaf)
                    except Grade.DoesNotExist:
                        grade_instance = None
                else:
                    grade_instance = None

                student = Student.objects.create(
                        user=user,
                        first_name=first_name,
                        second_name=second_name,
                        third_name=third_name,
                        last_name=last_name,
                        phone_num=phone_num,
                        dad_num=dad_num,
                        mom_num=mom_num,
                        school=school,
                        dad_job=dad_job,
                        government=government,
                        alsaf=grade_instance,)
                student.save()
                login(request, user)
                messages.success(request, 'لقد تم انشاء حسابك بنجاح ')
                return redirect('home')
        else:
            messages.error(request, 'عذراً كلمة المرور غير متوافقة')
    return render(request, 'LP_app/register.html', {'grade':grade})

def logout_user (request):
    logout(request)
    messages.success(request, 'تم تسجيل الخروج بنجاح')
    return redirect('/')  # Redirect to main page after logout

def dashboard(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        lesson_file = request.FILES.get('lesson')
        category_id = request.POST.get('category')
        grade_id = request.POST.get('grade')
        thumnale_image = request.FILES.get('thumnale_image')
        discrebtion = request.POST.get('discrebtion')
        pdf = request.FILES.get('bdf')

        if not title or not lesson_file or not category_id or not thumnale_image or not discrebtion or not grade_id:
            messages.error(request, "يرجى ملء جميع الحقول.")
            return redirect('dashboard')

        try:
            category = Category.objects.get(id=category_id)
            grade = Grade.objects.get(id=grade_id)
        except Category.DoesNotExist:
            messages.error(request, "التصنيف المحدد غير موجود.")
            return redirect('dashboard')

        Lesson.objects.create(
            title=title,
            lesson=lesson_file,
            category=category,
            grade=grade,
            thumnale_image=thumnale_image,
            discrebtion=discrebtion,
            bdf=pdf,
        )

        messages.success(request, 'تم حفظ الدرس بنجاح')
        return redirect('dashboard')

    # الحصول على فيديوهات المدرس المحدد
    lessons = Lesson.objects.all()
    lesson_titles = [lesson.title for lesson in lessons]
    lesson_views = sum([lesson.views for lesson in lessons])  # افترض أن لديك حقل views في نموذج Lesson
    lesson_num = len(lessons)
    categories = Category.objects.all()
    grades = Grade.objects.all()

    context = {
        'lesson_titles': lesson_titles,
        'lesson_views': lesson_views,
        'lesson_num': lesson_num,
        'categories': categories,
        'lessonss':lessons,
        'grades':grades,
    }
    return render(request, 'LP_app/dashboard.html', context)

def stat_dashboard(request):


    # الاحصائيات
    return render(request, 'LP_app/statstic.html')

def get_subscription_stats(request):
    stats = MonthlySubscription.objects.all().values('month', 'new_subscribers', 'teacher__user__username')
    data = {
        'labels': [f"{item['month']} - {item['teacher__user__username']}" for item in stats],
        'datasets': [{
            'label': 'الجدد في المنصة',
            'data': [item['new_subscribers'] for item in stats],
            'backgroundColor': "#eeb5ff",
            'borderColor': "#c507ff",
            'borderWidth': 0.5,
        }]
    }
    return JsonResponse(data)


def edit_lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        lesson_file = request.FILES.get('lesson')
        category_id = request.POST.get('category')
        grade_id = request.POST.get('grade')
        thumnale_image = request.FILES.get('thumnale_image')
        discrebtion = request.POST.get('discrebtion')
        pdf = request.FILES.get('bdf')

        # التحقق من أن جميع الحقول قد تم ملؤها
        if not title or not discrebtion or not category_id:
            messages.error(request, "يرجى ملء جميع الحقول.")
            return redirect('edit_lesson', pk=pk)
        try:
            category = Category.objects.get(id=category_id)
            grade = Grade.objects.get(id=grade_id)
        except Category.DoesNotExist:
            messages.error(request, "التصنيف المحدد غير موجود.")
            return redirect('dashboard')
        

        # تحديث الدرس
        lesson.title = title
        lesson.lesson = lesson_file if lesson_file else lesson.lesson
        lesson.category = category
        lesson.thumnale_image = thumnale_image if thumnale_image else lesson.thumnale_image
        lesson.discrebtion = discrebtion
        lesson.grade = grade
        lesson.bdf = pdf
        lesson.save()

        messages.success(request, 'تم تعديل الفيديو بنجاح')
        return redirect('dashboard')

    # إذا كان الطلب GET، املأ النموذج بالبيانات الحالية
    categories = Category.objects.all()
    grades = Grade.objects.all()

    context = {
        'lesson': lesson,
        'categories': categories,
        'grades':grades,
    }
    return render(request, 'LP_app/edit_lesson.html', context)

def delete_lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    
    if request.method == 'POST':
        lesson.delete()
        messages.success(request, 'تم حذف الفيديو بنجاح')
        return redirect('dashboard')

    return render(request, 'LP_app/delete_lesson.html', {'lesson' : lesson})


def teacher_video(request):
    categories = Category.objects.all()
    lessons = Lesson.objects.all()
    grades = Grade.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        lesson_file = request.FILES.get('lesson')
        category_id = request.POST.get('category')
        grade_id = request.POST.get('grade')
        thumnale_image = request.FILES.get('thumnale_image')
        discrebtion = request.POST.get('discrebtion')
        pdf = request.FILES.get('pdf')

        if not title or not lesson_file or not category_id or not thumnale_image or not discrebtion:
            messages.error(request, "يرجى ملء جميع الحقول.")
            return redirect('dashboard')

        try:
            category = Category.objects.get(id=category_id)
            grade = Grade.objects.get(id=grade_id)
        except Category.DoesNotExist:
            messages.error(request, "التصنيف المحدد غير موجود.")
            return redirect('dashboard')
        Lesson.objects.create(
            title=title,
            lesson=lesson_file,
            category=category,
            grade=grade,
            thumnale_image=thumnale_image,
            discrebtion=discrebtion,
            bdf=pdf,
        )
        messages.success(request, 'تم حفظ الدرس بنجاح')
        return redirect('teacher_video',)
        
    context = {
        'lessons':lessons,
        'categories':categories,
        'grades':grades,
    }
    
    return render(request, 'LP_app/teachers_videos.html', context)

def teacher_pdfs(request):
    grade = Grade.objects.all()
    pdfs = Pdfs.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        grade_id = request.POST.get('grade')
        thumnale_image = request.FILES.get('thumnale_image')
        pdf = request.FILES.get('pdf')

        if not title or not  thumnale_image or not pdf or not grade_id:
            messages.error(request, "يرجى ملء جميع الحقول.")
            return redirect('dashboard')

        try:
            grade = Grade.objects.get(id=grade_id)
        except Category.DoesNotExist:
            messages.error(request, "التصنيف المحدد غير موجود.")
            return redirect('dashboard')
        Pdfs.objects.create(
            name=title,
            grade=grade,
            image=thumnale_image,
            pdf=pdf,
        )
        messages.success(request, 'تم حفظ PDF بنجاح')
        return redirect('teacher_pdf')
        
    context = {
        'grades':grade,
        'pdfs':pdfs,
    }
    
    return render(request, 'LP_app/teacher_pdf.html', context)

def edit_pdf(request, pk):
    pdf = get_object_or_404(Pdfs, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        grade_id = request.POST.get('grade')
        thumnale_image = request.FILES.get('thumnale_image')
        new_pdf = request.FILES.get('bdf')

        # التحقق من أن جميع الحقول قد تم ملؤها
        if not title or not grade_id:
            messages.error(request, "يرجى ملء جميع الحقول.")
            return redirect('edit_pdf', pk=pk)
        try:
            grade = Grade.objects.get(id=grade_id)
        except Grade.DoesNotExist:
            messages.error(request, "التصنيف المحدد غير موجود.")
            return redirect('dashboard')
        

        # تحديث الدرس
        pdf.name = title
        pdf.image = thumnale_image if thumnale_image else pdf.image
        pdf.grade = grade 
        pdf.pdf = new_pdf if new_pdf else pdf.pdf
        pdf.save()

        messages.success(request, 'تم تعديل pdf بنجاح')
        return redirect('dashboard')

    # إذا كان الطلب GET، املأ النموذج بالبيانات الحالية
    grades = Grade.objects.all()

    context = {
        'pdf': pdf,
        'grades':grades,
    }
    return render(request, 'LP_app/edit_pdf.html', context)

def delete_pdf(request, pk):
    pdf = get_object_or_404(Pdfs, pk=pk)
    
    if request.method == 'POST':
        pdf.delete()
        messages.success(request, 'تم حذف PDF بنجاح')
        return redirect('dashboard')

    return render(request, 'LP_app/delete_pdf.html', {'pdf' : pdf})



def profile(request, pk):
    # تأكد من أن المستخدم يشاهد ملفه الشخصي فقط
    if request.user.id != pk:
        return redirect('home')  # إعادة التوجيه إلى الصفحة الرئيسية إذا حاول المستخدم الوصول إلى ملف شخصي آخر

    student = get_object_or_404(Student, user__id=pk)
    enrolled_courses = student.enrolled_courses.all()
    categories = Category.objects.all()
    context = {
        'student': student,
        'enrolled_courses':enrolled_courses,
        'categories':categories,
    }
    return render(request, 'LP_app/profile.html', context)

def edit_profile(request):
    if request.method == 'POST':
        # معالجة البيانات المقدمة وتحديث معلومات المستخدم
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        second_name = request.POST.get('second_name')
        third_name = request.POST.get('third_name')
        last_name = request.POST.get('last_name')
        phone_num = request.POST.get('phone_num')
        dad_num = request.POST.get('dad_num')
        mom_num = request.POST.get('mom_num')
        school = request.POST.get('school')
        dad_job = request.POST.get('dad_job')
        government = request.POST.get('government')
        alsaf_id = request.POST.get('alsaf')

        # الحصول على المستخدم الحالي
        student = Student.objects.get(user=request.user)

        # تحديث معلومات المستخدم
        user = request.user
        user.username = username
        user.email = email
        user.save()

        try:
            alsaf = Grade.objects.get(id=alsaf_id)
        except Grade.DoesNotExist:
            alsaf = None  # أو التعامل مع الحالة حسب الحاجة

        student.first_name = first_name
        student.second_name = second_name
        student.third_name = third_name
        student.last_name = last_name
        student.phone_num = phone_num
        student.dad_num = dad_num
        student.mom_num = mom_num
        student.school = school
        student.dad_job = dad_job
        student.government = government
        student.alsaf = alsaf
        student.save()

        messages.success(request, 'تم تحديث البيانات بنجاح!')
        return redirect('profile', pk=request.user.id)

    # إذا كان الطلب GET، قم بتحميل البيانات الحالية لعرضها في النموذج
    student = Student.objects.get(user=request.user)
    grade = Grade.objects.all()
    enrolled_courses = student.enrolled_courses.all()
    context = {
        'student': student,
        'grade': grade,
        'enrolled_courses':enrolled_courses,
    }

    return render(request, 'LP_app/edit_user.html', context)

def edit_ps(request):

    if request.method == 'POST':
        old_passw = request.POST.get('old-password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if request.user.check_password(old_passw):
            if password1 == password2 :
                request.user.set_password(password1)
                request.user.save()

                # تحديث الجلسة لضمان بقاء المستخدم مسجلاً بعد تغيير كلمة المرور
                update_session_auth_hash(request, request.user)
                messages.success(request, "تم تغيير كلمة المرور بنجاح!")
                return redirect('profile', pk=request.user.id)
            else:
                messages.error(request, "عذراً. يرجى التأكد من ان حقلا كلمة المرور الجديده متماثلان")
        else:
            messages.error(request, "عذراً. كلمة المرور القديمة غير صحيحة")            

    return render(request, 'LP_app/edit_ps.html')

@subscription_required
def pdfs(request):
    err = None
    if request.user.is_staff:
        pdfs = Pdfs.objects.all()
        if 'search-bar' in request.GET:
            searched = request.GET['search-bar']
            if searched:
                # Filter products based on the search query
                pdfs = pdfs.filter(Q(name__icontains=searched) | Q(grade__grade__icontains=searched))
                if not pdfs:
                    err = f'للأسف لا يوجد ملف بإسم {searched} يرجى المحاوله بكلمة بحث اقرب'        
    else:
        student = get_object_or_404(Student, user__id=request.user.id)
        student_grade = student.alsaf
        pdfs = Pdfs.objects.filter(grade=student_grade)
        if 'search-bar' in request.GET:
            searched = request.GET['search-bar']
            if searched:
                # Filter products based on the search query
                pdfs = pdfs.filter(Q(name__icontains=searched))
                if not pdfs:
                    err = f'للأسف لا يوجد ملف بإسم {searched} يرجى المحاوله بكلمة بحث اقرب' 

    context =  {
            'pdfs': pdfs,
            'err':err
            }
    return render(request, 'LP_app/books.html',context)
    
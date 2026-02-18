from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout as django_logout
from django.urls import reverse


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm

@login_required
def profile_edit(request):
    user = _get_user_from_session(request)
    if not user:
        return redirect('userlogin')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)

    return render(request, "profile_edit.html", {
        'form': form,
        'user_obj': user
    })



# Helper utilities
def _get_user_from_session(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    return Usersign_up.objects.filter(id=user_id).first()


def _get_vendor_from_session(request):
    vendor_id = request.session.get('vuser.id')
    if not vendor_id:
        return None
    return Vendorregister.objects.filter(id=vendor_id).first()


# Public pages
def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def vendor(request):
    return render(request, "vendor.html")


def user(request):
    return render(request, "user.html")


# User signup/login/logout
def signup(request):
    # If user is already logged in, go to userhome
    if request.session.get('user_id'):
        return redirect('userhome')

    if request.method == 'POST':
        form = User_signupform(request.POST)
        if form.is_valid():
            usr = form.save(commit=False)
            raw_password = form.cleaned_data.get('password')
            usr.password = make_password(raw_password)
            usr.save()
            return redirect('userlogin')
    else:
        form = User_signupform()

    return render(request, "signup.html", {'form': form})


def userlogin(request):
    # If already logged in, redirect
    if request.session.get('user_id'):
        return redirect('userhome')

    if request.method == 'POST':
        form = Userlogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = Usersign_up.objects.filter(username=username).first()
            if user and check_password(password, user.password):
                request.session['user_id'] = user.id
                # Optional: set a nicer session expiry or other session flags
                return redirect('userhome')
            # optionally: send back an error message in context (not included here)
    else:
        form = Userlogin()

    return render(request, "userlogin.html", {'form': form})


def userlogout(request):
    """
    Properly clear session keys we use for auth and call Django logout (if used).
    Template used earlier references 'userlogout' URL name — keep this name.
    """
    # Remove our custom session keys safely
    request.session.pop('user_id', None)
    request.session.pop('vuser.id', None)
    # Also flush session if you want to remove everything
    # request.session.flush()

    # If you ever used Django's auth login, this will log out that user too
    django_logout(request)
    return redirect('home')


# User home: show only approved packages
def userhome(request):
    pk = Packagecreate.objects.filter(aprovel=True)
    return render(request, "userhome.html", {'package': pk})


# Vendor flows
from .models import Vendorregister, Packagecreate

def _get_vendor_from_session(request):
    # support both old key 'vuser.id' and new recommended 'vuser_id'
    vendor_id = request.session.get('vuser_id') or request.session.get('vuser.id')
    if not vendor_id:
        return None
    return Vendorregister.objects.filter(id=vendor_id).first()

def vendorhome(request):
    ven = _get_vendor_from_session(request)
    if not ven:
        return redirect('vendorlogin')

    # fetch only packages belonging to this vendor
    pk = Packagecreate.objects.filter(vendor=ven)
    return render(request, "vendorhome.html", {'package': pk, 'vendor': ven})


def vendorsignup(request):
    if request.session.get('vuser.id'):
        return redirect('vendorhome')  # Already logged in

    if request.method == 'POST':
        fm = Vendorregistorform(request.POST)
        if fm.is_valid():
            data = fm.save(commit=False)
            raw_password = fm.cleaned_data.get('password')
            data.password = make_password(raw_password)
            data.save()
            return redirect('vendorlogin')
    else:
        fm = Vendorregistorform()

    return render(request, "vendorsignup.html", {'form': fm})


def vendorlogin(request):
    if request.method == 'POST':
        form = Vendorlogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            vuser = Vendorregister.objects.filter(email=email).first()

            if vuser and check_password(password, vuser.password):
                # store vendor id in session with recommended key
                request.session['vuser_id'] = vuser.id
                # optional: set session expiry (in seconds) e.g. 3600 for 1 hour
                # request.session.set_expiry(3600)
                return redirect('vendorhome')
            # else: maybe add error handling (invalid login)
    else:
        form = Vendorlogin()

    return render(request, "vendorlogin.html", {'form': form})


def vendorlogout(request):
    # Clear vendor session key and logout
    request.session.pop('vuser.id', None)
    django_logout(request)
    return redirect('vendorlogin')


def vcreate(request):
    """
    Vendor creating a package. We require vendor to be logged in and attach the vendor relation.
    """
    ven = _get_vendor_from_session(request)
    if not ven:
        return redirect('vendorlogin')

    if request.method == 'POST':
        form = vpackageform(request.POST, request.FILES)
        if form.is_valid():
            p = form.save(commit=False)
            p.vendor = ven
            p.save()
            return redirect('vendorhome')
    else:
        form = vpackageform()

    return render(request, "vcreate.html", {'form': form})


def vendordelete(request, pk):
    item = get_object_or_404(Packagecreate, pk=pk)
    # Ensure the logged-in vendor owns this package before deleting
    ven = _get_vendor_from_session(request)
    if not ven:
        return redirect('vendorlogin')

    if item.vendor_id != ven.id:
        # unauthorized — redirect or show message
        return redirect('vendorhome')

    if request.method == 'POST':
        item.delete()
        return redirect('vendorhome')

    # If GET, optionally render a confirm page; for now we redirect
    return redirect('vendorhome')


def vendorupdate(request, pk):
    """
    Fix: include request.FILES when updating so images (or file fields) are handled.
    Also ensure vendor owns the package before allowing update.
    """
    item = get_object_or_404(Packagecreate, pk=pk)
    ven = _get_vendor_from_session(request)
    if not ven:
        return redirect('vendorlogin')

    if item.vendor_id != ven.id:
        return redirect('vendorhome')

    if request.method == 'POST':
        form = vpackageform(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('vendorhome')
    else:
        form = vpackageform(instance=item)
    return render(request, "update.html", {'form': form})







# Booking flows
# at top: make sure you import these
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Packagecreate, Bookingdetails, Usersign_up
from .forms import Bookingdetailsform

def booking(request, package_id):
    # require logged-in user (using your session key)
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect(f"{reverse('userlogin')}?next={reverse('booking', args=[package_id])}")

    user = Usersign_up.objects.filter(id=user_id).first()
    if not user:
        return redirect('userlogin')

    package = get_object_or_404(Packagecreate, id=package_id)

    if request.method == 'POST':
        form = Bookingdetailsform(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            # Attach authoritative relations/server-side values
            booking.package = package
            # if Bookingdetails model has a FK named 'user'
            if hasattr(booking, 'user'):
                booking.user = user
            else:
                booking.user_id = user.id

            # Force fullname & phone from server user object (do not trust POST)
            # Adapt attribute names if your Usersign_up has different fields
            booking.fullname = getattr(user, 'username', '') or getattr(user, 'fullname', '')
            booking.phone = getattr(user, 'phone', '') or getattr(user, 'mobile', '')

            booking.save()
            return redirect('payment')
    else:
        # Prefill number_of_people and booking_date optionally
        initial = {
            'number_of_people': 1,
            # 'booking_date': package.date or ''   # optional
        }
        # Pre-fill fullname/phone so Django builds form fields (we'll render disabled ones)
        initial['fullname'] = getattr(user, 'username', '') or getattr(user, 'fullname', '')
        initial['phone'] = getattr(user, 'phone', '') or getattr(user, 'mobile', '')
        form = Bookingdetailsform(initial=initial)

    return render(request, "booking.html", {
        'form': form,
        'package': package,
        'user_obj': user,
    })


def bookingdisplay(request):
    user = _get_user_from_session(request)
    if not user:
        return redirect('userlogin')

    booking = Bookingdetails.objects.filter(user_id=user.id)
    return render(request, "bookingdisplay.html", {'booking': booking})


def vendorbookings(request):
    ven = _get_vendor_from_session(request)
    if not ven:
        return redirect('vendorlogin')

    packages = Packagecreate.objects.filter(vendor_id=ven.id)
    booking = Bookingdetails.objects.filter(package__in=packages)
    return render(request, "vendorbookings.html", {'booking': booking})


def profile(request):
    user = _get_user_from_session(request)
    if not user:
        return redirect('userlogin')

    # Use a single object for profile template (not a queryset)
    return render(request, "profile.html", {'user_obj': user})

from .forms import UserProfileForm




def payment(request):
    return render(request, "payment.html")

from django.shortcuts import render, get_object_or_404
from .models import Packagecreate

def package_detail(request, pk):
    pkg = get_object_or_404(Packagecreate, pk=pk)
    return render(request, 'package_detail.html', {'package': pkg})

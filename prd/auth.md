In این پاسخ، نکات کلیدی و مباحث جنگویی که به‌منظور پیاده‌سازی یک سیستم احراز هویت کامل با dj-rest-auth و allauth لازم است بدانید را دسته‌بندی کرده‌ایم. ابتدا به روش‌های صحیح override کردن مسیرها در URLconf و مسائل مربوط به ترتیب و namespace می‌پردازیم، سپس نحوه‌ی سفارشی‌سازی ویو تأیید ایمیل و templateها را توضیح می‌دهیم. در ادامه سراغ تنظیمات مربوط به mandatory email verification، مدیریت توکن‌ها و افزایش طول عمر access token، تعریف مسیر reset password confirm و رفع خطای reverse می‌رویم. در نهایت شیوه‌ی تست و اعتبارسنجی URLها با django-extensions و ساختار پوشه‌ی templates را جمع‌بندی می‌کنیم.

---

## ۱. Override کردن مسیرها (URLs) در Django

### ترتیب و اولویت URLها  
- Django بر اساس ترتیب موجود در `urlpatterns` مسیرها را یکی‌یکی امتحان می‌کند و به اولین تطابق پاسخ می‌دهد citeturn1search1.  
- اگر دو مسیر با همان الگو وجود داشته باشند، اولی که در لیست ظاهر شود برنده است؛ بنابراین برای override مطمئن باید مسیر سفارشی را دقیقاً همان‌جایی قرار دهید که Django ابتدا آن را ببیند citeturn1search0.

### include() و namespace  
- تابع `include()` مسیرهای یک ماژول URLconf دیگر را به‌طور کامل به پروژه تزریق می‌کند و در صورتی که همان مسیر در `include()` توسط اپ تعریف شده باشد، override مستقیم آن کارایی ندارد مگر مسیرهای اپ مورد نظر را دستی تعریف کنید citeturn1search2.  
- اگر از `namespace` در `include()` استفاده کنید، برای resolve کردن نام‌ها باید همیشه از `<namespace>:<name>` استفاده نمایید؛ حذف namespace در include یا تعریف مسیر اصلی بدون namespace ساده‌ترین راه برای دسترسی مستقیم به نام‌های URL است citeturn1search2.

---

## ۲. سفارشی‌سازی ویوی تأیید ایمیل (ConfirmEmailView)

### dj-rest-auth vs allauth  
- ویوی پیش‌فرض `dj_rest_auth.registration.views.ConfirmEmailView` یک APIView برمی‌گرداند و به `template_name` توجه نمی‌کند citeturn0search17.  
- اگر قصد دارید بعد از کلیک روی لینک تأیید، یک صفحه HTML رندر شود، باید از `allauth.account.views.ConfirmEmailView` استفاده کنید و کلاس خود را از آن ارث ببرید تا بتوانید `template_name` را ست کنید citeturn0search17.

```python
from allauth.account.views import ConfirmEmailView

class CustomConfirmEmailView(ConfirmEmailView):
    template_name = "authentication/email_confirm.html"
```

### TemplateResponseMixin و تعریف template_name  
- خطای `TemplateResponseMixin requires either a definition of 'template_name'` زمانی رخ می‌دهد که ویویی مبتنی بر TemplateResponseMixin تابع `get_template_names()` یا خاصیت `template_name` را نداشته باشد; پس حتماً در TemplateViewها `template_name` را تعیین کنید citeturn0search17.  
- برای placeholder داخلی dj-rest-auth که لینک تأیید را reverse می‌کند، مسیر زیر را override کنید تا TemplateView پیش‌فرض حذف یا اصلاح شود:

```python
re_path(
    r"^account-confirm-email/(?P<key>[-:\w]+)/$",
    CustomConfirmEmailView.as_view(),
    name="account_confirm_email",
)
```

---

## ۳. تنظیمات mandatory email verification

- برای اینکه کاربر نتواند تا قبل از تأیید ایمیل وارد شود، در `settings.py` مقدار زیر را قرار دهید:

```python
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_REQUIRED     = True
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
```
هر کاربر پس از ثبت‌نام یک ایمیل تأیید می‌گیرد و تا کلیک روی لینک، لاگین مسدود می‌شود citeturn0search8.

---

## ۴. مدیریت توکن‌ها و افزایش طول عمر Access Token

- با استفاده از djangorestframework-simplejwt می‌توانید مدت‌زمان عمر توکن‌ها را تنظیم کنید:

```python
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME":  timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES":     ("Bearer",),
}
REST_USE_JWT = True
```
- اگر از کوکی برای نگهداری JWT استفاده می‌کنید، مقادیر زیر را نیز اضافه کنید:

```python
JWT_AUTH_COOKIE         = "access-token"
JWT_AUTH_REFRESH_COOKIE = "refresh-token"
```
تمام این تنظیمات امنیت و کنترل بهتری روی توکن‌ها فراهم می‌کند citeturn0search16.

---

## ۵. مسیر Password Reset Confirm و رفع خطای Reverse

- dj-rest-auth به‌طور پیش‌فرض مسیر زیر را برای confirm ریست رمز تعریف می‌کند:

```python
path(
    "password/reset/confirm/<str:uidb64>/<str:token>/",
    PasswordResetConfirmView.as_view(),
    name="password_reset_confirm",
)
```
- خطای `Reverse for 'password_reset_confirm' not found` معمولاً به این دلیل است که این URL را در پروژه اضافه نکرده‌اید یا نام یا پارامترها را اشتباه پاس داده‌اید; فراموش نکنید حتماً این مسیر را قبل از سایر includeها تعریف کنید citeturn0search10.

---

## ۶. ساختار پوشه‌ی Templates و تنظیمات TEMPLATES

- تمام templateهای سفارشی نظیر `email_confirm.html` و `password_reset_confirm.html` را تحت پوشه‌ای مثل `templates/authentication/` قرار دهید و در `settings.py` مسیر آن را در key `'DIRS'` تعریف کنید:

```python
TEMPLATES = [
    {
        ...
        "DIRS": [BASE_DIR / "templates"],
        ...
    },
]
```
بدون این تنظیم، Django قادر به یافتن و رندر قالب‌های شما نخواهد بود citeturn0search5.

---

## ۷. بررسی و تست مسیرها با django-extensions

- نصب django-extensions:

```bash
pip install django-extensions
```
- افزودن به `INSTALLED_APPS`:

```python
INSTALLED_APPS += ["django_extensions"]
```
- اجرای دستور نمایش همه URLها:

```bash
python manage.py show_urls
```
این ابزار به شما کمک می‌کند مطمئن شوید همه‌ی مسیرها به‌درستی ثبت شده‌اند و نام‌ها و الگوها مطابق انتظار هستند citeturn0search10.

---

با تسلط بر این مباحث—override مسیرها، سفارشی‌سازی ویوها و templateها، تنظیمات email verification و توکن‌ها، و بررسی URLها—قادر خواهید بود یک سیستم احراز هویت کامل، امن و قابل توسعه در Django بسازید.
from allauth.account.views import ConfirmEmailView


class CustomConfirmEmailView(ConfirmEmailView):
    template_name = "authentication/email_confirm.html"

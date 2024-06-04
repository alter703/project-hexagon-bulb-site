from django.contrib import messages
from better_profanity import profanity


class ProfanityCheckMixin:
    def check_profanity(self, form, fields: list):
        for field in fields:
            content = form.cleaned_data.get(field, '')
            if profanity.contains_profanity(content):
                messages.warning(self.request, "Your submission contains offensive language. Please edit it.")
                return False
        return True

import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30)
    amount = models.IntegerField(default=0, verbose_name="Ilość zwróconych odpowiedzi")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Tagi"
        verbose_name = "Tag"


class Response(models.Model):
    def validate_date(self):
        if self > datetime.date.today():
            raise ValidationError("Data nie może być w przyszłości")

    NEED_THE_UPDATE = 'NEED_THE_UPDATE'
    NEED_CLARIFICATION = 'NEED_CLARIFICATION'
    NO_RESPONSE = 'NO_RESPONSE'
    OK = 'OK'
    FIXED = 'FIXED'
    STATUS_CHOICES = [(NEED_THE_UPDATE, "Odpowiedź wymaga zmiany/rozszerzenia"),
                      (NO_RESPONSE, "Nie ma jeszcze dodanej odpowiedzi"),
                      (NEED_CLARIFICATION, "Odpowiedź wymaga zmiany/rozszerzenia"),
                      (OK, "Odpowiedź poprawna"),
                      (FIXED, "Oczekuje na sprawdzenie przez administratora."), ]

    tag = models.OneToOneField(Tag, on_delete=models.CASCADE, unique=True, verbose_name="Tag")
    text = models.TextField(max_length=2500, unique=True, verbose_name="Treść")
    legal_basis = models.CharField(max_length=250, null=True, verbose_name="Podstawa prawna")
    source = models.URLField(max_length=250, blank=True, null=True, verbose_name="Źródło informacji")
    moderator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    response_status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=NO_RESPONSE,
                                       verbose_name="Status odpowiedzi:")
    legal_status_as_of = models.DateField(default=datetime.date.today(), verbose_name="Stan prawny na",
                                          validators=[validate_date, ])
    last_edit = models.DateTimeField(default=datetime.datetime.now(), verbose_name="Ostatnio edytowany")

    def __str__(self):
        if len(self.text) > 50:
            return f'{self.tag}: {self.text[:50]}...'
        else:
            return f'{self.tag}: {self.text}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.last_edit = datetime.datetime.now()

        super().save()

    class Meta:
        verbose_name_plural = "Odpowiedzi"
        verbose_name = "Odpowiedź"


class Pattern(models.Model):
    text = models.TextField(max_length=1000, verbose_name="Treść wzorca")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.text} [{self.tag}]'

    class Meta:
        verbose_name_plural = "Wzorce"
        verbose_name = "Wzorzec"


class Rating(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, verbose_name="Odpowiedź")
    rating = models.IntegerField(verbose_name="Ocena")
    ip = models.GenericIPAddressField(verbose_name="Adres IP")

    class Meta:
        unique_together = ('response', 'ip')
        verbose_name_plural = "Oceny"
        verbose_name = "Ocena"


class Report(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, verbose_name="Odpowiedź")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="Tag")
    UNRELATED = 'UNRELATED'
    INCOMPLETE = 'INCOMPLETE'
    INCOMPREHENSIBLE = 'INCOMPREHENSIBLE'
    OUTDATED = 'OUTDATED'
    LINGUISTIC_ERRORS = 'LINGUISTIC_ERRORS'
    OTHER = 'OTHER'
    CATEGORY_CHOICES = [(UNRELATED, 'Odpowiedź nie jest związana z zadanym pytaniem'),
                        (INCOMPLETE, 'Odpowiedź na zadane pytanie jest niekompletna'),
                        (INCOMPREHENSIBLE, 'Odpowiedź jest niezrozumiała'),
                        (OUTDATED, 'Odpowiedź nie jest zgodna z obowiązującymi przepisami'),
                        (LINGUISTIC_ERRORS, 'Odpowiedź wymaga poprawy błędów językowych'),
                        (OTHER, 'Inny')]
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default=OTHER,
                                verbose_name="Kategoria zgłoszenia")
    text = models.TextField(max_length=2500, verbose_name='Tekst')
    timestamp = models.DateTimeField(default=datetime.datetime.now(), verbose_name="Data zgłoszenia")

    class Meta:
        verbose_name_plural = "Zgłoszenia"
        verbose_name = "Zgłoszenie"

    def __str__(self):
        return f"Zgłoszenie dotyczące odpowiedzi z tagiem: {self.tag.name}"

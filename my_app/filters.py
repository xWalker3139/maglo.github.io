import django_filters
from django_filters import CharFilter

from .models import *

class SearchFilter(django_filters.FilterSet):
    class Meta:
        search = CharFilter(field_name='search', lookup_expr='icontains')
        model = SearchBarCopil
        fields = '__all__'

class AutoFilter(django_filters.FilterSet):
    class Meta:
        model = AnuntAdult
        fields = ['caroserie', 'capacitate_motor', 'combustibil', 'culoare', 'cutie_de_viteze', 'marca', 'rulaj', 'stare']
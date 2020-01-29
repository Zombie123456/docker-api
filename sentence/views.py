from rest_framework import viewsets
from rest_framework import mixins
from sentence.models import Sentence
from sentence.serializers import SentenceSerializer


class SentenceMemberViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin):
    model = Sentence
    permission_classes = []
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer


class SentenceManageViewSet(viewsets.GenericViewSet,
                            mixins.CreateModelMixin):
    model = Sentence
    permission_classes = []
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer
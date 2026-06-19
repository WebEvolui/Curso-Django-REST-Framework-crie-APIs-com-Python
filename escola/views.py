from escola.models import Estudante, Curso, Matricula
from escola.serializers import EstudanteSerializer, CursoSerializer, EstudanteSerializerV2, MatriculaSerializer, ListaMatriculasEstudanteSerializer, ListaMatriculasCursoSerializer
from rest_framework import viewsets, generics, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from escola.throttle import MatriculaUserRateThrottle

class EstudanteViewSet(viewsets.ModelViewSet):
    queryset = Estudante.objects.all().order_by('id')
    # serializer_class = EstudanteSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['nome']
    search_fields = ['nome', 'cpf']
    
    def get_serializer_class(self):
        if self.request.version == 'v2':
            return EstudanteSerializerV2
        return EstudanteSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all().order_by('id')
    serializer_class = CursoSerializer

class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all().order_by('id')
    serializer_class = MatriculaSerializer
    throttle_classes = [MatriculaUserRateThrottle]
    
class ListaMatriculaEstudante(generics.ListAPIView):    
    def get_queryset(self):
        queryset = Matricula.objects.filter(estudante__id=self.kwargs['pk'])
        return queryset
    
    serializer_class = ListaMatriculasEstudanteSerializer

class ListaMatriculaCurso(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Matricula.objects.filter(curso__id=self.kwargs['pk'])
        return queryset
    
    serializer_class = ListaMatriculasCursoSerializer



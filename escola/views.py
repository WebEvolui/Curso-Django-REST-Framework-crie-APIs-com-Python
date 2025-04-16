from escola.models import Estudante, Curso, Matricula
from escola.serializers import EstudanteSerializer, CursoSerializer, MatriculaSerializer, ListaMatriculasEstudanteSerializer, ListaMatriculasCursoSerializer
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny

class EstudanteViewSet(viewsets.ModelViewSet):
    queryset = Estudante.objects.all()
    serializer_class = EstudanteSerializer
    
class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    
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



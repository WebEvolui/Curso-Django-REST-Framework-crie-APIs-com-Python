from escola.models import Estudante, Curso, Matricula
from escola.serializers import (
    EstudanteSerializer,
    CursoSerializer,
    EstudanteSerializerV2,
    MatriculaSerializer,
    ListaMatriculasEstudanteSerializer,
    ListaMatriculasCursoSerializer,
)
from rest_framework import viewsets, generics, filters
from rest_framework.permissions import AllowAny
from escola.permissions import DjangoModelPermissionsWithView
from django_filters.rest_framework import DjangoFilterBackend
from escola.throttle import MatriculaUserRateThrottle


class EstudanteViewSet(viewsets.ModelViewSet):
    """
    Descrição da ViewSet:
    - Endpoint para CRUD de estudantes.

    Campos de ordenação:
    - nome: permite ordenar os resultados por nome.

    Campos de pesquisa:
    - nome: permite pesquisar os resultados por nome.
    - cpf: permite pesquisar os resultados por CPF.

    Métodos HTTP Permitidos:
    - GET, POST, PUT, PATCH, DELETE

    Classe de Serializer:
    - EstudanteSerializer: usado para serialização e desserialização de dados.
    - Se a versão da API for 'v2', usa EstudanteSerializerV2.
    """
    
    queryset = Estudante.objects.all().order_by("id")
    permission_classes = [DjangoModelPermissionsWithView]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["nome"]
    search_fields = ["nome", "cpf"]

    def get_serializer_class(self):
        if self.request.version == "v2":
            return EstudanteSerializerV2
        return EstudanteSerializer


class CursoViewSet(viewsets.ModelViewSet):
    """
    Descrição da ViewSet:
    - Endpoint para CRUD de cursos.

    Métodos HTTP Permitidos:
    - GET, POST, PUT, PATCH, DELETE
    """

    queryset = Curso.objects.all().order_by("id")
    serializer_class = CursoSerializer
    permission_classes = [DjangoModelPermissionsWithView]


class MatriculaViewSet(viewsets.ModelViewSet):
    """
    Descrição da ViewSet:
    - Endpoint para CRUD de matrículas.

    Métodos HTTP Permitidos:
    - GET, POST

    Throttle Classes:
    - MatriculaAnonRateThrottle: limite de taxa para usuários anônimos.
    - UserRateThrottle: limite de taxa para usuários autenticados.
    """

    queryset = Matricula.objects.all().order_by("id")
    serializer_class = MatriculaSerializer
    throttle_classes = [MatriculaUserRateThrottle]
    permission_classes = [DjangoModelPermissionsWithView]
    http_method_names = ["get", "post"]


class ListaMatriculaEstudante(generics.ListAPIView):
    """ 	
    Descrição da View:
    - Lista Matriculas por id de Estudante
    Parâmetros:
    - pk (int): O identificador primário do objeto. Deve ser um número inteiro.
    """

    serializer_class = ListaMatriculasEstudanteSerializer
    permission_classes = [DjangoModelPermissionsWithView]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Matricula.objects.none()

        return Matricula.objects.filter(estudante__id=self.kwargs["pk"])

class ListaMatriculaCurso(generics.ListAPIView):
    """
    Descrição da View:
    - Lista Matriculas por id de Curso
    Parâmetros:
    - pk (int): O identificador primário do objeto. Deve ser um número inteiro.
    """

    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = ListaMatriculasCursoSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Matricula.objects.none()

        return Matricula.objects.filter(curso__id=self.kwargs["pk"])

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
    Descrição da View:
    - Gerencia os estudantes da escola.
    Parâmetros:
    - id (int): O identificador primário do estudante. Deve ser um número inteiro.
    - nome (str): O nome do estudante. Deve ser uma string.
    - email (str): O email do estudante. Deve ser uma string única e válida.
    - cpf (str): O CPF do estudante. Deve ser uma string única.
    - data_nascimento (date): A data de nascimento do estudante. Deve ser uma data válida.
    - celular (str): O número de celular do estudante. Deve ser uma string.
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
    Descrição da View:
    - Gerencia os cursos disponíveis na escola.
    Parâmetros:
    - id (str): O identificador primário do curso. Deve ser uma string única.
    - nome (str): O nome do curso. Deve ser uma string.
    - nível (str): O nível do curso. Deve ser uma string, podendo ser "B" para Básico, "I" para Intermediário ou "A" para Avançado.
    """

    queryset = Curso.objects.all().order_by("id")
    serializer_class = CursoSerializer
    permission_classes = [DjangoModelPermissionsWithView]


class MatriculaViewSet(viewsets.ModelViewSet):
    """
    Descrição da View:
    - Gerencia as matrículas dos estudantes nos cursos.
    Parâmetros:
    - id (int): O identificador primário da matrícula. Deve ser um número inteiro.
    - estudante (int): O identificador do estudante associado à matrícula. Deve ser um número inteiro que corresponde a um estudante existente.
    - curso (int): O identificador do curso associado à matrícula. Deve ser um número inteiro que corresponde a um curso existente.
    - período (str): O período da matrícula. Deve ser uma string, podendo ser "M" para Matutino, "V" para Vespertino ou "N" para Noturno.
    
    Restrições:
    - Um estudante não pode se matricular no mesmo curso mais de uma vez. A combinação de estudante e curso deve ser única.
    
    Trhottling:
    - Limite de 5 requisições por minuto para cada usuário autenticado.
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

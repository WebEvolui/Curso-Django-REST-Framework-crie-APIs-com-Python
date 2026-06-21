from django.contrib import admin
from django.urls import path, include
from escola.views import EstudanteViewSet, CursoViewSet, MatriculaViewSet, ListaMatriculaEstudante, ListaMatriculaCurso
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Documentação da API Escola",
      default_version='v1',
      description="Documentação da API para gerenciamento de estudantes, cursos e matrículas.",
      terms_of_service="https://www.evolui.dev/termos/",
      contact=openapi.Contact(email="contato@evolui.dev"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

router = DefaultRouter()
router.register('estudantes', EstudanteViewSet, basename='Estudantes')
router.register('cursos', CursoViewSet, basename='Cursos')
router.register('matriculas', MatriculaViewSet, basename='Matriculas')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("<str:version>/", include(router.urls)),
    path('<str:version>/estudantes/<int:pk>/matriculas/', ListaMatriculaEstudante.as_view()),
    path('<str:version>/cursos/<int:pk>/matriculas/', ListaMatriculaCurso.as_view()),
    path('<str:version>/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('<str:version>/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

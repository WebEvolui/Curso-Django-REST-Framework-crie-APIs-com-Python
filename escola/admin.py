from django.contrib import admin
from escola.models import Estudante, Curso, Matricula

class EstudanteAdmin(admin.ModelAdmin):
    list_display = ('id', "nome", "email", "cpf", "data_nascimento", "celular")
    list_display_links = ("id", "nome")
    list_per_page = 20
    search_fields = ("nome", "cpf")
    ordering = ("nome",)
    
admin.site.register(Estudante, EstudanteAdmin) 

class CursoAdmin(admin.ModelAdmin):
    list_display = ('id', "codigo", "descricao", "nivel")
    list_display_links = ("id", "codigo")
    search_fields = ("codigo",)
    
admin.site.register(Curso, CursoAdmin)   

class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('id', "estudante", "curso", "periodo")
    list_display_links = ("id", "estudante")
    
admin.site.register(Matricula, MatriculaAdmin)
    
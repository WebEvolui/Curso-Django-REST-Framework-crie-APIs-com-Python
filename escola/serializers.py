from rest_framework import serializers
from escola.models import Estudante, Curso, Matricula
from escola.validators import cpf_invalido, nome_invalido, celular_invalido

class EstudanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudante
        fields = ['id', 'nome', 'email', 'cpf', 'data_nascimento', 'celular']
    
    def validate(self, data):
        if cpf_invalido(data['cpf']):
            raise serializers.ValidationError({"cpf": "CPF deve ter 11 dígitos."})
        if nome_invalido(data['nome']):
            raise serializers.ValidationError({"nome": "O nome deve conter apenas letras."})
        if celular_invalido(data['celular']):
            raise serializers.ValidationError({"celular": "Número de celular deve ter 13 dígitos. Formato: 33 99999-8888"})
        return data

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'
        
class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        exclude = []
        
class ListaMatriculasEstudanteSerializer(serializers.ModelSerializer):
    curso = serializers.ReadOnlyField(source='curso.descricao')
    periodo = serializers.SerializerMethodField()
    
    class Meta:
        model = Matricula
        fields = ['curso', 'periodo']
        
    def get_periodo(self, obj):
        return obj.get_periodo_display()
    
class ListaMatriculasCursoSerializer(serializers.ModelSerializer):
    nome_estudante = serializers.ReadOnlyField(source='estudante.nome')
    
    class Meta:
        model = Matricula
        fields = ['nome_estudante']
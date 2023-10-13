"""
Serializer for Recipe API's
"""
from rest_framework import serializers

from core.models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    """ Serializer for Recipe object """
    class Meta:
        model = Recipe
        fields = ('id','user','title','price','description','time_minutes','link')
        read_only_fields = ('id',)

class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ('description',)
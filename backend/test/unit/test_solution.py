import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import pytest
from unittest.mock import patch, MagicMock
from src.controllers.recipecontroller import RecipeController
from src.util.dao import DAO
from src.static.diets import Diet

@pytest.fixture
def mock_controller():
    dao = MagicMock(spec=DAO)
    controller = RecipeController(items_dao=dao)
    return controller

#Verifies that the correct recipe is returned when take_best is True
@pytest.mark.unit
@patch('src.controllers.recipecontroller.RecipeController.get_readiness_of_recipes')
def test_get_recipe_best(mock_get_readiness, mock_controller):
    mock_get_readiness.return_value = {'recipe1': 0.8, 'recipe2': 0.9}
    result = mock_controller.get_recipe(Diet.VEGAN, True)
    assert result in ['recipe1', 'recipe2']

#Verifies that the correct recipe is returned when take_best is False
@pytest.mark.unit
@patch('src.controllers.recipecontroller.RecipeController.get_readiness_of_recipes')
def test_get_recipe_random(mock_get_readiness, mock_controller):
    mock_get_readiness.return_value = {'recipe1': 0.8, 'recipe2': 0.9}
    result = mock_controller.get_recipe(Diet.VEGAN, False)
    assert result in ['recipe1', 'recipe2']

#Verifies that None is returned when no recipes are compatible with the diet
@pytest.mark.unit
@patch('src.controllers.recipecontroller.RecipeController.get_readiness_of_recipes')
def test_get_recipe_no_compatible_recipes(mock_get_readiness, mock_controller):
    mock_get_readiness.return_value = {}
    result = mock_controller.get_recipe(Diet.VEGAN, True)
    assert result is None

#Verifies that None is returned when readiness is below 0.1
@pytest.mark.unit
@patch('src.controllers.recipecontroller.RecipeController.get_readiness_of_recipes')
def test_get_recipe_readiness_below_threshold(mock_get_readiness, mock_controller):
    mock_get_readiness.return_value = {'recipe1': 0.05}
    result = mock_controller.get_recipe(Diet.VEGAN, True)
    assert result is None  # Förväntat resultat är None

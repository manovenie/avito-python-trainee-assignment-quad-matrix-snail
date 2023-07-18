import pytest
import asyncio
from matrix_handler.snail_matrix import prepare_matrix, traverse_matrix, get_matrix

SOURCE_URL = 'https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt'
TRAVERSAL = [
    10, 50, 90, 130,
    140, 150, 160, 120,
    80, 40, 30, 20,
    60, 100, 110, 70,
]

PREPARED_MATRIX = [
    [10, 20, 30, 40],
    [50, 60, 70, 80],
    [90, 100, 110, 120],
    [130, 140, 150, 160],
]


def test_prepare_matrix():
    with open("fixtures/test_matrix_string.txt") as test_matrix:
        assert prepare_matrix(test_matrix.read()) == PREPARED_MATRIX

    # test for empty string instead of matrix
    assert prepare_matrix("") == []

    # test for non-quadratic matrix from file
    with open("fixtures/test_non_quad_matrix.txt") as test_non_quad_matrix:
        assert prepare_matrix(test_non_quad_matrix.read()) == []


def test_traverse_matrix():
    assert traverse_matrix(PREPARED_MATRIX) == TRAVERSAL


def test_get_matrix():
    assert asyncio.run(get_matrix(SOURCE_URL)) == TRAVERSAL

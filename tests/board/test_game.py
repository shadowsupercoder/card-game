import requests
import pytest

from django.urls import reverse
from django.utils.translation import activate

from board.forms import GameInputForm


@pytest.mark.django_db
class TestGame():
    """Tests for game endpoint.
    get: the form with input fields for game.
    post: finding a winner player.
    """
   
    def test_get_form(self, client):
        """GET / returns the form with input fields for game."""
        response = client.get(reverse('game'))
        content = response.content

        assert response.status_code == 200
        assert '<label for="id_player_count">' in str(content)
        assert '<label for="id_square_count">' in str(content)
        assert '<label for="id_card_count">' in str(content)
        assert '<label for="id_colors">' in str(content)
        assert '<label for="id_cards">' in str(content)


@pytest.mark.parametrize('player_count, square_count, card_count, colors, \
    cards, validity',
    [
        (2, 9, 4, 'AVHFISKSH', 'A,VV,F,S', True),
        (5, 9, 4, 'AVHFISKSH', 'A,VV,F,S', False),
        (4, 99, 4, 'AVHFISKSH', 'A,VV,F,S', False),
        (4, 79, 201, 'AVHFISKSH', 'A,VV,F,S', False),
        # (4, 5, 20, 'AVHFISKSH', 'A,VV,F,S', False),
        # (4, 9, 5, 'AVHFISKSH', 'A,VV,F,S', False),
    ]
)
def test_form_is_valid(player_count, square_count, card_count, colors, cards, validity):
    form = GameInputForm(data={
        'player_count': player_count,
        'square_count': square_count,
        'card_count': card_count,
        'colors': colors,
        'cards': cards,
    })

    assert form.is_valid() is validity

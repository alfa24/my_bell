import uuid

from django.test import TestCase

from bell.models import Bell


class BellModelTest(TestCase):
    """Тест модели колокольчика"""

    def test_when_saved_an_uuid_created(self):
        """test: При сохранении создается уникальный индефикатор"""

        bell = Bell.objects.create()
        self.assertEqual(bell.link_ref.variant, uuid.RFC_4122)

    def test_get_absolute_url(self):
        """получить абсолютный url"""

        bell = Bell.objects.create()
        self.assertEqual(f'/bells/{bell.link_ref}/', bell.get_absolute_url())

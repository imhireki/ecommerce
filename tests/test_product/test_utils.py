import pytest

from apps.product import utils


@pytest.mark.unit
def test_resize_image(mocker):
    new_size = (512, 512)
    django_file = mocker.patch("apps.product.utils.File")
    pillow_image = mocker.patch("PIL.Image.open").return_value.__enter__.return_value
    resized_image_mock = pillow_image.resize.return_value

    resized_image = utils.resize_image(mocker.Mock(), new_size)

    assert resized_image == django_file.return_value
    pillow_image.resize.assert_called_with(new_size, resample=1, reducing_gap=2)
    resized_image_mock.save.assert_called()

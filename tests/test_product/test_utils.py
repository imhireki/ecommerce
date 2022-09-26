import pytest

from apps.product import utils


@pytest.mark.unit
def test_resize_image(mocker):
    new_size = (512, 512)
    django_file_mock = mocker.patch('apps.product.utils.File')
    pillow_image_mock = mocker.patch('PIL.Image.open')\
                        .return_value.__enter__.return_value
    resized_image_mock = pillow_image_mock.resize.return_value

    resized_image = utils.resize_image(mocker.Mock(), new_size)

    assert resized_image is django_file_mock.return_value 
    assert pillow_image_mock.resize.call_args.args[0] == new_size
    assert resized_image_mock.save.called


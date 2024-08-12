import logging

logger = logging.getLogger(__name__)


def post_delete_category_icon_file(sender, instance, **kwargs):
    """
    Delete the icon file associated with the category instance after the category is deleted.
    """
    if hasattr(instance, 'icon'):
        file = getattr(instance, 'icon')
        if file:
            file.delete(save=False)
            logger.info(f"Icon file deleted for category: {instance.id}")

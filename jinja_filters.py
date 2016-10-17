def message_alert_glyph(value):
    """
        Get alerts class icons from class alert.
    """
    tags = [
        ('error', 'fui-cross-circle'),
        ('info', 'fui-info-circle'),
        ('success', 'fui-check-circle'),
        ('warning', 'fui-alert-circle')
    ]

    for search, replace in tags:
        value = value.replace(search, replace)

    return value


def messages_alert_tags(value):
    """
        Get alerts class from alerts type
    """
    tags = [
        ('error', 'danger'),
        ('info', 'info'),
        ('success', 'success'),
        ('warning', 'warning')
    ]

    for search, replace in tags:
        value = value.replace(search, replace)

    return value

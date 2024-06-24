import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    cr.execute("UPDATE estate_property SET a_new_field_two = 'I am new'")
    _logger.info("Updated %s properties", cr.rowcount)

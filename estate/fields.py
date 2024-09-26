import re

from odoo import models, fields, api

from shapely import wkb, wkt
from shapely.geometry import shape
from shapely.geometry.point import Point

from odoo.exceptions import UserError


class PointField(fields.Field):
    type = 'geo_point'
    column_type = ('geography(POINT, 4326)', 'geography(POINT, 4326)')

    def convert_to_read(self, value, record, values=None):
        if value is None:
            return None

        if not isinstance(value, str):
            raise UserError(f"Invalid point type: {value} ({type(value)})")

        # try to split by comma and convert to float
        try:
            coord_tuple = tuple(float(coord.strip()) for coord in value.split(','))
            return coord_tuple
        except ValueError as e:
            pass

        is_hex_point = re.match(r'[0-9a-fA-F]{50}', value)
        if is_hex_point:
            point = wkb.loads(value, hex=True)
            return list(point.coords)
        else:
            # print why not match
            raise UserError(f"Invalid point format: {value} ({type(value)})")

    def convert_to_write(self, value, record):
        if value is None:
            return None

        try:
            coord_tuple = tuple(float(coord.strip()) for coord in value.split(','))
            point = Point(coord_tuple)
            return point.wkb_hex
        except ValueError as e:
            raise UserError(f"Invalid point format: {value}. Should be 'x,y' ({e})")


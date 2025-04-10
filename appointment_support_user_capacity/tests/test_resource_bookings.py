from datetime import datetime, timedelta

from odoo import Command
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestResourceBookings(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.resource_1 = cls.env["appointment.resource"].create(
            {
                "name": "Test Resource 1",
                "capacity": 2,
                "shareable": True,
            }
        )

        cls.resource_2 = cls.env["appointment.resource"].create(
            {
                "name": "Test Resource 2",
                "capacity": 15,
                "shareable": True,
            }
        )

        cls.resource_one_booking = cls.env["appointment.type"].create(
            {
                "name": "Test Resource multiple bookings",
                "schedule_based_on": "resources",
                "resource_ids": [(6, 0, [cls.resource_1.id])],
                "capacity_type": "one_booking",
            }
        )

        cls.resource_multiple_bookings = cls.env["appointment.type"].create(
            {
                "name": "Test Resource multiple bookings",
                "schedule_based_on": "resources",
                "resource_ids": [(6, 0, [cls.resource_1.id])],
                "capacity_type": "multiple_bookings",
            }
        )

        cls.resource_multiple_seats = cls.env["appointment.type"].create(
            {
                "name": "Test Resource multiple seats",
                "schedule_based_on": "resources",
                "resource_ids": [(6, 0, [cls.resource_2.id])],
                "capacity_type": "multiple_seats",
            }
        )

    def test_resource_one_booking(self):
        """Test: single booking per slot work correctly for resources"""
        start = datetime(2025, 4, 1, 14, 0, 0)
        end = start + timedelta(hours=1)

        booking_1 = self.env["calendar.event"].create(
            [
                {
                    "appointment_type_id": self.resource_one_booking.id,
                    "booking_line_ids": [
                        Command.create(
                            {
                                "appointment_resource_id": self.resource_1.id,
                                "capacity_reserved": 1,
                            }
                        )
                    ],
                    "name": "Booking 1",
                    "start": start,
                    "stop": end,
                }
            ]
        )

        # Ensure booking exists
        self.assertEqual(
            len(
                self.env["calendar.event"].search(
                    [
                        (
                            "appointment_type_id",
                            "=",
                            self.resource_one_booking.id,
                        ),
                        ("start", "=", start),
                        ("stop", "=", end),
                        (
                            "booking_line_ids.appointment_resource_id",
                            "=",
                            self.resource_1.id,
                        ),
                    ]
                )
            ),
            1,
            "Resource should be able to take one booking per slot!",
        )

    def test_resource_multiple_bookings(self):
        """Test: multiple bookings per slot work correctly for resources"""
        start = datetime(2025, 4, 1, 14, 0, 0)
        end = start + timedelta(hours=1)

        booking_1, booking_2 = self.env["calendar.event"].create(
            [
                {
                    "appointment_type_id": self.resource_multiple_bookings.id,
                    "booking_line_ids": [
                        Command.create(
                            {
                                "appointment_resource_id": self.resource_1.id,
                                "capacity_reserved": 1,
                            }
                        )
                    ],
                    "name": "Booking 1",
                    "start": start,
                    "stop": end,
                },
                {
                    "appointment_type_id": self.resource_multiple_bookings.id,
                    "booking_line_ids": [
                        Command.create(
                            {
                                "appointment_resource_id": self.resource_1.id,
                                "capacity_reserved": 1,
                            }
                        )
                    ],
                    "name": "Booking 2",
                    "start": start,
                    "stop": end,
                },
            ]
        )

        # Ensure both bookings exists
        self.assertEqual(
            len(
                self.env["calendar.event"].search(
                    [
                        (
                            "appointment_type_id",
                            "=",
                            self.resource_multiple_bookings.id,
                        ),
                        ("start", "=", start),
                        ("stop", "=", end),
                        (
                            "booking_line_ids.appointment_resource_id",
                            "=",
                            self.resource_1.id,
                        ),
                    ]
                )
            ),
            2,
            "Resource should be able to take two bookings in the same slot.",
        )

    def test_resource_multiple_seats(self):
        """Test: multiple seats per slot work correctly for resources"""
        start = datetime(2025, 4, 1, 14, 0, 0)
        end = start + timedelta(hours=1)

        booking_1, booking_2 = self.env["calendar.event"].create(
            [
                {
                    "appointment_type_id": self.resource_multiple_seats.id,
                    "booking_line_ids": [
                        Command.create(
                            {
                                "appointment_resource_id": self.resource_2.id,
                                "capacity_reserved": 10,
                            }
                        )
                    ],
                    "name": "Booking 1",
                    "start": start,
                    "stop": end,
                },
                {
                    "appointment_type_id": self.resource_multiple_seats.id,
                    "booking_line_ids": [
                        Command.create(
                            {
                                "appointment_resource_id": self.resource_2.id,
                                "capacity_reserved": 5,
                            }
                        )
                    ],
                    "name": "Booking 2",
                    "start": start,
                    "stop": end,
                },
            ]
        )

        # Ensure both bookings exists
        self.assertEqual(
            len(
                self.env["calendar.event"].search(
                    [
                        (
                            "appointment_type_id",
                            "=",
                            self.resource_multiple_seats.id,
                        ),
                        ("start", "=", start),
                        ("stop", "=", end),
                        (
                            "booking_line_ids.appointment_resource_id",
                            "=",
                            self.resource_2.id,
                        ),
                    ]
                )
            ),
            2,
            "Resource should be able to take bookings with multiple seats in the same slot.",
        )

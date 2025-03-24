from datetime import datetime, timedelta

from odoo import Command
from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


@tagged("post_install", "-at_install")
class TestAppointmentUserCapacity(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.staff_user = cls.env.ref("base.user_admin")

        cls.user_one_booking = cls.env["appointment.type"].create(
            {
                "name": "Test Appointment 1",
                "schedule_based_on": "users",
                "staff_user_ids": [(6, 0, [cls.env.ref("base.user_admin").id])],
                "capacity_type": "one_booking",
                "user_capacity": 1,
            }
        )

        cls.user_multiple_bookings = cls.env["appointment.type"].create(
            {
                "name": "Test User multiple bookings",
                "schedule_based_on": "users",
                "staff_user_ids": [(6, 0, [cls.env.ref("base.user_admin").id])],
                "capacity_type": "multiple_bookings",
                "user_capacity": 2,
            }
        )

        cls.user_multiple_seats = cls.env["appointment.type"].create(
            {
                "name": "Test User multiple seats",
                "schedule_based_on": "users",
                "staff_user_ids": [(6, 0, [cls.env.ref("base.user_admin").id])],
                "capacity_type": "multiple_seats",
                "user_capacity": 15,
            }
        )

    def test_user_capacity_must_be_one_for_one_booking(self):
        """Ensure that when 'capacity_type' is 'one_booking', 'user_capacity' must be exactly 1."""
        appointment = self.user_one_booking

        self.assertEqual(
            appointment.user_capacity,
            1,
            "User capacity should be 1 for 'One Booking per Slot'",
        )

        with self.assertRaises(
            ValidationError,
            msg="User capacity cannot be greater than 1 for 'One Booking per Slot'",
        ):
            appointment.write({"user_capacity": 2})

        with self.assertRaises(
            ValidationError,
            msg="User capacity cannot be less than 1 for 'One Booking per Slot'",
        ):
            appointment.write({"user_capacity": 0})

    def test_user_capacity_for_multiple_bookings_and_seats(self):
        """Ensure that user_capacity must be at least 1 in 'multiple_bookings' or 'multiple_seats'."""
        appointment = self.user_multiple_bookings

        with self.assertRaises(
            ValidationError,
            msg="User capacity cannot be less than 1 in case of multiple bookings and seats",
        ):
            appointment.write({"user_capacity": 0})

        appointment.write({"user_capacity": 3})
        self.assertEqual(
            appointment.user_capacity,
            3,
            "User capacity should be updated to a valid value.",
        )

    def test_user_one_booking(self):
        """Test single booking per slot for users type"""
        start = datetime(2025, 4, 1, 14, 0, 0)
        end = start + timedelta(hours=1)

        booking_1 = self.env["calendar.event"].create(
            [
                {
                    "appointment_type_id": self.user_one_booking.id,
                    "booking_line_ids": [
                        Command.create(
                            {
                                "appointment_user_id": self.staff_user.id,
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
                        ("appointment_type_id", "=", self.user_one_booking.id),
                        ("start", "=", start),
                        ("stop", "=", end),
                        (
                            "booking_line_ids.appointment_user_id",
                            "=",
                            self.staff_user.id,
                        ),
                    ]
                )
            ),
            1,
            "User should be able to take one booking per slot.",
        )

    def test_user_multiple_bookings(self):
        """Test multiple bookings per slot for users"""
        start = datetime(2025, 4, 1, 14, 0, 0)
        end = start + timedelta(hours=1)

        booking_1, booking_2 = self.env["calendar.event"].create(
            [
                {
                    "appointment_type_id": self.user_multiple_bookings.id,
                    "booking_line_ids": [
                        Command.create(
                            {
                                "appointment_user_id": self.staff_user.id,
                                "capacity_reserved": 1,
                            }
                        )
                    ],
                    "name": "Booking 1",
                    "start": start,
                    "stop": end,
                },
                {
                    "appointment_type_id": self.user_multiple_bookings.id,
                    "booking_line_ids": [
                        Command.create(
                            {
                                "appointment_user_id": self.staff_user.id,
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

        # Ensure both bookings exist
        self.assertEqual(
            len(
                self.env["calendar.event"].search(
                    [
                        ("appointment_type_id", "=", self.user_multiple_bookings.id),
                        ("start", "=", start),
                        ("stop", "=", end),
                        (
                            "booking_line_ids.appointment_user_id",
                            "=",
                            self.staff_user.id,
                        ),
                    ]
                )
            ),
            2,
            "User should be able to take two bookings in the same slot.",
        )

    def test_user_multiple_seats(self):
        """Test multiple seats per slot for users"""
        start = datetime(2025, 4, 1, 14, 0, 0)
        end = start + timedelta(hours=1)

        booking_1, booking_2 = self.env["calendar.event"].create(
            [
                {
                    "appointment_type_id": self.user_multiple_seats.id,
                    "booking_line_ids": [
                        Command.create(
                            {
                                "appointment_user_id": self.staff_user.id,
                                "capacity_reserved": 10,
                            }
                        )
                    ],
                    "name": "Booking 1",
                    "start": start,
                    "stop": end,
                },
                {
                    "appointment_type_id": self.user_multiple_seats.id,
                    "booking_line_ids": [
                        Command.create(
                            {
                                "appointment_user_id": self.staff_user.id,
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

        # Ensure both bookings exist
        self.assertEqual(
            len(
                self.env["calendar.event"].search(
                    [
                        ("appointment_type_id", "=", self.user_multiple_seats.id),
                        ("start", "=", start),
                        ("stop", "=", end),
                        (
                            "booking_line_ids.appointment_user_id",
                            "=",
                            self.staff_user.id,
                        ),
                    ]
                )
            ),
            2,
            "User should be able to take two bookings in the same slot.",
        )

from datetime import datetime, timedelta

from odoo import http
from odoo.tests.common import HttpCase, TransactionCase
from odoo.tests import tagged


@tagged("-at_install", "post_install")
class TestAppointmentBooking(HttpCase, TransactionCase):

    def setUp(cls):
        super().setUp()

        cls.reference_date = datetime(2025, 4, 1, 10, 0, 0)
        cls.staff_user = cls.env["res.users"].create(
            {
                "name": "Staff User",
                "login": "staff@example.com",
            }
        )
        cls.staff_user.partner_id = cls.env["res.partner"].create(
            {"name": "Staff Partner"}
        )
        cls.resource_1 = cls.env["appointment.resource"].create(
            {
                "capacity": 2,
                "name": "Resource 1",
                "shareable": True,
            }
        )
        cls.resource_2 = cls.env["appointment.resource"].create(
            {
                "capacity": 4,
                "name": "Resource 2",
                "shareable": True,
            }
        )

    # --------------------------------------
    # Appointment booking - Staff Users
    # --------------------------------------
    def test_appointment_user_booking_for_one_booking(self):
        appointment_type = self.env["appointment.type"].create(
            {
                "name": "One Booking Appointment",
                "appointment_tz": "UTC",
                "min_schedule_hours": 1.0,
                "max_schedule_days": 7,
                "capacity_type": "one_booking",
                "schedule_based_on": "users",
                "staff_user_ids": [(6, 0, [self.staff_user.id])],
                "slot_ids": [
                    (
                        0,
                        0,
                        {
                            "weekday": str(self.reference_date.isoweekday()),
                            "start_hour": 10,
                            "end_hour": 18,
                        },
                    )
                ],
            }
        )

        start = datetime(2025, 4, 1, 15, 0, 0)
        end = start + timedelta(hours=1)

        self.authenticate(self.staff_user.login, self.staff_user.login)

        appointment_data = {
            "csrf_token": http.Request.csrf_token(self),
            "datetime_str": start,
            "duration_str": "1.0",
            "email": "testuser@example.com",
            "name": "John Doe",
            "phone": "1234567890",
            "staff_user_id": self.staff_user.id,
        }

        # Book 1 out of 1 allowed staff booking
        url = f"/appointment/{appointment_type.id}/submit"
        response = self.url_open(url, data=appointment_data)
        self.assertEqual(response.status_code, 200, "Booking request should be successful")

        remaining_capacity = appointment_type._get_users_remaining_capacity(self.staff_user, start, end)
        self.assertEqual(
            remaining_capacity["total_remaining_capacity"],
            0,
            "Remaining bookings should be 0 after 1 booking",
        )

        overbooking_data = {
            "csrf_token": http.Request.csrf_token(self),
            "datetime_str": start,
            "duration_str": "1.0",
            "email": "user2@example.com",
            "name": "User 2",
            "phone": "0987654321",
            "staff_user_id": self.staff_user.id,
        }

        # Attempt to book 2nd time -> should fail due to one booking restriction
        response = self.url_open(url, data=overbooking_data)
        self.assertEqual(response.status_code, 200, "Should redirect when overbooking")

        expected_url_part = f"/appointment/{appointment_type.id}?state=failed-staff-user"
        self.assertIn(
            expected_url_part,
            response.url,
            "Redirect URL should indicate failed booking due to not available this slot",
        )

    def test_appointment_user_booking_for_multi_booking(self):
        appointment_type = self.env["appointment.type"].create(
            {
                "name": "Multi-bookings Appointment",
                "appointment_tz": "UTC",
                "min_schedule_hours": 1.0,
                "max_schedule_days": 7,
                "capacity_type": "multiple_bookings",
                "schedule_based_on": "users",
                "staff_user_ids": [(6, 0, [self.staff_user.id])],
                "user_capacity_count": 2,  # Max 2 bookings per staff
                "slot_ids": [
                    (
                        0,
                        0,
                        {
                            "weekday": str(self.reference_date.isoweekday()),
                            "start_hour": 10,
                            "end_hour": 18,
                        },
                    )
                ],
            }
        )

        start = datetime(2025, 4, 1, 15, 0, 0)
        end = start + timedelta(hours=1)

        self.authenticate(self.staff_user.login, self.staff_user.login)

        # Book 1 out of 2 allowed staff bookings
        appointment_data = {
            "csrf_token": http.Request.csrf_token(self),
            "datetime_str": start,
            "duration_str": "1.0",
            "email": "testuser@example.com",
            "name": "John Doe",
            "phone": "1234567890",
            "staff_user_id": self.staff_user.id,
        }

        url = f"/appointment/{appointment_type.id}/submit"
        response = self.url_open(url, data=appointment_data)
        self.assertEqual(response.status_code, 200, "Booking request should be successful")

        remaining_capacity = appointment_type._get_users_remaining_capacity(self.staff_user, start, end)
        self.assertEqual(
            remaining_capacity["total_remaining_capacity"],
            1,
            "Remaining bookings should be 1 after 1 booking",
        )

        # Book 2 out of 2 allowed staff bookings
        response = self.url_open(url, data=appointment_data)
        self.assertEqual(response.status_code, 200, "Booking request should be successful")

        remaining_capacity = appointment_type._get_users_remaining_capacity(self.staff_user, start, end)
        self.assertEqual(
            remaining_capacity["total_remaining_capacity"],
            0,
            "Remaining bookings should be 0 after 2 booking",
        )

        # Attempt to book 3rd time -> should fail due to staff overbooking
        overbooking_data = {
            "csrf_token": http.Request.csrf_token(self),
            "datetime_str": start,
            "duration_str": "1.0",
            "email": "user2@example.com",
            "name": "User 2",
            "phone": "0987654321",
            "staff_user_id": self.staff_user.id,
        }

        response = self.url_open(url, data=overbooking_data)
        self.assertEqual(response.status_code, 200, "Should redirect when overbooking")

        expected_url_part = f"/appointment/{appointment_type.id}?state=failed-staff-user"
        self.assertIn(
            expected_url_part,
            response.url,
            "Redirect URL should indicate failed booking due to staff overbooking",
        )

    def test_appointment_user_booking_for_multi_seats(self):
        appointment_type = self.env["appointment.type"].create(
            {
                "name": "Multi-seat Appointment",
                "appointment_tz": "UTC",
                "min_schedule_hours": 1.0,
                "max_schedule_days": 7,
                "capacity_type": "multiple_seats",
                "schedule_based_on": "users",
                "staff_user_ids": [(6, 0, [self.staff_user.id])],
                "user_capacity_count": 5,  # Max 5 seats per staff
                "slot_ids": [
                    (
                        0,
                        0,
                        {
                            "weekday": str(self.reference_date.isoweekday()),
                            "start_hour": 10,
                            "end_hour": 18,
                        },
                    )
                ],
            }
        )

        start = datetime(2025, 4, 1, 15, 0, 0)
        end = start + timedelta(hours=1)

        self.authenticate(self.staff_user.login, self.staff_user.login)

        # Book 3 user capacity out of 5 seats
        appointment_data = {
            "csrf_token": http.Request.csrf_token(self),
            "datetime_str": start,
            "duration_str": "1.0",
            "email": "testuser@example.com",
            "name": "John Doe",
            "phone": "1234567890",
            "asked_capacity": 3,
            "staff_user_id": self.staff_user.id,
        }

        url = f"/appointment/{appointment_type.id}/submit"
        response = self.url_open(url, data=appointment_data)
        self.assertEqual(response.status_code, 200, "Booking request should be successful")

        remaining_capacity = appointment_type._get_users_remaining_capacity(self.staff_user, start, end)
        self.assertEqual(
            remaining_capacity["total_remaining_capacity"],
            2,
            "Remaining capacity should be 2 after booking 3 seats",
        )

        # try to Book 3 user capacity out of 2 remaining seats
        overbooking_data = {
            "csrf_token": http.Request.csrf_token(self),
            "datetime_str": start,
            "duration_str": "1.0",
            "email": "user2@example.com",
            "name": "User 2",
            "phone": "0987654321",
            "asked_capacity": 3,
            "staff_user_id": self.staff_user.id,
        }

        response = self.url_open(url, data=overbooking_data)
        self.assertEqual(response.status_code, 200, "Should redirect when overbooking")

        expected_url_part = f"/appointment/{appointment_type.id}?state=failed-staff-user"
        self.assertIn(
            expected_url_part,
            response.url,
            "Redirect URL should indicate failed booking due to staff capacity",
        )

        remaining_capacity = appointment_type._get_users_remaining_capacity(self.staff_user, start, end)
        self.assertEqual(
            remaining_capacity["total_remaining_capacity"],
            2,
            "Remaining capacity should still be 2 after failed overbooking attempt",
        )

    # --------------------------------------
    # Appointment booking - Resources
    # --------------------------------------
    def test_appointment_resource_booking_for_one_booking(self):
        appointment_type = self.env["appointment.type"].create(
            {
                "name": "One Booking Appointment",
                "appointment_tz": "UTC",
                "min_schedule_hours": 1.0,
                "max_schedule_days": 7,
                "capacity_type": "one_booking",
                "schedule_based_on": "resources",
                "resource_ids": [(6, 0, [self.resource_1.id])],
                "slot_ids": [
                    (
                        0,
                        0,
                        {
                            "weekday": str(self.reference_date.isoweekday()),
                            "start_hour": 10,
                            "end_hour": 18,
                        },
                    )
                ],
            }
        )

        start = datetime(2025, 4, 1, 15, 0, 0)
        end = start + timedelta(hours=1)

        self.authenticate(self.staff_user.login, self.staff_user.login)

        # Book 1 out of 1 allowed resource booking
        appointment_data = {
            "csrf_token": http.Request.csrf_token(self),
            "datetime_str": start,
            "duration_str": "1.0",
            "email": "testuser@example.com",
            "name": "John Doe",
            "phone": "1234567890",
            "available_resource_ids": self.resource_1.id,
        }

        url = f"/appointment/{appointment_type.id}/submit"
        response = self.url_open(url, data=appointment_data)

        self.assertEqual(response.status_code, 200, "Booking request should be successful")

        remaining_capacity = appointment_type._get_resources_remaining_capacity(self.resource_1, start, end)
        self.assertEqual(
            remaining_capacity["total_remaining_capacity"],
            0,
            "Remaining capacity should be 0 after a One booking",
        )

        # Attempt to book 2nd time -> should fail due to one booking restriction
        overbooking_data = {
            "csrf_token": http.Request.csrf_token(self),
            "datetime_str": start,
            "duration_str": "1.0",
            "email": "user2@example.com",
            "name": "User 2",
            "phone": "0987654321",
            "available_resource_ids": self.resource_1.id,
        }

        response = self.url_open(url, data=overbooking_data)
        self.assertEqual(response.status_code, 200, "Should redirect when trying to overbook")

        expected_redirect_url = f"/appointment/{appointment_type.id}?state=failed-resource"
        self.assertIn(
            expected_redirect_url,
            response.url,
            "Redirect URL should indicate failed booking due to full resource",
        )

        remaining_capacity = appointment_type._get_resources_remaining_capacity(self.resource_1, start, end)
        self.assertEqual(
            remaining_capacity["total_remaining_capacity"],
            0,
            "Remaining capacity should still be 0 after failed overbooking",
        )

    def test_appointment_resource_booking_for_multi_booking(self):
        appointment_type = self.env["appointment.type"].create(
            {
                "name": "Multi-booking Appointment",
                "appointment_tz": "UTC",
                "min_schedule_hours": 1.0,
                "max_schedule_days": 7,
                "capacity_type": "multiple_bookings",
                "schedule_based_on": "resources",
                "resource_ids": [(6, 0, [self.resource_1.id])],
                "slot_ids": [
                    (
                        0,
                        0,
                        {
                            "weekday": str(self.reference_date.isoweekday()),
                            "start_hour": 10,
                            "end_hour": 18,
                        },
                    )
                ],
            }
        )

        start = datetime(2025, 4, 1, 15, 0, 0)
        end = start + timedelta(hours=1)

        self.authenticate(self.staff_user.login, self.staff_user.login)

        # Book 1 out of 2 allowed resource bookings
        booking_data = {
            "csrf_token": http.Request.csrf_token(self),
            "datetime_str": start,
            "duration_str": "1.0",
            "email": "testuser@example.com",
            "name": "John Doe",
            "phone": "1234567890",
            "available_resource_ids": self.resource_1.id,
        }

        url = f"/appointment/{appointment_type.id}/submit"
        response = self.url_open(url, data=booking_data)
        self.assertEqual(response.status_code, 200, "First booking should be successful")

        remaining_capacity = appointment_type._get_resources_remaining_capacity(self.resource_1, start, end)
        self.assertEqual(
            remaining_capacity["total_remaining_capacity"],
            1,
            "Remaining capacity should be 1 after first booking",
        )

        # Book 2 out of 2 allowed resource bookings
        response = self.url_open(url, data=booking_data)
        self.assertEqual(response.status_code, 200, "Second booking should be successful")

        remaining_capacity = appointment_type._get_resources_remaining_capacity(self.resource_1, start, end)
        self.assertEqual(
            remaining_capacity["total_remaining_capacity"],
            0,
            "Remaining capacity should be 0 after second booking",
        )

        overbooking_data = {
            "csrf_token": http.Request.csrf_token(self),
            "datetime_str": start,
            "duration_str": "1.0",
            "email": "user2@example.com",
            "name": "User 2",
            "phone": "0987654321",
            "available_resource_ids": self.resource_1.id,
        }

        # Attempt to overbook (3rd booking) -> should be rejected
        response = self.url_open(url, data=overbooking_data)
        self.assertEqual(response.status_code, 200, "Overbooking should trigger a redirect")

        expected_redirect_url = f"/appointment/{appointment_type.id}?state=failed-resource"
        self.assertIn(
            expected_redirect_url,
            response.url,
            "Redirect should indicate failed booking due to full resource capacity",
        )

        remaining_capacity_after = appointment_type._get_resources_remaining_capacity(self.resource_1, start, end)
        self.assertEqual(
            remaining_capacity_after["total_remaining_capacity"],
            0,
            "Remaining capacity should remain 0 after failed overbooking",
        )

    def test_appointment_resource_booking_for_multi_seats(self):
        appointment_type = self.env["appointment.type"].create(
            {
                "name": "Multi-seats Appointment",
                "appointment_tz": "UTC",
                "min_schedule_hours": 1.0,
                "max_schedule_days": 7,
                "capacity_type": "multiple_seats",
                "schedule_based_on": "resources",
                "resource_ids": [(6, 0, [self.resource_2.id])],
                "slot_ids": [
                    (
                        0,
                        0,
                        {
                            "weekday": str(self.reference_date.isoweekday()),
                            "start_hour": 10,
                            "end_hour": 18,
                        },
                    )
                ],
            }
        )

        start = datetime(2025, 4, 1, 15, 0, 0)
        end = start + timedelta(hours=1)

        self.authenticate(self.staff_user.login, self.staff_user.login)

        # Book 2 out of 4 available seats
        booking_data = {
            "csrf_token": http.Request.csrf_token(self),
            "datetime_str": start,
            "duration_str": "1.0",
            "email": "testuser@example.com",
            "name": "John Doe",
            "phone": "1234567890",
            "available_resource_ids": self.resource_2.id,
            "asked_capacity": 2,
        }

        url = f"/appointment/{appointment_type.id}/submit"
        response = self.url_open(url, data=booking_data)
        self.assertEqual(response.status_code, 200, "First booking should be successful")

        remaining_capacity = appointment_type._get_resources_remaining_capacity(self.resource_2, start, end)
        self.assertEqual(
            remaining_capacity["total_remaining_capacity"],
            2,
            "Remaining capacity should be 1 after first booking",
        )

        # Book 1 more seat (total 3/4 booked)
        booking_data["asked_capacity"] = 1
        response = self.url_open(url, data=booking_data)
        self.assertEqual(response.status_code, 200, "Second booking should be successful")

        remaining_capacity = appointment_type._get_resources_remaining_capacity(self.resource_2, start, end)
        self.assertEqual(
            remaining_capacity["total_remaining_capacity"],
            1,
            "Remaining capacity should be 0 after second booking",
        )

        # Try to book 3 seats (overbooking attempt)
        overbooking_data = {
            "csrf_token": http.Request.csrf_token(self),
            "datetime_str": start,
            "duration_str": "1.0",
            "email": "user2@example.com",
            "name": "User 2",
            "phone": "0987654321",
            "available_resource_ids": self.resource_2.id,
            "asked_capacity": 3,
        }

        response = self.url_open(url, data=overbooking_data)
        self.assertEqual(response.status_code, 200, "Overbooking should trigger a redirect")

        expected_redirect_url = f"/appointment/{appointment_type.id}?state=failed-resource"
        self.assertIn(
            expected_redirect_url,
            response.url,
            "Redirect should indicate failed booking due to full resource capacity",
        )

        remaining_capacity_after = appointment_type._get_resources_remaining_capacity(self.resource_2, start, end)
        self.assertEqual(
            remaining_capacity_after["total_remaining_capacity"],
            1,
            "Remaining capacity should remain 1 after failed overbooking",
        )

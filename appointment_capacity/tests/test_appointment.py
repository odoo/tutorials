from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from datetime import datetime, timedelta

@tagged('-at_install', 'post_install')
class TestAppointmentCapacity(TransactionCase):

    @classmethod
    def setUpClass(cls):
        """ Set up data for all test cases """
        super().setUpClass()
        cls.reference_monday = datetime(2022, 2, 14, 7, 0, 0)
        cls._test_context = {'tracking_disable': True}  # Example context
        appointments = cls.env['appointment.type'].create([{
            'appointment_tz': 'UTC',
            'min_schedule_hours': 1.0,
            'max_schedule_days': 8,
            'name': 'Managed Test',
            'resource_capacity': 'multi_seat',
            'schedule_based_on': 'resources',
            'slot_ids': [(0, 0, {
                'weekday': str(cls.reference_monday.isoweekday()),
                'start_hour': 6,
                'end_hour': 18,
            })],
        }, {
            'appointment_tz': 'UTC',
            'min_schedule_hours': 1.0,
            'max_schedule_days': 8,
            'name': 'Unmanaged Test',
            'resource_capacity': 'multi_seat',
            'schedule_based_on': 'resources',
            'slot_ids': [(0, 0, {
                'weekday': str(cls.reference_monday.isoweekday()),
                'start_hour': 6,
                'end_hour': 18,
            })],
        }])
        
        cls.appointment_manage_capacity = appointments[0]
        cls.appointment_regular = appointments[1]
        
        resources = cls.env['appointment.resource'].create([{
            'appointment_type_ids': [(4, cls.appointment_manage_capacity.id)],
            'capacity': 3,
            'name': 'Resource 1',
        }, {
            'appointment_type_ids': [(4, cls.appointment_manage_capacity.id)],
            'capacity': 2,
            'name': 'Resource 2',
            'shareable': True,
        }, {
            'appointment_type_ids': [(4, cls.appointment_manage_capacity.id), (4, cls.appointment_regular.id)],
            'capacity': 1,
            'name': 'Resource 3',
        }])
        
        cls.resource_1 = resources[0]
        cls.resource_2 = resources[1]
        cls.resource_3 = resources[2]
        # Create users (appointment staff)
        cls.staff_user_aust = cls.env['res.users'].create({
            'name': 'Aust User',
            'login': 'aust@example.com',
        })
        
        cls.staff_user_bxls = cls.env['res.users'].create({
            'name': 'Bxls User',
            'login': 'bxls@example.com',
        })

        # Ensure users have partners
        cls.staff_user_aust.partner_id = cls.env['res.partner'].create({'name': 'Aust Partner'})
        cls.staff_user_bxls.partner_id = cls.env['res.partner'].create({'name': 'Bxls Partner'})

        # Define a reference Monday
        cls.reference_monday = datetime(2025, 3, 17)  # Example: March 17, 2025 (Monday)

        # Create appointment type
        cls.apt_type_manage_capacity_users = cls.env['appointment.type'].create({
            'appointment_tz': 'Europe/Brussels',
            'appointment_duration': 1,
            'assign_method': 'time_resource',
            'category': 'recurring',
            'location_id': cls.staff_user_bxls.partner_id.id,
            'name': 'Bxls Appt Type with capacity',
            'max_schedule_days': 15,
            'min_cancellation_hours': 1,
            'schedule_based_on': 'users',
            'resource_capacity': 'multi_seat',
            'min_schedule_hours': 1,
            'staff_user_ids': [(6, 0, [cls.staff_user_aust.id, cls.staff_user_bxls.id])],
            'slot_ids': [(0, 0, {
                'weekday': str(cls.reference_monday.isoweekday()),
                'start_hour': 15,
                'end_hour': 16,
            })],
            'capacity_count': 5,
        })

    def test_appointment_user_remaining_capacity(self):
        """ Test that the remaining capacity of users is correctly computed """
        appointment = self.apt_type_manage_capacity_users
        user_1 = self.staff_user_aust
        user_2 = self.staff_user_bxls

        start = datetime(2025, 3, 21, 14, 0, 0)
        end = start + timedelta(hours=1)

        # Get initial capacities
        user_1_remaining_capacity = appointment._get_users_remaining_capacity(user_1, start, end)['total_remaining_capacity']
        user_2_remaining_capacity = appointment._get_users_remaining_capacity(user_2, start, end)['total_remaining_capacity']

        self.assertEqual(user_1_remaining_capacity, 5, "User 1 should start with 5 available slots.")
        self.assertEqual(user_2_remaining_capacity, 5, "User 2 should start with 5 available slots.")

        # Create bookings for users
        booking_1 = self.env['calendar.event'].create({
            'appointment_type_id': appointment.id,
            'booking_line_ids': [(0, 0, {'appointment_user_id': user_1.id, 'capacity_reserved': 2, 'capacity_used': 2})],
            'name': 'Booking 1',
            'start': start,
            'stop': end,
        })

        booking_2 = self.env['calendar.event'].create({
            'appointment_type_id': appointment.id,
            'booking_line_ids': [(0, 0, {'appointment_user_id': user_2.id, 'capacity_reserved': 1})],
            'name': 'Booking 2',
            'start': start,
            'stop': end,
        })

        # Get capacities after booking
        user_1_remaining_capacity = appointment._get_users_remaining_capacity(user_1, start, end)['total_remaining_capacity']
        user_2_remaining_capacity = appointment._get_users_remaining_capacity(user_2, start, end)['total_remaining_capacity']

        self.assertEqual(user_1_remaining_capacity, 3, "User 1 should have 3 slots left after booking 2.")
        self.assertEqual(user_2_remaining_capacity, 4, "User 2 should have 4 slots left after booking 1.")

        # Delete bookings
        (booking_1 + booking_2).unlink()

        # Check if capacity resets correctly
        user_1_remaining_capacity = appointment._get_users_remaining_capacity(user_1, start, end)['total_remaining_capacity']
        user_2_remaining_capacity = appointment._get_users_remaining_capacity(user_2, start, end)['total_remaining_capacity']

        self.assertEqual(user_1_remaining_capacity, 5, "User 1 should regain full capacity after deleting bookings.")
        self.assertEqual(user_2_remaining_capacity, 5, "User 2 should regain full capacity after deleting bookings.")


    
    def test_appointment_resources_remaining_capacity(self):
        """ Test that the remaining capacity of resources are correctly computed """
        appointment = self.appointment_manage_capacity
        resource_1 = self.resource_1
        resource_2 = self.resource_2

        start = datetime(2022, 2, 15, 14, 0, 0)
        end = start + timedelta(hours=1)

        self.assertEqual(appointment._get_resources_remaining_capacity(resource_1, start, end)['total_remaining_capacity'], 3)
        self.assertEqual(appointment._get_resources_remaining_capacity(resource_2, start, end)['total_remaining_capacity'], 2)

        # Create bookings for resource
        booking_1, booking_2 = self.env['calendar.event'].with_context(self._test_context).create([{
            'appointment_type_id': appointment.id,
            'booking_line_ids': [(0, 0, {'appointment_resource_id': resource_1.id, 'capacity_reserved': 3, 'capacity_used': resource_1.capacity})],
            'name': 'Booking 1',
            'start': start,
            'stop': end,
        }, {
            'appointment_type_id': appointment.id,
            'booking_line_ids': [(0, 0, {'appointment_resource_id': resource_2.id, 'capacity_reserved': 1})],
            'name': 'Booking 2',
            'start': start,
            'stop': end,
        }])
        bookings = booking_1 + booking_2

        self.assertEqual(appointment._get_resources_remaining_capacity(resource_1, start, end)['total_remaining_capacity'], 0)
        self.assertEqual(appointment._get_resources_remaining_capacity(resource_2, start, end)['total_remaining_capacity'], 1)

        bookings.unlink()
        resource_1.appointment_type_ids = [(4, self.appointment_manage_capacity.id)]
        self.assertEqual(appointment._get_resources_remaining_capacity(resource_1, start, end)['total_remaining_capacity'], 3)
        self.assertEqual(appointment._get_resources_remaining_capacity(resource_2, start, end)['total_remaining_capacity'], 2)
        self.assertEqual(appointment._get_resources_remaining_capacity(resource_1, start, end)[resource_1], 3)
        self.assertEqual(appointment._get_resources_remaining_capacity(resource_2, start, end)[resource_2], 2)

        booking = self.env['calendar.event'].with_context(self._test_context).create([{
            'appointment_type_id': appointment.id,
            'booking_line_ids': [
                (0, 0, {'appointment_resource_id': resource_1.id, 'capacity_reserved': 3, 'capacity_used': 3}),
                (0, 0, {'appointment_resource_id': resource_2.id, 'capacity_reserved': 1}),
            ],
            'name': 'Booking',
            'start': start,
            'stop': end,
        }])

        self.assertEqual(len(booking.appointment_resource_ids), 2)
        self.assertEqual(appointment._get_resources_remaining_capacity(resource_1, start, end)['total_remaining_capacity'], 0)
        self.assertEqual(appointment._get_resources_remaining_capacity(resource_1, start, end)[resource_1], 0)
        self.assertEqual(appointment._get_resources_remaining_capacity(resource_2, start, end)['total_remaining_capacity'], 1)

        self.assertDictEqual(
            appointment._get_resources_remaining_capacity(self.env['appointment.resource'], start, end),
            {'total_remaining_capacity': 0},
        )

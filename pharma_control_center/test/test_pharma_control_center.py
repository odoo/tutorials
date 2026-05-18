from datetime import date, timedelta
from odoo.tests import TransactionCase


class TestPharmaControlCenter(TransactionCase):

    def setUp(self):
        super(TestPharmaControlCenter, self).setUp()

        # Create test user
        self.test_user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'test@example.com',
            'email': 'test@example.com',
        })

        # Create test category
        self.test_category = self.env['pharmacy.category'].create({
            'name': 'Test Category',
        })

        # Create pharma control center record
        self.control_center = self.env['pharma.control.center'].create({
            'user_id': self.test_user.id,
            'display_name': 'Test User',
            'email': 'test@example.com',
            'phone': '+1234567890',
        })

    def test_pharma_control_center_creation(self):
        """Test creating a pharma control center record"""
        self.assertEqual(self.control_center.display_name, 'Test User')
        self.assertEqual(self.control_center.email, 'test@example.com')
        self.assertEqual(self.control_center.phone, '+1234567890')
        self.assertEqual(self.control_center.user_id, self.test_user)

    def test_profile_sync_on_create(self):
        """Test that user profile is synced when creating control center"""
        # Check that user and partner were updated
        self.assertEqual(self.test_user.name, 'Test User')
        self.assertEqual(self.test_user.email, 'test@example.com')
        self.assertEqual(self.test_user.partner_id.name, 'Test User')
        self.assertEqual(self.test_user.partner_id.email, 'test@example.com')
        self.assertEqual(self.test_user.partner_id.phone, '+1234567890')

    def test_profile_sync_on_write(self):
        """Test that user profile is synced when updating control center"""
        self.control_center.write({
            'display_name': 'Updated Name',
            'email': 'updated@example.com',
            'phone': '+0987654321',
        })

        # Check that user and partner were updated
        self.assertEqual(self.test_user.name, 'Updated Name')
        self.assertEqual(self.test_user.email, 'updated@example.com')
        self.assertEqual(self.test_user.partner_id.name, 'Updated Name')
        self.assertEqual(self.test_user.partner_id.email, 'updated@example.com')
        self.assertEqual(self.test_user.partner_id.phone, '+0987654321')

    def test_statistics_computation(self):
        """Test statistics computation"""
        # Create test medicines
        future_date = date.today() + timedelta(days=60)
        past_date = date.today() - timedelta(days=1)

        medicine1 = self.env['pharmacy.medicine'].create({
            'name': 'Test Medicine 1',
            'category_id': self.test_category.id,
            'batch_number': 'BATCH001',
            'expiry_date': future_date,
            'price': 10.0,
            'cost_price': 8.0,
            'quantity': 50,
            'storage_location': 'room_temp',
            'license_category': 'white',
        })

        medicine2 = self.env['pharmacy.medicine'].create({
            'name': 'Test Medicine 2',
            'category_id': self.test_category.id,
            'batch_number': 'BATCH002',
            'expiry_date': past_date,  # Expired
            'price': 20.0,
            'cost_price': 15.0,
            'quantity': 0,  # Out of stock
            'storage_location': 'cold',
            'license_category': 'green',
        })

        # Create test patient
        patient = self.env['pharmacy.patient'].create({
            'name': 'Test Patient',
            'doctor_id': self.test_user.id,
            'age': 30,
            'gender': 'male',
            'phone': '+1234567890',
            'email': 'patient@example.com',
        })

        # Force computation of statistics
        self.control_center._compute_statistics()

        # Check medicine statistics
        self.assertEqual(self.control_center.total_medicines, 2)
        self.assertEqual(self.control_center.total_stock_quantity, 50)
        self.assertEqual(self.control_center.stock_value, 500.0)  # 50 * 10
        self.assertEqual(self.control_center.out_of_stock_count, 1)
        self.assertEqual(self.control_center.expired_count, 1)

        # Check patient statistics
        self.assertEqual(self.control_center.total_patients, 1)


class TestPharmacyMedicine(TransactionCase):

    def setUp(self):
        super(TestPharmacyMedicine, self).setUp()

        # Create test category
        self.test_category = self.env['pharmacy.category'].create({
            'name': 'Test Category',
        })

    def test_medicine_creation(self):
        """Test creating a medicine"""
        future_date = date.today() + timedelta(days=365)

        medicine = self.env['pharmacy.medicine'].create({
            'name': 'Aspirin',
            'description': 'Pain reliever',
            'manufacturer': 'Test Pharma',
            'category_id': self.test_category.id,
            'batch_number': 'ASP001',
            'expiry_date': future_date,
            'price': 5.50,
            'cost_price': 3.00,
            'quantity': 100,
            'reorder_level': 20,
            'storage_location': 'room_temp',
            'license_category': 'white',
            'dosage': '500mg',
        })

        self.assertEqual(medicine.name, 'Aspirin')
        self.assertEqual(medicine.quantity, 100)
        self.assertEqual(medicine.in_stock, True)
        self.assertEqual(medicine.need_reorder, False)

    def test_profit_margin_computation(self):
        """Test profit margin calculation"""
        future_date = date.today() + timedelta(days=365)

        medicine = self.env['pharmacy.medicine'].create({
            'name': 'Test Medicine',
            'category_id': self.test_category.id,
            'batch_number': 'TEST001',
            'expiry_date': future_date,
            'price': 10.0,
            'cost_price': 8.0,
            'quantity': 50,
            'storage_location': 'room_temp',
            'license_category': 'white',
        })

        # Profit margin = ((10 - 8) / 8) * 100 = 25%
        self.assertEqual(medicine.profit_margin, 25.0)

    def test_expiry_status_computation(self):
        """Test expiry status computation"""
        today = date.today()
        future_date = today + timedelta(days=60)  # Fresh
        soon_date = today + timedelta(days=15)    # Expiring soon
        past_date = today - timedelta(days=1)     # Expired

        # Fresh medicine
        fresh_med = self.env['pharmacy.medicine'].create({
            'name': 'Fresh Medicine',
            'category_id': self.test_category.id,
            'batch_number': 'FRESH001',
            'expiry_date': future_date,
            'price': 10.0,
            'quantity': 10,
            'storage_location': 'room_temp',
            'license_category': 'white',
        })

        # Expiring soon medicine
        expiring_med = self.env['pharmacy.medicine'].create({
            'name': 'Expiring Medicine',
            'category_id': self.test_category.id,
            'batch_number': 'EXP001',
            'expiry_date': soon_date,
            'price': 10.0,
            'quantity': 10,
            'storage_location': 'room_temp',
            'license_category': 'white',
        })

        # Expired medicine
        expired_med = self.env['pharmacy.medicine'].create({
            'name': 'Expired Medicine',
            'category_id': self.test_category.id,
            'batch_number': 'EXPD001',
            'expiry_date': past_date,
            'price': 10.0,
            'quantity': 10,
            'storage_location': 'room_temp',
            'license_category': 'white',
        })

        self.assertEqual(fresh_med.expiry_status, 'fresh')
        self.assertEqual(expiring_med.expiry_status, 'expiring_soon')
        self.assertEqual(expired_med.expiry_status, 'expired')

    def test_reorder_computation(self):
        """Test reorder level computation"""
        future_date = date.today() + timedelta(days=365)

        # Medicine above reorder level
        medicine_ok = self.env['pharmacy.medicine'].create({
            'name': 'OK Medicine',
            'category_id': self.test_category.id,
            'batch_number': 'OK001',
            'expiry_date': future_date,
            'price': 10.0,
            'quantity': 50,
            'reorder_level': 20,
            'storage_location': 'room_temp',
            'license_category': 'white',
        })

        # Medicine at reorder level
        medicine_reorder = self.env['pharmacy.medicine'].create({
            'name': 'Reorder Medicine',
            'category_id': self.test_category.id,
            'batch_number': 'REORDER001',
            'expiry_date': future_date,
            'price': 10.0,
            'quantity': 20,
            'reorder_level': 20,
            'storage_location': 'room_temp',
            'license_category': 'white',
        })

        # Medicine below reorder level
        medicine_low = self.env['pharmacy.medicine'].create({
            'name': 'Low Medicine',
            'category_id': self.test_category.id,
            'batch_number': 'LOW001',
            'expiry_date': future_date,
            'price': 10.0,
            'quantity': 10,
            'reorder_level': 20,
            'storage_location': 'room_temp',
            'license_category': 'white',
        })

        self.assertEqual(medicine_ok.need_reorder, False)
        self.assertEqual(medicine_reorder.need_reorder, True)
        self.assertEqual(medicine_low.need_reorder, True)


class TestPharmacyPatient(TransactionCase):

    def setUp(self):
        super(TestPharmacyPatient, self).setUp()

        # Create test doctor
        self.test_doctor = self.env['res.users'].create({
            'name': 'Dr. Test',
            'login': 'doctor@example.com',
            'email': 'doctor@example.com',
        })

    def test_patient_creation(self):
        """Test creating a patient"""
        patient = self.env['pharmacy.patient'].create({
            'name': 'John Doe',
            'doctor_id': self.test_doctor.id,
            'age': 35,
            'gender': 'male',
            'phone': '+1234567890',
            'email': 'john@example.com',
            'blood_group': 'A+',
            'medical_history': 'Hypertension',
            'allergies': 'Penicillin',
        })

        self.assertEqual(patient.name, 'John Doe')
        self.assertEqual(patient.doctor_id, self.test_doctor)
        self.assertEqual(patient.age, 35)
        self.assertEqual(patient.gender, 'male')
        self.assertEqual(patient.blood_group, 'A+')
        self.assertEqual(patient.active, True)

    def test_unique_email_constraint(self):
        """Test unique email constraint"""
        # Create first patient
        self.env['pharmacy.patient'].create({
            'name': 'Patient 1',
            'doctor_id': self.test_doctor.id,
            'email': 'unique@example.com',
        })

        # Try to create second patient with same email - should raise error
        with self.assertRaises(Exception):
            self.env['pharmacy.patient'].create({
                'name': 'Patient 2',
                'doctor_id': self.test_doctor.id,
                'email': 'unique@example.com',
            })

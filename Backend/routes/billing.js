const express = require('express');
const router = express.Router();
const BillingController = require('../controllers/billingController');
const auth = require('../middleware/auth');

// Patient names endpoint (open access for now)
router.get('/patient-names', BillingController.getPatientNames);

// Invoice endpoints
router.post('/invoices', BillingController.createInvoice);
router.get('/invoices', BillingController.getInvoices);
router.get('/invoices/:invoiceId', BillingController.getInvoiceById);
router.patch('/invoices/:invoiceId/status', BillingController.updateInvoiceStatus);

// Unpaid appointments
router.get('/patients/:patientId/unpaid-appointments', BillingController.getUnpaidAppointments);
router.post('/appointments/:appointmentId/pay', BillingController.payAppointment);

module.exports = router;

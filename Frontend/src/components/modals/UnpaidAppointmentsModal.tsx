import React, { useState, useEffect, useMemo } from 'react';
import Modal from '../ui/Modal';
import Button from '../ui/Button';
import Input from '../ui/Input';
import { SearchIcon, DollarSignIcon, CheckCircleIcon, ClockIcon } from 'lucide-react';
import { apiService } from '../../services/api';
import { toast } from 'sonner';

interface UnpaidAppointmentsModalProps {
    isOpen: boolean;
    onClose: () => void;
}

const UnpaidAppointmentsModal: React.FC<UnpaidAppointmentsModalProps> = ({
    isOpen,
    onClose
}) => {
    const [patients, setPatients] = useState<any[]>([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedPatient, setSelectedPatient] = useState<any | null>(null);
    const [unpaidAppointments, setUnpaidAppointments] = useState<any[]>([]);
    const [loadingPatients, setLoadingPatients] = useState(false);
    const [loadingAppointments, setLoadingAppointments] = useState(false);
    const [payingId, setPayingId] = useState<string | null>(null);

    useEffect(() => {
        if (isOpen) {
            fetchPatients();
        } else {
            // Reset state on close
            setSearchTerm('');
            setSelectedPatient(null);
            setUnpaidAppointments([]);
        }
    }, [isOpen]);

    const fetchPatients = async () => {
        setLoadingPatients(true);
        try {
            const response = await apiService.getPatientNames();
            if (response.success && response.data) {
                setPatients(response.data);
            }
        } catch (error) {
            console.error('Error fetching patients:', error);
            toast.error('Failed to load patients.');
        } finally {
            setLoadingPatients(false);
        }
    };

    const fetchUnpaidAppointments = async (patientId: string) => {
        setLoadingAppointments(true);
        try {
            const response = await apiService.getUnpaidAppointments(patientId);
            if (response.success && response.data) {
                setUnpaidAppointments(response.data);
            }
        } catch (error) {
            console.error('Error fetching unpaid appointments:', error);
            toast.error('Failed to load appointments.');
        } finally {
            setLoadingAppointments(false);
        }
    };

    const handlePatientSelect = (patient: any) => {
        setSelectedPatient(patient);
        setSearchTerm(''); // clear search when selected to clean up UI
        fetchUnpaidAppointments(patient.id);
    };

    const handlePay = async (appointmentId: string) => {
        setPayingId(appointmentId);
        try {
            const response = await apiService.payAppointment(appointmentId);
            if (response.success) {
                toast.success('Appointment marked as paid!');
                // Remove the paid appointment from the list
                setUnpaidAppointments(prev => prev.filter(app => app.id !== appointmentId));
            } else {
                toast.error(response.message || 'Failed to process payment');
            }
        } catch (error) {
            console.error('Error paying appointment:', error);
            toast.error('Payment failed');
        } finally {
            setPayingId(null);
        }
    };

    const filteredPatients = useMemo(() => {
        if (!searchTerm) return [];
        const lowerTerm = searchTerm.toLowerCase();
        return patients.filter(p => 
            p.name?.toLowerCase().includes(lowerTerm) || 
            p.patientCode?.toLowerCase().includes(lowerTerm) || 
            p.email?.toLowerCase().includes(lowerTerm)
        ).slice(0, 5); // show max 5 suggestions
    }, [searchTerm, patients]);

    return (
        <Modal isOpen={isOpen} onClose={onClose} title="Settle Unpaid Appointments">
            <div className="space-y-6">
                
                {/* Patient Selection Segment */}
                {!selectedPatient ? (
                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-2">
                            Search Patient
                        </label>
                        <div className="relative">
                            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <SearchIcon className="h-5 w-5 text-gray-400" />
                            </div>
                            <Input
                                placeholder="Search by name, ID, or email..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                className="pl-10"
                            />
                        </div>
                        {loadingPatients ? (
                            <p className="mt-2 text-sm text-gray-500 text-center">Loading registry...</p>
                        ) : (
                            filteredPatients.length > 0 && (
                                <ul className="mt-2 bg-white border border-gray-200 rounded-md shadow-sm max-h-60 overflow-y-auto">
                                    {filteredPatients.map(patient => (
                                        <li 
                                            key={patient.id}
                                            onClick={() => handlePatientSelect(patient)}
                                            className="px-4 py-2 hover:bg-blue-50 cursor-pointer border-b last:border-0 border-gray-100 transition-colors"
                                        >
                                            <div className="font-medium text-gray-900">{patient.name || patient.email}</div>
                                            {patient.patientCode && <div className="text-xs text-gray-500">ID: {patient.patientCode}</div>}
                                        </li>
                                    ))}
                                </ul>
                            )
                        )}
                        {searchTerm && filteredPatients.length === 0 && !loadingPatients && (
                            <p className="mt-2 text-sm text-gray-500 text-center">No patients found matching "{searchTerm}"</p>
                        )}
                    </div>
                ) : (
                    <div className="space-y-4">
                        <div className="flex items-center justify-between bg-slate-50 p-4 rounded-lg border border-slate-100">
                            <div>
                                <p className="text-sm text-slate-500">Selected Patient</p>
                                <p className="font-semibold text-slate-900">{selectedPatient.name}</p>
                                <p className="text-xs text-slate-500">{selectedPatient.patientCode || selectedPatient.email}</p>
                            </div>
                            <Button variant="outline" size="sm" onClick={() => setSelectedPatient(null)}>
                                Change
                            </Button>
                        </div>

                        {/* Appointments List */}
                        <div>
                            <h3 className="text-sm font-semibold text-slate-800 mb-3 flex items-center">
                                <ClockIcon className="w-4 h-4 mr-2" />
                                Pending Unpaid Appointments
                            </h3>
                            
                            {loadingAppointments ? (
                                <div className="text-center py-6 text-slate-500">Finding records...</div>
                            ) : unpaidAppointments.length === 0 ? (
                                <div className="text-center py-8 bg-gray-50 rounded-lg border border-dashed border-gray-200">
                                    <CheckCircleIcon className="w-8 h-8 text-green-500 mx-auto mb-2" />
                                    <p className="text-sm font-medium text-gray-900">All Clear</p>
                                    <p className="text-xs text-gray-500">No unpaid appointments for this patient.</p>
                                </div>
                            ) : (
                                <div className="space-y-3">
                                    {unpaidAppointments.map(appt => (
                                        <div key={appt.id} className="flex justify-between items-center p-4 bg-white border border-gray-200 rounded-lg shadow-sm hover:border-blue-300 transition-colors">
                                            <div>
                                                <div className="font-medium text-slate-900 text-sm">
                                                    {new Date(appt.appointment_date).toLocaleDateString()} at {appt.appointment_time}
                                                </div>
                                                <div className="text-xs text-slate-500 mt-1">
                                                    Consultation with Dr. {appt.doctor_first_name} {appt.doctor_last_name}
                                                </div>
                                                <div className="text-xs text-slate-500">
                                                    Purpose: {appt.reason_for_visit}
                                                </div>
                                                <div className="text-xs font-semibold text-blue-600 mt-1">
                                                    Fee: Rs. {appt.consultation_fee || '0.00'}
                                                </div>
                                            </div>
                                            <Button 
                                                variant="primary" 
                                                size="sm" 
                                                onClick={() => handlePay(appt.id)}
                                                disabled={payingId === appt.id}
                                                className="shrink-0 ml-4"
                                            >
                                                {payingId === appt.id ? 'Processing...' : (
                                                    <><DollarSignIcon className="w-4 h-4 mr-1"/> Pay</>
                                                )}
                                            </Button>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </div>
            
            {/* Modal Actions */}
            <div className="mt-8 flex justify-end gap-3 pt-5 border-t border-slate-100">
                <Button variant="outline" onClick={onClose}>
                    Close
                </Button>
            </div>
        </Modal>
    );
};

export default UnpaidAppointmentsModal;
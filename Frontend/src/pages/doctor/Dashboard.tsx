import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { CalendarIcon, UsersIcon, ClockIcon, Brain, ArrowRight } from 'lucide-react';

const ActionCard = ({ title, description, icon: Icon, onClick }: any) => {
  return (
    <div onClick={onClick} className="group bg-white border-2 border-slate-200 shadow-[0_4px_24px_rgba(0,0,0,0.06)] rounded-2xl p-6 hover:border-blue-400 hover:shadow-[0_8px_32px_rgba(0,0,0,0.12)] hover:-translate-y-1 transition-all duration-300 cursor-pointer flex flex-col justify-between h-full">
      <div>
        <div className="w-10 h-10 rounded-xl bg-slate-50 flex items-center justify-center mb-5 group-hover:bg-blue-50 group-hover:text-blue-600 text-slate-600 transition-colors">
          <Icon className="h-5 w-5" strokeWidth={2} />
        </div>
        <h3 className="text-base font-semibold text-slate-900 mb-2">{title}</h3>
        <p className="text-sm text-slate-500 leading-relaxed">{description}</p>
      </div>
      <div className="mt-5 flex items-center text-sm font-medium text-blue-600 opacity-0 group-hover:opacity-100 transition-all -translate-x-2 group-hover:translate-x-0 duration-300">
        Access module <ArrowRight className="ml-1.5 w-4 h-4" />
      </div>
    </div>
  );
};

const DoctorDashboard: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuthStore();

  const actions = [
    { title: 'Appointments', description: 'Manage clinical schedule and upcoming consultancies.', icon: CalendarIcon, onClick: () => navigate('/doctor/appointments') },
    { title: 'My Patients', description: 'Review patient records and clinical histories thoroughly.', icon: UsersIcon, onClick: () => navigate('/doctor/patients') },
    { title: 'Current Queue', description: 'Monitor physical wait lines and live appointment statuses.', icon: ClockIcon, onClick: () => navigate('/doctor/queue') },
    { title: 'Diagnostic AI', description: 'Leverage predictive tools to assist disease screening.', icon: Brain, onClick: () => navigate('/doctor/ai-predictions') }
  ];

  return (
    <div className="bg-transparent text-slate-900 w-full font-sans relative pb-12">
      <div className="max-w-6xl mx-auto space-y-8 mt-4">
        <div className="flex flex-col gap-2 pb-6 border-b border-slate-100">
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
            Welcome, Dr. {user?.name?.split(' ').pop() || 'Physician'}
          </h1>
          <p className="text-slate-500 text-sm">
            Quickly navigate schedules, review clinical data, and connect with patient care streams.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {actions.map((action, idx) => <ActionCard key={idx} {...action} />)}
        </div>
      </div>
    </div>
  );
};

export default DoctorDashboard;

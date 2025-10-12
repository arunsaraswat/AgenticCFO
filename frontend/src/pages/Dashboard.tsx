/**
 * Dashboard page component.
 */
import React, { useState, useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';
import AuthService from '@/services/authService';
import { DashboardData } from '@/types';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import Header from '@/components/layout/Header';

/**
 * Dashboard page with user stats and information.
 */
const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const data = await AuthService.getDashboardData();
        setDashboardData(data);
      } catch (err) {
        setError('Failed to load dashboard data');
        console.error('Dashboard error:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (isLoading) {
    return (
      <>
        <Header />
        <LoadingSpinner text="Loading dashboard..." />
      </>
    );
  }

  if (error) {
    return (
      <>
        <Header />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Header />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Message */}
        <div className="bg-white shadow rounded-lg p-6 mb-6">
          <h1 className="text-3xl font-bold text-gray-900">
            {dashboardData?.message || `Welcome, ${user?.full_name}!`}
          </h1>
          <p className="mt-2 text-gray-600">
            Here's an overview of your activity
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {dashboardData?.stats && Object.entries(dashboardData.stats).map(([key, value]) => (
            <div
              key={key}
              className="bg-white shadow rounded-lg p-6 hover:shadow-lg transition-shadow"
            >
              <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide">
                {key.replace(/_/g, ' ')}
              </h3>
              <p className="mt-2 text-3xl font-bold text-primary-600">{value}</p>
            </div>
          ))}
        </div>

        {/* User Info Card */}
        <div className="mt-6 bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Account Information</h2>
          <dl className="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
            <div>
              <dt className="text-sm font-medium text-gray-500">Email</dt>
              <dd className="mt-1 text-sm text-gray-900">{user?.email}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Full Name</dt>
              <dd className="mt-1 text-sm text-gray-900">{user?.full_name}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Account Status</dt>
              <dd className="mt-1">
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  {user?.is_active ? 'Active' : 'Inactive'}
                </span>
              </dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Member Since</dt>
              <dd className="mt-1 text-sm text-gray-900">
                {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
              </dd>
            </div>
          </dl>
        </div>
      </div>
    </>
  );
};

export default Dashboard;

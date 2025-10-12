/**
 * User profile page component.
 */
import React, { useState, useEffect } from 'react';
import AuthService from '@/services/authService';
import { UserProfile } from '@/types';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import Header from '@/components/layout/Header';

/**
 * Profile page displaying detailed user information.
 */
const Profile: React.FC = () => {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await AuthService.getProfile();
        setProfile(data);
      } catch (err) {
        setError('Failed to load profile');
        console.error('Profile error:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProfile();
  }, []);

  if (isLoading) {
    return (
      <>
        <Header />
        <LoadingSpinner text="Loading profile..." />
      </>
    );
  }

  if (error || !profile) {
    return (
      <>
        <Header />
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error || 'Profile not found'}
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Header />
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white shadow rounded-lg">
          {/* Profile Header */}
          <div className="px-6 py-8 border-b border-gray-200">
            <div className="flex items-center">
              <div className="flex-shrink-0 h-20 w-20 rounded-full bg-primary-600 flex items-center justify-center">
                <span className="text-3xl font-bold text-white">
                  {profile.full_name.charAt(0).toUpperCase()}
                </span>
              </div>
              <div className="ml-6">
                <h1 className="text-2xl font-bold text-gray-900">{profile.full_name}</h1>
                <p className="text-gray-600">{profile.email}</p>
              </div>
            </div>
          </div>

          {/* Profile Details */}
          <div className="px-6 py-8">
            <h2 className="text-lg font-bold text-gray-900 mb-6">Profile Details</h2>
            <dl className="space-y-6">
              <div>
                <dt className="text-sm font-medium text-gray-500">User ID</dt>
                <dd className="mt-1 text-sm text-gray-900">{profile.id}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Email Address</dt>
                <dd className="mt-1 text-sm text-gray-900">{profile.email}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Full Name</dt>
                <dd className="mt-1 text-sm text-gray-900">{profile.full_name}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Account Status</dt>
                <dd className="mt-1">
                  <span
                    className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      profile.is_active
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {profile.is_active ? 'Active' : 'Inactive'}
                  </span>
                </dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Role</dt>
                <dd className="mt-1">
                  <span
                    className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      profile.is_superuser
                        ? 'bg-purple-100 text-purple-800'
                        : 'bg-blue-100 text-blue-800'
                    }`}
                  >
                    {profile.is_superuser ? 'Admin' : 'User'}
                  </span>
                </dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Account Created</dt>
                <dd className="mt-1 text-sm text-gray-900">
                  {new Date(profile.created_at).toLocaleString()}
                </dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Last Updated</dt>
                <dd className="mt-1 text-sm text-gray-900">
                  {new Date(profile.updated_at).toLocaleString()}
                </dd>
              </div>
            </dl>
          </div>
        </div>
      </div>
    </>
  );
};

export default Profile;

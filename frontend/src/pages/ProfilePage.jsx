import { useState, useEffect } from 'react';
import { useAuthStore } from '../store/authStore';
import { HiOutlineUser, HiOutlineMail, HiOutlinePencil, HiOutlineCheck } from 'react-icons/hi';

export default function ProfilePage() {
  const { user, fetchUser, updateUser } = useAuthStore();
  const [fullName, setFullName] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  useEffect(() => {
    if (user) {
      setFullName(user.full_name);
    }
  }, [user]);

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  };

  const handleUpdate = async () => {
    setIsUpdating(true);
    const result = await updateUser(fullName);
    setIsUpdating(false);
    if (result.success) {
      setIsEditing(false);
      showToast('Profil berhasil diperbarui!');
    } else {
      showToast(result.message, 'error');
    }
  };

  if (!user) {
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <span className="loading loading-spinner loading-lg text-primary"></span>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto fade-in">
      <h1 className="text-2xl font-bold mb-6">Profil Saya</h1>

      {/* Toast */}
      {toast && (
        <div className={`alert ${toast.type === 'error' ? 'alert-error' : 'alert-success'} mb-4 fade-in`}>
          <span>{toast.message}</span>
        </div>
      )}

      {/* Profile Card */}
      <div className="glass-card p-6">
        {/* Avatar */}
        <div className="flex items-center gap-4 mb-8">
          <div className="avatar placeholder">
            <div className="bg-primary text-primary-content w-16 rounded-full">
              <span className="text-2xl font-bold">{user.full_name?.charAt(0)?.toUpperCase()}</span>
            </div>
          </div>
          <div>
            <h2 className="text-xl font-bold">{user.full_name}</h2>
            <p className="text-base-content/60 text-sm">{user.email}</p>
          </div>
        </div>

        <div className="divider"></div>

        {/* Info Fields */}
        <div className="space-y-5">
          {/* Email (read-only) */}
          <div>
            <label className="label">
              <span className="label-text font-semibold flex items-center gap-2">
                <HiOutlineMail className="w-4 h-4" /> Email
              </span>
            </label>
            <input
              type="text"
              className="input input-bordered w-full"
              value={user.email}
              disabled
            />
            <p className="text-xs text-base-content/40 mt-1">Email tidak dapat diubah</p>
          </div>

          {/* Full Name */}
          <div>
            <label className="label">
              <span className="label-text font-semibold flex items-center gap-2">
                <HiOutlineUser className="w-4 h-4" /> Nama Lengkap
              </span>
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                id="profile-fullname"
                className="input input-bordered w-full"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                disabled={!isEditing}
              />
              {!isEditing ? (
                <button
                  className="btn btn-outline btn-primary"
                  onClick={() => setIsEditing(true)}
                  id="profile-edit-btn"
                >
                  <HiOutlinePencil className="w-5 h-5" />
                </button>
              ) : (
                <button
                  className="btn btn-primary"
                  onClick={handleUpdate}
                  disabled={isUpdating || fullName === user.full_name}
                  id="profile-save-btn"
                >
                  {isUpdating ? (
                    <span className="loading loading-spinner loading-sm"></span>
                  ) : (
                    <HiOutlineCheck className="w-5 h-5" />
                  )}
                </button>
              )}
            </div>
          </div>

          {/* User ID */}
          <div>
            <label className="label">
              <span className="label-text font-semibold">User ID</span>
            </label>
            <input
              type="text"
              className="input input-bordered w-full"
              value={`#${user.id}`}
              disabled
            />
          </div>
        </div>
      </div>
    </div>
  );
}

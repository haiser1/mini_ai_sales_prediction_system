import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import api from '../api/axios';

export const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (email, password) => {
        set({ isLoading: true });
        try {
          const res = await api.post('/auth/login', { email, password });
          const { access_token } = res.data.data;
          set({ token: access_token, isAuthenticated: true, isLoading: false });
          // Fetch user profile after login
          await get().fetchUser();
          return { success: true };
        } catch (error) {
          set({ isLoading: false });
          const message = error.response?.data?.message || 'Login failed';
          return { success: false, message };
        }
      },

      register: async (full_name, email, password) => {
        set({ isLoading: true });
        try {
          const res = await api.post('/auth/register', { full_name, email, password });
          const { access_token } = res.data.data;
          set({ token: access_token, isAuthenticated: true, isLoading: false });
          // Fetch user profile after register
          await get().fetchUser();
          return { success: true };
        } catch (error) {
          set({ isLoading: false });
          const message = error.response?.data?.message || 'Registration failed';
          return { success: false, message };
        }
      },

      fetchUser: async () => {
        try {
          const res = await api.get('/users/me');
          set({ user: res.data.data });
        } catch (error) {
          console.error('Failed to fetch user:', error);
        }
      },

      updateUser: async (full_name) => {
        try {
          const res = await api.put('/users/me', { full_name });
          set({ user: res.data.data });
          return { success: true, message: res.data.message };
        } catch (error) {
          const message = error.response?.data?.message || 'Update failed';
          return { success: false, message };
        }
      },

      logout: () => {
        set({ user: null, token: null, isAuthenticated: false });
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        token: state.token,
        isAuthenticated: state.isAuthenticated,
        user: state.user,
      }),
    }
  )
);

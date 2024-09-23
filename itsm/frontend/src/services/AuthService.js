import apiClient from '../api/api';
import Cookies from 'js-cookie';

export const login = async (username, password) => {
  try {
    const response = await apiClient.post(
      '/auth/token',
      new URLSearchParams({
        username,
        password,
      }),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    );

    const { access_token } = response.data;
    Cookies.set('token', access_token, {
      expires: 1,
      secure: true,
      sameSite: 'Strict',
    });

    return response.data;
  } catch (error) {
    throw new Error(
      'Login failed: ' + (error.response?.data?.message || error.message)
    );
  }
};

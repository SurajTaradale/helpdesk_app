import apiClient from '../api/api';
import Cookies from 'js-cookie';

export const agentLoginApi = async (username, password) => {
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
    Cookies.set('agent_token', access_token, {
      expires: 1,
      secure: false,
      sameSite: 'Strict',
    });

    return response.data;
  } catch (error) {
    throw new Error(
      'Login failed: ' + (error.response?.data?.message || error.message)
    );
  }
};

export const customerLoginApi = async (username, password) => {
  try {
    const response = await apiClient.post(
      '/auth/customer/login',
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
    Cookies.set('customeruser_token', `${access_token}`, {
      expires: 1,
      secure: false,
      sameSite: 'Strict',
    });

    return response.data;
  } catch (error) {
    throw new Error(
      'Login failed: ' + (error.response?.data?.message || error.message)
    );
  }
};

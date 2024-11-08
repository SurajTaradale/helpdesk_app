import agentapiClient from '../api/agentapiClient';
import { logout } from '../store/agentSlice';

export const userlist = async (page_no, count_per_page, dispatch, navigate) => {
  try {
    const response = await agentapiClient.get('/api/v1/agent/userslist', {
      params: {
        page_no,
        count_per_page,
      },
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    return response;
  } catch (error) {
    console.log(error);
    const statusCode = error?.status;
    const errorMessage = error?.message || error.message;

    // Handle 401 Unauthorized error
    if (statusCode === 401) {
      // Dispatch the logout action
      dispatch(logout());
      // Navigate to the login page
      navigate('/agent/login');
    }

    // Return an object with status code and message
    return {
      success: false,
      statusCode,
      errorMessage,
    };
  }
};

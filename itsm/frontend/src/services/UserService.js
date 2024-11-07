import agentapiClient from '../api/agentapiClient';

export const userlist = async (page_no, count_per_page) => {
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
    throw new Error(
      'Login failed: ' + (error.response?.data?.message || error.message)
    );
  }
};

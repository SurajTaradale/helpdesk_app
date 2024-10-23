import { useSelector } from 'react-redux';
import Cookies from 'js-cookie';

export const AgentAuth = () => {
  const isAgentAuthenticated = useSelector(
    (state) => state.agent.isAgentAuthenticated
  );
  const token = Cookies.get('agent_token');

  return { isAgentAuthenticated, token };
};

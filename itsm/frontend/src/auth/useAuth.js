import { useSelector } from 'react-redux';
import Cookies from 'js-cookie';

export const useAuth = () => {
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const token = Cookies.get('token');

  return { isAuthenticated, token };
};

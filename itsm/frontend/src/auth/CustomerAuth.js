import { useSelector } from 'react-redux';
import Cookies from 'js-cookie';

export const CustomerAuth = () => {
  const isCustomerAuthenticated = useSelector(
    (state) => state.customer.isCustomerAuthenticated
  );
  const token = Cookies.get('customeruser_token');

  return { isCustomerAuthenticated, token };
};

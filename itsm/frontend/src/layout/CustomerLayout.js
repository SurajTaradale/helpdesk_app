import React from 'react';

const CustomerLayout = ({ children }) => {
  return (
    <div className="customer-layout">
      <header>Customer Header</header>
      <main>{children}</main>
      <footer>Customer Footer</footer>
    </div>
  );
};

export default CustomerLayout;

import React from 'react';

const AgentLayout = ({ children }) => {
  return (
    <div className="agent-layout">
      <header>Agent Header</header>
      <main>{children}</main>
      <footer>Agent Footer</footer>
    </div>
  );
};

export default AgentLayout;

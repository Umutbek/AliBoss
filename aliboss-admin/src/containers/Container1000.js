import React from 'react';

function Container1000({ children }) {
  return (
    <div className="container-fluid" style={{ maxWidth: 1000 }}>
      { children }
    </div>
  );
}

export default Container1000;

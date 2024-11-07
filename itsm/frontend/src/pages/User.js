// MainPage.js
import React, { useState, useEffect } from 'react';
import PaginationTable from '../components/PaginationTable';
import { userlist } from '../services/UserService';

const User = () => {
  const [totalRecords, setTotalRecords] = useState(0);
  const [data, setData] = useState([]);

  const fetchData = async (page, rowsPerPage) => {
    const response = await userlist(page, rowsPerPage);
    const result = await response.json();

    setTotalRecords(result.total); // Assuming your API returns total records
    return result; // Adjust based on your API response structure
  };

  return (
    <div>
      <h1>Your Table with Pagination</h1>
      <PaginationTable
        header={['Column 1', 'Column 2', 'Column 3']} // Adjust headers as needed
        totalRecords={totalRecords}
        recordsPerPage={10} // Default records per page
        fetchData={fetchData}
      />
    </div>
  );
};

export default User;

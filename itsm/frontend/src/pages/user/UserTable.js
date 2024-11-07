import { useEffect, useState } from 'react';
import {
  Card,
  FormControl,
  Grid2,
  TextField,
  Autocomplete,
  TableRow,
  TableCell,
  Skeleton,
  Typography,
  InputLabel,
  Select,
  MenuItem,
  ThemeProvider,
  createTheme,
  useTheme,
} from '@mui/material';
import DoneSharpIcon from '@mui/icons-material/DoneSharp';
import CloseSharpIcon from '@mui/icons-material/CloseSharp';
import { Link } from 'react-router-dom';
import ReactTable from '../../components/ReactTable';
import { userlist } from '../../services/UserService';

const UserTable = () => {
  const [pagination, setPagination] = useState({ pageIndex: 0, pageSize: 10 });
  const [paginationInfo, setPaginationInfo] = useState({ total: 0 });
  const [usersData, setUsersData] = useState([]);
  const [tableLoading, setTableLoading] = useState(false);
  useEffect(() => {
    setTableLoading(true);
    const fetchUsers = async () => {
      try {
        const response = await userlist(
          pagination.pageIndex + 1,
          pagination.pageSize
        );
        setUsersData(response.data.users);
        setPaginationInfo({ total: response.data.total_users });
        setTableLoading(false);
      } catch (error) {
        setTableLoading(false);
        console.error('Error fetching users:', error);
      }
    };

    fetchUsers();
  }, [pagination]);

  const theme = createTheme({
    palette: {
      common: {
        pcgDarkBlue: '#123456',
        pcgLightBlue: '#789abc',
      },
    },
  });

  const data = usersData.map((user) => ({
    Username: user.login,
    Name: `${user.first_name} ${user.last_name}`,
    Email: user?.preferences?.UserEmail,
    Validity: user.valid_id,
    path: 'update',
    FullData: user,
  }));

  const columns = [
    {
      header: 'Username',
      accessorKey: 'Username',
    },
    {
      header: 'Name',
      accessorKey: 'Name',
    },
    {
      header: 'Email',
      accessorKey: 'Email',
    },
    {
      header: 'Validity',
      accessorKey: 'Validity',
      cell: (props) => {
        return (
          <>
            <Typography variant="subtitle1">
              {props.row.original.Validity === 1 ? <>Valid</> : <>InValid</>}
            </Typography>
          </>
        );
      },
    },
  ];

  return (
    <>
      {tableLoading ? (
        <>
          <Card content={false}>
            {[0, 1, 2, 3, 4, 5].map((item) => (
              <TableRow key={item}>
                <TableCell />
                {[0, 1, 2, 3, 4, 5, 6].map((col) => (
                  <TableCell key={col}>
                    <Skeleton animation="wave" width={'8vw'} height={'15vh'} />
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </Card>
        </>
      ) : (
        <Grid2>
          <ReactTable
            data={data}
            columns={columns}
            paginationInfo={paginationInfo}
            pagination={pagination}
            setPagination={setPagination}
            theme={theme}
          />
        </Grid2>
      )}
    </>
  );
};

export default UserTable;

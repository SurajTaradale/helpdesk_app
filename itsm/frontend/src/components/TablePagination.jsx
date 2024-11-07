import PropTypes from 'prop-types';
import {
  Button,
  Grid,
  Pagination,
  Stack,
  Typography,
  ThemeProvider,
} from '@mui/material';

const TablePagination = ({
  getPageCount,
  setPageIndex,
  getState,
  pagination,
  totalPages,
  theme,
}) => {
  const handleChangePagination = (event, value) => {
    setPageIndex(value - 1);
  };

  return (
    <ThemeProvider theme={theme}>
      <Grid
        container
        alignItems="center"
        justifyContent="space-between"
        sx={{ width: 'auto' }}
      >
        <Grid item>
          <Stack direction="row" spacing={1} alignItems="center">
            {pagination && (
              <Typography variant="caption" sx={{ color: 'black' }}>
                {`Showing ${pagination.pageIndex * 10 + 1} to ${
                  totalPages < 10 ? totalPages : pagination.pageIndex * 10 + 10
                } of ${totalPages}`}
              </Typography>
            )}
          </Stack>
        </Grid>
        <Grid item>
          <Pagination
            count={getPageCount()}
            page={getState().pagination.pageIndex + 1}
            onChange={handleChangePagination}
            color="primary"
            showFirstButton
            showLastButton
          />
        </Grid>
      </Grid>
    </ThemeProvider>
  );
};

TablePagination.propTypes = {
  getPageCount: PropTypes.func.isRequired,
  setPageIndex: PropTypes.func.isRequired,
  getState: PropTypes.func.isRequired,
  pagination: PropTypes.object.isRequired,
  totalPages: PropTypes.number.isRequired,
  theme: PropTypes.object.isRequired,
};

export default TablePagination;

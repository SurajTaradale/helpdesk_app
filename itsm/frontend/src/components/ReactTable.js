import PropTypes from 'prop-types';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMediaQuery } from '@mui/material';
import {
  Card,
  Table,
  TableBody,
  TableContainer,
  TableCell,
  TableHead,
  TableRow,
  Box,
  Divider,
  Typography,
  Stack,
} from '@mui/material';
import {
  useReactTable,
  getCoreRowModel,
  flexRender,
} from '@tanstack/react-table';
import { styled } from '@mui/material/styles';
import TablePagination from './TablePagination';
import EmptyTable from './EmptyTable';

const ScrollX = styled('div')({
  width: '100%',
  overflowX: 'auto',
  display: 'block',
});

function ReactTable({
  data,
  columns,
  paginationInfo,
  pagination,
  setPagination,
  theme,
}) {
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const navigate = useNavigate();

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    manualPagination: true,
    rowCount: paginationInfo.total,
    onPaginationChange: setPagination,
    state: {
      pagination,
    },
  });

  const handleRowClick = (rowData) => {
    navigate(`${rowData.path}`, { state: { rowData } });
  };

  return (
    <Card sx={{ padding: '20px', border: 'none', boxShadow: 'none' }}>
      <ScrollX>
        <Box sx={{ p: 2 }}>
          <TablePagination
            getPageCount={table.getPageCount}
            setPageIndex={table.setPageIndex}
            getState={table.getState}
            pagination={pagination}
            totalPages={paginationInfo.total}
            position="top"
            theme={theme}
          />
        </Box>

        {isMobile ? (
          <Stack spacing={2}>
            {table.getRowModel().rows.length > 0 ? (
              table.getRowModel().rows.map((row) => (
                <Card key={row.id} variant="outlined" sx={{ padding: 2 }}>
                  {row.getVisibleCells().map((cell) => (
                    <Box
                      key={cell.id}
                      sx={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        mb: 1,
                        borderBottom: '1px solid #ededed',
                        paddingBottom: 1,
                      }}
                    >
                      <Typography variant="subtitle2" color="textSecondary">
                        {flexRender(
                          cell.column.columnDef.header,
                          cell.getContext()
                        )}
                      </Typography>
                      <Typography variant="body2">
                        {flexRender(
                          cell.column.columnDef.cell,
                          cell.getContext()
                        )}
                      </Typography>
                    </Box>
                  ))}
                </Card>
              ))
            ) : (
              <EmptyTable msg="No matching results found" />
            )}
          </Stack>
        ) : (
          <TableContainer>
            <Table>
              <TableHead
                sx={{ backgroundColor: theme.palette.common.pcgDarkBlue }}
              >
                {table.getHeaderGroups().map((headerGroup) => (
                  <TableRow key={headerGroup.id}>
                    {headerGroup.headers.map((header) => (
                      <TableCell
                        key={header.id}
                        sx={{
                          color: 'white',
                          borderWidth: 1,
                          borderColor: '#ededed',
                          borderStyle: 'solid',
                        }}
                      >
                        {header.isPlaceholder
                          ? null
                          : flexRender(
                              header.column.columnDef.header,
                              header.getContext()
                            )}
                      </TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableHead>
              <TableBody>
                {table.getRowModel().rows.length > 0 ? (
                  table.getRowModel().rows.map((row) => (
                    <TableRow key={row.id}>
                      {row.getVisibleCells().map((cell, index) => (
                        <TableCell
                          key={cell.id}
                          sx={{
                            borderWidth: 1,
                            borderColor: '#D3D3D3',
                            borderStyle: 'solid',
                            verticalAlign: 'top',
                          }}
                        >
                          {index === 0 ? (
                            // Make the first cell clickable
                            <Box
                              component="a"
                              sx={{ cursor: 'pointer', color: 'primary.main' }}
                              onClick={() => handleRowClick(row.original)}
                            >
                              {flexRender(
                                cell.column.columnDef.cell,
                                cell.getContext()
                              )}
                            </Box>
                          ) : (
                            flexRender(
                              cell.column.columnDef.cell,
                              cell.getContext()
                            )
                          )}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={table.getAllColumns().length}>
                      <EmptyTable msg="No matching results found" />
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>
        )}

        <Divider />
        <Box sx={{ p: 2 }}>
          <TablePagination
            getPageCount={table.getPageCount}
            setPageIndex={table.setPageIndex}
            getState={table.getState}
            pagination={pagination}
            totalPages={paginationInfo.total}
            position="bottom"
            theme={theme}
          />
        </Box>
      </ScrollX>
    </Card>
  );
}

ReactTable.propTypes = {
  columns: PropTypes.array.isRequired,
  data: PropTypes.array.isRequired,
  paginationInfo: PropTypes.object.isRequired,
  pagination: PropTypes.object.isRequired,
  setPagination: PropTypes.func.isRequired,
  theme: PropTypes.object.isRequired,
};

export default ReactTable;

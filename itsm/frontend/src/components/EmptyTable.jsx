import PropTypes from "prop-types";

// material-ui
import { styled } from "@mui/material/styles";
import { Stack, Typography } from "@mui/material";

const StyledGridOverlay = styled(Stack)(() => ({
  height: "400px",
  "& .ant-empty-img-5": {
    fillOpacity: 0.95,
  },
}));

const EmptyTable = ({ msg }) => {
  return (
    <StyledGridOverlay alignItems="center" justifyContent="center" spacing={1}>
      <Typography align="center" variant="h5" sx={{color: "black"}}>
        {msg}
      </Typography>
    </StyledGridOverlay>
  );
};

EmptyTable.propTypes = {
  msg: PropTypes.string,
};

export default EmptyTable;

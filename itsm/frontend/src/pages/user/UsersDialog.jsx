import {
  Dialog,
  DialogContent,
  DialogContentText,
  Typography,
  Button,
  Box,
  ThemeProvider,
} from "@mui/material";
import React from "react";
import axios from "axios";
import CloseIcon from "@mui/icons-material/Close";
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

const UsersDialog = ({ userData, userAction, userActionMessage, settingsState, setSettingsState, actionPerformed, setActionPerformed, theme, }) => {
  const { user, setUser, setAuthError } = "";
  const { showSnackbar } = "";

  const handleConfirm = () => {
    if (userAction === 'Delete') {
      let config = {
        method: "delete",
        url: `${process.env.API_ENDPOINT}/application_user/delete/${userData.Username}`,
        headers: {
          Apikey: user.apikey,
          "Content-Type": "text/plain",
        },
        data: JSON.stringify({ username: userData.Username }),
      };
      axios.request(config).then((response) => {
        showSnackbar(response.data.message, 'success');
        setSettingsState(false);
        setActionPerformed(!actionPerformed);
      }).catch((error) => {
        if (
          error?.response?.status === 403 &&
          error?.response?.data?.message?.includes("Inactive account!")
        ) {
          setAuthError(true);
          setUser();
        } else {
          showSnackbar(error?.response?.data?.message || error?.message, "error");
        }
      });
    } else if (userAction === 'Activate' || userAction === 'Deactivate') {
      let active;
      if (userAction === 'Activate') {
        active = true;
      } else if (userAction === 'Deactivate') {
        active = false;
      } else {
        return;
      }
      let actionConfig = {
        method: "post",
        url: `${process.env.API_ENDPOINT}/application_user/activate-deactivate`,
        headers: {
          Apikey: user.apikey,
          "Content-Type": "text/plain",
        },
        data: JSON.stringify({ username: userData.Username, active: active }),
      };
      axios.request(actionConfig).then((response) => {
        showSnackbar(response.data.message, 'success');
        setSettingsState(false);
        setActionPerformed(!actionPerformed);

      }).catch((error) => {
        if (
          error?.response?.status === 403 &&
          error?.response?.data?.message?.includes("Inactive account!")
        ) {
          setAuthError(true);
          setUser();
        } else {
          showSnackbar(error?.response?.data?.message || error?.message, "error");
        }
      });
    } else if (userAction === 'Password Reset') {
      let config = {
        method: "post",
        url: `${process.env.API_ENDPOINT}/application_user/username/${userData.Username}/resetPasswordRequest`,
        headers: {
          Apikey: user.apikey,
          "Content-Type": "text/plain",
        },
        data: JSON.stringify({ username: userData.Username }),
      };
      axios.request(config).then((response) => {
        showSnackbar(response.data.message, 'success');
        setSettingsState(false);
        setActionPerformed(!actionPerformed);
      }).catch((error) => {
        if (
          error?.response?.status === 403 &&
          error?.response?.data?.message?.includes("Inactive account!")
        ) {
          setAuthError(true);
          setUser();
        } else {
          showSnackbar(error?.response?.data?.message || error?.message, "error");
        }
      });
    } else if (userAction === 'Resend Activation') {
      let config = {
        method: "post",
        url: `${process.env.API_ENDPOINT}/application_user/resend-activation`,
        headers: {
          Apikey: user.apikey,
          "Content-Type": "text/plain",
        },
        data: JSON.stringify({ username: userData.Username }),
      };
      axios.request(config).then((response) => {
        showSnackbar(response.data.message, 'success');
        setSettingsState(false);
        setActionPerformed(!actionPerformed);
      }).catch((error) => {
        if (
          error?.response?.status === 403 &&
          error?.response?.data?.message?.includes("Inactive account!")
        ) {
          setAuthError(true);
          setUser();
        } else {
          showSnackbar(error?.response?.data?.message || error?.message, "error");
        }
      });
    } else {
      setSettingsState(false);
    }
  }
  const handleClose = () => {
    setSettingsState(false);
  };

  return (
    <ThemeProvider theme={theme}>
      <Dialog
        open={settingsState}
        onClose={handleClose}
        scroll="paper"
      >
        <DialogContent>
          <Box>
            <DialogContentText component="div">
              <Box
                sx={{
                  display: "flex",
                  justifyContent: "center",
                  gap: 3,
                  flexDirection: { xs: "column", md: "row" },
                  alignItems: "center",
                  flexWrap: "wrap",
                  flexDirection: "column"
                }}
              >
                <Box
                  display={"flex"}
                  flexDirection={"row"}
                  flexWrap={"wrap"}
                  justifyContent={"center"}
                >
                  <Typography variant="body1" sx={{ fontWeight: "normal", textAlign: "-webkit-center" }}>
                    {userActionMessage[0]}
                  </Typography>
                  &nbsp;
                  <Typography variant="body1" sx={{ fontWeight: "bold", textAlign: "-webkit-center" }}>
                    {userActionMessage[1]}
                  </Typography>
                </Box>
                <Box sx={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  width: "100%",
                }}>
                  <Button
                    size="small"
                    variant="contained"
                    sx={{
                      textTransform: "none",
                      color: "white",
                      backgroundColor: theme.palette.common.pcgRed
                    }}
                    startIcon={<CloseIcon />}
                    onClick={(e) => { handleClose(e); }}
                  >
                    Cancel
                  </Button>
                  <Button
                    size="small"
                    variant="contained"
                    sx={{
                      textTransform: "none",
                      color: "white",
                      backgroundColor: theme.palette.common.pcgGreen
                    }}
                    startIcon={<CheckCircleIcon />}
                    onClick={(e) => { handleConfirm(e); }}
                  >
                    Confirm
                  </Button>
                </Box>
              </Box>
            </DialogContentText>
          </Box>
        </DialogContent>
      </Dialog>
    </ThemeProvider>
  );
};

export default UsersDialog;

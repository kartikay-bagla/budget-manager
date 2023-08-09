import React from 'react';
import ExpenseForm from './CreateExpenseModal';
import { Box, Modal } from '@mui/material';
import Fab from '@mui/material/Fab';
import AddIcon from '@mui/icons-material/Add';


const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};


const CreateExpensePopup = () => {
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  return (
    <Box>
      <Fab
        color="primary" aria-label="add" onClick={handleOpen}
        sx={{ position: 'fixed', bottom: 16, right: 16 }}
      >
        <AddIcon />
      </Fab>

      {/* The popup content */}
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-create-expense-form"
        aria-describedby="modal-form-to-create-expense-entry"
      >
        <Box sx={style}>
          <ExpenseForm />
        </Box>
      </Modal>
    </Box>
  );
};

export default CreateExpensePopup;

import React, { useState } from 'react';
import { TextField } from '@mui/material';

const InputField = ({ name, label, validationType, value, onChange }) => {
  const [error, setError] = useState('');

  const validate = (value) => {
    let errorMessage = '';

    // Validate based on validationType
    switch (validationType) {
      case 'email':
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
        if (!emailRegex.test(value)) {
          errorMessage = 'Invalid email address';
        }
        break;

      case 'number':
        if (isNaN(value)) {
          errorMessage = 'Please enter a valid number';
        }
        break;

      default:
        break;
    }

    setError(errorMessage); // Set error message for this input field
    return errorMessage === ''; // Return true if valid
  };

  const handleChange = (event) => {
    const { value } = event.target;
    onChange(name, value); // Pass value to parent form
    validate(value); // Validate input value
  };

  return (
    <div>
      <TextField
        name={name}
        label={label}
        value={value}
        onChange={handleChange}
        fullWidth
        error={!!error}
        helperText={error}
      />
    </div>
  );
};

export default InputField;

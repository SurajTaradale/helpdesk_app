import { useLocation } from 'react-router-dom';
import React from 'react';
import {  useState } from 'react';
import InputField from '../../components/InputField';
import { Button, Container } from '@mui/material';
// import { useNavigate } from 'react-router-dom';

const UserCreateEdit = () => {
  // const navigate = useNavigate();
  const location = useLocation();
  const rowData = location.state?.rowData?.FullData;
  const [formData, setFormData] = useState({
    email: rowData?.preferences?.UserEmail
      ? rowData?.preferences?.UserEmail
      : '',
    phone: '',
  });

  const [errors, setErrors] = useState({
    email: '',
    phone: '',
  });
  // Handle input changes and pass the new value to the parent form
  const handleInputChange = (name, value) => {
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  // Validate the form to check if all fields are valid
  const validateForm = () => {
    // If all fields pass validation, return true
    return Object.values(errors).every((error) => error === '');
  };

  // Handle form submission
  const handleSubmit = (event) => {
    event.preventDefault(); // Prevent default form submit
    if (validateForm()) {
      // Form is valid, proceed with submission
      console.log(formData);
    } else {
      // Form has errors, don't submit
      console.log('Form has errors, not submitting');
    }
  };

  // Check if submit button should be disabled (if there are any errors)
  const isSubmitDisabled = Object.values(errors).some((error) => error !== '');

  return (
    <Container>
      <form onSubmit={handleSubmit}>
        <InputField
          name="email"
          label="Email"
          validationType="email"
          value={formData.email}
          onChange={handleInputChange}
        />
        <InputField
          name="phone"
          label="Phone"
          validationType="number"
          value={formData.phone}
          onChange={handleInputChange}
        />
        <Button
          type="submit"
          variant="contained"
          disabled={isSubmitDisabled} // Disable submit if there are validation errors
        >
          Submit
        </Button>
      </form>
    </Container>
  );
};

export default UserCreateEdit;

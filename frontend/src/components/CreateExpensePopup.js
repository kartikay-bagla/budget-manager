import React, { useEffect } from 'react';
import M from 'materialize-css';
import ExpenseForm from './CreateExpenseModal';

const CreateExpensePopup = () => {
    useEffect(() => {
      // Initialize the popup when the component mounts
      const options = {
        // You can customize the popup options here
      };
      const popup = document.querySelectorAll('.modal');
      M.Modal.init(popup, options);
    }, []);
  
    return (
      <div>
        <div className='right-align'>
        <button className="waves-effect waves-light btn-flat teal lighten-1 white-text modal-trigger" data-target="popupModal">
            Add Expense
        </button>
        </div>
  
        {/* The popup content */}
        <div id="popupModal" className="modal">
          <div className="modal-content">
            <ExpenseForm />
          </div>
        </div>
      </div>
    );
  };
  
  export default CreateExpensePopup;
  
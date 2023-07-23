// components/BudgetProgressBar.js
import React from 'react';

const BudgetProgressBar = ({ budget }) => {
    // budget.amount is max, budget.expenses is value
    // budget.category.name is what we need to display
    let perc = budget.expenses*100/budget.amount;
    let progress_color = "determinate teal";
    if (perc > 100) {
        perc = 100;
        progress_color = "determinate red";
    }
    return (
        <div className='card'>
            <div className='card-content'>
                <span className="card-title">{budget.category.name}</span>
                {budget.expenses}/{budget.amount}
            </div>
            <div className='card-action'>
                <div className="progress">
                    <div className={progress_color} style={{width: perc+"%"}}></div>
                </div>
            </div>
        </div>
    );
};

export default BudgetProgressBar;

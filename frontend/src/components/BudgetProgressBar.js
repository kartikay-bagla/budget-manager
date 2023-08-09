// components/BudgetProgressBar.js
import { Box, LinearProgress, Tooltip, Typography } from '@mui/material';
import React from 'react';
import numberFormatter from '../utils/utils';

const ERR_VAL = "#f44336";
const ERR_BUF = "#d50000";
const ERR_BGR = "#212121";

const WAR_VAL = "#cddc39";
const WAR_BUF = "#827717";
const WAR_BGR = "#212121";

const GEN_VAL = "#009688";
const GEN_BUF = "#004d40";
const GEN_BGR = "#212121";

const BudgetProgressBar = ({ budget }) => {
    // budget.amount is max, budget.expenses is value
    // budget.category.name is what we need to display
    let past_expenses = budget.past_expenses;
    let total_expenses = budget.expenses;
    let max_amount = budget.amount;
    let buffer_perc = total_expenses * 100 / max_amount;
    let value_perc = past_expenses * 100 / max_amount;

    let val_col = GEN_VAL;
    let buf_col = GEN_BUF;
    let bgr_col = GEN_BGR;

    if (buffer_perc >= 100) {
        buffer_perc = 100;
    }
    if (value_perc >= 100) {
        value_perc = 100;
    }

    if (buffer_perc >= 80) {
        val_col = WAR_VAL;
        buf_col = WAR_BUF;
        bgr_col = WAR_BGR;
    }
    if (buffer_perc >= 90) {
        val_col = ERR_VAL;
        buf_col = ERR_BUF;
        bgr_col = ERR_BGR;
    }

    return (
        <Box sx={{ width: '100%' }}>
            <Tooltip title={`${numberFormatter.format(budget.past_expenses)} + ${numberFormatter.format(budget.future_expenses)} (upcoming)`} placement="top" arrow>
                <Typography variant='subtitle2'>{budget.category.name} - {numberFormatter.format(budget.expenses)}/{numberFormatter.format(budget.amount)}</Typography>
            </Tooltip>
            <LinearProgress
                variant="buffer" value={value_perc}
                valueBuffer={buffer_perc}
                sx={{
                    '.MuiLinearProgress-dashed': { backgroundImage: 'none', backgroundColor: bgr_col, animation: 'none' },
                    '.MuiLinearProgress-barColorPrimary': { backgroundColor: val_col },
                    '.MuiLinearProgress-bar2Buffer': { backgroundColor: buf_col }
                }}
            />
        </Box>
    );
};

export default BudgetProgressBar;

import axios from "axios";

const BASE_URL = "http://localhost:8000/api/v1";

export async function get_expenses(start_date, end_date) {
    return axios.get(`${BASE_URL}/expenses/?start_date=${start_date}&end_date=${end_date}`)
}

export async function get_categories() {
    return axios.get(`${BASE_URL}/categories/`)
}

export async function add_non_recurring_expense(category_id, description, amount, date) {
    let data = {
        "is_recurring": false,
        "category_id": category_id,
        "description": description,
        "amount": amount,
        "date": date,
    };
    return axios.post(`${BASE_URL}/expenses/`, data);
}

export async function add_recurring_expense(category_id, description, amount, date, start_date, end_date, frequency) {
    let data = {
        "is_recurring": true,
        "category_id": category_id,
        "description": description,
        "amount": amount,
        "date": date,
        "recurring_start_date": start_date,
        "recurring_end_date": end_date,
        "recurring_frequency": frequency,
    };
    return axios.post(`${BASE_URL}/expenses/`, data);
}

import axios from "axios";

export async function get_expenses(start_date, end_date) {
    return axios.get(`http://localhost:8000/api/v1/expenses/?start_date=${start_date}&end_date=${end_date}`)
}
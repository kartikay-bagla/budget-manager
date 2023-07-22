export function get_today_date() {
    // return date as yyyy-mm-dd
    let a = new Date(); 
    let y = a.getFullYear();
    let m = (a.getMonth() + 1).toString().padStart(2, "0");
    let d = a.getDate().toString().padStart(2, "0");
    return `${y}-${m}-${d}`;
}

export function get_current_month_start_date() {
    // return date of start of current month as yyyy-mm-dd
    const today = new Date();
    let year = today.getFullYear();
    let month = (today.getMonth() + 1).toString().padStart(2, "0");
    return `${year}-${month}-01`
}

export function get_next_month_start_date() {
    // return date of start of next month as yyyy-mm-dd
    const today = new Date();
    let current_month = today.getMonth() + 1;
    let next_month = current_month < 12 ? current_month + 1 : 1;
    next_month = next_month.toString().padStart(2, "0");
    let current_year = today.getFullYear();
    let next_year = current_month < 12 ? current_year : current_year + 1;
    return `${next_year}-${next_month}-01`
}

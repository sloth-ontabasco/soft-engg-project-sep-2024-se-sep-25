export function formatDate(dateString) {
    if (!dateString) return 'N/A'; // Handle null or undefined dates
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      year: '2-digit',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false
    }).format(date).replace(',', '');
  }
  
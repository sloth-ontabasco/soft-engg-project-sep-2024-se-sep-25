export function formatDate(dateString) {
    if (!dateString) return 'N/A'; // Handle null or undefined dates
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    }).format(date);
  }
  
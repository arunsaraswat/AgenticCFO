/**
 * Utility functions for formatting numbers, currency, and percentages
 * according to financial dashboard standards.
 */

/**
 * Format number as currency with proper thousand separators and decimals.
 *
 * @param amount - The amount to format
 * @param decimals - Number of decimal places (default: 2)
 * @returns Formatted currency string (e.g., "$1,234.56")
 *
 * @example
 * formatCurrency(1234.567) // "$1,234.57"
 * formatCurrency(1234.567, 0) // "$1,235"
 */
export const formatCurrency = (amount: number | null | undefined, decimals = 2): string => {
  if (amount === null || amount === undefined) return '—';

  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(amount);
};

/**
 * Format large numbers with abbreviations (K, M, B).
 *
 * @param num - The number to format
 * @param decimals - Number of decimal places (default: 1)
 * @returns Formatted number string (e.g., "1.2M", "345K")
 *
 * @example
 * formatNumber(1234567) // "1.2M"
 * formatNumber(12345) // "12.3K"
 * formatNumber(123) // "123"
 */
export const formatNumber = (num: number | null | undefined, decimals = 1): string => {
  if (num === null || num === undefined) return '—';

  const absNum = Math.abs(num);
  const sign = num < 0 ? '-' : '';

  if (absNum >= 1_000_000_000) {
    return `${sign}${(absNum / 1_000_000_000).toFixed(decimals)}B`;
  }
  if (absNum >= 1_000_000) {
    return `${sign}${(absNum / 1_000_000).toFixed(decimals)}M`;
  }
  if (absNum >= 10_000) {
    return `${sign}${(absNum / 1_000).toFixed(decimals)}K`;
  }

  return `${sign}${absNum.toLocaleString('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: decimals,
  })}`;
};

/**
 * Format number as percentage.
 *
 * @param num - The number to format (0.123 = 12.3%)
 * @param decimals - Number of decimal places (default: 1)
 * @returns Formatted percentage string (e.g., "12.3%")
 *
 * @example
 * formatPercentage(0.1234) // "12.3%"
 * formatPercentage(0.1234, 2) // "12.34%"
 * formatPercentage(0.001) // "0.1%"
 */
export const formatPercentage = (num: number | null | undefined, decimals = 1): string => {
  if (num === null || num === undefined) return '—';

  const percentage = num * 100;

  // Use more decimals for very small percentages
  if (Math.abs(percentage) < 1 && percentage !== 0) {
    decimals = Math.max(decimals, 2);
  }

  return `${percentage.toFixed(decimals)}%`;
};

/**
 * Format date to locale string.
 *
 * @param date - Date to format (string or Date object)
 * @param options - Intl.DateTimeFormat options
 * @returns Formatted date string
 *
 * @example
 * formatDate("2025-01-15") // "1/15/2025"
 * formatDate("2025-01-15", { month: 'long', day: 'numeric', year: 'numeric' }) // "January 15, 2025"
 */
export const formatDate = (
  date: string | Date | null | undefined,
  options?: Intl.DateTimeFormatOptions
): string => {
  if (!date) return '—';

  const dateObj = typeof date === 'string' ? new Date(date) : date;

  if (isNaN(dateObj.getTime())) return '—';

  return dateObj.toLocaleDateString('en-US', options);
};

/**
 * Format bytes to human-readable size.
 *
 * @param bytes - Number of bytes
 * @returns Formatted size string (e.g., "1.5 MB")
 *
 * @example
 * formatBytes(1536) // "1.5 KB"
 * formatBytes(1048576) // "1.0 MB"
 */
export const formatBytes = (bytes: number | null | undefined): string => {
  if (bytes === null || bytes === undefined || bytes === 0) return '0 Bytes';

  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return `${(bytes / Math.pow(k, i)).toFixed(1)} ${sizes[i]}`;
};

/**
 * Format duration in seconds to human-readable string.
 *
 * @param seconds - Duration in seconds
 * @returns Formatted duration string (e.g., "2m 30s")
 *
 * @example
 * formatDuration(150) // "2m 30s"
 * formatDuration(45) // "45s"
 * formatDuration(3665) // "1h 1m 5s"
 */
export const formatDuration = (seconds: number | null | undefined): string => {
  if (seconds === null || seconds === undefined) return '—';

  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);

  const parts: string[] = [];
  if (h > 0) parts.push(`${h}h`);
  if (m > 0) parts.push(`${m}m`);
  if (s > 0 || parts.length === 0) parts.push(`${s}s`);

  return parts.join(' ');
};

/**
 * Parse markdown table to array of objects.
 * Handles the markdown table format returned by Cash Commander.
 *
 * @param markdownTable - Markdown table string
 * @returns Array of row objects
 */
export const parseMarkdownTable = (markdownTable: string): Record<string, string>[] => {
  const lines = markdownTable.trim().split('\n');
  if (lines.length < 3) return [];

  // Extract headers (first line)
  const headers = lines[0]
    .split('|')
    .map(h => h.trim())
    .filter(h => h.length > 0);

  // Skip separator line (second line)
  // Parse data rows (third line onward)
  const rows = lines.slice(2).map(line => {
    const values = line
      .split('|')
      .map(v => v.trim())
      .filter(v => v.length > 0);

    const row: Record<string, string> = {};
    headers.forEach((header, idx) => {
      row[header] = values[idx] || '';
    });

    return row;
  });

  return rows;
};
